import sys

if sys.version_info < (2, 7):
    sys.exit("Upgrade python to at least version 2.7")

try:
    import numpy as np
except:
    sys.exit("Could not find required module numpy\n")

import math

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib import cm
import matplotlib.pyplot as plt


def prin2dev(s1, s2, s3):
    I1 = s1 + s2 + s3
    J2 = 1.0 / 6.0 * ((s1 - s2) ** 2 + (s2 - s3) ** 2 + (s1 - s3) ** 2)
    ksi = I1 / np.sqrt(3.0)
    r = np.sqrt(2.0 * J2)
    costheta = (3 * s1 - I1) / (2 * np.sqrt(3 * J2))
    theta = np.arccos(costheta)
    return ksi, r, theta,


def dev2prin(ksi, r, theta):
    I1 = np.sqrt(3.0) * ksi
    J2 = np.power(r, 2) / 2.0
    s1 = (np.sqrt(6.0) * r * np.cos(theta) + np.sqrt(3.0) * ksi) / 3.0
    delta = -I1 ** 2 + 12 * J2 + 6 * I1 * s1 - 9 * s1 ** 2
    s2 = 1.0 / 6.0 * (3 * I1 - 3 * s1 + np.sqrt(3.0 * delta))
    s3 = 1.0 / 6.0 * (3 * I1 - 3 * s1 - np.sqrt(3.0 * delta))
    return s1, s2, s3,


def func_A(x):
    a = 0.0106828
    b = 0.00303988
    c = -7.99161
    d = 0.976358
    return a + b / (1 + np.exp(-c * (x - d)))


def func_B(x):
    a = 0.147638
    b = 0.0196849
    c = -8.00035
    d = 0.984383
    return a + b / (1 + np.exp(-c * (x - d)))


def func_C(x):
    a = 0.614183
    b = 0.0818906
    c = -8.00013
    d = 0.984351
    return a + b / (1 + np.exp(-c * (x - d)))


def func_D(x):
    a = 0.302349
    b = 0.638141
    c = 7.94842
    d = 1.09069
    return a + b / (1 + np.exp(-c * (x - d)))


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


if __name__ == "__main__":
    ksi = np.arange(-10, 1.0, 0.1)
    theta = np.arange(0, np.pi / 3, np.pi / 20)
    [ksi, theta] = np.meshgrid(ksi, theta)
    r, = solver(1.0, ksi, theta)
    x, y, z = dev2prin(ksi, r, theta)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(x, y, z)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    plt.show()

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()
