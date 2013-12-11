import sys
import pylab as pl
import numpy as num
import math
import itertools
import scipy.stats
import scipy.signal

def dNorm(x,mode=1):
		l=len(x)
		if mode==1 :
			a=num.mean(x)
			b=num.std(x)
			y=[(z-a)/b for z in x] 
		if mode ==2 :
			a=num.mean(x)
			b=num.std(x)
 			x1=[float((z-a))/float(b) for z in x]
			y=[1.0/float(1+num.exp(-xx)) for xx in x1]
		return y

def makeUniform(t,v,r,t_start,t_end,fg):
	chunk=int(num.round(float(t_end-t_start)/float(r)))
	tc=[t_start+i*r for i in range(chunk+1)]
	tc[-1]=t_end
	val=[[]]*len(tc)
	if (type(t[0])==list):
		l=len(t)
	else:
		l=1
	for i in range(l):
		if type(t[i])==list: 
			tt=t[i]
			vv=v[i]
		else :
			 tt=t 
			 vv=v
		for j in range(len(tt)):
			for h in range(len(tc)-1):
				if (tc[h] <= tt[j] < tc[h+1] or tt[j]==tc[-1]):
					val[h]=val[h]+[vv[j]]
					break
	sv=[num.mean(val[x]) if val[x]!=[] else fg for x in range(len(tc)-1)]
	return [tc[0:-1],sv]

def pairing(t1,v1,t2,v2,th=1):
	p=[]
	for tx,vx in zip(t1,v1):
		for ty,vy in zip(t2,v2):
			if abs(ty-tx) < th :
				p.append((vx,vy))
	return p	
	
	
	# This is a very simple outlier detection have to be more sophisticated
def replaceOutlier(v,p):
	l=len(v)
	w=v
	w[0:p]=[num.median(w[0:p])]*p
	a=float(scipy.stats.mstats.mquantiles([math.fabs(x) for x in num.diff(w)], prob=0.99))
	print a
	oD=0
	for j in range(l):
		if j<p:
			continue
		else :
			if (math.fabs(w[j]-w[j-1]) > a and oD == 0) :
				rO=w[j]
				w[j]=w[j-1]
				
			

	return w
def lowpass(v,wn):
		b, a = scipy.signal.butter(6, wn, 'low')
		w = scipy.signal.filtfilt(b, a, v)
		return w

def missValueFill(v,smoothing_factor,fg):
	qu=[]
	for i,w in enumerate(v):
		if w!=fg :
			qu.append(w)
			if len(qu)>smoothing_factor : qu.pop(0)
		if w==fg :
			v[i]=num.mean(qu)
			qu.append(v[i])
			if len(qu)>smoothing_factor : qu.pop(0)

	for i,w in enumerate(v):
		if math.isnan(w):
			continue
		else:
			v[0:i]=[v[i]]*i
			break
	return v
	
def dataClean(t,v,wn=0.1,res=1,fg=-10,smoothingSlide=5):
		#fg=-1 #fllag for missing value
		#wn=0.1 # lowpass normalized bandwidth
		# smoothingSlide=5
		vr1 = lowpass(v,wn)
		#~ tp,vr2 =makeUniform(t,vr1,1,t[0],t[-1],fg)
		#~ vp=missValueFill(vr2,smoothingSlide,fg)
		#~ week_sample=(24*7)/res
		#~ week=vp[0:week_sample]
		#~ vr=trendOmit(vp[week_sample:-1],week)
		#~ tr=tp[week_sample:-1]
		return [t,vr1]
		
def trendOmit(v,A):
	# A is sample cleaned data with no event
	# A[0] should point to the same day of week and same hour as v[0]
	l=len(v)
	d=len(A)
	k=l/d
	#~ w=v
	for c in range(k-1):
		w=v[(c*d):((c+1)*d)]
		v[(c*d):((c+1)*d)]=[math.log(v[(c*d):((c+1)*d)][x])-math.log(A[x]) for x in range(d)]
		#~ A=v[(c*d):((c+1)*d)]
	c=k
	v[(c*d):-1]=[v[(c*d):-1][x]-A[x] for x in range(len(v[(c*d):-1]))]
	return v
	
#~ 
#~ if __name__ == '__main__':
	#~ v=[0,2,4,5,3,2,5,6,100,100,1,2,4,5,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7]
	#~ print replaceOutlier(v,3)
	
