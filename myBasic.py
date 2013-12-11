from itertools import combinations
import random
from math import radians, cos, sin, asin, sqrt
def order(v,w):
	a=zip(v,w)
	a.sort()
	l=zip(*a)
	v=list(l[0])
	w=list(l[1])
	return [v,w]
	
def del_indices(ls,ind):
	w=[i for j, i in enumerate(ls) if j not in ind]
	return w
def makeOneLineCSV(fName):
	w=[]
	with open('csv/'+fName,'r') as f:
		for line in f:
			w.append(line.strip())
		s=','.join(w)
	f=open('csv/'+fName,'w')
	f.write(s)
	f.close()
	
def flatten(ls):
	return [item for sublist in ls for item in sublist]
	
def list2dic(ls,zs=None,ts=None):
	if zs is None:
		d={}
		for w in ls:
			if w in d.keys():
				d[w]=d[w]+1
			else:
				d[w]=1
		return d
	else:
		d={}
		for i,w in enumerate(ls):
			if w in d.keys():
				if ts is None:
					d[w]=d[w]+[zs[i]]
				else:
					d[w][1]=d[w][1]+[zs[i]]
					d[w][0]=d[w][0]+[ts[i]]
			else:
				if ts is None:
					d[w]=[zs[i]]
				else:
					d[w]=[[ts[i]],[zs[i]]]
		return d

def bracket(a,b,g):
	# 'a' is value list and 'b' is cluster labels
	# output is a list of list and a list of clusters
	# g is maximum gap allowed
	l=len(a)
	if l!=len(b):
		print 'length error in input of bracketing'
		return
	a,b=order(a,b)
	prev=b[0]
	prevV=a[0]
	outB=[]
	outC=[]
	s=a[0]
	for i in range(len(a)):
		if (b[i]!=prev or (a[i]-prevV)>g):
			outB.append([s,prevV])
			outC.append(prev)
			s=a[i]
			prevV=a[i]
			prev=b[i]
		else:
			prevV=a[i]
			prev=b[i]
	outB.append([s,prevV])
	outC.append(prev)
	return [outB,outC]
	
def joinBr(B,C):
	l=len(B)
	p=B[0]
	c=C[0]
	Br=[]
	Cr=[]
	bb=0
	jump=0
	for i in range(l):
		if i==0 : continue
		if (B[i][0]-p[1]<2) and (C[i]==c):
			p=[p[0],B[i][1]]
			bb=1
		else:
			Br.append(p)
			Cr.append(c)
			bb=0
			p=B[i]
			c=C[i]
	if bb==1:
		Br.append(p)
		Cr.append(c)
	else:
		Br.append(B[-1])
		Cr.append(C[-1])		
	return [Br,Cr]
	
def combSum(v,q=2):
	l=len(v)
	s=0.0
	if l < q:
		return 0
	for comb in combinations(v,2):
		s=s+comb[0]*comb[1]
	return 2*s / (l*(l-1))
	

def randColor():
	x = random.randint(0, 16777215)
	s= "#%x" % x
	return s

def pickColor(m):
	n=int(m)
	c=["#ffffcc","#ff5400","#a7bf42","#ffff00",
	"#9937d2","#feb8c6","#780909","#cde312",
	"#19bac1","#fbfbfb","#195839","#514fad",
	"#0f0e1c","#9e143f","#0bf01c","#779679",
	"#0f1e11","#0e103f","#00001c","#779fff",
	"#f44f00","#b2b200","#0f0f10","#1b2100"]
	if n >= len(c):
		print "Color index exceeded. 'blue' was returned as default"
		return '#0000ff'
	return c[n]
	
def header2id(fName,key):
	#add id to each line showing the number of headers starting with key
	i=0
	m=0
	with open(fName,'r') as f:
		for line in f:
			if m==0:
				p=line.strip()+',Community,Quantity\n'
			t=line.split(',')
			if t[0]==key:
				if m!=0:
					for w in dic.keys():
						p=p+w+','+str(dic[w])+'\n'
				i=i+1
				dic={}
			else:
				w=line.strip()+','+str(i)
				if w not in dic.keys():
					dic[w]=1
				else:
					dic[w]=dic[w]+1
			m=1
	for w in dic.keys():
		p=p+w+','+str(dic[w])+'\n'
	return p

def geoDis(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km
    
#~ def avgDis(C):
	#~ """C is the list of the cities"""
	#~ with open('Files/latLong','r') as f:
		#~ for i,line in enumerate(f):
			#~ if i==0:
				#~ continue
			#~ city.append
			
