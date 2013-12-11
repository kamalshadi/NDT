#!/usr/bin/env python

from myParser import *
from ipCluster import cluster2sub
import csv
import os
import sys
import subprocess
import statvfs

def usage():
    return """
    Summary:
    Reading undirected weighted similarity graph and do the walktrap clustering plus subnet mapping
			"""


def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option('-g', '--gap', dest='g', default='/24', help='Optional: threshold to split brackets')
    parser.add_option('-f', '--fileName', dest='fName', default=None, help='Required: filename for data')
    parser.add_option('-p', '--prefix', dest='prefix', default=None, help='Required: filename for data')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    options, args = parser.parse_args()
    if options.fName is None or options.prefix is None:
        print 'Error: Please provide --filename to read data \n (do not include .G suffix)'
        sys.exit(1)
    return (options, args)


if __name__ == '__main__':
    options, args = parse_args()
    fName = options.fName
    prefix = options.prefix
    g = options.g
    walktrapFile(fName)
    qq = 'WalkTrap/walktrap CSV/' + fName + ".walktrap -b -d1 -s |grep community| cut -d'=' -f2 > CSV/" + fName + '.C'
    os.system(qq)
    C = UoSM_input(fName)
    uos = cluster2sub(C,g)
    with open('CSV/' + fName + '.net', 'a+b') as f:
        f.write(prefix+','+str(uos)+'\n')
