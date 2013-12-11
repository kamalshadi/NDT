#!/usr/bin/env python

import csv
import os
import sys
import subprocess
import statvfs
import pylab as pl
import numpy as num
from scipy.stats.mstats import mquantiles

def usage():
    return """
Summary:
./geoUoS -p False/True -f <filename> 
locate the UoS in city resolution
"""
		

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option("-f", "--fileName", dest="fName", default=None, 
                      help="Required: filename for geo data")
    parser.add_option('-c', '--column', dest='col', default=None, help='Required: stats are calculated for given column')           
        
    
                       
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    if options.fName is None or options.col is None:
        print "Error: Please provide --filename and --column to read data \n \
        (do not include .dat suffix)"
        sys.exit(1)

    return (options, args)
		
def PDF(a,nBins=50):
	pdf,bins=num.histogram(a,nBins,density=True)
	x= bins[0:len(pdf)]
	g=bins[2]-bins[1]
	return [[o*g for o in pdf],x]
	

if __name__ == '__main__':
	(options, args) = parse_args()
	fName=options.fName
	col=int(options.col)
	fg=0
	mb=[]
	with open('Dump/'+fName+'.dat','r') as f:
		val=csv.reader(f)
		i=0
		for line in val:
			if i==0:
				i=1
				continue
			mb.append(float(line[col]))

	a1,a2=mquantiles(mb,[.05,.95])
	mbs=[xx for xx in mb if a1<xx<a2]
	print 'Number of datapoints: '+str(len(mbs))
	p,x=PDF(mbs)
	pl.plot(x,p)
	#~ pl.xlim(1,5)
	pl.show()
				
