import sys
from scipy import signal
from scipy.signal import periodogram

def getPowerSpectralDensity(X,fs=1.0):
	assert fs > 0
	f, Pxx_den = signal.periodogram(X, fs,scaling='density',window=None,detrend=False)
	return (f,Pxx_den) 


if __name__ == '__main__':
	if len(sys.argv) < 3:
		fs = 200
		file = open("SampleData.txt",'r')
	else:
		fs = int(sys.argv[1])
		file = open(sys.argv[2],'r')
	lines = file.readlines()
	t = []
	p = []
	for iline in lines:
		data = list(map(float,iline.split()))
		t.append(data[0])
		p.append(data[1])
	f,p_den = getPowerSpectralDensity(p,fs)

	with open("PSD.txt",'w') as ofile:
		for ifreq,ipxx in zip(f,p_den):
			ofile.write(str(ifreq)+","+str(ipxx)+"\n")


	

