#!/usr/bin/env python

import csv
import os
import sys
import subprocess
import statvfs
import networkx as nx
from ipCluster import *
from ipClass import *
from myBasic import *

def usage():
    return """
graph from the similarity graph based on RTT
look at csv2gml
"""
		
def csv2gml(fName,eps=.3):
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
		occur={}
		l=len(myDic[w])
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
		print "Graph is not connected, Looped over components."
	return nx.connected_component_subgraphs(G)
	
def walktrapFile(G):
	#Writing the graph edge as needed by walktrap
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
	
def UoSM_input(G):
	#for the name of the graph add .G
	#for the name of communities add .C
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

def parse_args():
    from optparse import OptionParser
    parser = OptionParser(usage=usage())
    parser.add_option("-f", "--file", dest="fName", default=None, 
                      help="Required: Filename to read the data")
    parser.add_option("-e", "--eps", dest="eps", default=.3, type="float",
                      help="Optional: edge threshold")
    parser.add_option('-g', '--gap', dest='g', default='/24', help='Optional: threshold to split brackets')
    parser.add_option('-p', '--prefix', dest='prefix', default=None, help='Required: filename for data')
                       
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    (options, args) = parser.parse_args()
    if options.fName is None:
        print "Error: Please provide --dir to read data \n \
        (do not include D- prefix)"
        sys.exit(1)
    return (options, args)


if __name__ == '__main__':
	(options, args) = parse_args()
	fName=options.fName
	g = options.g
	prefix = options.prefix
	Gl=csv2gml(fName)
	if Gl!=0:
		print "Number of Components: "+str(len(Gl))
		uos=[]
		for j,G in enumerate(Gl):
			print 'Component '+str(j)
			walktrapFile(G)
			qq = 'WalkTrap/walktrap CSV/' + fName + ".walktrap -b -d1 -s |grep community| cut -d'=' -f2 > CSV/" + fName + '.C'
			os.system(qq)
			C = UoSM_input(G)
			print 'Number of Communities: '+str(len(C))
			uos = uos+cluster2sub(C,g)
		with open('CSV/' + fName + '.net', 'a+b') as f:
			f.write(prefix+','+str(uos)+'\n')
	
