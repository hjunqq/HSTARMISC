import numpy as np
import matplotlib.pyplot as plt

resfile = open("D:\\Example\\ToumiBeam\\Static\\1.flavia.res", 'r')
strain = []
stress = []
damage = []
pickpoint = 1575

point1 = 2370
point2 = 2424

p1dis = []
p2dis = []


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
                elif ipoint ==point1:
                    p1dis.append(list(map(float, subvar[1:])))
                elif ipoint == point2:
                    p2dis.append(list(map(float, subvar[1:])))
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
    elif var[0] == "Yield":
        iline += 1
        for ipoin in range(len(lines) - iline):
            subline = lines[iline + ipoin]
            subvar = subline.split()
            ipoint = subvar[0]
            try:
                ipoint = int(ipoint)
                if ipoint == pickpoint:
                    damage.append(list(map(float, subvar[1:])))
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

for i in range(85):
    zstrain.append(p2dis[i][0]-p1dis[i][0])

for istress in stress:
    xstress.append(istress[0])
    zstress.append(-istress[1])

# maxstress = np.max(xstress)
# maxindex = np.where(xstress == maxstress)[0][0]
#
# maxstrain = xstrain[maxindex]
# maxstress = xstress[maxindex]
#
# xstrain = np.divide(xstrain, maxstrain)
# xstress = np.divide(xstress, maxstress)

# px = np.linspace(0.0, 4.0, 20)
# py = []
#
# for i in px:
#     if i < 1:
#         py.append(1.2 * i - 0.2 * i ** 6)
#     else:
#         py.append(i / (2.723 * (i - 1) ** 1.7 + i))
#
# print("px")
# for ipx in px:
#     print(ipx)
# print("py")
# for ipy in py:
#     print(ipy)


plt.figure()
l1 = plt.plot(zstrain, zstress, 'g', label='Numerical')
# l2 = plt.plot(px, py, 'gx', label='Ref')
# plt.xlim(0, 3.5)
# plt.ylim(0, 1.1)
plt.xlabel(u'$??/??_0$')
plt.ylabel('$f/f_c$')
plt.legend()
plt.show()

# for idam in damage:
#     print((1.0 - idam[0]) ** 2)
#
# poisson = -np.divide(zstrain, xstrain)
# for i in poisson:
#     print(i)
# plt.figure()
# plt.plot(poisson)
# plt.show()
