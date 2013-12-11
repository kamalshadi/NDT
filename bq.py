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
    parser.add_option('-s', '--server', dest='server', default=None, help='Optional: subnet of servers')
    parser.add_option('-p', '--prefix', dest='prefix', default=None, help='optional: prefix of clients')
    parser.add_option('-l', '--continent', dest='continent', default=None, help='optional: Continent of client')
    parser.add_option('-k', '--country', dest='country', default=None, help='optional: Country of client')
    parser.add_option('-r', '--region', dest='region', default=None, help='optional: region of client')
    parser.add_option('-c', '--city', dest='city', default=None, help='optional: City of client')
    parser.add_option('-t', '--table', dest='table', default=None, help='Required: Time in YEAR_MO format')
    parser.add_option('-f', '--filename', dest='fName', default=None, help='Required: Filename for output')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    options, args = parser.parse_args()
    if options.table is None or options.fName is None:
        print 'Error: Please provide --time in yyyy_mo format and --filename'
        sys.exit(1)
    return (options, args)


if __name__ == '__main__':
    options, args = parse_args()
    f = open('MyQuery/queryStr', 'r')
    qstr = f.read()
    qstr1 = qstr.replace("'", '"')
    server = prefix = options.server
    prefix = options.prefix
    country = options.country
    region = options.region
    city = options.city
    continent = options.continent
    table = options.table
    t1 = table.split(',')
    fName = options.fName
    st = []
    field1 = []
    field2 = []
    where = []
    for w in t1:
        st.append('[measurement-lab:m_lab.' + w + ']')

    st = ','.join(st)
    qstr = qstr1.replace('TABLE', st)
    if prefix:
        pp = prefix.split(',')
        st = []
        for w in pp:
            ip, s = [ xx.strip() for xx in w.split('/') ]
            a = int('1' * int(s) + '0' * (32 - int(s)), 2)
            st.append('format_ip(parse_ip(web100_log_entry.connection_spec.remote_ip) &' + str(a) + ')= "' + ip + '" ')

        con = '(' + '\n OR \n'.join(st) + ')'
        where.append(con)
    if server:
        temp = server.split(',')
        st = []
        for w in temp:
            ip, s = [ xx.strip() for xx in w.split('/') ]
            a = int('1' * int(s) + '0' * (32 - int(s)), 2)
            st.append('format_ip(parse_ip(web100_log_entry.connection_spec.local_ip) &' + str(a) + ')= "' + ip + '" ')

        con = '(' + '\n OR \n'.join(st) + ')'
        where.append(con)
    if continent:
        if continent == '?':
            field1.append('connection_spec.client_geolocation.continent_code as continent')
            field2.append('continent')
        else:
            temp = continent.split(',')
            field1.append('connection_spec.client_geolocation.continent_code as continent')
            field2.append('continent')
            st = [ 'connection_spec.client_geolocation.continent_code="' + xx.strip() + '"' for xx in temp ]
            where.append('(' + ' OR \n'.join(st) + ')')
    if country:
        if country == '?':
            field1.append('connection_spec.client_geolocation.country_name as country')
            field2.append('country')
        else:
            print country
            temp = country.split(',')
            field1.append('connection_spec.client_geolocation.country_name as country')
            field2.append('country')
            st = [ 'connection_spec.client_geolocation.country_name="' + xx.strip() + '"' for xx in temp ]
            where.append('(' + ' OR \n'.join(st) + ')')
    if region:
        if region == '?':
            field1.append('connection_spec.client_geolocation.region as region')
            field2.append('region')
        else:
            temp = region.split(',')
            field1.append('connection_spec.client_geolocation.region as region')
            field2.append('region')
            st = [ 'connection_spec.client_geolocation.region="' + xx.strip() + '"' for xx in temp ]
            where.append('(' + ' OR \n'.join(st) + ')')
    if city:
        if city == '?':
            field1.append('connection_spec.client_geolocation.city as city')
            field2.append('city')
        else:
            temp = city.split(',')
            field1.append('connection_spec.client_geolocation.city as city')
            field2.append('city')
            st = [ 'connection_spec.client_geolocation.city="' + xx.strip() + '"' for xx in temp ]
            where.append('(' + ' OR \n'.join(st) + ')')
    if field1 == []:
        qstr = qstr.replace(',FIELD1', '')
        qstr = qstr.replace(',FIELD2', '')
    else:
        qstr = qstr.replace('FIELD1', ','.join(field1))
        qstr = qstr.replace('FIELD2', ','.join(field2))
    if where == []:
        qstr = qstr.replace('COND', '')
    else:
        cond = ' AND \n' + ' AND \n'.join(where)
        qstr = qstr.replace('COND', cond)
        f = open('CSV/' + fName, 'w')
        qq = "bq -q --format=csv query --max_rows 100000 '" + qstr.strip() + ";' > CSV/" + fName
        r = os.system(qq)
        print 'File generated: ' + fName
