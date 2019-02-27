#!/usr/bin/env python3

import sys
import random

import dns.resolver, dns.name
import dns.message, dns.query

root_nameservers = (
        'a.root-servers.net.',
        'b.root-servers.net.',
        'c.root-servers.net.',
        'd.root-servers.net.',
        'e.root-servers.net.',
        'f.root-servers.net.',
        'g.root-servers.net.',
        'h.root-servers.net.',
        'i.root-servers.net.',
        'j.root-servers.net.',
        'k.root-servers.net.',
        'l.root-servers.net.',
        'm.root-servers.net.'
        );

edu_nameservers = (
        '192.5.6.30',   #a.edu-servers.net.
        '192.26.92.30', #c.edu-servers.net.
        '192.31.80.30', #d.edu-servers.net.
        '192.35.51.30', #f.edu-servers.net.
        '192.42.93.30', #g.edu-servers.net.
        '192.41.162.30',#l.edu-servers.net.
        );


def dns_resolve(domain):
    # tested tuple comes in handy to check if the root or .edu servers are
    # visited ones
    tested = ();

    ADDITIONAL_RDCLASS = 65535
    qr, aa, tc, rd, ra, ad, cd = [0 for _ in range(7)]

    nameserver = random.choice(edu_nameservers)
    print("resolving against: ", nameserver)

    try:
        myResolver = dns.resolver.Resolver()
        myResolver.nameservers = nameserver

        request = dns.message.make_query(domain, dns.rdatatype.NS)
        request.flags |= dns.flags.AD
        request.find_rrset(request.additional, dns.name.root,
                ADDITIONAL_RDCLASS, dns.rdatatype.OPT, create=True, force_unique=True)

        response = dns.query.udp(request, nameserver)

        # To get the Rdatas from the RRset
        for rdata in response.authority[0]:
            print('Authority Section:', rdata)

        for rdata in response.additional:
            print('Addtional Section:', rdata)


        for rdata in response.answer:
            print('Answer Section:', rdata)

        #FIXME: Could try to figure out a better way to see active flags.
        if(response.flags & dns.flags.QR):
            qr = 1
        if(response.flags & dns.flags.AA):
            aa = 1
        if(response.flags & dns.flags.TC):
            tc = 1
        if(response.flags & dns.flags.RD):
            rd = 1
        if(response.flags & dns.flags.RA):
            ra = 1
        if(response.flags & dns.flags.AD):
            ad = 1
        if(response.flags & dns.flags.CD):
            cd = 1

        print( qr, aa, tc, rd, ra, ad, cd)

    except dns.resolver.NoAnswer:
        print("There is no Answer for the quried domain" )
    except dns.resolver.NoNameservers:
        print("All nameservers failed to answer the query")
    except dns.resolver.NXDOMAIN:
        print("No such domain exists")
    except dns.exception.DNSException:
        print("Unhandled DNS Exception")
    except dns.exception.Timeout:
        print("DNS timeout")
    except dns.exception.FormError:
        print("DNS message malformat")
    except dns.exception.SyntaxError:
        print("Text input malformat")
    except dns.exception.TooBig:
        print("DNS message is too big")
    except dns.exception.UnexpectedEnd:
        print("Text input ended unexpectedly")

def main(argv):
    if len(argv) == 1:
        print("Usage: python edu-probe.py uic.edu")
    else:
        for arg in sys.argv[1:]:
            # caller function/wrapper should be here
            dns_resolve(arg)
            print("Args: ", arg)

if __name__ == "__main__":
    main(sys.argv)
