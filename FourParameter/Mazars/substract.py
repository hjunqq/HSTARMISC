import numpy as np
import sys


def isint(value):
    try:
        int(value)
        return True
    except:
        return False


if __name__ == '__main__':
    # sys.argv="D:\Example\Koyna_Simple\static\1.flavia.res DISPLACEMENT 11352 1.000000 2.000000"
    # if len(sys.argv)!=0:
    #     for idx in range(1, len(sys.argv)):
    #         try:
    #             dum[idx - 1] = (sys.argv[idx])
    #         except:
    #             sys.exit("Argument '{0}' is not a valid float". \
    #                      format(sys.argv[idx]))
    # else:
    # resfile = input("input file_path name\n>")
    # valname = input("input val name\n>")
    # npoint = int(input("input npoint\n>"))
    # startblock = input("input start block number\n>")
    # endblock=input("input start end number\n>")


    resfile = "D:\\Example\\Koyna_Simple\\static\\1.flavia.res"
    valname = "DISPLACEMENT"
    npoint = 11352
    startblock = "1.000000"
    endblock = "2.000000"

    disp0 = np.zeros((npoint, 3))
    disp1 = np.zeros((npoint, 3))
    fres = open(resfile, 'r')

    lines = fres.readlines()
    jline = 0
    for iline in range(len(lines)):
        if jline > len(lines) - 1:
            break
        iline = jline
        line = lines[iline]
        var = line.split()
        if var[0] == valname and var[2] == startblock:
            Head = line
            iline += 1
            for ipoin in range(len(lines) - iline):
                subline = lines[iline + ipoin]
                subvar = subline.split()
                ipoint = subvar[0]
                if isint(ipoint):
                    disp0[int(ipoint) - 1] = list(map(float, subvar[1:]))
                else:
                    jline = iline + ipoin
                    break
        if var[0] == valname and var[2] == endblock:
            iline += 1
            for ipoin in range(len(lines) - iline):
                subline = lines[iline + ipoin]
                subvar = subline.split()
                ipoint = subvar[0]
                if isint(ipoint):
                    disp1[int(ipoint) - 1] = list(map(float, subvar[1:]))
                else:
                    jline = iline + ipoin
                    break
    disp2 = disp0 - disp1
    with open('1.flavia.res', 'w') as f:
        f.write(str(Head))
        for ipoin in range(npoint):
            f.write(str(ipoin + 1) + " " + str(disp1[0][0]) + " " + str(disp1[0][1]) + " " + str(disp1[0][2]) + "\n")

    print("finish")
