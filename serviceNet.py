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
    parser.add_option('-t', '--table', dest='table', default=None, help='Required: Time in YEAR_MO format') 
    parser.add_option('-s', '--suffix', dest='suf', default=None, help='Roptional: change the filename by adding suffix')         
        
    
                       
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    if options.fName is None or options.table is None:
        print "Error: Please provide --filename and --table to download data "
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
	suf=options.suf
	t1=options.table
	t2=t1.split(',')
	tt=[]
	for w in t2:
		tt.append("[measurement-lab:m_lab."+w.strip()+"]")
	table=','.join(tt)
	log=fName
	if suf is not None:
		fName=fName+suf
	fg=0
	count=0
	if not os.path.exists('CSV/D-'+fName):
		os.makedirs('CSV/D-'+fName)
	with open('CSV/'+log+'.net','r') as f:
		i=0
		for line in f:
			if i==0:
				i=1
				continue
			st=line.split('[')[1]		
			uos=eval('['+st)
			for w in uos:
				t=[xx.strip() for xx in w.split('U')]
				qq=[]
				for h in t:
					sub,l1=h.split('/')
					l=int(l1)
					mask=int('1'*l+'0'*(32-l),2)
					qq.append('format_ip(parse_ip(web100_log_entry.connection_spec.remote_ip) & ' + str(mask) + ')= \"'+ sub.strip() +'\"')
				q=' OR \n'.join(qq)
				with open('MyQuery/uosData','r') as f:
					query1=f.read()
				query = query1.replace('COND',q)
				query = query.replace('TABLE',table)
				add='bq -q --format=csv query --max_rows 100000 '
				shel=add+'\''+query+'\' > CSV/D-'+fName+'/uos'+str(count)
				os.system(shel)
				count=count+1
				print 'uos number finished: '+str(count)
