import sys

try:
    import numpy as np
except:
    sys.exit("Could not find required module numpy\n")
try:
    import matplotlib.pyplot as plt
except:
    sys.exit("Could not find required module matplotlib\n")

from matplotlib.transforms import Affine2D

from matplotlib.projections import PolarAxes

from mpl_toolkits.axisartist import angle_helper

from mpl_toolkits.axisartist.grid_finder import MaxNLocator

from mpl_toolkits.axisartist.floating_axes import GridHelperCurveLinear, FloatingSubplot


def fractional_polar_axes(f, thlim=(0, 180), rlim=(0, 1), step=(30, 0.2),

                          thlabel='theta', rlabel='r', ticklabels=True):
    """Return polar axes that adhere to desired theta (in deg) and r limits. steps for theta

    and r are really just hints for the locators. Using negative values for rlim causes

    problems for GridHelperCurveLinear for some reason"""

    th0, th1 = thlim  # deg

    r0, r1 = rlim

    thstep, rstep = step

    # scale degrees to radians:

    tr_scale = Affine2D().scale(np.pi / 180., 1.)

    tr = tr_scale + PolarAxes.PolarTransform()

    theta_grid_locator = angle_helper.LocatorDMS((th1 - th0) // thstep)

    r_grid_locator = MaxNLocator((r1 - r0) // rstep)

    theta_tick_formatter = angle_helper.FormatterDMS()

    grid_helper = GridHelperCurveLinear(tr,

                                        extremes=(th0, th1, r0, r1),

                                        grid_locator1=theta_grid_locator,

                                        grid_locator2=r_grid_locator,

                                        tick_formatter1=theta_tick_formatter,

                                        tick_formatter2=None)

    a = FloatingSubplot(f, 111, grid_helper=grid_helper)

    f.add_subplot(a)

    # adjust x axis (theta):

    a.axis["bottom"].set_visible(False)

    a.axis["top"].set_axis_direction("bottom")  # tick direction

    a.axis["top"].toggle(ticklabels=ticklabels, label=bool(thlabel))

    a.axis["top"].major_ticklabels.set_axis_direction("top")

    a.axis["top"].label.set_axis_direction("top")

    # adjust y axis (r):

    a.axis["left"].set_axis_direction("bottom")  # tick direction

    a.axis["right"].set_axis_direction("top")  # tick direction

    a.axis["left"].toggle(ticklabels=ticklabels, label=bool(rlabel))

    # add labels:

    a.axis["top"].label.set_text(thlabel)

    a.axis["left"].label.set_text(rlabel)

    # create a parasite axes whose transData is theta, r:

    auxa = a.get_aux_axes(tr)

    # make aux_ax to have a clip path as in a?:

    auxa.patch = a.patch

    # this has a side effect that the patch is drawn twice, and possibly over some other

    # artists. So, we decrease the zorder a bit to prevent this:

    a.patch.zorder = -2

    # add sector lines for both dimensions:

    thticks = grid_helper.grid_info['lon_info'][0]

    rticks = grid_helper.grid_info['lat_info'][0]

    for th in thticks[1:-1]:  # all but the first and last

        auxa.plot([th, th], [r0, r1], '--', c='grey', zorder=-1)

    for ri, r in enumerate(rticks):

        # plot first r line as axes border in solid black only if it isn't at r=0

        if ri == 0 and r != 0:

            ls, lw, color = 'solid', 2, 'black'

        else:

            ls, lw, color = 'dashed', 1, 'grey'

        # From http://stackoverflow.com/a/19828753/2020363

        auxa.add_artist(plt.Circle([0, 0], radius=r, ls=ls, lw=lw, color=color, fill=False,

                                   transform=auxa.transData._b, zorder=-1))

    return auxa


def prin2dev(s1, s2, s3):
    I1 = s1 + s2 + s3
    J2 = 1.0 / 6.0 * ((s1 - s2) ** 2 + (s2 - s3) ** 2 + (s1 - s3) ** 2)
    ksi = I1 / np.sqrt(3.0)
    r = np.sqrt(2.0 * J2)
    costheta = (3 * s1 - I1) / (2 * np.sqrt(3 * J2))
    theta = np.arccos(costheta)
    return ksi, r, theta,


def func_A(x):
    a = 0.00272838
    b = -0.00245495
    c = 0.0243294
    d = -0.577651
    e = 0.658845
    f = 0.000399051
    g = -0.00182517
    h = 0.00196932
    i = 7.34557
    return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 2 + g * x + h) / (
        1 + np.exp(-i * (x - e)))


def func_B(x):
    a = 0.018581
    b = -0.0730444
    c = 0.351311
    d = -1.34359
    e = 1.10255
    f = -0.0132454
    g = 0.109353
    h = -0.12372
    i = 10.4333
    return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 2 + g * x + h) / (
        1 + np.exp(-i * (x - e)))


