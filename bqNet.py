#!/usr/bin/env python

import csv
import os
import sys
import subprocess
import statvfs

def usage():
    return """
    Summary:Using bq.py you could download NDT data used for Community detection and clustering
    The data will be saved in csv file in format:
    test_id, minRTT, DownloadRate, City, Region, country ,Server
    Note that geolocation if not queried by user explicitly are not included.
    you could filter tha data by prefix -p and location -k -r -c
    -p prefix in form 0.0.0.0/x
    -k Countries of origion
    -r regions of origin (State)
    -c cities of origin
    -s Servers running test (add /x to the end of server name considering its subnet)
    -t unix start and end time (required)\nExample :
    ./bq.py -t 2013_09 -p 98.112.0.0/16,98.113.0.0/17 -k United States -r CA,NY -t 2013_09 
    ./bq.py -t 2013_09,2013_10 -p 98.0.0.0/13 -k ? -r  ? -c ? (to have field of geolocation)
			"""

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option('-p', '--prefix', dest='prefix', default=None, help='optional: prefix of clients')
    parser.add_option('-t', '--table', dest='table', default=None, help='Required: Time in YEAR_MO format')
    parser.add_option('-f', '--filename', dest='fName', default=None, help='Required: Filename for output')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    options, args = parser.parse_args()
    if options.table is None or options.fName is None or options.prefix is None:
        print 'Error: Please provide --time in yyyy_mo format and --filename and --prefix'
        sys.exit(1)
    return (options, args)


if __name__ == '__main__':
    options, args = parse_args()
    f = open('MyQuery/queryStrNet', 'r')
    qstr = f.read()
    qstr1 = qstr.replace("'", '"')
    prefix = options.prefix
    table = options.table
    t1 = table.split(',')
    fName = options.fName
    st = []
    where = []
    for w in t1:
        st.append('[measurement-lab:m_lab.' + w + ']')
    st = ','.join(st)
    qstr = qstr1.replace('TABLE', st)
    pp = prefix.split(',')
    st = []
    for w in pp:
    	ip, s = [ xx.strip() for xx in w.split('/') ]
    	a = int('1' * int(s) + '0' * (32 - int(s)), 2)
    	st.append('format_ip(parse_ip(web100_log_entry.connection_spec.remote_ip) &' + str(a) + ')= "' + ip + '" ')
    con = '(' + '\n OR \n'.join(st) + ')'
    where.append(con)
    cond = ' AND \n' + ' AND \n'.join(where)
    qstr = qstr.replace('COND', cond)
    f = open('CSV/' + fName, 'w')
    qq = "bq -q --format=csv query --max_rows 100000 '" + qstr.strip() + ";' > CSV/" + fName
    r = os.system(qq)
