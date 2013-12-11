#!/usr/bin/env python

import csv
import os
import sys
import subprocess
import statvfs

def usage():
    return """
    Summary: Check if prefix is /24
			"""

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option('-p', '--prefix', dest='prefix', default=None, help='optional: prefix of clients')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    options, args = parser.parse_args()
    if options.prefix is None:
        print 'Error: Please provide --prefix'
        sys.exit(12)
    return (options, args)


if __name__ == '__main__':
    options, args = parse_args()
    prefix = options.prefix
    e=prefix.split('/')[1].strip()
    if e=='24':
		sys.exit(11)
    else:
		sys.exit(0)
