#!/usr/bin/env python3

import sys

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
        'l.edu-servers.net.'
        );

def main(argv):
    if len(argv) == 1:
        print("Usage: python edu-probe.py uic.edu")
    else:
        for arg in sys.argv[1:]:
            # caller function/wrapper should be here
            print("Args: ", arg)

if __name__ == "__main__":
    main(sys.argv)
