import numpy as num
import pylab as pl
from scipy.stats import t
import math
import Queue as qx
from eventDetection import *

def sigDiff(s,l,p=.01):
	#calculate significant change for x with confidance p
	tval=abs(t.ppf(p/2,l-1))
	return tval*s*math.sqrt(2.0/l)


def test_event(diff,m,y):
	if abs(m-y)<diff:
		return 0
	if y-m>=diff:
		return +1
	if y-m<=diff:
		return -1
		
def qiHe(x,W=30,l=10,a=0.4,b=0.3):
	# x is N-sample sequence
	# W is window size
	# a is outlier thereshold
	# b is LS thereshold
	# l is intial training < W 
	N=len(x)
	pl.plot(range(N),x,'b-')
	c=W
	vc=x[0:c]
	fg=True 
	loop=0
	while fg:
		m=num.median(vc)
		s=num.std(vc)
		pl.plot([loop*W+i for i in range(W)],[float(m)]*W,'r--')
		for i,w in enumerate(vc):
			#~ pl.plot(loop*W+i,w,'r*')
			if abs(w-m) > 3*s :
				pl.plot(loop*W+i,w,'r*')
		loop=loop+1
		if (loop*W)+c > N :
			break
		vc=x[(loop*W):((loop*W)+c)]
		
		
if __name__=='__main__':
	l=30	# parameter of an algorithm
	p=.01
	N=3000
	mu, sigma, n = 0, 1, N
	a = num.random.normal(mu,sigma,n)
	#~ diff=sigDiff(sigma,l)   # has to be replaced by t-statistics
	#~ print diff
	a[100:140]=a[100:140]-2
	a[200:227]=a[200:227]+2
	a[260]=-5.0
	a[500:520]=a[500:520]+1
	a[670:700]=a[670:700]-2
	a[1000:1500]=a[1000:1500]+1
	a[2000:2227]=a[2000:2227]-5
	a[2227:2500]=a[2227:2500]+3
	#~ a,ev1=genEvent(l,.1,1,.1)
	out=eventDetection(a,1,l,p)
	f, (ax1, ax2) = pl.subplots(2, sharex=True, sharey=False)
	ax1.plot(range(len(a)),a)
	pl.ylabel('Sequence Magnitude',fontsize=20)
	pl.xlabel('Sample Number',fontsize=20)
	for w in out:
		if w[1]>0 :
			ax2.vlines(w[0],0,abs(w[1]),color='green',linewidths=4)
		else:
			ax2.vlines(w[0],0,abs(w[1]),color='red',linewidths=4)
	pl.ylabel('Event Power',fontsize=20)
	f.subplots_adjust(hspace=0)
	pl.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
	pl.show()

