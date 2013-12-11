import Queue as qx
import numpy as num
from scipy.stats import t
import math
from numpy.random import randint,normal


def eventVector(a,N):
	# a is a tuple or list of int for shift position
	if a==[]:
		return [0]*N
	if type(a[0]) == tuple :
		x= [int(w[0]) for w in a]+[N]
	else:
		x=[int(w) for w in a]+[N]
	e=0
	ind=0
	out=[0]*N
	for k in x:
		out[ind:k]=[e]*(k-ind)
		if e==0:
			e=1
		else :
			e=0
		ind=k
	return out
	
def invEvent(a):
	# a is event vector
	return([1-x for x in a])
	
def roc(a,b):
	# a is real event vector
	# b is algorithm detected
	z=[a[i]*b[i] for i in range(len(a))]
	tp=float(sum(z))/sum(a)
	ap=invEvent(a)
	z=[ap[i]*b[i] for i in range(len(b))]
	fp=float(sum(z))/sum(ap)
	return(fp,tp)
	
def genEvent(l,r,d,outlier=0):
	# l is the length of the event
	# r is the l/N where N is the length of the output ( r < 1/3 )
	# d is the level of the event
	if r > 0.3 :
		print "please provide 0<r<0.3"
		return None
	sign=2*randint(2)-1
	N=int(math.ceil(l/r))
	a = normal(0,1,N)
	i1=l+randint(N-2*l)
	i2=i1+l
	a[i1:i2]=[x+sign*d for x in a[i1:i2]]
	# adding some outlier
	m=int(math.ceil(outlier*N))
	for j in range(m):
		ind=randint(N)
		sign=2*randint(2)-1
		mag=sign*randint(1,5)
		a[ind]=a[ind]+mag
	ev=eventVector([i1,i2],N)
	return [a,ev]
	
	
	
	
		  
def sigDiff(s,l,p=.01):
	#calculate significant change for x with confidance p
	tval=abs(t.ppf(p/2,l-1))
	return tval*s*math.sqrt(2.0/l)
	
def eventDetection(a,sigma=1,l=30,p=0.01):
	N=len(a)
	diff=sigDiff(sigma,l)
	q=qx.Queue(N)
	#loading
	for w in a:
		q.put(w,False)
	V=[0.0]*l
	for i in range(l):
		V[i]=q.get(False)
	ev=qx.Queue(l)
	i=l-1
	inp=qx.Queue(N)
	out=[]
	while ((not q.empty()) or (not inp.empty())) :
		if V[-1] is not None:
			if len(V)==l:
				m=num.mean(V)
			else:
				pass
			try:
				v=inp.get(False)
			except qx.Empty:
				v=q.get(False)
			i=i+1
			if abs(v-m) <= diff:
				if len(V) < l:
					V=V+[v]
				else:
					V[:]=V[1:]+[v]
				continue
			else:
				ep=1
				if v-m < 0: #Downward shift
					RSI=(m-v-diff)/(l*sigma)
					for j in range(0,l-1):
						try:
							can=inp.get(False)
						except qx.Empty:
							try:
								can=q.get(False)
							except qx.Empty:
								ep=0
								break
						ev.put(can,False)
						RSI=RSI+(-can+m-diff)/(l*sigma)
						if RSI <= 0:
							while not ev.empty():
								inp.put(ev.get(False),False)
							if len(V) < l :
								V=V+[v]
							elif len(V)==l:
								V=V[1:]+[v]
							else:
								print 'ERROR in V vector'
							ep=0
							break
					if ep==1:
						temp=list(ev.queue)
						V=[v]
						m=num.mean(V+temp)
						for w in temp:
							inp.put(w,False)
						#~ pl.plot(i,v,'r*')
						ev=qx.Queue(l)
						out.append((i,-RSI))

				else:						 #upward shift
					RSI=(v-m-diff)/(l*sigma)
					for j in range(0,l-1):
						try:
							can=inp.get(False)
						except qx.Empty:
							try:
								can=q.get(False)
							except qx.Empty:
								ep=0
								break
						ev.put(can,False)
						RSI=RSI+(can-m-diff)/(l*sigma)
						if RSI <= 0:
							while not ev.empty():
								inp.put(ev.get(False),False)
							if len(V) < l :
								V=V+[v]
							elif len(V)==l:
								V=V[1:]+[v]
							else:
								print 'ERROR in V vector'
							ep=0
							break
					if ep==1:
						temp=list(ev.queue)
						V=[v]
						m=num.mean(V+temp)
						for w in temp:
							inp.put(w,False)
						#~ pl.plot(i,v,'r*')
						ev=qx.Queue(l)
						out.append((i,RSI))
		else:
			try:
				V[V.index(None)]=inp.get(False)
			except qx.Empty:
				try:
					V[V.index(None)]=q.get(False)
				except qx.Empty:
					continue
			i=i+1
		#~ pl.plot(i,m,'ks')
	#~ pl.show()
	return out
