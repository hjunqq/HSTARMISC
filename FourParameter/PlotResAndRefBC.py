import numpy as np
import matplotlib.pyplot as plt

resfile = open("D:\\Example\\\OneElem\\BC\\1.flavia.res", 'r')
strain = []
stress = []
pickpoint = 8
maxpoint = 100
lines = resfile.readlines()
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
                    strain.append(list(map(float, subvar[1:])))
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
                    stress.append(list(map(float, subvar[1:])))
            except:
                jline = iline + ipoin
                break
        jline = iline + ipoin
    else:
        jline = iline + 1
print("Read finish")

xstrain = []
zstrain = []
xstress = []
zstress = []

for istrain in strain:
    xstrain.append(istrain[0])
    zstrain.append(istrain[2])

for istress in stress:
    xstress.append(istress[0])
    zstress.append(istress[2])

maxstress = np.min(xstress)
maxindex = np.where(xstress == maxstress)[0][0]

maxstrain = xstrain[maxindex]
maxstress = xstress[maxindex]

xstrain = np.multiply(xstrain, -1000)
zstrain = np.multiply(zstrain, -1000)
xstress = np.divide(xstress, maxstress)

BS1_curve = np.loadtxt('Mazars\\kupfer_S1.txt')
BS3_curve = np.loadtxt('Mazars\\kupfer_S2.txt')
px1 = []
py1 = []
px2 = []
py2 = []
for ibs in BS1_curve:
    px1.append(ibs[0])
    py1.append(ibs[1])
for ibs in BS3_curve:
    px2.append(ibs[0])
    py2.append(ibs[1])

maxstress = np.min(py1)
maxindex = np.where(py1 == maxstress)[0][0]
px1 = np.multiply(px1, -1000)
px2 = np.multiply(px2, -1000)
py1 = np.divide(py1, maxstress)
py2 = np.divide(py2, maxstress)

plt.figure()
l1 = plt.plot(xstrain, xstress, 'g', label='Numerical')
l2 = plt.plot(zstrain, xstress, 'g')
l3 = plt.plot(px1, py1, 'gx', label='Ref')
l4 = plt.plot(px2, py2, 'gx')

# plt.xlim(0, 3.5)
# plt.ylim(0, 1.1)
plt.xlabel(u'$ε/ε_0$')
plt.ylabel('$f/f_t$')
plt.legend()
plt.show()


# poisson = -np.divide(zstrain, xstrain)
# for i in poisson:
#     print(i)
# plt.figure()
# plt.plot(poisson)
# plt.show()

