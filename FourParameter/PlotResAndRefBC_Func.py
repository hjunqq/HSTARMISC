import numpy as np
import matplotlib.pyplot as plt

resfile = open("D:\\Example\\\OneElem\\BC\\1.flavia.res", 'r')
strain = []
stress = []
pickpoint = 7
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

xstrain = np.divide(xstrain, maxstrain)
xstress = np.divide(xstress, maxstress)

px = np.linspace(0.0, 4.0, 40)
py = []
alpha_a = 1.2
alpha_d = 1.635
for i in px:
    if i < 1:
        py.append(alpha_a * i + (3 - 2 * alpha_a) * i ** 2 + (alpha_a - 2) * i ** 3)
    else:
        py.append(i / (alpha_d * (i - 1) ** 2 + i))

plt.figure()
l1 = plt.plot(xstrain, xstress, 'g', label='Numerical')
l2 = plt.plot(px, py, 'gx', label='Ref')
plt.xlim(0, 3.5)
plt.ylim(0, 1.1)
plt.xlabel(u'$ε/ε_0$')
plt.ylabel('$f/f_c$')
plt.legend()
plt.show()
