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
            'lines.linewidth': '1',
            'legend.fontsize': '16',
            # 'figure.figsize': '26, 24'  # set figure size
        }
pylab.rcParams.update(params)

l1marker = 'o-'
l2marker = '+-'
l3marker = '1-'
l4marker = '2-'
l5marker = '3-'

# 

f = open("Parallel\\PETSc.dat", 'r')
lines = f.readlines()
core = []
time = []
rate = []
eff = [] 
i = 0
for iline in lines:
	if iline[0] == '#':
		i+=1
	else:
		data = list(map(float,iline.split()))
		if i == 1:
			core.append(data[0])
			time.append(data[1])
			rate.append(data[2])
			eff.append(data[3])


plt.figure(figsize=(4,3.75))
plt.plot(core,time,l1marker,linewidth=1.0,  markersize=1)
plt.xlim(0,16)
plt.ylim(0,7000)
plt.xlabel(r"进程数")
plt.ylabel(r"总时间（$\mathrm{s}$）")
plt.tight_layout()
# plt.show()
plt.savefig("Parallel\\PETSc100KTime.pdf")

plt.figure(figsize=(4,3.75))
plt.plot(core,rate,l1marker,linewidth=1.0,  markersize=1)
plt.xlim(0,16)
plt.ylim(0,8)
plt.xlabel(r"进程数")
plt.ylabel(r"加速比")
plt.tight_layout()
# plt.show()
plt.savefig("Parallel\\PETSc100KAcc.pdf")

# plt.figure(figsize=(4,3.75))
# l1 = plt.plot(xTes1,yTes1,l1marker,label=r"试验 1",linewidth=0.5,  markersize=1)
# l2 = plt.plot(xTes2,yTes2,l2marker,label=r"试验 2",linewidth=0.5,  markersize=2)
# l3 = plt.plot(xRes1,yRes1,l3marker,label=r"$\alpha_t=0.3$",linewidth=0.5,  markersize=2)
# l4 = plt.plot(xRes2,yRes2,l4marker,label=r"$\alpha_t=0.4$",linewidth=0.5,  markersize=2)
# l5 = plt.plot(xRes3,yRes3,l5marker,label=r"$\alpha_t=0.5$",linewidth=0.5,  markersize=2)
# plt.xlim(0,0.125)
# plt.ylim(0,1000)
# plt.xlabel(r"位移（$\textrm{mm}$）")
# plt.ylabel(r"力（$\textrm{N}$）")
# plt.legend()
# plt.tight_layout()
# plt.savefig("FourParameter\\Figs\\ToumiCase.pdf")
# plt.close()
