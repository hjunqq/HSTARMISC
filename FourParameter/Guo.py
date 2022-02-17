import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize


def ut(ft, x):
    if x < 1:
        return 1.2 * x - 0.2 * x ** 6
    else:
        return x / (0.312 * ft * ft * (x - 1) ** 1.7 + x)


def getx(ft, beta):
    def fun(x):
        return x / (0.312 * ft * ft * (x - 1) ** 1.7 + x) - beta

    sol = optimize.root(fun)
    x = sol.x
    return x


def get_curve(ft):
    x = []
    y = []
    for i in range(100):
        ix = getx(ft, i / 100.0 + 1.0)
        # ix = i / 100 + 1.0
        iy = ut(ft, ix)
        x.append(ix)
        y.append(iy)
    return x, y


def plot():
    scale = 1.0
    ft0 = 3.0

    scale = 1.0
    ft = ft0 * scale
    x, y = get_curve(ft)
    y = np.dot(y, scale)
    plt.plot(x, y)

    scale = 0.9
    ft = ft0 * scale
    x, y = get_curve(ft)
    x = np.add(x, getx(ft, scale) - 1.0)
    y = np.dot(y, scale)
    plt.plot(x, y)

    scale = 0.8
    ft = ft0 * scale
    x, y = get_curve(ft)
    x = np.add(x, getx(ft, scale) - 1.0)
    y = np.dot(y, scale)
    plt.plot(x, y)

    scale = 0.7
    ft = ft0 * scale
    x, y = get_curve(ft)
    x = np.add(x, getx(ft, scale) - 1.0)
    y = np.dot(y, scale)
    plt.plot(x, y)

    scale = 0.6
    ft = ft0 * scale
    x, y = get_curve(ft)
    x = np.add(x, getx(ft, scale) - 1.0)
    y = np.dot(y, scale)
    plt.plot(x, y)

    scale = 0.5
    ft = ft0 * scale
    x, y = get_curve(ft)
    x = np.add(x, getx(ft, scale) - 1.0)
    y = np.dot(y, scale)
    plt.plot(x, y)

    plt.show()


if __name__ == "__main__":
    plot()
