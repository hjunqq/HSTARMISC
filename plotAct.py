# encoding:utf-8

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

fig = plt.figure()
ax = plt.axes(xlim=(1,2),ylim=(0,20000))
# ax = plt.axes()
# fig.autofmt_xdate()
# fig.autofmt_ydate()
fig_line, = ax.plot([],[])

def update(t):
    actfile = open("D:\\HSTAR_Q\\HSTAR_Q\\Example\\NooruPlane\\Coarse\\1.act",'r')

    react = []
    x = []
    y = []
    lines = actfile.readlines()
    for line in lines:
        var = list(map(float,line.split()))
        react.append(var)
        x.append(var[0])
        y.append(var[1])
    print("read finish")
    actfile.close()
    fig_line.set_data(x,y)
    return fig_line,



anim = animation.FuncAnimation(fig,update,interval=5*1000)
plt.show()

# plt.plot(x,y)
# plt.show()
