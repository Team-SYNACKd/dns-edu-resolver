#!/usr/bin/env python3

import sys




def main(argv):
    if len(argv) == 1:
        print("Usage: python edu-probe.py uic.edu")
    else:
        for arg in sys.argv[1:]:
            # caller function/wrapper should be here
            print("Args: ", arg)


if __name__ == "__main__":
    main(sys.argv)
