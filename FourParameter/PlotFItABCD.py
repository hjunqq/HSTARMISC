import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.unicode'] = True
matplotlib.rcParams['text.latex.preamble'] = [
       '\\usepackage{CJK}',
       r'\AtBeginDocument{\begin{CJK}{UTF8}{gbsn}}',
       r'\AtEndDocument{\end{CJK}}',
]
import matplotlib.pylab as pylab
params = {
            'axes.labelsize': '16',
            'xtick.labelsize': '16',
            'ytick.labelsize': '16',
            'legend.fontsize': '16',
            # 'figure.figsize': '26, 24'  # set figure size
        }
pylab.rcParams.update(params)
f = open("FourParameter\\FITABCD.data", 'r')
lines = f.readlines()
x = []
fA = []
fB = []
fC = []
fD = []
eA = []
eB = []
eC = []
eD = []
i = 0
for iline in lines:
    i +=1
    if i > 1:    #skip comment
        data = list(map(float,iline.split()))
        x.append(data[0])
        fA.append(data[1])
        fB.append(data[2])
        fC.append(data[3])
        fD.append(data[4])
        eA.append(data[5])
        eB.append(data[6])
        eC.append(data[7])
        eD.append(data[8])

plt.figure(figsize=(4,3.75))
l2 = plt.plot(x,eA,'o-',label=u"试验 $A$",linewidth=0.5,  markersize=2)
l1 = plt.plot(x,fA,'k-.',label=u"拟合 $A$",linewidth=0.5)
plt.xlim(0,5)
plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
plt.legend()
plt.tight_layout()
#plt.show()
plt.savefig("FourParameter\\Figs\\VarPara_A.pdf")
plt.close()

plt.figure(figsize=(4,3.75))
l2 = plt.plot(x,eB,'o-',label=u"试验 $B$",linewidth=0.5,  markersize=2)
l1 = plt.plot(x,fB,'k-.',label=u"拟合 $B$",linewidth=0.5)
plt.xlim(0,5)
plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
plt.legend()
plt.tight_layout()
plt.savefig("FourParameter\\Figs\\VarPara_B.pdf")
plt.close()

plt.figure(figsize=(4,3.75))
l2 = plt.plot(x,eC,'o-',label=u"试验 $C$",linewidth=0.5,  markersize=2)

l1 = plt.plot(x,fC,'k-.',label=u"拟合 $C$",linewidth=0.5)
plt.xlim(0,5)
plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
plt.legend()
plt.tight_layout()
plt.savefig("FourParameter\\Figs\\VarPara_C.pdf")
plt.close()

plt.figure(figsize=(4,3.75))
l2 = plt.plot(x,eD,'o-',label=u"试验 $D$",linewidth=0.5,  markersize=2)

l1 = plt.plot(x,fD,'k-.',label=u"拟合 $D$",linewidth=0.5)
plt.xlim(0,5)
plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
plt.legend()
plt.tight_layout()
plt.savefig("FourParameter\\Figs\\VarPara_D.pdf")
plt.close()
exit

plt.figure(linewidth=0.75,figsize=(9,6))
p1 = plt.subplot(221)
l2 = plt.plot(x,eA,'o-',label=r"Testing $A$",linewidth=0.5,  markersize=2)
l1 = plt.plot(x,fA,'k-.',label=r"Fitting $A$",linewidth=0.5)
p1.set_xlim(0,5)
plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
p1.legend()
p2 = plt.subplot(222)
l2 = plt.plot(x,eB,'o-',label=r"Testing $B$",linewidth=0.5,  markersize=2)
l1 = plt.plot(x,fB,'k-.',label=r"Fitting $B$",linewidth=0.5)
p2.set_xlim(0,5)
plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
p2.legend()
p3 = plt.subplot(223)
l2 = plt.plot(x,eC,'o-',label=u"Testing $C$",linewidth=0.5,  markersize=2)

l1 = plt.plot(x,fC,'k-.',label=u"Fitting $C$",linewidth=0.5)
p3.set_xlim(0,5)
plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
p3.legend()
p4 = plt.subplot(224)
l2 = plt.plot(x,eD,'o-',label=u"Testing $D$",linewidth=0.5,  markersize=2)

l1 = plt.plot(x,fD,'k-.',label=u"Fitting $D$",linewidth=0.5)
p4.set_xlim(0,5)
plt.xlabel(r'$\varepsilon^*/\varepsilon_0$')
p4.legend()
plt.savefig("FourParameter\\Figs\\VarPara_ABCD.pdf")
print(i)
