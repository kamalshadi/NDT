from myBasic import *
from itertools import combinations
import pylab as pl
import numpy as num


def PDF(a,nBins=100):
	pdf,bins=num.histogram(a,nBins,density=True)
	x= bins[0:len(pdf)]
	g=bins[2]-bins[1]
	return [[o*g for o in pdf],x]
	
def CDF(a):
	nBins=100
	pdf,bins=num.histogram(a,nBins,density=True)
	cdf1=num.cumsum(pdf)
	g=bins[2]-bins[1]
	cdf=[x*g*100 for x in cdf1]
	x= bins[0:len(cdf)]
	return [cdf,x]

if __name__=='__main__':
	fName='verizon'
	place='CSV/'+fName+'.lat'
	dis=[]
	disu=[]
	with open(place,'r') as f:
		i=0
		for line in f:
			if i==0:
				i=1
				continue
			w=eval(line)
			h=flatten(w)
			if len(h)>1:
				for comb in combinations(h,2):
					dis.append(geoDis(float(comb[0][1]), float(comb[0][0]), float(comb[0][1]), float(comb[1][0])))
			for hu in w:
				if len(hu)>1:
					for comb in combinations(hu,2):
						disu.append(geoDis(float(comb[0][1]), float(comb[0][0]), float(comb[0][1]), float(comb[1][0])))
	p,x=CDF(dis)
	pl.plot(x,p,label='Prefix-only clustering')
	p,x=CDF(disu)
	pl.plot(x,p,'r',label='Our method')
	pl.xlabel('Distance between clients (km)',fontsize=20)
	pl.ylabel('CDF',fontsize=20)
	pl.legend()
	pl.title('Verizon network (Pre-Clustered in /24)',fontsize=20)
	pl.show()
	
				
				
				
			
