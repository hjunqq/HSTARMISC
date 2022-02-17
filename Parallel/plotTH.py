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

f = open("Parallel\\TH.dat", 'r')
lines = f.readlines()
core1 = []
time1 = []
rate1 = []
core2 = []
time2 = []
rate2 = []
i = 0
for iline in lines:
	if iline[0] == '#':
		i+=1
	else:
		data = list(map(float,iline.split()))
		if i == 1:
			core1.append(data[0])
			time1.append(data[1])
			rate1.append(data[2])
		if i == 2:
			core2.append(data[0])
			time2.append(data[1])
			rate2.append(data[2])


plt.figure(figsize=(4,3.75))
plt.plot(core1,time1,l1marker,linewidth=1.0,  markersize=1)
plt.xlim(0,120)
plt.ylim(0,400)
plt.xlabel(r"进程数")
plt.ylabel(r"总时间（$\mathrm{s}$）")
plt.tight_layout()
# plt.show()
plt.savefig("Parallel\\THTimeFst.pdf")

plt.figure(figsize=(4,3.75))
plt.plot(core1,rate1,l1marker,linewidth=1.0,  markersize=1)
plt.xlim(0,120)
plt.ylim(0,40)
plt.xlabel(r"进程数")
plt.ylabel(r"加速比")
plt.tight_layout()
# plt.show()
plt.savefig("Parallel\\THAccFst.pdf")


plt.figure(figsize=(4,3.75))
plt.plot(core2,time2,l1marker,linewidth=1.0,  markersize=1)
plt.xlim(0,1000)
plt.ylim(0,400)
plt.xlabel(r"进程数")
plt.ylabel(r"总时间（$\mathrm{s}$）")
plt.tight_layout()
# plt.show()
plt.savefig("Parallel\\THTimeSnd.pdf")

plt.figure(figsize=(4,3.75))
plt.plot(core2,rate2,l1marker,linewidth=1.0,  markersize=1)
plt.xlim(0,1000)
plt.ylim(0,90)
plt.xlabel(r"进程数")
plt.ylabel(r"加速比")
plt.tight_layout()
# plt.show()
plt.savefig("Parallel\\THAccSnd.pdf")

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
