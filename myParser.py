import csv
import re
from ipClass import *
from myBasic import *
import networkx as nx
from graphvisu import myDraw
import numpy as num
import math

def parseCSV(f,mode=3):
	pV=[]
	t=[]
	idd=[]
	temp1=[]
	temp2=[]
	temp3=['init']
	i=0
	if mode==1: #this is good for progress variable
		val=csv.reader(f)
		for o,row in enumerate(val):
			if i>0 :
				temp1.append(row[1])
				temp2.append(row[2])
				temp3.insert(0,row[0])
				a=temp3.pop()
				if (temp3[0] != a and a!='init'):
					t.append(temp1[0:-1])
					pV.append(temp2[0:-1])
					idd.append(test_id_2_ip(a))
					temp1=[temp1[-1]]
					temp2=[temp2[-1]]
				
			else :
				patch=[row[1],row[2]]
				i=2
	if mode==2:
		val=csv.reader(f,delimiter=';')
		for row in val:
			if i==0 :
				patch=row
				i=2
				continue
			if i>0 :
				idd.append(row[0])
				t1=row[1].strip('[]')
				t2=t1.split(',')
				t.append(t2)
				v1=row[2].strip('[]')
				v2=v1.split(',')
				pV.append(v2)
	if mode==3:
		val=csv.reader(f,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for row in val:
			if i==0:
				patch=[row[1],row[2]]
				i=2
				continue
			if i>0:
				idd.append(row[0])
				t1=row[1].strip('"\'')
				t2=t1.split(',')
				v1=row[2].strip('"\'')
				v2=v1.split(',')
				pV.append(v2)
				t.append(t2)
			
			
		
	return [idd,t,pV,patch]
	
def readCSV(fName,mode=3):
	f=open('CSV/'+fName,'r')
	idd,t,v,s = parseCSV(f,mode)
	z=[]
	tt=[]
	ax=[]
	ttl=[]
	for o,w in enumerate(idd):
		tp=[float(t[o][x]) for x in range(len(t[o]))]
		vp=[float(v[o][x]) for x in range(len(v[o]))]
		tp,vp = order(tp,vp)
		z.append(vp)
		tt.append(tp)
		ttl.append(w)
	return [tt,z,s,ttl]
	
def test_id_2_ip(test_id):
	x=r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
	if type(test_id)!=list :
		ip=re.search(x,test_id)
		if ip:
			return ip.group()
	else :
		ipl=[None]*len(test_id)
		for i,w in enumerate(test_id):
			ip=re.search(x,w)
			if ip:
				ipl[i]=ip.group()
		return ipl
			
def test_id_2_time(test_id):
	if type(test_id)!=list :
		w=test_id[0:10]+' @ ' +test_id[20:28]
		return w
	else :
		tl=[None]*len(test_id)
		for i,w in enumerate(test_id):
			tl[i]=w[0:10]+' @ ' +w[20:28]
		return tl
		
def serverRead(fName):
	sIP=[]
	with open('CSV/'+fName,'r') as f:
		val=csv.reader(f,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i,item in enumerate(val):
			sIP.append(item[-1])
	del sIP[0]
	return sIP
	
def clientRead(fName):
	cIP=[]
	with open('CSV/'+fName,'r') as f:
		val=csv.reader(f,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for item in val:
			w=test_id_2_ip(item[0])
			cIP.append(w)
	del cIP[0]
	return cIP
	
def timeRead(fName):
	t=[]
	with open('CSV/'+fName,'r') as f:
		val=csv.reader(f,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for item in val:
			t.append(test_id_2_time(item[0]))
	del t[0]
	return t
			
	
def readCol(fName,L=None):
	#this functions read coloumns in L instead for the first row and return
	# n by len(L) list of list
	i=0
	p=[]
	if type(L)!=list and L:
		with open('CSV/'+fName) as f:
			val=csv.reader(f)
			for row in val:
				if i==0:
					i=1
					continue
				p.append(row[L])
	else:
		with open('CSV/'+fName) as f:
			val=csv.reader(f)
			for row in val:
				if i==0:
					i=1
					continue
				if L :
					p.append(row[L[0]:L[-1]+1])
				else:
					p.append(row)
	return p
				
def csv2gml(fName,eps=.1):
	""" this function reads csv file with heading :
		test_id  ,  minRTT  , .... ,  server
		and then makes edges between clients if their similarities
		is above eps and returns the graph """
	p = readCol(fName)
	lIP = ['a'*9]*len(p)
	lS = ['a'*9]*len(p)
	minRTT=[0]*len(p)
	sim={}
	E=[]
	axial={}
	with open('Files/serverMap','r') as f:
		st=f.read()
	serverMap=eval(st)
	uds=0
	to_del=[]
	for i,xx in enumerate(p):
		try:
			lIP[i] = ipClass(xx[0].strip()).sub('/24').string().split('/')[0].strip()
			#~ lIP[i] = xx[0].strip()
			#~ lS[i] = ipClass(xx[-1]).sub('/24').string().strip()
			lS[i]=serverMap[xx[-1]][0]
			minRTT[i] = float(xx[1])
		except ValueError:
			to_del.append(i)
			continue
		except KeyError:
			to_del.append(i)
			uds=uds+1
			continue
		try:
			axial[lIP[i]]=[lS[i]]+axial[lIP[i]]
		except KeyError:
			axial[lIP[i]]=[lS[i]]
	print 'Unrecognized test (no server info):'+str(uds)
	ll=len(p)
	for i in range(ll):
		try:
			if len(set(axial[lIP[i]])) < 2:
				to_del.append(i)
		except KeyError:
			to_del.append(i)
	lS=del_indices(lS,to_del)
	lIP=del_indices(lIP,to_del)
	minRTT=del_indices(minRTT,to_del)
	myDic=list2dic(lS,zip(lIP,minRTT))
	ll=len(myDic)
	print 'Number of servers : '+ str(ll)
	if ll<2:
		return 0
	for i,w in enumerate(myDic.keys()):
		print '--------------------------------'
		print w
		occur={}
		l=len(myDic[w])
		print 'loop '+str(i+1)+' of '+str(ll)+' :'
		print '          '+str(l)+' clients -> '+str(l*(l-1)/2)+' loops'
		print '--------------------------------'
		print '\n\n'
		v=[ww[1] for ww in myDic[w]]
		sigma=num.std(v)
		if sigma < 1:
			continue
		for comb in combinations(myDic[w],2):
			a=comb[0][0]
			b=comb[1][0]
			if a==b:
				continue
			delta=abs(comb[0][1]-comb[1][1])
			if a > b :
				link=(a,b)
			else:
				link=(b,a)
			#~ if link in occur.keys():
				#~ occur[link]=occur[link]+1
			#~ else:
				#~ occur[link]=0
			#~ if link not in sim.keys():
				#~ sim[link]=[math.exp(-delta/sigma)]
			#~ elif (link in sim.keys() and occur[link]==0):
				#~ sim[link]=sim[link]+[math.exp(-delta/sigma)]
			#~ else:
				#~ pass  # This definitely has to be changed
			try:
				occur[link]=occur[link]+1
			except KeyError:
				occur[link]=0
			try:
				if occur[link]==0:
					sim[link]=sim[link]+[math.exp(-delta/sigma)]
				else:
					sim[link][-1]=max(sim[link][-1],math.exp(-delta/sigma))
			except KeyError:
				sim[link]=[math.exp(-delta/sigma)]
	G=nx.Graph()
	for w in sim.keys():
		weight=combSum(sim[w])   # weighting function 1
		#~ if len(sim[w]) < 2:			# weighting function 2
			#~ weight=0
		#~ else:
			#~ weight=float(num.mean(sim[w]))
		if weight > eps:
			G.add_edge(w[0],w[1],weight=weight)
	if G.size()==0 or G.order()==0:
		return 0
	#~ G=score(G,1)  # Added robustness
	#~ if G.size()==0 or G.order()==0:
		#~ print 'SCORE Nullification'
		#~ return 0
	if not nx.is_connected(G):
		print "Graph is not connected, Largest component is used\n"
		G=nx.connected_component_subgraphs(G)[0]
	nx.write_graphml(G,"CSV/"+fName+'.G')
	myDraw(G,'PIC/Raw_'+fName+'.png')
	return G.size()
	
def walktrapFile(fName):
	#Writing the graph edge as needed by walktrap
	G=nx.read_graphml("CSV/"+fName+'.G')
	a=sorted(G.nodes())
	b=range(len(a))
	myDic=list2dic(a,b)
	f=open("CSV/"+fName+'.walktrap','w')
	for edge in G.edges():
		w=G[edge[0]][edge[1]]['weight']
		ind1=myDic[edge[0]][0]
		ind2=myDic[edge[1]][0]
		s= str(ind1)+' '+str(ind2)+ ' ' + str(w) + '\n'
		f.write(s)
	f.close()

def communityGraph(fName):
	#for the name of the graph add .G
	# for the name of communities add .C
	G=nx.read_graphml("CSV/"+fName+'.G')
	a=sorted(G.nodes())
	b=[str(xx) for xx in range(len(a))]
	myDic=list2dic(b,a)
	C=0
	with open('CSV/'+fName+'.C','r') as f:
		for k,line in enumerate(f):
			C=C+1
			t1=line.strip(' {}\t\n')
			t2=t1.split(',')
			cc = pickColor(k).strip()
			for w in t2:
				n=myDic[w.strip()]
				G.node[n[0].strip()]['color'] = cc
	print "Number of communities: "+str(C)
	myDraw(G,"PIC/C_"+fName+".png")
	
def UoSM_input(fName):
	#for the name of the graph add .G
	#for the name of communities add .C
	G=nx.read_graphml("CSV/"+fName+'.G')
	a=sorted(G.nodes())
	b=[str(xx) for xx in range(len(a))]
	myDic=list2dic(b,a)
	C=[]
	with open('CSV/'+fName+'.C','r') as f:
		for line in f:
			t1=line.strip(' {}\t\n')
			t2=t1.split(',')
			t=[xx.strip() for xx in t2]
			ll=[myDic[xx][0] for xx in t]
			C.append(ll)
	return C
	
	
def score(G,e):
	fg=True
	while fg:
		G=del_noises(G,e)
		if G.size()==0 or G.order()==0:
			return G
		elif min(G.degree(G.nodes(),'weight').values()) >= e :
			return G
		else:
			pass
			
def del_noises(G,e):
	nl=G.nodes()
	nw=G.degree(nl,'weight').values()
	nw,nl=order(nw,nl)
	l=range(len(nw))
	for j in l:
		if nw[j]<e:
			G.remove_node(nl[j])
		else:
			return G
	return G
		
	
	
	
		
		
