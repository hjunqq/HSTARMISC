# coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
import contextlib
import winsound


@contextlib.contextmanager
def printoptions(*args, **kwargs):
    original = np.get_printoptions()
    np.set_printoptions(*args, **kwargs)
    yield
    np.set_printoptions(**original)


def isint(value):
    try:
        int(value)
        return True
    except:
        return False


def isfloat(value):
    try:
        float(value)
        return True
    except:
        return False


if __name__ == '__main__':
    mu0 = 0.167
    E = 2.69e10
    ft = 2.954e6
    cf = 0.126
    e0 = ft / E


    def poisson(x):
        return (0.2 * (1 + 0.68815 * x - 1.78667 * x ** 2 + 2.1465 * x ** 3)) / (1 - 0.5 * x ** 2 +
                                                                                 0.8573 * x ** 3)
        return 0.2
        return 0.2 + 0.16 / (1 + np.exp(-8 * (x - 1)))
        if x <= 0.8:
            return mu0
        elif x <= 1.0:
            return 0.36 - (0.36 - mu0) * np.sqrt(1 - (5 * x - 4) ** 2)
        else:
            return 0.36


    def DMat(mu):
        D = np.array([[1, -mu, -mu],
                      [-mu, 1, -mu],
                      [-mu, -mu, 1]])
        return D / E


    def UT(x):
        f = np.array([[ft], [0], [0]]) * x
        mu = poisson(x)
        return np.dot(DMat(mu), f)


    def UC(x):
        f = np.array([[0], [0], [-ft / cf]]) * x
        mu = poisson(x)
        return np.dot(DMat(mu), f)


    def BC(x):
        f = np.array([[0], [-1.28 * ft / cf], [-1.28 * ft / cf]]) * x
        mu = poisson(x)
        return np.dot(DMat(mu), f)


    def TC(x):
        f = np.array([[-2.09081 * ft / cf],
                      [-2.09081 * ft / cf],
                      [-7.81838 * ft / cf]]) * x
        mu = poisson(x)
        return np.dot(DMat(mu), f)


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


    def fx(x, s):
        a = func_A(x)
        b = func_B(x)
        c = func_C(x)
        d = func_D(x)
        fa = a * J2(s)
        fb = b * np.sqrt(J2(s))
        fc = c * s[0][0]
        fd = d * I1(s)
        return x ** 3 - (fb + fc + fd) * x ** 2 - fa * x


    def muller(x, s):
        x0 = x
        x1 = x0 + 0.02
        x2 = (x1 - x0) * 0.618 + x0
        for i in range(200):
            fx0 = fx(x0, s)
            fx1 = fx(x1, s)
            fx2 = fx(x2, s)
            fx2x1 = (fx2 - fx1) / (x2 - x1)
            fx1x0 = (fx1 - fx0) / (x1 - x0)
            fx2x0 = (fx2 - fx0) / (x2 - x0)
            fx2x1x0 = (fx2x1 - fx1x0) / (x2 - x0)
            w = fx2x1 + fx2x0 - fx1x0
            xcritia = min(x0, x1, x2) * 0.618

            fxa = fx2x1x0
            fxb = w - 2 * fx2x1x0 * x2
            fxc = fx2 - w * x2 + fx2x1x0 * x2 ** 2
            fdelta = fxb ** 2 - 4 * fxa * fxc

            if fdelta <= 0:
                x3 = max(-fxb / (2 * fxa), xcritia)
            # x3 = max(x2-fx2/w,xcritia)
            else:
                x3 = max(x2 - fx2 / w, xcritia)

            if x2 != 0:
                delta = ((x3 - x2) / x2) ** 2
            else:
                delta = x3 ** 2
            if delta < 1e-10:
                break
            else:
                x0 = x1
                x1 = x2
                x2 = x3
        return x3, i,


    def equivstrain(x, s):
        for i in range(100):
            a = func_A(x)
            b = func_B(x)
            c = func_C(x)
            d = func_D(x)
            fa = a * J2(s)
            fb = b * np.sqrt(J2(s))
            fc = c * s[0][0]
            fd = d * I1(s)
            es = ((fb + fc + fd) + np.sqrt((fb + fc + fd) ** 2 + 4.0 * fa)) / 2.0
            y = es / e0
            if ((x - y) ** 2 < 1.0e-10):
                return es, i,
            else:
                x = 0.85 * x + 0.15 * y
        return es, i,


    def I1(epsilon):
        return np.sum(epsilon)


    def J2(e):
        return 1.0 / 6.0 * ((e[0][0] - e[1][0]) ** 2 + (e[1][0] - e[2][0]) ** 2 + (e[2][0] - e[0][0]) ** 2)


    # simudata = open("strain.txt",'r')
    # lines = simudata.readlines()
    # UT = np.array([[0,0,0]])
    # for line in lines:
    #     var = line.split()
    #     UT = np.append(UT,[list(map(float,var))],axis=0)
    #
    # times = []
    # beta = 0
    # for iut in UT:
    #     s = np.array([[iut[0]],[iut[1]],[iut[2]]])
    #     es,i, = equivstrain(beta,s)
    #     times.append(i)
    #     beta = es/e0
    #     print(iut[0],es,i)
    #
    # winsound.Beep(500, 2000)
    # exit()


    # times = []
    # px = []
    # py1 = []
    # py2 = []
    # for x in np.arange(0.1, 2.5, 0.01):
    #     s = BC(x)
    #     es,i, = equivstrain(x-0.01, s)
    #     # es,i, = muller(es/e0,s)
    #     times.append(i)
    #     px.append(x)
    #     py1.append(x)
    #     py2.append(es/e0)
    #     print(x, es / e0,i)
    # print(np.average(times))
    # plt.plot(px,py1,label='theory')
    # plt.plot(px,py2,label='calcu')
    # plt.legend()
    #
    # winsound.Beep(600,500)
    #
    # plt.show()
    # exit()

    for x in np.arange(0.01, 4.0, 0.01):
        # print(poisson(x))
        ut_s = UT(x)
        uc_s = UC(x)
        bc_s = BC(x)
        tc_s = TC(x)
        fa = np.array([[J2(ut_s) / ut_s[0][0] ** 2,
                        np.sqrt(J2(ut_s)) / ut_s[0][0],
                        ut_s[0][0] / ut_s[0][0],
                        I1(ut_s) / ut_s[0][0]],
                       [J2(uc_s) / ut_s[0][0] ** 2,
                        np.sqrt(J2(uc_s)) / ut_s[0][0],
                        uc_s[0][0] / ut_s[0][0],
                        I1(uc_s) / ut_s[0][0]],
                       [J2(bc_s) / ut_s[0][0] ** 2,
                        np.sqrt(J2(bc_s)) / ut_s[0][0],
                        bc_s[0][0] / ut_s[0][0],
                        I1(bc_s) / ut_s[0][0]],
                       [J2(tc_s) / ut_s[0][0] ** 2,
                        np.sqrt(J2(tc_s)) / ut_s[0][0],
                        tc_s[0][0] / ut_s[0][0],
                        I1(tc_s) / ut_s[0][0]]
                       ])
        fb = np.array([1, 1, 1, 1])
        fx = np.linalg.solve(fa, fb)
        np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
        with printoptions(precision=5, suppress=True):
            print(fx)

        es = equivstrain(x, uc_s)
