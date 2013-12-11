#!/usr/bin/env python

from myParser import *
from ipCluster import cluster2sub
import csv
import os
import sys
import subprocess
import statvfs
import urllib
from myBasic import *


def usage():
    return """
Summary:
./geoUoS -p False/True -f <filename> 
locate the UoS in city resolution
"""
def header2id(fName,key):
	#add id to each line showing the number of headers starting with key
	dic={}
	fg=1
	with open('CSV/'+fName+'.geo','r') as f:
		for k,line in enumerate(f):
			t=line.strip().split(',')
			if t[0]=='Community':
				C=t[1]
			elif t[0]==key and fg==1:
				p=line.strip()+',Community,Quantity\n'
				fg=0
			elif t[0]==key:
				continue
			else:
				if dic.keys() and (line.strip()+','+C in dic.keys()):
					dic[line.strip()+','+C]=dic[line.strip()+','+C]+1
				else:
					dic[line.strip()+','+C]=1
	for w in dic.keys():
		p=p+w+','+str(dic[w])+'\n'
	with open('CSV/'+fName+'.geo','w') as f:
		f.write(p)
		

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option("-f", "--fileName", dest="fName", default=None, 
                      help="Required: filename for geo data")
        
    
                       
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    if options.fName is None:
        print "Error: Please provide --filename to read data \n \
        (do not include .G suffix)"
        sys.exit(1)

    return (options, args)
    
    
def set_size(m):
	quant=int(m)
	if quant < 5 :
		return 'tiny'	
	elif 4<quant<9 :
		return 'small'
	else:
		return 'mid'

def marker2par(s):
	return "markers=color:"+s[0]+"|size:"+s[1]+"|"+s[-1]
	
if __name__ == '__main__':
	(options, args) = parse_args()
	fName=options.fName
	with open("CSV/"+fName+".geo",'r') as f:
		s=[]
		for j,line in enumerate(f):
			if j==0:continue
			city,region,C,quant=[xx.strip() for xx in line.split(',')]
			lp=[pickColor(C).replace('#','0x'),set_size(quant),city+","+region]
			s.append(marker2par(lp))
	ss='&'.join(s)
	base="http://maps.googleapis.com/maps/api/staticmap?size=1200x800&"
	dic={}
	ad=base+ss+"&sensor=false"
	print ad
	urllib.urlretrieve(ad,"PIC/"+fName+".png")


