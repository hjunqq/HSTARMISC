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

# 

f = open("FourParameter\\Toumi.curve", 'r')
lines = f.readlines()
xTes1 = []
yTes1 = []
xTes2 = []
yTes2 = []
xRes1 = []
yRes1 = []
xRes2 = []
yRes2 = []
xRes3 = []
yRes3 = []
i = 0
for iline in lines:
	if iline[0] == '#':
		i+=1
	else:
		data = list(map(float,iline.split()))
		if i == 1:
			xTes1.append(data[0])
			yTes1.append(data[1])
		elif i == 2:
			xTes2.append(data[0])
			yTes2.append(data[1])
		elif i == 3:
			xRes1.append(data[0])
			yRes1.append(data[1])
		elif i == 4:
			xRes2.append(data[0])
			yRes2.append(data[1])
		elif i == 5:
			xRes3.append(data[0])
			yRes3.append(data[1])

plt.figure(figsize=(4,3.75))
l1 = plt.plot(xTes1,yTes1,l1marker,label=r"Test 1",linewidth=0.5,  markersize=1)
l2 = plt.plot(xTes2,yTes2,l2marker,label=r"Test 2",linewidth=0.5,  markersize=2)
l3 = plt.plot(xRes1,yRes1,l3marker,label=r"$\alpha_t=0.3$",linewidth=0.5,  markersize=2)
l4 = plt.plot(xRes2,yRes2,l4marker,label=r"$\alpha_t=0.4$",linewidth=0.5,  markersize=2)
l5 = plt.plot(xRes3,yRes3,l5marker,label=r"$\alpha_t=0.5$",linewidth=0.5,  markersize=2)
plt.xlim(0,0.125)
plt.ylim(0,1000)
plt.xlabel(r"Displacement($\textrm{mm}$)")
plt.ylabel(r"Force($\textrm{N}$)")
plt.legend()
plt.tight_layout()
plt.savefig("FourParameter\\Figs\\ToumiCaseEN.pdf")
plt.close()
