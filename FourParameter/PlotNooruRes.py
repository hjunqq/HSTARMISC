import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
matplotlib.rcParams['text.latex.preamble'] = ['\\usepackage{CJK}',
	   r'\AtBeginDocument{\begin{CJK}{UTF8}{gbsn}}',
	   r'\AtEndDocument{\end{CJK}}',]


l1marker = 'o-'
l2marker = '+-'
l3marker = '1-'
l4marker = '2-'
l5marker = '3-'



#4a
xRes1 = []
xRes2 = []
xRes3 = []
xRes4 = []
yRes1 = []
yRes2 = []
yRes3 = []
yRes4 = []
i = 0
with open("FourParameter\\NooruPlate4a.Curve", 'r') as f:
	lines = f.readlines()
	for iline in lines:
		if iline[0] == '#':
			i+=1
		else:
			data = list(map(float,iline.split()))
			if i == 1:
				xRes1.append(data[0])
				yRes1.append(data[1])
			elif i == 2:
				xRes2.append(data[0])
				yRes2.append(data[1])
			elif i == 3:
				xRes3.append(data[0])
				yRes3.append(data[1])
			elif i == 4:
				xRes4.append(data[0])
				yRes4.append(data[1])

plt.figure(figsize=(4,3.75))
l1 = plt.plot(xRes1,yRes1,l1marker,label=r"Meschke",linewidth=0.5,  markersize=1)
l2 = plt.plot(xRes2,yRes2,l2marker,label=r"Experiment",linewidth=0.5,  markersize=2)
l3 = plt.plot(xRes3,yRes3,l3marker,label=r"Xu",linewidth=0.5,  markersize=2)
l4 = plt.plot(xRes4,yRes4,l4marker,label=r"本文",linewidth=0.5,  markersize=2)
plt.xlim(0,0.1)
plt.ylim(0,22)
plt.xlabel(r'位移(mm)')
plt.ylabel(r'力(kN)')

plt.legend()
plt.subplots_adjust(left=0.15)
plt.tight_layout()
plt.savefig("FourParameter\\Figs\\NooruPlate4a.pdf")
#plt.show()
plt.close()

#4b
xRes1 = []
xRes2 = []
xRes3 = []
xRes4 = []
yRes1 = []
yRes2 = []
yRes3 = []
yRes4 = []
i = 0
with open("FourParameter\\NooruPlate4b.Curve", 'r') as f:
	lines = f.readlines()
	for iline in lines:
		if iline[0] == '#':
			i+=1
		else:
			data = list(map(float,iline.split()))
			if i == 1:
				xRes1.append(data[0])
				yRes1.append(data[1])
			elif i == 2:
				xRes2.append(data[0])
				yRes2.append(data[1])
			elif i == 3:
				xRes3.append(data[0])
				yRes3.append(data[1])
			elif i == 4:
				xRes4.append(data[0])
				yRes4.append(data[1])

plt.figure(figsize=(4,3.75))
l1 = plt.plot(xRes1,yRes1,l1marker,label=r"Meschke",linewidth=0.5,  markersize=1)
l2 = plt.plot(xRes2,yRes2,l2marker,label=r"Experiment",linewidth=0.5,  markersize=2)
l3 = plt.plot(xRes3,yRes3,l3marker,label=r"Xu",linewidth=0.5,  markersize=2)
l4 = plt.plot(xRes4,yRes4,l4marker,label=r"本文",linewidth=0.5,  markersize=2)
plt.xlim(0,0.1)
plt.ylim(0,22)
plt.xlabel(r'位移(mm)')
plt.ylabel(r'力(kN)')
plt.legend()
plt.subplots_adjust(left=0.15)
plt.tight_layout()
plt.savefig("FourParameter\\Figs\\NooruPlate4b.pdf")
#plt.show()
plt.close()
