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
## Tempure Drop 
### Elastic
f = open("SDOpenPoints.dat", 'r')
lines = f.readlines()
openPair = []
closePair = []
totalPair = 2070

timeCurveX = [0.,9.,10.]
timeCurveY = [1.,1.,10.]

timeTag = []
for istep in range(8):
        timeTag.append(1.0)
for istep in range(9,29):
        timeTag.append((10.0-1.0)/20*(istep-8)+1.0)

i = 0
for iline in lines:
    i +=1
    if i > 1:    #skip comment
        data = list(map(int,iline.split()))
        openPair.append(data[0])
        closePair.append(data[1])

openPair=np.divide(openPair,totalPair)
plt.figure(figsize=(4,3.75))
# l1 = plt.plot(timeTag,openPair,'o-',label=r"Open points(\%)",linewidth=0.5,  markersize=2)
l1 = plt.plot(timeTag,openPair,'s-',linewidth=0.5,  markersize=2,label=r"Elastic")
# plt.xlim(0,28)
plt.xlim(0,11)
plt.ylim(0,0.12)
plt.xlabel(r'Over load times($\times h_d$)', labelpad = 0.5)
plt.ylabel(r'Percentage of open-point pairs(\%)', labelpad = 0.5)
# plt.legend(r'Open points(\%)')
x1 = 4.0
y1 = np.interp(x1,timeTag,openPair)
plt.plot([x1,x1],[0,y1],'--',linewidth=0.5)
plt.scatter(x1,y1,s=10,color='g')
plt.annotate(r'$k=4.0$',xy=(x1,y1),xytext=(x1+0.5,y1-0.005))
# Damage
f = open("DDOpenPoints.dat", 'r')
lines = f.readlines()
openPair = []
closePair = []
totalPair = 2070

timeCurveX = [0.,9.,10.]
timeCurveY = [1.,1.,10.]

timeTag = []
for istep in range(8):
        timeTag.append(1.0)
for istep in range(9,29):
        timeTag.append((10.0-1.0)/20*(istep-8)+1.0)

i = 0
for iline in lines:
    i +=1
    if i > 1:    #skip comment
        data = list(map(int,iline.split()))
        openPair.append(data[0])
        closePair.append(data[1])

nStep = len(openPair)

openPair=np.divide(openPair,totalPair)
l2 = plt.plot(timeTag[0:nStep],openPair[0:nStep],'*-',linewidth=0.5,  markersize=3,label=r"Damage")

x1 = 4.12
y1 = np.interp(x1,timeTag[0:nStep],openPair[0:nStep])
plt.plot([x1,x1],[0,y1],'--',linewidth=0.5)
plt.scatter(x1,y1,s=10,color='g')
plt.annotate(r'$k=4.12$',xy=(x1,y1),xytext=(x1+0.5,y1-0.005))
plt.legend(loc='upper right')
# plt.show()
plt.savefig("DDSD_EN.pdf")
plt.close()

## Tempure Rise 
### Elastic
f = open("SROpenPoints.dat", 'r')
lines = f.readlines()
openPair = []
closePair = []
totalPair = 2070

timeCurveX = [0.,9.,10.]
timeCurveY = [1.,1.,10.]

timeTag = []
for istep in range(8):
        timeTag.append(1.0)
for istep in range(9,29):
        timeTag.append((10.0-1.0)/20*(istep-8)+1.0)

i = 0
for iline in lines:
    i +=1
    if i > 1:    #skip comment
        data = list(map(int,iline.split()))
        openPair.append(data[0])
        closePair.append(data[1])

openPair=np.divide(openPair,totalPair)
plt.figure(figsize=(4,3.75))
# l1 = plt.plot(timeTag,openPair,'o-',label=r"Open points(\%)",linewidth=0.5,  markersize=2)
l1 = plt.plot(timeTag,openPair,'s-',linewidth=0.5,  markersize=2,label=r"Elastic")
plt.xlim(0,11)
# plt.ylim(0,0.12)
plt.xlabel(r'Over load times($\times h_d$)', labelpad = 0.5)
plt.ylabel(r'Percentage of open-point pairs(\%)', labelpad = 0.5)
# plt.legend(r'Open points(\%)')
x1 = 4.00
y1 = np.interp(x1,timeTag,openPair)
plt.plot([x1,x1],[0,y1],'--',linewidth=0.5)
plt.scatter(x1,y1,s=10,color='g')
plt.annotate(r'$k=4.00$',xy=(x1,y1),xytext=(x1+0.5,y1-0.005))
# Damage
f = open("DROpenPoints.dat", 'r')
lines = f.readlines()
openPair = []
closePair = []
totalPair = 2070

timeCurveX = [0.,9.,10.]
timeCurveY = [1.,1.,10.]

timeTag = []
for istep in range(8):
        timeTag.append(1.0)
for istep in range(9,29):
        timeTag.append((10.0-1.0)/20*(istep-8)+1.0)

i = 0
for iline in lines:
    i +=1
    if i > 1:    #skip comment
        data = list(map(int,iline.split()))
        openPair.append(data[0])
        closePair.append(data[1])

nStep = len(openPair)

openPair=np.divide(openPair,totalPair)
# l1 = plt.plot(timeTag,openPair,'o-',label=r"Open points(\%)",linewidth=0.5,  markersize=2)
l2 = plt.plot(timeTag[0:nStep],openPair[0:nStep],'*-',linewidth=0.5,  markersize=3,label=r"Damage")
plt.xlim(0,11)
plt.ylim(0,0.12)
plt.xlabel(r'Over load times($\times h_d$)', labelpad = 0.5)
plt.ylabel(r'Percentage of open-point pairs(\%)', labelpad = 0.5)
# plt.legend(r'Open points(\%)')
x1 = 5.08
y1 = np.interp(x1,timeTag[0:nStep],openPair[0:nStep])
plt.plot([x1,x1],[0,y1],'--',linewidth=0.5)
plt.scatter(x1,y1,s=10,color='g')
plt.annotate(r'$k=5.08$',xy=(x1,y1),xytext=(x1+0.5,y1-0.005))
plt.legend(loc='upper right')
# plt.show()
plt.savefig("DRSR_EN.pdf")
plt.close()