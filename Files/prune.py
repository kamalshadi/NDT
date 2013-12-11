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
def flatten(ls):
	return [item for sublist in ls for item in sublist]
if __name__=='__main__':
	a=[]
	ip=[]
	with open('ndtServers','r') as f:
		for line in f:
			w=line.split(' ')
			a.append(w[0][0:3])
			ip.append(w[1].strip())
	dic=list2dic(ip,a)
	with open('serverMap','w') as f:
		f.write(str(dic))
	with open('serverMap','r') as f:
		st=f.read()
	dic=eval(st)
	print type(dic)
	
