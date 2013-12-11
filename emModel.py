#!/usr/bin/env python

import csv
import os
import sys
import subprocess
import statvfs
import pylab as pl
import numpy as num

def PDF(a,nBins=100):
	pdf,bins=num.histogram(a,nBins,density=True)
	x= bins[0:len(pdf)]
	g=bins[2]-bins[1]
	return [[o*g for o in pdf],x]

def order(v,w):
	a=zip(v,w)
	a.sort()
	l=zip(*a)
	v=list(l[0])
	w=list(l[1])
	return [v,w]

def usage():
    return """
Summary:
./geoUoS -p False/True -f <filename> 
locate the UoS in city resolution
"""

		

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option("-d", "--dirc", dest="dirc", default=None, 
                      help="Required: sub_directory in Dump")
    parser.add_option("-u", "--uos", dest="uos", default="1", 
                      help="Required: filename for geo data")
        
    
                       
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    if options.dirc is None:
        print "Error: Please provide --dir to read data \n \
        (do not include D- prefix)"
        sys.exit(1)

    return (options, args)
    
    
if __name__ == '__main__':
	(options, args) = parse_args()
	dirc=options.dirc
	uos=options.uos
	ad="Dump/D-"+dirc+"/uos_"+uos
	i=0
	ld=[]
	#~ meta=open(ad+".m",w)
	dic={}
	logt=[]
	dt=[]
	cc=[]
	cl={}
	tl={}
	with open(ad,'r') as f:
		val=csv.reader(f,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i,line in enumerate(val):
			if i==0:
				l=len(line)
				i=1
				continue
			else:
				cIP=line[0].strip()
				cc.append(cIP)
				server=line[-1]
				log=line[1]
				logt.append(int(log))
				t=[float(xx) for xx in line[2].strip('"').split(',')]
				down=float(line[l-2])/max(t)
				try:
					cl[cIP]=cl[cIP]+[down]
					tl[cIP]=tl[cIP]+[int(log)]
				except KeyError:
					cl[cIP]=[down]
					tl[cIP]=[int(log)]
				dt.append(down)
				dic[(cIP,server,log)]={'throughput':down}
				ld.append(down)
	print '\n\n\n'
	print len(cc)
	print len(set(cc))
	print '\n\n\n'
	p,x=PDF(ld,50)
	pl.plot(x,p)
	pl.xlabel('Download Throughput')
	pl.ylabel('PDF')
	#~ pl.xlim(0,2)
	pl.show()
	cal=sorted(cl.keys())
	for i in range(len(cal)):
		pl.errorbar(i, num.mean(cl[cal[i]]), yerr=num.std(cl[cal[i]]), fmt='o',ecolor='g')
		pl.text(i,num.mean(cl[cal[i]])+.1,str(len(cl[cal[i]])))
	pl.xlabel('User')
	pl.ylabel('Download Throughput')
	pl.show()
	cal=sorted(tl.keys())
	for i in range(len(tl)):
		pl.plot([i]*len(tl[cal[i]]), tl[cal[i]],'r*')
		#~ pl.text(i,num.mean(cl[cal[i]])+.1,str(len(cl[cal[i]])))
	pl.xlabel('User')
	pl.ylabel('Time of test')
	pl.show()
	#~ pl.plot(*order(logt,dt))
	#~ pl.show()
