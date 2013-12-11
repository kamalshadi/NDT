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
		

if __name__ == '__main__':
	(options, args) = parse_args()
	fName=options.fName
	fg=0
	with open('CSV/'+fName+'.net','r') as f:
		i=0
		for line in f:
			lf=[]
			if i==0:
				i=i+1
				s="echo '(lat,long)'  > CSV/"+fName+".lat"
				r=os.system(s)
				continue
			print 'prefix '+str(i)
			i=i+1
			st=line.split('[')[1]		
			uos=eval('['+st)
			for w in uos:
				lu=[]
				t=[xx.strip() for xx in w.split('U')]
				qq=[]
				for h in t:
					sub,l1=h.split('/')
					l=int(l1)
					mask=int('1'*l+'0'*(32-l),2)
					qq.append('format_ip(parse_ip(web100_log_entry.connection_spec.remote_ip) & ' + str(mask) + ')= \"'+ sub.strip() +'\"')
				q=' OR \n'.join(qq)
				with open('MyQuery/uos2lat','r') as f:
					query1=f.read()
				query = query1.replace('COND',q)
				add='bq -q --format=csv query --max_rows 100000 '
				shel=add+'\''+query+'\' > CSV/'+fName+'.temp'
				os.system(shel)
				with open('CSV/'+fName+'.temp','r') as temp:
					jj=0
					for latlon in temp:
						if jj==0:
							jj=1
							continue
						lat,lon=latlon.split(',')
						tup=(lat.strip(),lon.strip())
						lu.append(tup)
				lf.append(lu)
			shel='echo "'+str(lf)+'">>CSV/'+fName+'.lat'
			os.system(shel)
