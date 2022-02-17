import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
matplotlib.rcParams['text.latex.preamble'] = ['\\usepackage{CJK}',
	   r'\AtBeginDocument{\begin{CJK}{UTF8}{gbsn}}',
	   r'\AtEndDocument{\end{CJK}}',]
import matplotlib.pylab as pylab
params = {
            'axes.labelsize': '16',
            'xtick.labelsize': '16',
            'ytick.labelsize': '16',
            'legend.fontsize': '16',
            # 'figure.figsize': '26, 24'  # set figure size
        }
pylab.rcParams.update(params)


l1marker = 'o-'
l2marker = '+'
l3marker = '1-'

# Compress Secion

f = open("FourParameter\\CompCompress.Curv", 'r')
lines = f.readlines()
xFix = []
yFix = []
xTes = []
yTes = []
xVar = []
yVar = []
i = 0
for iline in lines:
	if iline[0] == '#':
		i+=1
	else:
		data = list(map(float,iline.split()))
		if i == 1:
			xFix.append(data[0])
			yFix.append(data[1])
		elif i == 2:
			xTes.append(data[0])
			yTes.append(data[1])
		elif i == 3:
			xVar.append(data[0])
			yVar.append(data[1])

plt.figure(figsize=(4,3.75))
l1 = plt.plot(xFix,yFix,l1marker,label=u"compression",linewidth=0.5,  markersize=1)
l2 = plt.plot(xTes,yTes,l2marker,label=u"Guo's",linewidth=0.5,  markersize=2)
l3 = plt.plot(xVar,yVar,l3marker,label=u"tension",linewidth=0.5,  markersize=2)
plt.xlim(0,4.5)
plt.ylim(0,1.2)
plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
plt.ylabel(r'$\sigma^*/\sigma_0$')
plt.legend()
plt.tight_layout()
plt.savefig("FourParameter\\Figs\\VarPara_CompressCompair_EN.pdf")
plt.close()
	

# UC Secion

f = open("FourParameter\\CompStretch.Curv", 'r')
lines = f.readlines()
xFix = []
yFix = []
xTes = []
yTes = []
xVar = []
yVar = []
i = 0
for iline in lines:
	if iline[0] == '#':
		i+=1
	else:
		data = list(map(float,iline.split()))
		if i == 1:
			xFix.append(data[0])
			yFix.append(data[1])
		elif i == 2:
			xTes.append(data[0])
			yTes.append(data[1])
		elif i == 3:
			xVar.append(data[0])
			yVar.append(data[1])

plt.figure(figsize=(4,3.75))
l1 = plt.plot(xFix,yFix,l1marker,label=u"compression",linewidth=0.5,  markersize=1)
l2 = plt.plot(xTes,yTes,l2marker,label=u"Guo's",linewidth=0.5,  markersize=2)
l3 = plt.plot(xVar,yVar,l3marker,label=u"tension",linewidth=0.5,  markersize=2)
plt.xlim(0,4.5)
plt.ylim(0,1.2)
plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
plt.ylabel(r'$\sigma^*/\sigma_0$')
plt.legend()
plt.tight_layout()
plt.savefig("FourParameter\\Figs\\VarPara_StretchCompair_EN.pdf")
plt.close()

