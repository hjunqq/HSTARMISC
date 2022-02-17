import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import font_manager

from gpro.Mesh import Mesh
from gpro.Result import Result

sns.set_theme(style="darkgrid")


matplotlib.use('pgf')
plt.rcParams.update({
    "text.usetex": True,# use default xelatex
    "text.latex.preamble": [
    '\\usepackage{xeCJK}',
    r'\AtBeginDocument{\begin{xeCJK}{UTF8}{gbsn}}',
    r'\AtEndDocument{\end{xeCJK}}',
    ],
    "pgf.rcfonts": False,# turn off default matplotlib fonts properties
    "pgf.preamble": [
         r'\usepackage{fontspec}',
         r'\setmainfont{Times New Roman}',# EN fonts Romans
         r'\usepackage{xeCJK}',# import xeCJK
         r'\setCJKmainfont{SimSun}',# set CJK fonts as SimSun
         r'\xeCJKsetup{CJKecglue=}',# turn off one space between CJK and EN fonts
         ]
})

# plt.rc('font', family='Times New Roman')
#
# matplotlib.rcParams['text.usetex'] = True
# # matplotlib.rcParams['text.latex.unicode'] = True
# matplotlib.rcParams['text.latex.preamble'] = [
#     '\\usepackage{CJK}',
#     r'\AtBeginDocument{\begin{CJK}{UTF8}{gbsn}}',
#     r'\AtEndDocument{\end{CJK}}',
# ]


def get_mesh(s):
    file = r'G:\ZSJ\hstardebug (zz1109)\oblique_bolt\{0}\1bem.flavia.msh'.format(s)
    msh = Mesh(file)
    msh.read()
    return msh


def get_res(s):
    file = r'G:\ZSJ\hstardebug (zz1109)\oblique_bolt\{0}\1bem.flavia.res'.format(s)
    res = Result(file)
    res.read()
    return res


def plot_beam(msh, fig):
    x = []
    y = []
    for node in msh.node:
        x.append(node.coordinates[0])
        y.append(node.coordinates[2])

    # plot line
    if fig == None:
        fig = plt.figure()
    elem_to_plot = [1, 2]
    for elem in msh.element:
        if elem.index in elem_to_plot:
            node_list = elem.nodes
            plot_x = []
            plot_y = []
            for node in node_list:
                idx = node - 1
                plot_x.append(x[idx])
                plot_y.append(y[idx])
            plt.plot(plot_x, plot_y, 'k-', linewidth=1.0)
    return fig


def plot_moment(msh, res, fig):
    if fig == None:
        fig = plt.figure()
        plot_beam(msh, fig)

    x = []
    y = []
    val = []
    for node in msh.node:
        x.append(node.coordinates[0])
        y.append(node.coordinates[2])

    val = res.get_all_value_by_time(5, 51)

    moment_y = []
    for ival in val:
        moment_y.append(ival.value[4])

    elem_to_plot = [1, 2]
    node_to_plot = []
    for elem in msh.element:
        if elem.index in elem_to_plot:
            node_to_plot += elem.nodes
            mesh_x = []
            mesh_y = []
            res_x = []
            res_y = []
            l_dir = np.array([x[elem.nodes[1] - 1] - x[elem.nodes[0] - 1],
                              y[elem.nodes[1] - 1] - y[elem.nodes[0] - 1], 0])
            z_dir = np.array([0, 0, 1])
            l_normal = np.cross(l_dir, z_dir)
            l_normal = l_normal / np.sqrt(np.sum(l_normal ** 2))
            for node in elem.nodes:
                idx = node - 1
                mesh_x.append(x[idx])
                mesh_y.append(y[idx])
                res_x.append(x[idx] + moment_y[idx] * l_normal[0] / 1000)
                res_y.append(y[idx] + moment_y[idx] * l_normal[1] / 1000)
            l1 = plt.plot(mesh_x, mesh_y, 'k-', linewidth=1.0)
            l2 = plt.plot(res_x, res_y, 'r', linewidth=0.5)
            plt.fill_between(mesh_x, mesh_y, res_y)
    return fig


def extract_res(s):
    res = get_res(s)
    val = res.get_all_value_by_time(5, 51)
    moment_y = []
    for ival in val:
        moment_y.append(ival.value[4])
    return moment_y


