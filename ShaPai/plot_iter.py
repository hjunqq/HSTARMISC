#!/usr/bin/python
import re

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib

import seaborn as sns
from matplotlib.lines import Line2D
import matplotlib.font_manager as fm

plt.rc('font', family='Times New Roman')

matplotlib.rcParams['text.usetex'] = True
# matplotlib.rcParams['text.latex.unicode'] = True
matplotlib.rcParams['text.latex.preamble'] = [
    '\\usepackage{CJK}',
    r'\AtBeginDocument{\begin{CJK}{UTF8}{gbsn}}',
    r'\AtEndDocument{\end{CJK}}',
]

re_iblks = re.compile(r"(?<=\biblks=|iincs=|istep=|iiter=)\s+\d\s?")


class conv_type:
    def __init__(self):
        self.iter_state = []
        self.iter_bt = []
        self.dnorm = []
        self.tnorm = []
        self.ratio = []
        self.step = []

    def append(self, str, istep):
        values = str.split()
        iter_state = int(values[1])
        iter_bt = int(values[3])
        dnorm = float(values[5])
        tnorm = float(values[7])
        tnorm = min(tnorm, 100)
        self.iter_state.append(iter_state)
        self.iter_bt.append(iter_bt)
        self.dnorm.append(dnorm)
        self.tnorm.append(tnorm)
        self.ratio.append(dnorm / tnorm)
        self.step = istep

    def get_iter_bt(self):
        return self.iter_bt[-1]

    def get_ratio(self):
        return self.ratio[-1]

    def get_len(self):
        return len(self.iter_bt)

    def clear(self):
        self.__init__()

    def to_dataframe(self):
        return pd.DataFrame([self.iter_bt, self.ratio])


def circled(x):
    return chr(0x245F + x)


