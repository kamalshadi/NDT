#!/usr/bin/env python

import csv
import os
import sys
import subprocess
import statvfs
import pylab as pl

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
    
    
def order(v,w):
	a=zip(v,w)
	a.sort()
	l=zip(*a)
	v=list(l[0])
	w=list(l[1])
	return [v,w]

if __name__ == '__main__':
	(options, args) = parse_args()
	dirc=options.dirc
	uos=options.uos
	ad="Dump/D-"+dirc+"/uos_"+uos
	i=0
	dic={}
	with open(ad,'r') as f:
		val=csv.reader(f,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i,line in enumerate(val):
			if i==0:
				l=len(line)
				i=1
				continue
			else:
				cIP=line[0]
				server=line[-1]
				log=int(line[1])
				t=[float(xx)/1e6 for xx in line[2].strip('"').split(',')]
				rtt=[float(xx) for xx in line[3].strip('"').split(',')]
				cwnd=[float(xx) for xx in line[4].strip('"').split(',')]
				congS=[float(xx) for xx in line[5].strip('"').split(',')]
				octsOut=int(line[6])
				octsR=int(line[7])
				acked=int(line[8])
				pr=str(100*float(octsR)/float(octsOut))
				pa=str(100*float(acked)/float(octsOut))
				down=float(acked)/(1e6*max(t))
				t,w=order(t,zip(rtt,cwnd,congS))
				rtt,cwnd,congS=[list(xx) for xx in zip(*w)]
				try:
					dic[cIP].append([t,rtt,cwnd,congS,down,pr,pa])
				except KeyError:
					dic[cIP]=[[t,rtt,cwnd,congS,down,pr,pa]]
	for w in dic.keys():
		for test in dic[w]:
			t=test[0]
			rtt=test[1]
			cwnd=test[2]
			congS=test[3]
			down=test[4]
			pr=test[5]
			pa=test[6]
			fig=pl.figure()
			ax=pl.subplot(221)
			ax.plot(t,rtt)
			pl.ylabel('RTT')
			ax=pl.subplot(222)
			ax.plot(t,cwnd)
			pl.ylabel('cwnd')
			ax=pl.subplot(223)
			ax.plot(t,congS)
			pl.ylabel('Congestion Signal')
			ax=pl.subplot(224)
			pl.xlim(0,1)
			pl.ylim(0,1)
			pl.text(.1,.8,'Throughput: \n'+str(down))
			pl.text(.1,.5,'Percentage Retransmited:\n '+pr)
			pl.text(.1,.2,'Percentage Acked: \n'+pa)
			pl.suptitle(w)
			pl.show()
				
				
				
