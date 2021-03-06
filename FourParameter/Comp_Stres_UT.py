import numpy as np
import matplotlib.pyplot as plt

cfile = open("D:\\Example\\OneElemCompress\\UT\\1.flavia.res", 'r')
sfile = open("D:\\Example\\OneElem\\Var\\UT\\1.flavia.res", 'r')
cstrain = []
cstress = []
sstrain = []
sstress = []
pickpoint = 7
maxpoint = 100



##C
lines = cfile.readlines()
jline = 0
for iline in range(len(lines)):
    if jline > len(lines) - 1:
        break
    iline = jline
    line = lines[iline]
    var = line.split()
    if var[0] == "strain":
        iline += 1
        for ipoin in range(len(lines) - iline):
            subline = lines[iline + ipoin]
            subvar = subline.split()
            ipoint = subvar[0]
            try:
                ipoint = int(ipoint)
                if ipoint == pickpoint:
                    cstrain.append(list(map(float, subvar[1:])))
            except:
                jline = iline + ipoin
                break
        jline = iline + ipoin
    elif var[0] == "STRESS":
        iline += 1
        iline += 6
        for ipoin in range(len(lines) - iline):
            subline = lines[iline + ipoin]
            subvar = subline.split()
            ipoint = subvar[0]
            try:
                ipoint = int(ipoint)
                if ipoint == pickpoint:
                    cstress.append(list(map(float, subvar[1:])))
            except:
                jline = iline + ipoin
                break
        jline = iline + ipoin
    else:
        jline = iline + 1

cxstrain = []
czstrain = []
cxstress = []
czstress = []

for istrain in cstrain:
    cxstrain.append(istrain[0])
    czstrain.append(istrain[2])

for istress in cstress:
    cxstress.append(istress[0])
    czstress.append(istress[2])

maxstress = np.max(cxstress)
maxindex = np.where(cxstress == maxstress)[0][0]

maxstrain = cxstrain[maxindex]
maxstress = cxstress[maxindex]

cxstrain = np.divide(cxstrain, maxstrain)
cxstress = np.divide(cxstress, maxstress)

##S
lines = sfile.readlines()
jline = 0
for iline in range(len(lines)):
    if jline > len(lines) - 1:
        break
    iline = jline
    line = lines[iline]
    var = line.split()
    if var[0] == "strain":
        iline += 1
        for ipoin in range(len(lines) - iline):
            subline = lines[iline + ipoin]
            subvar = subline.split()
            ipoint = subvar[0]
            try:
                ipoint = int(ipoint)
                if ipoint == pickpoint:
                    sstrain.append(list(map(float, subvar[1:])))
            except:
                jline = iline + ipoin
                break
        jline = iline + ipoin
    elif var[0] == "STRESS":
        iline += 1
        iline += 6
        for ipoin in range(len(lines) - iline):
            subline = lines[iline + ipoin]
            subvar = subline.split()
            ipoint = subvar[0]
            try:
                ipoint = int(ipoint)
                if ipoint == pickpoint:
                    sstress.append(list(map(float, subvar[1:])))
            except:
                jline = iline + ipoin
                break
        jline = iline + ipoin
    else:
        jline = iline + 1


print("Read finish")

sxstrain = []
szstrain = []
sxstress = []
szstress = []

for istrain in sstrain:
    sxstrain.append(istrain[0])
    szstrain.append(istrain[2])

for istress in sstress:
    sxstress.append(istress[0])
    szstress.append(istress[2])

maxstress = np.max(sxstress)
maxindex = np.where(sxstress == maxstress)[0][0]

maxstrain = sxstrain[maxindex]
maxstress = sxstress[maxindex]

sxstrain = np.divide(sxstrain, maxstrain)
sxstress = np.divide(sxstress, maxstress)


px = np.linspace(0.0, 4.0, 40)
py = []
for i in px:
    if i < 1:
        py.append(1.2 * i - 0.2 * i ** 6)
    else:
        py.append(i / (2.723 * (i - 1) ** 1.7 + i))

plt.figure()
l1 = plt.plot(cxstrain, cxstress, 'g', label='Compress')
l2 = plt.plot(px, py, 'gx', label='Ref')
l3 = plt.plot(sxstrain, sxstress, 'b', label='Stretch')
plt.xlim(0, 3.5)
plt.ylim(0, 1.1)
plt.xlabel(u'$??/??_0$')
plt.ylabel('$f/f_c$')
plt.legend()
plt.show()
