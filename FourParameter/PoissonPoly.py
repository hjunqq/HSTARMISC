# coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
import contextlib
from scipy import optimize
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
    maxiter = 1000


    def poisson(x):
        """ x load rate"""
        a = 0.0925059
        b = -0.173128
        c = -0.00111889
        d = 0.191915
        e = 0.190388
        return a * x ** 4 + b * x ** 3 + c * x ** 2 + d * x + e
        return (0.2 * (1 + 0.68815 * x - 1.78667 * x ** 2 + 2.1465 * x ** 3)) / (1 - 0.5 * x ** 2 +
                                                                                 0.8573 * x ** 3)


    def DMat(mu):
        D = np.array([[1, -mu, -mu],
                      [-mu, 1, -mu],
                      [-mu, -mu, 1]])
        return D / E


    def UT(y):
        if y <= 1.0:
            def fun(x):
                return 1.2 * x - 0.2 * x ** 6 - y

            sol = optimize.root(fun, y)
            x = sol.x
        elif y > 1.0:
            def fun(x):
                return x / (2.723 * (x - 1) ** 1.7 + x) - (2.0 - y)

            sol = optimize.root(fun, y)
            x = sol.x
        mu = poisson(y)
        f = np.array([[ft], [0], [0]]) * x
        sp = np.dot(DMat(mu), f)
        return sp


    def UC(y):
        if y <= 1.0:
            def fun(x):
                return 1.746 * x - 0.492 * x ** 2 - 0.254 * x ** 3 - y

            sol = optimize.root(fun, y)
            x = sol.x
        else:
            def fun(x):
                return x / (1.635 * (x - 1) ** 2 + x) - (2.0 - y)

            sol = optimize.root(fun, y)
            x = sol.x
        f = np.array([[0], [0], [-ft / cf]]) * x
        mu = poisson(y)
        sp = np.dot(DMat(mu), f)
        return sp


    def BC(y):
        if y <= 1.0:
            def fun(x):
                return 1.746 * x - 0.492 * x ** 2 - 0.254 * x ** 3 - y

            sol = optimize.root(fun, y)
            x = sol.x
        else:
            def fun(x):
                return x / (1.635 * (x - 1) ** 2 + x) - (2.0 - y)

            sol = optimize.root(fun, y)
            x = sol.x
        f = np.array([[0], [-1.28 * ft / cf], [-1.28 * ft / cf]]) * x
        mu = poisson(y)
        sp = np.dot(DMat(mu), f)
        return sp


    def TC(y):
        if y <= 1.0:
            def fun(x):
                return 1.746 * x - 0.492 * x ** 2 - 0.254 * x ** 3 - y

            sol = optimize.root(fun, y)
            x = sol.x
        else:
            def fun(x):
                return x / (1.635 * (x - 1) ** 2 + x) - (2.0 - y)

            sol = optimize.root(fun, y)
            x = sol.x
        f = np.array([[-2.09081 * ft / cf],
                      [-2.09081 * ft / cf],
                      [-7.81838 * ft / cf]]) * x
        mu = poisson(y)
        sp = np.dot(DMat(mu), f)
        return sp


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
        x1 = x0 / 0.618
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
                x = 0.9 * x + 0.1 * y
        return es, i,


    def I1(epsilon):
        return np.sum(epsilon)


    def J2(e):
        return 1.0 / 6.0 * ((e[0][0] - e[1][0]) ** 2 + (e[1][0] - e[2][0]) ** 2 + (e[2][0] - e[0][0]) ** 2)


    def plotTheoryCurve():
        plt.figure()

        # Plot UT Curve
        px = []
        py = []
        for x in np.arange(0.1, 1.5, 0.01):
            iut = UT(x)
            px.append(iut[0][0])
            if x < 1.0:
                py.append(x)
            else:
                py.append(2.0 - x)
        plt.plot(px, py, 'g', label='UT')
        # Plot UC Curve
        px = []
        py = []
        for x in np.arange(0.1, 1.5, 0.01):
            iuc = UC(x)
            px.append(iuc[0][0])
            if x < 1.0:
                py.append(x)
            else:
                py.append(2.0 - x)
        plt.plot(px, py, 'r', label='UC')
        plt.legend()
        plt.show()
        winsound.Beep(500, 2000)
        exit()


    # plotTheoryCurve()

    # simudata = open("strain.txt",'r')
    # lines = simudata.readlines()
    # simstrain = np.array([[0,0,0]])
    # for line in lines:
    #     var = line.split()
    #     simstrain = np.append(simstrain,[list(map(float,var))],axis=0)
    #
    # times = []
    # beta = 0
    # for iut in simstrain:
    #     s = np.array([[iut[0]],[iut[1]],[iut[2]]])
    #     es,i, = equivstrain(beta,s)
    #     times.append(i)
    #     beta = es/e0
    #     print(iut[0],es,i)
    #
    # winsound.Beep(500, 2000)
    # exit()

    def check():
        times = []
        px = []
        py1 = []
        py2 = []
        for x in np.arange(0.1, 1.5, 0.01):
            sref = UT(x)
            s = TC(x)
            es, i, = equivstrain(1.0, s)
            # es,i, = muller(x,s)
            times.append(i)
            px.append(x)
            py1.append(sref[0] / e0)
            py2.append(es / e0)
            print(x, sref[0][0] / e0, es / e0, i)
        print(np.average(times))
        plt.plot(px, py1, label='theory')
        plt.plot(px, py2, label='calcu')
        plt.legend()

        winsound.Beep(600, 500)

        plt.show()
        exit()


    # check()

    def test():
        # Test Modify Poisson
        def getloadstat(x):
            if x <= 1:
                y = 1.2 * x - 0.2 * x ** 6
            else:
                y = x / (2.723 * (x - 1) ** 1.7 + x)
                y = 2.0 - y
            return y

        x1 = []
        x2 = []
        for r in np.arange(0.01, 1.2, 0.01):
            s = UT(r)
            es, iter, = equivstrain(0, s)
            refx = es / e0
            f = np.array([[0], [-1.28 * ft / cf], [-1.28 * ft / cf]]) * refx
            # f = np.array([[0],[0],[-ft/cf]])*refx
            # f = np.array([[ft],[0],[0]])*refx
            x = 0
            mu = poisson(r)
            s0 = np.dot(DMat(mu), f)
            s0[0][0] = 0
            # s0[0][0] = 0
            for i in range(100):
                es, iter, = equivstrain(x, s0)
                x = es / e0
                y = getloadstat(x)
                # print(refx, x, iter)
                mu = poisson(y)
                s0 = np.dot(DMat(mu), f)
            x1.append(refx)
            x2.append(x)
            print(r, refx, x, iter)
        plt.plot(x1, 'g', label="ref")
        plt.plot(x2, 'r', label='cal')
        plt.legend()
        plt.show()
        exit()


    test()

    px = []
    for x in np.arange(0.01, 1.99, 0.01):
        # print(poisson(x))
        ut_s = UT(x)
        uc_s = UC(x)
        bc_s = BC(x)
        tc_s = TC(x)
        px.append(ut_s[0][0])
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
            print(ut_s[0][0], fx, x)

            # es = equivstrain(x, uc_s)
            # for ipx in px:
            #     print(ipx)
