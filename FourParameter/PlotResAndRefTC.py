import numpy as np
import matplotlib.pyplot as plt


def Act(file):
    react = []
    lines = file.readlines()
    jline = 0
    iline = lines[jline]
    var = iline.split()
    noutfix = len(var) - 1
    for iline in range(len(lines)):
        if jline > len(lines) - 1:
            break
        iline = jline
        line = lines[iline]
        var = line.split()
        react.append(list(map(float, var[1:])))
        # act format
        jline += 3
        jline += noutfix * 3
        jline += 1
        #
        jline += 1

    print("Read Finish")
    return react


resfile = open("D:\\Example\\\OneElem\\TC\\1.flavia.res", 'r')
actfile = open("D:\\Example\\\OneElem\\TC\\1.act")
act = Act(actfile)

strain = []
stress = []
pickpoint = 13
maxpoint = 100
lines = resfile.readlines()
jline = 0
for iline in range(len(lines)):
    if jline > len(lines) - 1:
        break
    iline = jline
    line = lines[iline]
    var = line.split()
    if var[0] == "DISPLACEMENT":
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

# for istress in stress:
#     xstress.append(istress[0])
#     zstress.append(istress[2])

for iact in act:
    zstress.append(sum(iact))

maxstress = np.min(zstress)
maxindex = np.where(zstress == maxstress)[0][0]

maxstrain = zstrain[maxindex]
maxstress = zstress[maxindex]

zstrain = np.divide(zstrain, maxstrain)
zstress = np.divide(zstress, maxstress)

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
l1 = plt.plot(zstrain, zstress, 'g', label='Numerical')
l2 = plt.plot(px, py, 'gx', label='Ref')
plt.xlim(0, 3.5)
plt.ylim(0, 1.1)
plt.xlabel(u'$ε/ε_0$')
plt.ylabel('$f/f_c$')
plt.legend()
plt.show()