def plot_conv():
    conv_set = []
    cur_conv = conv_type()

    iconv = conv_type()

    static = []

    istep = 1

    index = 0
    iter_bt = 0
    total_bt = 0
    sum_bt = 0
    with open(file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            tag = line.split()[0]
            if tag == 'iter_state':
                iconv.append(line, istep)
                if iconv.get_iter_bt() == 0:
                    iter_bt += 1
                    sum_bt += 1
                    if cur_conv.get_len() > 0:
                        conv_set.append(cur_conv)
                        print("step:{}, niter:{}".format(istep + 1, cur_conv.get_len()))
                    cur_conv = conv_type()
                cur_conv.append(line, istep)
                iconv.clear()
                total_bt += 1
            else:
                values = line.split()
                iblks = int(values[1])
                istep = int(values[5])
                iiter = int(values[7])
                ratio = float(values[13])

                iter_ratio = cur_conv.get_ratio()

                index += 1
                a = {'index': index, 'blks': iblks, 'step': istep, 'iter': iiter, 'ratio': ratio, 'iter_bt': iter_bt,
                     'total_bt': total_bt,
                     'iter_ratio': iter_ratio}

                iter_bt = 0
                total_bt = 0
                static.append(a)

    conv_set.append(cur_conv)

    static = pd.DataFrame.from_dict(static)
    static['cumsum_iter_bt'] = static['total_bt'].cumsum()

    total_width, n = 1, 2
    width = total_width / n

    fig = plt.figure(figsize=(8, 3))

    ax1 = fig.add_subplot(111)

    color_group = ['tab:blue'
        , 'tab:orange'
        , 'tab:green'
        , 'tab:red'
        , 'tab:purple'
        , 'tab:brown'
        , 'tab:pink'
        , 'tab:gray'
        , 'tab:olive'
        , 'tab:cyan']

    # markers = ['.','x','+','5']
    markers = [m for m, func in Line2D.markers.items()
               if func != 'nothing' and m not in Line2D.filled_markers]

    markersize = 4
    prev_step = 0
    total_iter = 0
    max_iiter = 0
    for istep in range(plot_step):
        for iiter in range(global_niter):

            niter = int(
                static.iter_bt.where((static.step == istep + 1) & (static.iter == iiter + 1))[
                    istep * global_niter + iiter])

            print("istep: {}, iiter: {}, niter_bt:{},".format(istep, iiter, niter))

            iiter_bt = 0
            for iconv in conv_set:

                if (iiter_bt < niter + prev_step) & (iiter_bt >= prev_step):
                    print(iiter_bt)
                    ax1.plot(np.array(iconv.iter_bt) + total_iter, np.array(iconv.ratio), linewidth=0.5,
                             marker=markers[2 + iiter_bt - prev_step], markersize=markersize,
                             color=color_group[iiter_bt - prev_step], alpha=0.5)

                    total_iter += iconv.get_len()
                    # 绘制竖线
                    ax1.axvline(total_iter, linestyle="-.", linewidth=0.2, alpha=0.5)

                if iiter_bt >= niter + prev_step:
                    break

                iiter_bt += 1
            max_iiter = max(max_iiter, niter)
            prev_step = iiter_bt
            # ax1.axvline(total_iter, linestyle="-.", linewidth=0.5)

    upper_iter = int(static['cumsum_iter_bt'][plot_step * 2 - 1])
    ax1.set_xlim(0, upper_iter)
    # ax1.set_xlim(0,1011)
    ax1.set_ylim(10e-21, 10e2)
    ax1.set_yscale('log')
    ax1.set_xlabel('total contact iteration step')
    ax1.set_ylabel('residual')

    a = static['iter_bt'].where((static['iter'] == 1) & (static['step'] <= plot_step))
    b = static['iter_bt'].where((static['iter'] == 2) & (static['step'] <= plot_step))
    x = static['cumsum_iter_bt']
    w = static['total_bt']
    l1 = ax1.plot(x, static['iter_ratio'].where(static['step'] <= plot_step), label=r'contact residual', color='green',
                  linewidth=0.5, linestyle='--', alpha=0.5)
    # marker=markers[0], markersize=markersize)
    l2 = ax1.plot(x, static['ratio'].where(static['step'] <= plot_step), label=r'incremental residual', color='purple',
                  linewidth=0.5, linestyle='-.')
    # marker=markers[1], markersize=markersize)

    l3 = ax1.plot([0], marker=markers[2], markersize=markersize, label=r'1st contact iteration', linewidth=0.5, alpha=0.5)
    l4 = ax1.plot([0], marker=markers[3], markersize=markersize, label=r'2nd contact iteration', linewidth=0.5, alpha=0.5)
    l5 = ax1.plot([0], marker=markers[4], markersize=markersize, label=r'3rd contact iteration', linewidth=0.5, alpha=0.5)

    ax3 = ax1.twinx()
    bar1 = ax3.bar(x - w / 2, a, width=w, label='predictor step', color='blue', alpha=0.3)
    bar2 = ax3.bar(x - w / 2, b, width=w, label='corrector step', color='orange', alpha=0.3)

    ax3.set_ylabel('nonlinear iteration step')

    font = dict(size=10, color='r')

    for i, v in enumerate(x):
        if (i % 2 == 0) & (1 + i / 2 <= plot_step):
            idx = 1 + int(i / 2)
            if idx % tag_step == 0:
                ax3.text(v - 1, 0.5, r'$' + str(idx) + '$', **font)
    # v - 2.5 值随着x轴变化

    ax3.set_ylim(0, 10)

    marker_style = dict(linestyle=' ', color='r', markersize=8, linewidth=0.1,
                        markerfacecolor="r", markeredgecolor="none")

    tx1 = ax1.plot([0], ' ', marker=r'$1$', label=r'incremental analysis step', **marker_style)

    # lns = [bar1] + [bar2] + l1 + l2 + l3 + l4 + l5 + tx1
    lns = [bar1]
    if max_iiter == 1:
        lns = [bar1] + [bar2] + l1 + l2 + l3 + tx1
    elif max_iiter == 2:
        lns = [bar1] + [bar2] + l1 + l2 + l3 + l4 + tx1
    elif max_iiter == 3:
        lns = [bar1] + [bar2] + l1 + l2 + l3 + l4 + l5 + tx1

    labs = [l.get_label() for l in lns]

    l = ax3.legend(lns, labs, ncol=4, bbox_to_anchor=(0.5, 1.4), loc=9)
    # plt.setp(l.texts, family='Times New Roman')
    plt.tight_layout()
    plt.savefig(output)  # T -total L-local D-damage


if __name__ == "__main__":
    # file_path = "G:\\HSTAR_Q\\HSTAR_Q\\Example\\Beam\\4SInGroupL\\1.conv"
    # output = "Beam_Local.pdf"
    # file_path = "G:\\HSTAR_Q\\HSTAR_Q\\Example\\Beam\\4SInGroupT\\1.conv"
    # output = "Beam_Total.pdf"
    # file_path = "G:\\HSTAR_Q\\HSTAR_Q\\Example\\Beam\\8SInGroupL\\1.conv"
    # output = "Beam_Refine_Local.pdf"
    # file_path = "G:\\HSTAR_Q\\HSTAR_Q\\Example\\Beam\\8SInGroupT\\1.conv"
    # output = "Beam_Refine_Total.pdf"
    # file_path = r"G:\HSTAR_Q\HSTAR_Q\Example\Arc\14SInGroup\1.dt.conv"
    # output = "Arc_Refine_Total.pdf"

    plot_step = 100
    tag_step = 10
    global_niter = 2
    file = "G:\\HSTAR_Q\\HSTAR_Q\\Example\\Beam\\4SInGroupL\\1.conv"
    output = "Beam_Local.pdf"
    plot_conv()
    file = "G:\\HSTAR_Q\\HSTAR_Q\\Example\\Beam\\4SInGroupT\\1.conv"
    output = "Beam_Total.pdf"
    plot_conv()
    file = "G:\\HSTAR_Q\\HSTAR_Q\\Example\\Beam\\8SInGroupL\\1.conv"
    output = "Beam_Refine_Local.pdf"
    plot_conv()
    file = "G:\\HSTAR_Q\\HSTAR_Q\\Example\\Beam\\8SInGroupT\\1.conv"
    output = "Beam_Refine_Total.pdf"
    plot_conv()

    # plot_step = 50
    # file_path = "G:\\HSTAR_Q\\HSTAR_Q\\Example\\Arc\\9SInGroupL\\1.conv"
    # output = "Arc_Local.pdf"
    # plot_conv()
    # file_path = "G:\\HSTAR_Q\\HSTAR_Q\\Example\\Arc\\9SInGroupT\\1.conv"
    # output = "Arc_Total.pdf"
    # plot_conv()
    # file_path = "G:\\HSTAR_Q\\HSTAR_Q\\Example\\Arc\\14SInGroupL\\1.conv"
    # output = "Arc_Refine_Local.pdf"
    # plot_conv()
    # file_path = "G:\\HSTAR_Q\\HSTAR_Q\\Example\\Arc\\14SInGroupT\\1.conv"
    # output = "Arc_Refine_Total.pdf"

    plot_step = 50
    file = "G:\\HSTAR_Q\\HSTAR_Q\\Example\\Arc\\9SInGroupL\\1.dl.conv"
    output = "Arc_Local.pdf"
    plot_conv()
    file = "G:\\HSTAR_Q\\HSTAR_Q\\Example\\Arc\\9SInGroupL\\1.dt.conv"
    output = "Arc_Total.pdf"
    plot_conv()

    file = r"G:\HSTAR_Q\HSTAR_Q\Example\Arc\14SInGroupL\1.dl.conv"
    output = "Arc_Refine_Local.pdf"
    plot_conv()
    file = r"G:\HSTAR_Q\HSTAR_Q\Example\Arc\14SInGroupL\1.dt.conv"
    output = "Arc_Refine_Total.pdf"

    plot_conv()
