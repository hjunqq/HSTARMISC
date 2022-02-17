import math

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set_theme(style="darkgrid")
from matplotlib.lines import Line2D

from gpro.Result import Result, Component

plt.rc('font', family='Times New Roman')

matplotlib.rcParams['text.usetex'] = True
# matplotlib.rcParams['text.latex.unicode'] = True
matplotlib.rcParams['text.latex.preamble'] = [
    '\\usepackage{CJK}',
    r'\AtBeginDocument{\begin{CJK}{UTF8}{gbsn}}',
    r'\AtEndDocument{\end{CJK}}',
]


def get_test(s):
    d1000 = {'x': [], 'y': []}
    x = []
    y = []
    with open("ZhangShengLongTest\\{0}.dat".format(s), "r") as f:
        for line in f:
            vals = line.split()
            x.append(float(vals[0]))
            y.append(float(vals[1]))
    d1000['x'] = x
    d1000['y'] = y

    return d1000


def extract_beam(s):
    file = r'G:\ZSJ\hstardebug (zz1109)\oblique_bolt\{0}\1bem.flavia.res'.format(s)
    res = Result(file)
    res.read()
    time, moment = res.get_time_series(2, 5)
    time = np.array(time)
    momenty=[]
    for ival in moment:
        momenty.append(ival[4])
    momenty = np.array(momenty)
    time = 500 * time

    return {'x': time, 'y': momenty}


def extract_result(s):
    file = r'G:\ZSJ\hstardebug (zz1109)\oblique_bolt\{0}\1.flavia.res'.format(s)
    res = Result(file)
    res.read()
    time, displacement1 = res.get_time_series(5192, 0)
    time, displacement2 = res.get_time_series(2220, 0)
    _, displacement3 = res.get_time_series(2159, 0)
    _, displacement4 = res.get_time_series(5173, 0)
    # z_disp = method_1(displacement1,displacement2,displacement3,displacement4)
    # z_disp = method_2(displacement3, displacement4)

    time = np.array(time)

    # 正弯矩取上面两个点，负弯矩取下面两个点
    if s.__contains__('_-'):
        z_disp = method_2(displacement1, displacement2)
        z_disp = np.array(z_disp)
        time = - 500 * time
    else:
        z_disp = method_2(displacement3, displacement4)
        z_disp = np.array(z_disp)

        time = 500 * time

    # time = -1*time
    # z_disp = -1*z_disp
    return {'x': time, 'y': z_disp}


"""有问题，deprecated"""


def method_1(displacement1, displacement2, displacement3, displacement4):
    z_disp = []
    l = 1.7
    for ival, jval, kval, lval in zip(displacement1, displacement2, displacement3, displacement4):
        disp1 = ival[0]
        disp2 = jval[0]
        disp3 = kval[0]
        disp4 = lval[0]
        dist1 = disp1 - disp2
        dist2 = disp3 - disp4
        theta = 2 * math.asin(abs(dist1) + abs(dist2) / (2 * 0.3)) * 1000
        z_disp.append(theta)
    return z_disp


def method_2(displacement1, displacement2):
    z_disp = []
    l = 1.7
    for ival, jval in zip(displacement1, displacement2):
        disp1 = ival[2]
        disp2 = jval[2]
        theta1 = math.atan(disp1 / l) * 1000.0
        theta2 = math.atan(disp2 / l) * 1000.0
        z_disp.append(theta1 + theta2)
    return z_disp


if __name__ == '__main__':

    # beam_two = extract_beam('two-2blk\\4hstar_-1000kN')
    # beem_four = extract_beam('four-2blk\\4hstar_-1000kN')
    # b1 = plt.plot(beam_two['x'], beam_two['y'], label='-1000kN-N', linewidth=0.2)
    # b2 = plt.plot(beem_four['x'], beem_four['y'], label='+1000kN-N', linewidth=0.2)
    # plt.axes(xlim=(0,300))
    # plt.show()

    num_n1000 = extract_result('two-2blk\\4hstar_-1000kN')
    num_p1000 = extract_result('two-2blk\\4hstar_+1000kN')
    num_n1500 = extract_result('two-2blk\\4hstar_-1500kN')
    num_p1500 = extract_result('two-2blk\\4hstar_+1500kN')
    num_n2000 = extract_result('two-2blk\\4hstar_-2000kN')
    num_p2000 = extract_result('two-2blk\\4hstar_+2000kN')
    num_n2500 = extract_result('two-2blk\\4hstar_-2500kN')
    num_p2500 = extract_result('two-2blk\\4hstar_+2500kN')
    # num_test = extract_result('4hstar_test')

    test_1000 = get_test('1000')
    test_1500 = get_test('1500')
    test_2000 = get_test('2000')
    test_2500 = get_test('2500')

    fig = plt.figure()
    ax = plt.axes(xlim=(-400, 400), ylim=(-15, 20))
    ax.set_xlabel(r'弯矩/(kN·m)')
    ax.set_ylabel(r'转角/($rad^{-3}$)')

    markers = [m for m, func in Line2D.markers.items()
               if func != 'nothing' and m not in Line2D.filled_markers]

    marker = markers[2]

    l1 = plt.plot(num_n1000['x'], num_n1000['y'], label='-1000kN-N', linewidth=0.2)
    l2 = plt.plot(num_p1000['x'], num_p1000['y'], label='+1000kN-N', linewidth=0.2)
    l3 = plt.plot(num_n1500['x'], num_n1500['y'], label='-1500kN-N', linewidth=0.2)
    l4 = plt.plot(num_p1500['x'], num_p1500['y'], label='+1500kN-N', linewidth=0.2)
    l5 = plt.plot(num_n2000['x'], num_n2000['y'], label='-2000kN-N', linewidth=0.2)
    l6 = plt.plot(num_p2000['x'], num_p2000['y'], label='+2000kN-N', linewidth=0.2)
    l7 = plt.plot(num_n2500['x'], num_n2500['y'], label='-2500kN-N', linewidth=0.2)
    l8 = plt.plot(num_p2500['x'], num_p2500['y'], label='+2500kN-N', linewidth=0.2)

    # l9 = plt.plot(num_test['x'], num_test['y'], label='+2500kN-N', linewidth=0.1)

    t1 = plt.plot(test_1000['x'], test_1000['y'], marker=markers[2], linestyle='', label='1000kN-T', linewidth=0.2)
    t2 = plt.plot(test_1500['x'], test_1500['y'], marker=markers[3], linestyle='', label='1500kN-T', linewidth=0.2)
    t3 = plt.plot(test_2000['x'], test_2000['y'], marker=markers[4], linestyle='', label='2000kN-T', linewidth=0.2)
    t4 = plt.plot(test_2500['x'], test_2500['y'], marker=markers[5], linestyle='', label='2500kN-T', linewidth=0.2)
    # sns.lineplot(x=num_n1000['x'], y=num_n1000['y'])
    # sns.lineplot(x=num_p1000['x'], y=num_p1000['y'])
    # sns.lineplot(x=test_1000['x'], y=test_1000['y'])
    # sns.lineplot(x=test_1500['x'], y=test_1500['y'])
    # sns.lineplot(x=test_2000['x'], y=test_2000['y'])
    # sns.lineplot(x=test_2500['x'], y=test_2500['y'])
    plt.legend(ncol=4, bbox_to_anchor=(0.5, 1.4), loc=9)
    plt.tight_layout()
    # plt.savefig("Test_Numerical.pdf")
    plt.show()
    print('test')