def gather_res():
    table = []
    s_array = ['four-2blk\\4hstar_-1000kN',
               'four-2blk\\4hstar_-1500kN',
               'four-2blk\\4hstar_-2000kN',
               'four-2blk\\4hstar_-2500kN',
               'four-2blk\\4hstar_+1000kN',
               'four-2blk\\4hstar_+1500kN',
               'four-2blk\\4hstar_+2000kN',
               'four-2blk\\4hstar_+2500kN']

    for s in s_array:
        moment_y = extract_res(s)
        table.append(moment_y)

    table = pd.DataFrame(table)
    return table


def extract_timeseries(s):
    res = get_res(s)
    time, value = res.get_time_series(2, 5)
    moment_y = []

    time = np.array(time)

    if s.__contains__('_-'):
        time = -500 * time
    else:
        time = 500 * time

    for ival in value:
        moment_y.append(ival[4])

    moment_y = np.array(moment_y)
    return {'x': time, 'y': moment_y}


if __name__ == '__main__':
    # table = gather_res()
    # table.to_csv('beam_res.csv')

    b_p1000 = extract_timeseries('four-2blk\\4hstar_+1000kN')
    b_p1500 = extract_timeseries('four-2blk\\4hstar_+1500kN')
    b_p2000 = extract_timeseries('four-2blk\\4hstar_+2000kN')
    b_p2500 = extract_timeseries('four-2blk\\4hstar_+2500kN')
    b_n1000 = extract_timeseries('four-2blk\\4hstar_-1000kN')
    b_n1500 = extract_timeseries('four-2blk\\4hstar_-1500kN')
    b_n2000 = extract_timeseries('four-2blk\\4hstar_-2000kN')
    b_n2500 = extract_timeseries('four-2blk\\4hstar_-2500kN')

    # moment = np.array([i for i in range(101)])
    fontP = font_manager.FontProperties()
    fontP.set_family('SimSun')

    figure = plt.figure()
    ax = plt.axes(xlim=(-400, 400), ylim=(-400, 200))
    ax.set_xlabel(r'荷载弯矩/(kN·m)', fontproperties=fontP)
    ax.set_ylabel(r'螺栓弯矩/(N·m)', fontproperties=fontP)

    # mask the first step
    b_p1000['y'][0] = np.nan
    b_p1500['y'][0] = np.nan
    b_p2000['y'][0] = np.nan
    b_p2500['y'][0] = np.nan

    plt.plot(b_p1500['x'], b_p1500['y'], label='+1000kN', linewidth=0.2)
    plt.plot(b_p2000['x'], b_p2000['y'], label='+1500kN', linewidth=0.2)
    plt.plot(b_p1000['x'], b_p1000['y'], label='+2000kN', linewidth=0.2)
    plt.plot(b_p2500['x'], b_p2500['y'], label='+2500kN', linewidth=0.2)

    # mask the abnormal data
    b_n1000['y'][b_n1000['y'].argmax():] = np.nan
    b_n1500['y'][b_n1500['y'].argmax():] = np.nan
    b_n2000['y'][b_n2000['y'].argmax():] = np.nan
    b_n2500['y'][b_n2500['y'].argmax():] = np.nan
    b_n1000['y'][0] = np.nan
    b_n1500['y'][0] = np.nan
    b_n2000['y'][0] = np.nan
    b_n2500['y'][0] = np.nan
    plt.plot(b_n1000['x'], b_n1000['y'], label='-1000kN', linewidth=0.2)
    plt.plot(b_n1500['x'], b_n1500['y'], label='-1000kN', linewidth=0.2)
    plt.plot(b_n2000['x'], b_n2000['y'], label='-1000kN', linewidth=0.2)
    plt.plot(b_n2500['x'], b_n2500['y'], label='-1000kN', linewidth=0.2)
    #
    plt.legend(ncol=4, bbox_to_anchor=(0.5, 1.4), loc=9, prop=fontP)
    plt.tight_layout()
    plt.savefig('moment_curve.pdf')
    print("finished")
    #
    # table = pd.DataFrame(list(zip(b_p1000['x'],
    #                               b_p1000['y'], b_p1500['y'], b_p2000['y'], b_p2500['y'],
    #                               b_n1000['y'], b_n1500['y'], b_n2000['y'], b_n2500['y'])),
    #                      columns=['time','+1000kN', '+1500kN', '+2000kN', '+2500kN',
    #                               '-1000kN', '-1500kN', '-2000kN', '-2500kN'])
    #
    #
    # # seaborn.lineplot(data=table)
    # table.to_csv('beam_curve.csv')