def func_C(x):
    a = 0.100572
    b = -0.0750469
    c = -0.0490797
    d = -4.93846
    e = 1.09745
    f = 0.0371884
    g = -0.375246
    h = 1.67987
    i = 0.361683
    return (a * x ** 3 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 3 + g * x + h) / (
        1 + np.exp(-i * (x - e)))


def func_D(x):
    a = 397.496
    b = 1360.57
    c = -30474.5
    d = 0.379982
    e = 5.17342
    f = 127.107
    g = 1196.75
    h = 3865.45
    i = -0.662301
    return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 2 + g * x + h) / (
        1 + np.exp(-i * (x - e)))


def solver(x, ksi, theta):
    pa = func_A(x)
    pb = func_B(x)
    pc = func_C(x)
    pd = func_D(x)
    fa = pa / 2.
    fb = np.sqrt(2.0) / 2.0 * pb + np.sqrt(6.0) / 3.0 * np.cos(theta) * pc
    fc = (np.sqrt(3.0) / 3 * pc + np.sqrt(3) * pd) * ksi - 1
    r = (-fb + np.sqrt(fb ** 2 - 4 * fa * fc)) / (2 * fa)
    return r,


def dev2prin(ksi, r, theta):
    I1 = np.sqrt(3.0) * ksi
    J2 = np.power(r, 2) / 2.0
    s1 = (np.sqrt(6.0) * r * np.cos(theta) + np.sqrt(3.0) * ksi) / 3.0
    delta = -I1 ** 2 + 12 * J2 + 6 * I1 * s1 - 9 * s1 ** 2
    for i in range(delta.size):
        delta[i]=max(delta[i],0)
    s2 = 1.0 / 6.0 * (3 * I1 - 3 * s1 + np.sqrt(3.0 * delta))
    s3 = 1.0 / 6.0 * (3 * I1 - 3 * s1 - np.sqrt(3.0 * delta))
    return s1, s2, s3,


if __name__ == "__main__":
    # ksi = -1
    # theta = np.arange(0, np.pi / 3, np.pi / 60)
    # r, = solver(1.0, ksi, theta)
    #
    # theta = theta /np.pi*180
    #
    # print("r,theta")
    # for i in range(len(theta)):
    #     print(r[i],theta[i])

    # plot
    # f1 = plt.figure()

    # ax = fractional_polar_axes(f1,thlim=(0, 60), rlim=(0, 10), step=(15, 1))
    # ax.set_theta_zero_location('N')
    # ax.set_theta_direction(-1)
    # ax.plot(theta, r, color='r')

    # ksi = -1.5
    # theta = np.arange(0, np.pi / 3, np.pi / 60)
    # r, = solver(1.0, ksi, theta)
    # theta = theta /np.pi*180
    #
    # print("r,theta")
    # for i in range(len(theta)):
    #     print(r[i],theta[i])

    # ax.grid(True)
    # plt.show()


    theta = 0
    ksi = np.arange(-1,4,0.1)
    r, = solver(1.0,ksi,theta)
    # print("ksi,r,theta")
    # for i in range(len(ksi)):
    #     print("{0},{1},{2}".format(ksi[i],r[i],theta))


    x,y,z = dev2prin(ksi,r,theta)

    print("x,y,z")
    for i in range(len(x)):
        print("{0},{1},{2}".format(x[i],y[i],z[i]))


    theta = np.pi/3
    ksi = np.arange(-1,4,0.1)
    r, = solver(1.0,ksi,theta)
    x,y,z = dev2prin(ksi,r,theta)

    print("x,y,z")
    for i in range(len(x)):
        print("{0},{1},{2}".format(x[i],y[i],z[i]))
