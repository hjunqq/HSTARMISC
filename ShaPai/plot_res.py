# coding:utf-8

import numpy as np
import matplotlib.pyplot as plt


def isint(value):
    try:
        int(value)
        return True
    except:
        return False


if __name__ == '__main__':
    resfile = open("D:\\Example\\\FourElem\\BC\\1.flavia.res", 'r')
    disp = []
    tofor = []
    stress = []
    prinstr = []
    strain = []
    damage = []
    estran = []
    time = []
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
        if var[0] == "DISPLACEMENT":
            iline += 1
            for ipoin in range(len(lines) - iline):
                subline = lines[iline + ipoin]
                subvar = subline.split()
                ipoint = subvar[0]
                if isint(ipoint):
                    if int(ipoint) == pickpoint:
                        disp.append(list(map(float, subvar[1:])))
                else:
                    jline = iline + ipoin
                    break
        elif var[0] == "tofor":
            iline += 1
            for ipoin in range(len(lines) - iline):
                subline = lines[iline + ipoin]
                subvar = subline.split()
                ipoint = subvar[0]
                if isint(ipoint):
                    if int(ipoint) == pickpoint:
                        tofor.append(list(map(float, subvar[1:])))
                else:
                    jline = iline + ipoin
                    break
        elif var[0] == "STRESS":
            iline += 1
            iline += 6
            for ipoin in range(len(lines) - iline):
                subline = lines[iline + ipoin]
                subvar = subline.split()
                ipoint = subvar[0]
                if isint(ipoint):
                    if int(ipoint) == pickpoint:
                        stress.append(list(map(float, subvar[1:])))
                else:
                    jline = iline + ipoin
                    break
        elif var[0] == "PRINCIPALSTRESS":
            iline += 1
            iline += 3
            for ipoin in range(len(lines) - iline):
                subline = lines[iline + ipoin]
                subvar = subline.split()
                ipoint = subvar[0]
                if isint(ipoint):
                    if int(ipoint) == pickpoint:
                        prinstr.append(list(map(float, subvar[1:])))
                else:
                    jline = iline + ipoin
                    break
        elif var[0] == "Yield":
            iline += 1
            for ipoin in range(len(lines) - iline):
                subline = lines[iline + ipoin]
                subvar = subline.split()
                ipoint = subvar[0]
                if isint(ipoint):
                    if int(ipoint) == pickpoint:
                        damage.append(list(map(float, subvar[1:])))
                else:
                    jline = iline + ipoin
                    break
        elif var[0] == "EStrain":
            iline += 1
            for ipoin in range(len(lines) - iline):
                jline = iline + ipoin
                subline = lines[jline]
                subvar = subline.split()
                ipoint = subvar[0]
                if isint(ipoint):
                    if int(ipoint) == pickpoint:
                        estran.append(list(map(float, subvar[1:])))
                else:
                    break
        elif var[0] == 'strain':
            iline += 1
            for ipoin in range(len(lines) - iline):
                jline = iline + ipoin
                subline = lines[jline]
                subvar = subline.split()
                ipoint = subvar[0]
                if isint(ipoint):
                    if int(ipoint) == pickpoint:
                        strain.append(list(map(float, subvar[1:])))
                else:
                    break
    print("Read finish")

    xdisp = []
    zdisp = []
    mainepsilon = []
    xstress = []
    xforce = []
    for idisp in strain:
        xdisp.append(idisp[0])
        zdisp.append(idisp[2])
    for iprinstr in prinstr:
        mainepsilon.append(iprinstr[0])
    for istress in stress:
        xstress.append(istress[0])
    for iforce in tofor:
        xforce.append(iforce[0])

    maxstress = np.min(xstress)
    maxindex = np.where(xstress == maxstress)[0][0]
    maxstrain = xdisp[maxindex]
    maxforce = xforce[maxindex]
    print(maxindex, maxstrain, maxstrain, maxforce)
    xdisp = np.multiply(xdisp, -1000)
    zdisp = np.multiply(zdisp, -1000)
    # xdisp = np.divide(xdisp,maxstrain)
    # zdisp = np.divide(zdisp,-zdisp[maxindex])
    # xstress = np.divide(xstress,maxstress)
    xstress = np.divide(xstress, maxstress / 2)
    # xforce = np.divide(xforce,maxforce)

    # x = np.linspace(0.0, 4.0, 20)
    # y = []

    # UT
    # for i in x:
    #     if i<1:
    #         y.append(1.2*i-0.2*i**6)
    #     else:
    #         y.append(i/(2.723*(i-1)**1.7+i))

    # UC
    # alpha_a = 1.745548
    # alpha_d = 1.635
    # for i in x:
    #     if i<1:
    #         y.append(alpha_a*i+(3-2*alpha_a)*i**2+(alpha_a-2)*i**3)
    #     else:
    #         y.append(i/(alpha_d*(i-1)**2+i))

    # BC


    plt.figure()
    ax1 = plt.subplot(111)
    # l1 = ax1.plot(xdisp,xstress,'g',label='Numerical')
    # # l2 = ax1.plot(x,y,'gx',label='Ref')
    # ax1.set_xlim(0,4)
    # ax1.set_ylim(0,1.1)
    # ax1.set_xlabel(u'$ε/ε_0$')
    # ax1.set_ylabel('$f/f_c$')
    # ax1.legend()

    l1 = ax1.plot(xdisp, xstress, 'g', label='Numerical')
    l2 = ax1.plot(zdisp, xstress, 'g')

    BS1_curve = np.loadtxt('Mazars\\kupfer_S1.txt')
    BS3_curve = np.loadtxt('Mazars\\kupfer_S2.txt')
    x = []
    y = []
    for ibs in BS1_curve:
        x.append(ibs[0])
        y.append(ibs[1])

    maxstress = np.min(y)
    maxindex = np.where(y == maxstress)[0][0]
    x = np.multiply(x, -1000)
    y = np.divide(y, -19.1e6)

    l3 = ax1.plot(x, y, 'gx', label='Ref')

    x = []
    y = []
    for ibs in BS3_curve:
        x.append(ibs[0])
        y.append(ibs[1])

    maxstress = np.min(y)
    maxindex = np.where(y == maxstress)[0][0]
    x = np.multiply(x, -1000)
    y = np.divide(y, -19.1e6)
    # y = np.divide(y, maxstress)
    l4 = ax1.plot(x, y, 'gx')

    # ax1.set_xlim(-3.5,3.5)
    # ax1.set_ylim(0,1.1)
    ax1.set_xlabel(u'$ε$')
    ax1.set_ylabel('$f/f_c$')
    ax1.legend(loc=3)

    # ax1.plot(xdisp,xforce,'y')
    # ax2 = plt.subplot(312)
    # ax2.plot(estran)
    # ax3 = plt.subplot(313)
    # ax3.plot(damage)
    plt.show()
