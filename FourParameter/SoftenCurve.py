# coding:utf-8

import contextlib

import FourParameter.SolveABCD as SolveABCD
import numpy as np
from scipy import optimize


@contextlib.contextmanager
def printoptions(*args, **kwargs):
    original = np.get_printoptions()
    np.set_printoptions(*args, **kwargs)
    yield
    np.set_printoptions(**original)


def UT(e, mu, ft, ct, beta):
    ''' 
    '''
    f = np.array([[ft], [0], [0]])
    s = SolveABCD.force_2_strain(e, mu, f)

    def fun(x):
        return x / (2.723 * (x - 1) ** 1.7 + x) - (2.0 - beta)

    sol = optimize.root(fun, beta)
    x = sol.x
    s = np.multiply(s, x)
    return s


def UC(e, mu, ft, ct, beta):
    f = np.array([[0], [0], [-ft / ct]])
    s = SolveABCD.force_2_strain(e, mu, f)

    def fun(x):
        return x / (1.7 * (x - 1) ** 2 + x) - (2.0 - beta)

    sol = optimize.root(fun, beta)
    x = sol.x
    s = np.multiply(s, x)
    beta = 2.0 - beta
    return s


def BC(e, mu, ft, ct, beta):
    f = np.array([[0], [-1.28 * ft / ct], [-1.28 * ft / ct]])
    s = SolveABCD.force_2_strain(e, mu, f)

    def fun(x):
        return x / (1.7 * (x - 1) ** 2 + x) - (2.0 - beta)

    sol = optimize.root(fun, beta)
    x = sol.x
    s = np.multiply(s, x)
    beta = 2.0 - beta
    return s


def TC(e, mu, ft, ct, beta):
    f = np.array([[-2.09081 * ft / ct],
                  [-2.09081 * ft / ct],
                  [-7.81838 * ft / ct]])
    s = SolveABCD.force_2_strain(e, mu, f)

    def fun(x):
        return x / (1.7 * (x - 1) ** 2 + x) - (2.0 - beta)

    sol = optimize.root(fun, beta)
    x = sol.x
    s = np.multiply(s, x)
    beta = 2.0 - beta
    return s


def I1(epsilon):
    return np.sum(epsilon)


def J2(e):
    return 1.0 / 6.0 * ((e[0][0] - e[1][0]) ** 2 + (e[1][0] - e[2][0]) ** 2 + (e[2][0] - e[0][0]) ** 2)


def strain(e, mu, ft, ct):
    for beta in np.arange(1.0, 1.99, 0.01):
        ut_s = UT(e, mu, ft, ct, beta)
        uc_s = UC(e, mu, ft, ct, beta)
        bc_s = BC(e, mu, ft, ct, beta)
        tc_s = TC(e, mu, ft, ct, beta)

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
        with printoptions(precision=5, suppress=True):
            print(uc_s[0][0], fx, beta)
    print("################################################################")


if __name__ == "__main__":
    e = 3.14e10
    mu = 0.167
    ft = 3.47e6
    ct = 0.126
    strain(e, mu, ft, ct)
