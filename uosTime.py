from myBasic import order
import pylab as pl
import numpy as num
from eventDetection import *
from scipy.stats.mstats import mquantiles

	
def PDF(a,nBins=50):
	pdf,bins=num.histogram(a,nBins,density=True)
	x= bins[0:len(pdf)]
	g=bins[2]-bins[1]
	return [[o*g for o in pdf],x]
	

if __name__=='__main__':
	l=20
	p=.01
	ii=['81','352','349','88']
	fName='comcast'
	out=[]
	tt=[]
	xmin=1e16
	xmax=0
	pn=0
	down=[]
	for i in ii:
		ad='CSV/D-'+fName+'/uos'+i
		mb=[]
		t=[]
		with open(ad,'r') as f:
			k=0
			for line in f:
				if k==0:
					k=1
					continue
				mb.append(float(line.split(',')[3]))
				t.append(float(line.split(',')[1]))
		down=down+mb
		t,a1=order(t,mb)
		xmin=min(min(t),xmin)
		xmax=max(max(t),xmax)
		tt.append(t)
		out.append(eventDetection(a1,num.std(a1),l,p))
		pl.subplot(2,2,pn)
		pn=pn+1
		pl.plot(t,a1)
		pl.xlabel('Time',fontsize=20)
	pl.suptitle('Download Throughput for different uos in comcast',fontsize=20)
	pl.show()
	#~ f, (ax1, ax2) = pl.subplots(2, sharex=True, sharey=False)
	#~ ax1.plot(range(len(a1)),a1)
	#~ pl.ylabel('Sequence Magnitude',fontsize=20)
	#~ pl.xlabel('Sample Number',fontsize=20)
	for j in [0,1,2,3]:
		pl.subplot(2,2,j)
		for w in out[j]:
			if w[1]>0 :
				pl.vlines(tt[j][w[0]],0,abs(w[1]),color='green',linewidths=4)
			else:
				pl.vlines(tt[j][w[0]],0,abs(w[1]),color='red',linewidths=4)
		pl.xlim(xmin,xmax)
		pl.xlabel('Time',fontsize=20)
	pl.suptitle('Event Power',fontsize=20)
	#~ f.subplots_adjust(hspace=0)
	#~ pl.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
	pl.show()
	q1,q2=mquantiles(down,[.05,.95])
	down1=[xx for xx in down if xx<10]
	a,b=PDF(down1)
	pl.plot(b,a)
	pl.show()
