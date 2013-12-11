from ipClass import *
from subnet import *
import pylab as pl
import numpy as num
from ipCluster import *
if __name__=='__main__':
	lse=[]
	lsb=[]
	oo=[]
	with open('Inputs/comcast','r') as f:
		st=f.read()
	ip=st.split(',')
	for xx in ip:
		a=subnet(xx.strip())
		aa=ipClass(a.first())
		az=ipClass(a.last())
		lse.append(az.int())
		lsb.append(aa.int())
	b=sorted(lsb)
	e=sorted(lse)
	l=len(b)
	clus=[('0','0')]*l
	state_end=-1
	state_beg=-1
	for i,st in enumerate(b):
		if i==l-1:
			pass
		if e[i]>state_end and st> state_beg:
			state_end=e[i]
			state_beg=st
			clus[i][0]=st
			clus[i][1]=e[i]
		elif 
		
		
		
	
