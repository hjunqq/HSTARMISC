#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt


def isint(value):
    try:
        int(value)
        return True
    except:
        return False
def readdata(file):
    resfile = open(file,'r')
    disp = []
    tofor = []
    stress = []
    prinstr = []
    damage = []
    time = []
    pickpoint = 3
    maxpoint = 100
    lines = resfile.readlines()
    jline = 0
    for iline in range(len(lines)):
        if jline >= len(lines):
            break
        iline = jline
        line = lines[iline]
        var = line.split()
        if var[0]=="DISPLACEMENT":
            iline +=1
            for ipoin in range(len(lines)-iline):
                subline = lines[iline+ipoin]
                subvar = subline.split()
                ipoint = subvar[0]
                if isint(ipoint): 
                    if int(ipoint)==pickpoint:
                        disp.append(list(map(float,subvar[1:])))
                else:
                    jline =iline+ipoin
                    break
        elif var[0]=="tofor":
            iline +=1
            for ipoin in range(len(lines)-iline):
                subline = lines[iline+ipoin]
                subvar = subline.split()
                ipoint = subvar[0]
                if isint(ipoint):
                    if int(ipoint)==pickpoint:
                        tofor.append(list(map(float,subvar[1:])))
                else:
                    jline =iline+ipoin
                    break
        elif var[0]=="STRESS":
            iline +=1
            iline +=6
            for ipoin in range(len(lines)-iline):
                subline = lines[iline+ipoin]
                subvar = subline.split()
                ipoint = subvar[0]
                if isint(ipoint):
                    if int(ipoint)==pickpoint:
                        stress.append(list(map(float,subvar[1:])))
                else:
                    jline =iline+ipoin
                    break
        elif var[0]=="PRINCIPALSTRESS":
            iline +=1
            iline+=3
            for ipoin in range(len(lines)-iline):
                subline = lines[iline+ipoin]
                subvar = subline.split()
                ipoint = subvar[0]
                if isint(ipoint):
                    if int(ipoint)==pickpoint:
                        prinstr.append(list(map(float,subvar[1:])))
                else:
                    jline =iline+ipoin
                    break
        elif var[0]=="Yield":   
            iline +=1
            for ipoin in range(len(lines)-iline):   
                subline = lines[iline+ipoin]
                subvar = subline.split()
                ipoint = subvar[0]
                if isint(ipoint):
                    if int(ipoint)==pickpoint:
                        damage.append(list(map(float,subvar[1:])))
                else:
                    jline =iline+ipoin
                    break      
        else:
            iline +=1
            jline = iline+ipoin 
    print("Read finish")
    return disp,prinstr

if __name__=='__main__':
    xdisp = []
    mainepsilon =[]
    disp,prinstr = readdata("D:\\HSTAR_Q\\HSTAR_Q\\Example\\OneElem\\Var\\UT\\1.flavia.res")
    for idisp in disp:
        xdisp.append(idisp[0])
    for iprinstr in prinstr:
        mainepsilon.append(iprinstr[0])

    plt.figure()
    ax1 = plt.subplot(211)
    ax1.plot(xdisp)
    ax2 = plt.subplot(212)
    ax2.plot(mainepsilon)
    plt.show()