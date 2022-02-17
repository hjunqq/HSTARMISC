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

l1marker = 'ko-'
l2marker = 'k+'
l3marker = 'k1-'

# UT Secion
f = open("FourParameter\\UT.Curve", 'r')
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
l1 = plt.plot(xFix,yFix,l1marker,label=u"固定参数",linewidth=0.5,  markersize=1)
l2 = plt.plot(xTes,yTes,l2marker,label=u"试验",linewidth=0.5,  markersize=3)
l3 = plt.plot(xVar,yVar,l3marker,label=u"变参数",linewidth=0.5,  markersize=3)
plt.xlim(0,4.5)
plt.ylim(0,1.2)
plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
plt.ylabel(r'$\sigma^*/\sigma_0$')
plt.legend()
plt.tight_layout()
plt.savefig("FourParameter\\Figs\\FixVarComp_UT.pdf")
plt.close()
	

# UC Secion
f = open("FourParameter\\UC.Curve", 'r')
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
l1 = plt.plot(xFix,yFix,l1marker,label=u"固定参数",linewidth=0.5,  markersize=1)
l2 = plt.plot(xTes,yTes,l2marker,label=u"试验",linewidth=0.5,  markersize=3)
l3 = plt.plot(xVar,yVar,l3marker,label=u"变参数",linewidth=0.5,  markersize=3)
plt.xlim(0,4.5)
plt.ylim(0,1.2)
plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
plt.ylabel(r'$\sigma^*/\sigma_0$')
plt.legend()
plt.tight_layout()
plt.savefig("FourParameter\\Figs\\FixVarComp_UC.pdf")
plt.close()

# BC Secion
f = open("FourParameter\\BC.Curve", 'r')
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
l1 = plt.plot(xFix,yFix,l1marker,label=u"固定参数",linewidth=0.5,  markersize=1)
l2 = plt.plot(xTes,yTes,l2marker,label=u"试验",linewidth=0.5,  markersize=3)
l3 = plt.plot(xVar,yVar,l3marker,label=u"变参数",linewidth=0.5,  markersize=3)
plt.xlim(0,4.5)
plt.ylim(0,1.2)
plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
plt.ylabel(r'$\sigma^*/\sigma_0$')
plt.legend()
plt.tight_layout()
plt.savefig("FourParameter\\Figs\\FixVarComp_BC.pdf")
plt.close()

# TC Secion
f = open("FourParameter\\TC.Curve", 'r')
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
l1 = plt.plot(xFix,yFix,l1marker,label=u"固定参数",linewidth=0.5,  markersize=1)
l2 = plt.plot(xTes,yTes,l2marker,label=u"试验",linewidth=0.5,  markersize=3)
l3 = plt.plot(xVar,yVar,l3marker,label=u"变参数",linewidth=0.5,  markersize=3)
plt.xlim(0,4.5)
plt.ylim(0,1.2)
plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
plt.ylabel(r'$\sigma^*/\sigma_0$')
plt.legend()
plt.tight_layout()
plt.savefig("FourParameter\\Figs\\FixVarComp_TC.pdf")
plt.close()