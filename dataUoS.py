#!/usr/bin/env python

import csv
import os
import sys
import subprocess
import statvfs

def usage():
    return """
Summary:
./dataUoS -t time -f <filename> 
download upload or download for whole prefixes in Inputes/fname 
and log them to Dump/fname.dat
"""
		

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option("-f", "--fileName", dest="fName", default=None, 
                      help="Required: filename for geo data")
    parser.add_option('-t', '--table', dest='table', default=None, help='Required: Time in YEAR_MO format')           
        
    
                       
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    if options.fName is None or options.table is None:
        print "Error: Please provide --filename to read data \n \
        (do not include .G suffix)"
        sys.exit(1)

    return (options, args)
		

if __name__ == '__main__':
	(options, args) = parse_args()
	fName=options.fName
	fg=0
	t1=options.table
	t2=t1.split(',')
	tt=[]
	for w in t2:
		tt.append("[measurement-lab:m_lab."+w.strip()+"]")
	table=','.join(tt)
	with open('Inputs/'+fName,'r') as f:
		st=f.read()
	uos=st.split(',')
	log="Dump/"+fName
	tID=[]
	with open(log,'w') as f:
		for i,w1 in enumerate(uos):
			w=w1.strip()
			try:
				sub,l1=w.split('/')
			except ValueError:
				pass
			l=int(l1)
			mask=int('1'*l+'0'*(32-l),2)
			tID.append('format_ip(parse_ip(web100_log_entry.connection_spec.remote_ip) & ' + str(mask) + ')="'+sub.strip()+'"')
		l=len(tID)
		m=l
		ing=0
		while l>0:
			temp=tID[0:20]
			cond='\n OR \n'.join(temp)
			del tID[0:20]
			l=len(tID)
			with open('MyQuery/servicePlan','r') as f2:
				query1=f2.read()
			query1 = query1.replace('COND',cond)
			query = query1.replace('TABLE',table)
			add='bq -q --format=csv query --max_rows 1000000 '
			if ing==0:
				shel=add+'\''+query+'\' > '+log+'.dat'
				print "Downloading NDT web100 variables ..."
				ing=1
			else:
				shel=add+'\''+query+'\' | tail -n+2 >> '+log+'.dat'
			#~ print shel
			#~ raw_input()
			r=os.system(shel)
			print 'Percentage remained: '+str((1-float(m-l)/m)*100)
