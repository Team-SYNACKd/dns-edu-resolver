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
        'a.edu-servers.net.',
        'c.edu-servers.net.',
        'd.edu-servers.net.',
        'f.edu-servers.net.',
        'g.edu-servers.net.',
        'l.edu-servers.net.',
        )


visited = []
tested_edu_server = []

def dns_resolve(domain, nameservers):
    # tested tuple comes in handy to check if the root or .edu servers are
    # visited ones
    serverlist = []

    ADDITIONAL_RDCLASS = 65535
    qr, aa, tc, rd, ra, ad, cd = [0 for _ in range(7)]

    #nameserver_ip = edu_nameservers[nameserver]
    print("resolving against: ", nameservers)
    visited.append(nameservers)

    #FIXME: Hack to get the IP of the resolving nameservers. We need to find better ways if possible
    #FIXME: Catch any expections that can occur
    myResolver = dns.resolver.Resolver()
    nameserver_ip = myResolver.query(str(nameservers), dns.rdatatype.A)

    try:
        request = dns.message.make_query(str(domain), dns.rdatatype.NS)
        request.flags |= dns.flags.AD
        request.find_rrset(request.additional, dns.name.root,
                ADDITIONAL_RDCLASS, dns.rdatatype.OPT, create=True, force_unique=True)

        for ip in nameserver_ip:
            response = dns.query.udp(request, str(ip))

        dns_id = response.id
        opcode = dns.opcode.to_text(response.opcode())
        rcode = dns.rcode.to_text(response.rcode())
        qdcount = len(response.question)
        nscount = len(response.authority)
        arcount = len(response.additional)
        ancount = len(response.answer)

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

        for ip in nameserver_ip:
            print('Header', domain, nameservers, ip, dns_id, opcode, rcode, qdcount, nscount, arcount, ancount, qr, aa, tc, rd, ra, ad, cd)

        # To get the Rdatas from the RRset
        if (ancount > 0):
            for rdata in response.answer[0]:
                r_class = response.answer[0].rdclass
                r_type = response.answer[0].rdtype
                r_ttl = response.answer[0].ttl
                print('Answer Section:', domain, nameservers, r_class, r_type, r_ttl, rdata)
                if (r_type is 2):
                    serverlist.append(rdata)

        if (nscount > 0):
            for rdata in response.authority[0]:
                r_class = response.authority[0].rdclass
                r_type = response.authority[0].rdtype
                r_ttl = response.authority[0].ttl
                print('Authority Section:', domain, nameservers, r_class, r_type, r_ttl, rdata)
                if (r_type is 2):
                    serverlist.append(rdata)

        if (arcount > 0):
            for rdata in response.additional[0]:
                r_class = response.additional[0].rdclass
                r_type = response. additional[0].rdtype
                r_ttl = response.additional[0].ttl
                print('Addtional Section:', domain, nameservers, r_class, r_type, r_ttl, rdata)

        for server in range(0, len(serverlist)):
            if serverlist[server] in visited:
                pass
            else:
                dns_resolve(domain, serverlist[server])

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
            # caller function/wrapper should be here
            while True:
                domain = input("Enter the domain: ")
                edu_nameserver = random.choice(list(edu_nameservers))
                if edu_nameserver in tested_edu_server:
                    pass
                else:
                    tested_edu_server.append(edu_nameserver)
                    dns_resolve(domain, edu_nameserver)
                    del visited[:] # If querying same domain - delete what exits to query again fresh

if __name__ == "__main__":
    main(sys.argv)
