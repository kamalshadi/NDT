#~ from util import search_binary
#~ import numpy as num
#~ import datetime as dx
#~ import calendar as cal
#~ import time
import ipaddress as ix
if __name__ == "__main__":
	fName="2013_09-ip-98.112.0.0s13" #Name of the file for uos
	paris="2013_10_02" #Name of the parsed paris-traceroutes
	with open('CSV/'+fName+'.uos','r') as f:
		st=f.read()
	uos=eval(st)
	networks=[]
	for w in uos:
		t=[unicode(xx.strip()) for xx in w.split('U')]
		networks.append([ix.ip_network(xx) for xx in t])
	dat=[{}]*len(networks)
	i=0
	j=0
	with open("Paris/"+paris,'r') as f:
		for q,line in enumerate(f):
			if i==0:
				i=1
				continue
			w =unicode(line.strip().split(' ')[2])
			ip=ix.ip_address(w)
			for kk,net in enumerate(networks):
				com=-1
				for sub in net:
					if ip in net:
						com=kk
						break
				if com!=-1:
					break
			if com!=-1:
				server=line.strip().split(' ')[1]
				val=line.strip().split(' ')[-1]
				try:
					dat[com][server].append(val)
				except KeyError:
					dat[com][server]=[val]
