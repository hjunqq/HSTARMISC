# coding:utf-8

import contextlib

import matplotlib.pyplot as plt
import numpy as np
import winsound
from scipy import optimize


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
        return 0.167
        if x <= 0.8:
            return 0.2
        elif 0.8 < x <= 1.0:
            return 0.36 - 0.16 * np.sqrt(1 - (5 * x - 4) ** 2)
        elif x > 1.0:
            return 0.36
        return (0.2 * (1 + 0.68815 * x - 1.78667 * x ** 2 + 2.1465 * x ** 3)) / (1 - 0.5 * x ** 2 +
                                                                                 0.8573 * x ** 3)


    def DMat(mu):
        D = np.array([[1.0, -mu, -mu],
                      [-mu, 1.0, -mu],
                      [-mu, -mu, 1.0]])
        return D / E


    def StressD(mu):
        varlambda = E * mu / ((1 + mu) * (1 - 2 * mu))
        G = E / (2 * (1 + mu))
        D = np.array([[varlambda + 2 * G, varlambda, varlambda],
                      [varlambda, varlambda + 2 * G, varlambda],
                      [varlambda, varlambda, varlambda + 2 * G]])
        return D


    def Damage(y):
        if y <= 1.0:
            def fun(x):
                return 1.2 * x - 0.2 * x ** 6 - y

            sol = optimize.root(fun, y)
            x = sol.x
        else:
            def fun(x):
                return x / (2.723 * (x - 1) ** 1.7 + x) - (2.0 - y)

            sol = optimize.root(fun, y)
            x = sol.x
        d = 1.0 - np.sqrt(y / (1.2 * x))
        return d


    def BetaTDamage(x):
        k = (1 - x) ** 2
        if k >= 1.0:
            def fun(x):
                return 1.2 - 0.2 * x ** 5 - k

            sol = optimize.root(fun, 0.5)
            x = sol.x
            if x < 0:
                x = 0
            beta = 1.2 * x - 0.2 * x ** 6
        else:
            def fun(x):
                return 1 / (2.723 * (x - 1) ** 1.7 + x) - k

            sol = optimize.root(fun, 1)
            x = sol.x
            beta = x / (2.723 * (x - 1) ** 1.7 + x)
            beta = 2 - beta
        return beta


    def BetaCDamage(x):
        k = (1 - x) ** 2
        if k >= 1.0:
            def fun(x):
                return 1.746 - 0.492 * x - 0.254 * x ** 2 - k

            sol = optimize.root(fun, 0.5)
            x = sol.x
            beta = 1.746 * x - 0.492 * x ** 2 - 0.254 * x ** 3
            if x < 0:
                x = 0
        else:
            def fun(x):
                return 1 / (1.635 * (x - 1) ** 2 + x) - k

            sol = optimize.root(fun, 1)
            x = sol.x
            beta = x / (1.635 * (x - 1) ** 2 + x)
            beta = 2 - beta
        return beta


    def UT(y):
        f = np.array([[ft], [0], [0]])
        mu = mu0
        sp = np.dot(DMat(mu), f)
        if y <= 1.0:
            def fun(x):
                return 1.2 * x - 0.2 * x ** 6 - y

            sol = optimize.root(fun, y)
            x = sol.x
            beta = y
        elif y > 1.0:
            def fun(x):
                return x / (2.723 * (x - 1) ** 1.7 + x) - (2.0 - y)

            sol = optimize.root(fun, y)
            x = sol.x
            beta = 2.0 - y
        sp = np.multiply(sp, x)
        return sp


    def UT_Stress(y):
        return np.array([[ft], [0], [0]]) * y


    def UC(y):
        f = np.array([[0], [0], [-ft / cf]])
        mu = mu0
        sp = np.dot(DMat(mu), f)
        if y <= 1.0:
            def fun(x):
                return 1.746 * x - 0.492 * x ** 2 - 0.254 * x ** 3 - y

            sol = optimize.root(fun, y)
            x = sol.x
            beta = y
        else:
            def fun(x):
                return x / (1.635 * (x - 1) ** 2 + x) - (2.0 - y)

            sol = optimize.root(fun, y)
            x = sol.x
            beta = 2.0 - y
        sp = np.multiply(sp, x)
        return sp


    def UC_Stress(y):
        return np.array([[0], [0], [-ft / cf]]) * y


    def BC(y):
        f = np.array([[0], [-1.28 * ft / cf], [-1.28 * ft / cf]])
        mu = mu0
        sp = np.dot(DMat(mu), f)
        if y <= 1.0:
            def fun(x):
                return 1.746 * x - 0.492 * x ** 2 - 0.254 * x ** 3 - y

            sol = optimize.root(fun, y)
            x = sol.x
            beta = y
        else:
            def fun(x):
                return x / (1.635 * (x - 1) ** 2 + x) - (2.0 - y)

            sol = optimize.root(fun, y)
            x = sol.x
            beta = 2.0 - y
        sp = np.multiply(sp, x)
        return sp


    def BC_Stress(y):
        return np.array([[0], [-1.28 * ft / cf], [-1.28 * ft / cf]]) * y


    def TC(y):
        f = np.array([[-2.09081 * ft / cf],
                      [-2.09081 * ft / cf],
                      [-7.81838 * ft / cf]])
        mu = mu0
        sp = np.dot(DMat(mu), f)
        if y <= 1.0:
            def fun(x):
                return 1.746 * x - 0.492 * x ** 2 - 0.254 * x ** 3 - y

            sol = optimize.root(fun, y)
            x = sol.x
            beta = y
        else:
            def fun(x):
                return x / (1.635 * (x - 1) ** 2 + x) - (2.0 - y)

            sol = optimize.root(fun, y)
            x = sol.x
            beta = 2.0 - y
        f = np.array([[-2.09081 * ft / cf],
                      [-2.09081 * ft / cf],
                      [-7.81838 * ft / cf]]) * y
        sp = np.multiply(sp, x)
        return sp


    def TC_Stress(y):
        return np.array([[-2.09081 * ft / cf],
                         [-2.09081 * ft / cf],
                         [-7.81838 * ft / cf]]) * y


    def func_A(x):
        a = 0.000797445
        b = 0.00178923
        c = 0.0277033
        d = -0.287551
        e = 1
        f = 7.63879E-05
        g = 1.00038E-05
        h = -0.00124502
        i = 5.36423

        return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 2 + g * x + h) / (
                1 + np.exp(-i * (x - e)))


    def func_B(x):
        a = 0.15859
        b = -0.427646
        c = 0.685937
        d = -0.00415398
        e = 1
        f = -0.0776056
        g = 0.211639
        h = -0.201007
        i = 4.47598
        return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 2 + g * x + h) / (
                1 + np.exp(-i * (x - e)))


    def func_C(x):
        a = -0.100753
        b = 0.275878
        c = 1.20938
        d = -0.00422647
        e = 1
        f = 0.0492903
        g = -0.134804
        h = 0.128791
        i = 4.46827
        return (a * x ** 3 + b * x + c) / (1 + np.exp(-d * (x - e))) + (f * x ** 3 + g * x + h) / (
                1 + np.exp(-i * (x - e)))


    def func_D(x):
        a = -0.00862732
        b = 0.02459
        c = 0.465522
        d = -0.00443683
        e = 1
        f = 0.00421752
        g = -0.0116139
        h = 0.0112586
        i = 4.44938
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
        for i in range(1):
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


    def equivstrain_stress(x, strain, stress):
        for i in range(100):
            a = func_A(x)
            b = func_B(x)
            c = func_C(x)
            d = func_D(x)
            fa = a * J2(strain)
            fb = b * np.sqrt(J2(strain))
            fc = c * strain[0][0]
            fd = d * I1(strain)
            estrain = ((fb + fc + fd) + np.sqrt((fb + fc + fd) ** 2 + 4.0 * fa)) / 2.0
            fa = a * J2(stress)
            fb = b * np.sqrt(J2(stress))
            fc = c * stress[0][0]
            fd = d * I1(stress)
            estress = ((fb + fc + fd) + np.sqrt((fb + fc + fd) ** 2 + 4.0 * fa)) / 2.0

            y = estress / e0
            if ((x - y) ** 2 < 1.0e-10):
                return estrain, i,
            else:
                x = 0.8 * x + 0.2 * y
        return estrain, i,


    def equivstress(x, s):
        a = func_A(x)
        b = func_B(x)
        c = func_C(x)
        d = func_D(x)
        fa = a * J2(s)
        fb = b * np.sqrt(J2(s))
        fc = c * s[0][0]
        fd = d * I1(s)
        es = ((fb + fc + fd) + np.sqrt((fb + fc + fd) ** 2 + 4.0 * fa)) / 2.0
        return es, 1,


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
        for x in np.arange(0.01, 0.8, 0.01):
            betat = BetaTDamage(x)
            betac = BetaCDamage(x)
            sref = UT(betat)
            s = TC(betac)
            es, i, = equivstrain(betat, s)
            # es,i, = muller(x,s)
            times.append(i)
            px.append(betat)
            py1.append(sref[0] / e0)
            py2.append(es / e0)
            print(betat, sref[0][0] / e0, es / e0, i)
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
        for r in np.arange(0.1, 1.0, 0.02):
            s = UC(r)
            es, iter, = equivstrain(1.0, s)
            refx = es / e0
            # f = np.array([[0], [-1.28 * ft / cf], [-1.28 * ft / cf]]) * refx
            f = np.array([[0], [0], [-ft / cf]]) * refx
            # f = np.array([[ft],[0],[0]])*refx
            x = 0
            mu = poisson(r)
            s0 = np.dot(DMat(mu), f)
            s0[0][0] = 0
            s0[1][0] = 0
            for i in range(100):
                es, iter, = equivstrain(1.0, s0)
                # es,iter, = muller(x,s0)
                x = es / e0
                y = getloadstat(x)
                # print(refx, x, iter)
                mu = 0.167
                stress = np.dot(StressD(mu), s0)
                estress, iter = equivstress(1.0, stress)
                y = estress / ft

                def fun(x):
                    return 1.2 * x - 0.2 * x ** 6 - y

                sol = optimize.root(fun, y)
                x = sol.x
                es, iter, = equivstrain(1.0, s0)
            x1.append(refx)
            x2.append(x)
            print(r, refx, x, iter)
        plt.plot(x1, 'g', label="ref")
        plt.plot(x2, 'r', label='cal')
        plt.legend()
        plt.show()
        exit()


    # test()

    class Curve:
        def __init__(self, x=[[]], y=[[]]):
            self.x = x
            self.y = y


    px = []
    ut_curve = Curve()
    uc_curve = Curve()
    bc_curve = Curve()
    tc_curve = Curve()


    def strain():
        for x in np.arange(-0.32, 1, 0.01):
            # print(poisson(x))
            betat = BetaTDamage(x)
            betac = BetaCDamage(x)
            # print(betat,betac)
            mu = poisson(betat)

            ut_s = UT(betat)

            ut_stress = UT_Stress(betat)
            ut_curve.x.append(ut_s.tolist())
            ut_curve.y.append(ut_stress.tolist())

            uc_s = UC(betac)
            uc_stress = UC_Stress(betac)
            uc_curve.x.append(uc_s.tolist())
            uc_curve.y.append(uc_stress.tolist())

            bc_s = BC(betac)
            bc_stress = BC_Stress(betac)
            bc_curve.x.append(bc_s.tolist())
            bc_curve.y.append(bc_stress.tolist())

            tc_s = TC(betac)
            tc_stress = TC_Stress(betac)
            tc_curve.x.append(tc_s.tolist())
            tc_curve.y.append(tc_stress.tolist())

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
            # np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
            with printoptions(precision=5, suppress=True):
                print(ut_s[0][0], fx, x)
        print("################################################################")

        ############################################################################


    def stress():
        for x in np.arange(0.01, 1.0, 0.01):
            # print(poisson(x))
            betat = BetaTDamage(x)
            betac = BetaCDamage(x)

            mu = poisson(betat)

            ut_s = UT(betat)
            ut_stress = UT_Stress(betat)
            ut_curve.x.append(ut_s)
            ut_curve.y.append(ut_stress)

            uc_s = UC(betac)
            uc_stress = UC_Stress(betac)
            uc_curve.x.append(uc_s)
            uc_curve.y.append(uc_stress)

            bc_s = BC(betac)
            bc_stress = BC_Stress(betac)
            bc_curve.x.append(bc_s)
            bc_curve.y.append(bc_stress)

            tc_s = TC(betac)
            tc_stress = TC_Stress(betac)
            tc_curve.x.append(tc_s)
            tc_curve.y.append(tc_stress)
            fa = np.array([[J2(ut_stress) / ut_stress[0][0] ** 2,
                            np.sqrt(J2(ut_stress)) / ut_stress[0][0],
                            ut_stress[0][0] / ut_stress[0][0],
                            I1(ut_stress) / ut_stress[0][0]],
                           [J2(uc_stress) / ut_stress[0][0] ** 2,
                            np.sqrt(J2(uc_stress)) / ut_stress[0][0],
                            uc_stress[0][0] / ut_stress[0][0],
                            I1(uc_stress) / ut_stress[0][0]],
                           [J2(bc_stress) / ut_stress[0][0] ** 2,
                            np.sqrt(J2(bc_stress)) / ut_stress[0][0],
                            bc_stress[0][0] / ut_stress[0][0],
                            I1(bc_stress) / ut_stress[0][0]],
                           [J2(tc_stress) / ut_stress[0][0] ** 2,
                            np.sqrt(J2(tc_stress)) / ut_stress[0][0],
                            tc_stress[0][0] / ut_stress[0][0],
                            I1(tc_stress) / ut_stress[0][0]]
                           ])
            fb = np.array([1, 1, 1, 1])
            fx = np.linalg.solve(fa, fb)
            with printoptions(precision=5, suppress=True):
                print(ut_s[0][0], fx, x)

                # fa = fx[0] * J2(uc_stress)
                # fb = fx[1] * np.sqrt(J2(uc_stress))
                # fc = fx[2] * uc_stress[0][0]
                # fd = fx[3] * I1(uc_stress)
                # es = ((fb + fc + fd) + np.sqrt((fb + fc + fd) ** 2 + 4.0 * fa)) / 2.0
                # print(es,ut_stress[0][0],ut_stress[0][0]/(1.0-Damage(x))**2)
                # es = equivstrain(x, uc_s)
                # for ipx in px:
                #     print(ipx)


    stress()
