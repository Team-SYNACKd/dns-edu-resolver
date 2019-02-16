#!/usr/bin/perl
# Some versions of pos Net::DNS broken with taint mode
##!/usr/bin/perl -T
use strict;
use warnings;

$| = 1;

use Net::DNS;

my @root_nameservers = qw(
    a.root-servers.net.
    b.root-servers.net.
    c.root-servers.net.
    d.root-servers.net.
    e.root-servers.net.
    f.root-servers.net.
    g.root-servers.net.
    h.root-servers.net.
    i.root-servers.net.
    j.root-servers.net.
    k.root-servers.net.
    l.root-servers.net.
    m.root-servers.net.
);

my @edu_nameservers = qw(
    a.edu-servers.net.
    c.edu-servers.net.
    d.edu-servers.net.
    f.edu-servers.net.
    g.edu-servers.net.
    l.edu-servers.net.
);

my %tested;

# expect a list of domains, one per line via stdin
while ( my $domain = <> ) {
    chomp $domain;

    # append TLD if necessary
    if ( $domain !~ m{ [.] edu [.]? \z }ixms ) {
        # strip trailing dot if it exists
        $domain =~ s{ [.] \z }{}xms;
        $domain .= '.edu.';
    }

    # reset %tested for each domain
    %tested = ();
    for my $root_instance (@root_nameservers) {
        $tested{$domain}{$root_instance} = 1;
    }

    # select random TLD NS
    my $nameserver = $edu_nameservers[ rand @edu_nameservers ];

    do_query( { nameserver => $nameserver, domain => $domain } );
}

sub do_query {
    my ($arg_ref)  = @_;
    my $nameserver = $arg_ref->{nameserver} or return;
    my $domain     = $arg_ref->{domain} or return;

    $nameserver = lc $nameserver;
    $domain     = lc $domain;

    return if $tested{$domain}{$nameserver};

    # hack to not go back to edu_servers
    for my $edu_instance (@edu_nameservers) {
        $tested{$domain}{$edu_instance} = 1;
    }

    my $res = Net::DNS::Resolver->new;
    $res->recurse(0);
    $res->retry(2);
    $res->retrans(3);
    $res->persistent_udp(1);

    $res->nameserver($nameserver);

    my $query = $res->send( $domain, 'NS', 'IN' );
    $tested{$domain}{$nameserver} = 1;

    if ( !$query ) {
        print "noresponse,$domain,$nameserver,IN,NS\n";
        return;
    }

    my $raddr = $res->answerfrom;
    my $id = $query->header->id;
    my $opcode = $query->header->opcode;
    my $rcode = $query->header->rcode;
    my $qr = $query->header->qr;
    my $aa = $query->header->aa;
    my $tc = $query->header->tc;
    my $rd = $query->header->rd;
    my $ra = $query->header->ra;
    my $ad = $query->header->ad;
    my $cd = $query->header->cd;
    my $qdcount = $query->header->qdcount;
    my $nscount = $query->header->nscount;
    my $arcount = $query->header->arcount;

    my %serverlist;

    print "header,$domain,$nameserver,$raddr,$id,$opcode,$rcode,$qr,$aa,$tc,$rd,$ra,$ad,$cd,$qdcount,$nscount,$arcount\n";

    if ( $query->header->ancount > 0 ) {
        my @answers = $query->answer;
        for my $rr (@answers) {
            my $class = $rr->class;
            my $type = $rr->type;
            my $ttl = $rr->ttl;
            my $rdata = $rr->rdatastr;
            # clean up SOA rdata so it is one line without comments
            if ( $type eq 'SOA' ) {
                $rdata =~ s{ [(] \s }{}xms;
                $rdata =~ s{ [)] .* }{}xms;
                $rdata =~ s{ [;] \s \S+ }{}gxms;
                $rdata =~ s{ \s+ }{ }gxms;
            }
            print "answer,$domain,$nameserver,$class,$type,$ttl,$rdata\n";
            if ( $type eq 'NS' ) {
                $serverlist{$rdata} = 1;
            }
        }
    }
    if ( $query->header->nscount > 0 ) {
        my @authorities = $query->authority;
        for my $rr (@authorities) {
            my $class = $rr->class;
            my $type = $rr->type;
            my $ttl = $rr->ttl;
            my $rdata = $rr->rdatastr;
            # clean up SOA rdata so it is one line without comments
            if ( $type eq 'SOA' ) {
                $rdata =~ s{ [(] \s }{}xms;
                $rdata =~ s{ [)] .* }{}xms;
                $rdata =~ s{ [;] \s \S+ }{}gxms;
                $rdata =~ s{ \s+ }{ }gxms;
            }
            print "authority,$domain,$nameserver,$class,$type,$ttl,$rdata\n";
            if ( $type eq 'NS' ) {
                $serverlist{$rdata} = 1;
            }
        }
    }
    if ( $query->header->arcount > 0 ) {
        my @additionals = $query->additional;
        for my $rr (@additionals) {
            my $class = $rr->class;
            my $type = $rr->type;
            my $ttl = $rr->ttl;
            my $rdata = $rr->rdatastr;
            # clean up SOA rdata so it is one line without comments
            if ( $type eq 'SOA' ) {
                $rdata =~ s{ [(] \s }{}xms;
                $rdata =~ s{ [)] .* }{}xms;
                $rdata =~ s{ [;] \s \S+ }{}gxms;
                $rdata =~ s{ \s+ }{ }gxms;
            }
            # TODO: print qname, it will usually not be consistent with domain
            print "additional,$domain,$nameserver,$class,$type,$ttl,$rdata\n";
        }
    }

    for my $nameserver (keys %serverlist) {
        do_query( { domain => $domain, nameserver => lc $nameserver } );
    }

    return;
}
