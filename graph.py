#!/usr/bin/env python

import csv
import os
import sys
import subprocess
import statvfs
from myParser import csv2gml

def usage():
    return """
graph from the similarity graph based on RTT
look at csv2gml
"""
		

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option("-f", "--file", dest="fName", default=None, 
                      help="Required: Filename to read the data")
    parser.add_option("-e", "--eps", dest="eps", default=.3, type="float",
                      help="Optional: edge threshold")
        
    
                       
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    if options.fName is None:
        print "Error: Please provide --dir to read data \n \
        (do not include D- prefix)"
        sys.exit(1)

    return (options, args)


if __name__ == '__main__':
	(options, args) = parse_args()
	fName=options.fName
	code=csv2gml(fName)
	if code  < 1 :
		sys.exit(11)
	
