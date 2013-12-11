import numpy as num
import pylab as pl
import math

def lowpass(v,wn):
		b, a = scipy.signal.butter(6, wn, 'low')
		w = scipy.signal.filtfilt(b, a, v)
		return w
		

def sigPower(z):
	l=len(z)
	return float(sum([num.abs(x)**2 for x in z]))/float(l)
	

def fiD(m,T0,fs=1,p=.5):
	sn=2*T0*fs
	s=num.array(range(-sn/2,sn/2+1))
	l=len(s)
	out=num.array([0.0+0.0j]*l)
	for i,n in enumerate(s):
		if n < T0*fs/2 and n >= -T0*fs/2:
			out[i]=num.exp(-2.0*1j*math.pi*n*m/float(T0*fs))
	return out
	
def syncAve(z,l):
	fg=True
	ind=l
	out=num.array([0.0]*l)
	z=num.array(z)
	i=0
	while fg:
		try:
			unused=z[ind-1]
			if len(out)==0:
				out=z[(i*l):ind]
			else:
				out=out+z[(i*l):ind]
			ind=ind+l
			i=i+1
		except IndexError:
			break
	return sigPower(out)
	
	
if __name__=='__main__':
	t=num.array(range(24*30))
	y=num.sin(2*math.pi*t/24)+num.sin(2*math.pi*t/48)+.1*num.random.normal(0,1,24*30)
	#~ y=num.random.normal(0,1,24*30)+0.0j
	TT=[6,12,18,24,32,36,44,48]
	for w in TT:
		mag=syncAve(y,w)
		pl.vlines(w,0,mag)
	pl.show()
	
		
		
	
	
