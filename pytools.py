# encoding: utf-8

"""
为大程序填文件提供一些函数，复制文件和删除4或8
"""

import sys
import os
from shutil import copyfile


def copyfiles(sdir, ddir,prob='P2G'):
    """
    复制文件
    """
    # Fempre to GeHoMadrid
    if(prob=='P2G'):
        copyfile(sdir + "\\1.corn", ddir + "\\1.cor")
        copyfile(sdir + "\\1.elen", ddir + "\\1.ele")
        copyfile(sdir + "\\1.flavia.msh", ddir + "\\1.flavia.msh")
        print("文件已经成功复制")
        print("正在删除elen中的一列")
        del4or8(ddir)
    # Fempre to FindContact
    if(prob=='P2F'):
        copyfile(sdir + "\\1.corn", ddir + "\\1.cor")
        copyfile(sdir + "\\1.elen", ddir + "\\1.ele")
        copyfile(sdir + "\\1.flavia.msh", ddir + "\\1.flavia.msh")
    # FindContact to Fempre
    if(prob=='F2P'):
        copyfile(sdir + "\\1.corn", ddir + "\\1.cor")
        copyfile(sdir + "\\1.elen", ddir + "\\1.ele")
        copyfile(sdir + "\\1.flavia.msh", ddir + "\\1.flavia.msh")
        add4or8(ddir)
    # FindContact to GeHoMadrid
    if(prob=='F2G'):
        copyfile(sdir + "\\1.corn", ddir + "\\1.cor")
        copyfile(sdir + "\\1.elen", ddir + "\\1.ele")
        copyfile(sdir + "\\1.flavia.msh", ddir + "\\1.flavia.msh")
    # GeHoMadrid to Fempre
    if(prob=='G2P'):
        copyfile(sdir + "\\1.cor", ddir + "\\1.cor")
        copyfile(sdir + "\\1.ele", ddir + "\\1.ele")
        copyfile(sdir + "\\1.flavia.msh", ddir + "\\1.flavia.msh")
        add4or8(ddir)
    if(prob=='F2F'):
        copyfile(sdir + "\\1.corn", ddir + "\\1.cor")
        copyfile(sdir + "\\1.elen", ddir + "\\1.ele")
        add4or8(ddir)


def add4or8(ddir):
    """ 
    添加4或8
    """
    fin = open(ddir + "\\1.ele", 'r')
    try:
        fout = open(ddir + "\\1.elebak", 'w')
    except:
        os.remove(ddir + "\\1.elebak")
        fout = open(ddir + "\\1.elebak", 'w')

    data = fin.readlines()
    for iline in data:
        var = iline.split()
        tstr = var[0]
        i4or8 = len(var)-2
        tstr = tstr + '   '+str(i4or8)+'   ' + '    '.join(var[1:])
        tstr = tstr + '\n'
        fout.write(tstr)
        tstr = ""
    fin.close()
    fout.close()
    os.remove(ddir + "\\1.ele")
    os.rename(ddir + "\\1.elebak", ddir + "\\1.ele")

def del4or8(ddir):
    """ 
    删除4或8
    """
    fin = open(ddir + "\\1.ele", 'r')
    fout = open(ddir + "\\1.elebak", 'w')

    data = fin.readlines()
    for iline in data:
        var = iline.split()
        tstr = var[0]
        tstr = tstr + '   ' + '    '.join(var[2:])
        tstr = tstr + '\n'
        fout.write(tstr)
        tstr = ""
    fin.close()
    fout.close()
    os.remove(ddir + "\\1.ele")
    os.rename(ddir + "\\1.elebak", ddir + "\\1.ele")



if __name__=='__main__':
    print(sys.argv[0])
    print(sys.argv[1])
    print(sys.argv[2])
    print(len(sys.argv))
    if len(sys.argv) <3:
        print("请指定源目录和目的目录。")
        exit(1)
    src = sys.argv[1]
    dst = sys.argv[2]
    if(len(sys.argv))>3:
        prob = sys.argv[3]
    
    copyfiles(src,dst,prob)