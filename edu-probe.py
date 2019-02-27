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

    except dns.resolver.NoAnswer:
        pass

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
