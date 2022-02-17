# coding:utf-8
'''SolveABCD Function0 v
'''
import numpy as np


def force_2_strain(e, mu, f):
    """
    in:
        f is np.array
    out:
        epsilon is np.array
    """
    poisson = np.array([[1, -mu, -mu],
                        [-mu, 1, -mu],
                        [-mu, -mu, 1]])
    strain = np.dot(poisson, f) / e
    return strain


def value_in_function(s, s0):
    """"""
    s1 = s[0]
    s2 = s[1]
    s3 = s[2]
    i1 = np.sum(s)
    j2 = ((s1 - s2) ** 2 + (s1 - s3) ** 2 + (s2 - s3) ** 2) / 6
    f_value = np.zeros(4)
    f_value[0] = j2 / s0 / s0
    f_value[1] = np.sqrt(j2) / s0
    f_value[2] = s1 / s0
    f_value[3] = i1 / s0
    return f_value


def Solve(e, mu, ft, ct):
    fc = ft / ct
    s0 = ft / e
    fa = np.zeros((4, 4))
    fb = np.array([1, 1, 1, 1])
    # Uniaxial Tensile
    f_uniaxial_tensile = np.array([ft, 0, 0])
    s_uniaxial_tensile = force_2_strain(e, mu, f_uniaxial_tensile)
    # Uniaxial Compress
    f_uniaxial_compress = np.array([0, 0, -fc])
    s_uniaxial_compress = force_2_strain(e, mu, f_uniaxial_compress)
    # Biaxial Compress
    f_biaxial_compress = np.array([0, -1.28 * fc, -1.28 * fc])
    s_biaxial_compress = force_2_strain(e, mu, f_biaxial_compress)
    # Triaxial Compress
    f_triaxial_compress = np.array([2.7 / np.sqrt(2) * fc - 4 * fc,
                                    2.7 / np.sqrt(2) * fc - 4 * fc,
                                    -2.7 * np.sqrt(2) * fc - 4 * fc])
    s_triaxial_compress = force_2_strain(e, mu, f_triaxial_compress)

    fa[0] = value_in_function(s_uniaxial_tensile, s0)
    fa[1] = value_in_function(s_uniaxial_compress, s0)
    fa[2] = value_in_function(s_biaxial_compress, s0)
    fa[3] = value_in_function(s_triaxial_compress, s0)
    abcd = np.linalg.solve(fa, fb)
    # print('{0:10.5f},{1:10.5f},{2:10.5f},{3:10.5f}'.format(fa[0][0], fa[0][1], fa[0][2], fa[0][3]))
    # print('e = {0:10.5e}, ft = {1:10.5e}, s0 = {2:10.5e}'.format(e,ft,s0))
    return abcd


def equiv_strain_f(e, mu, ft, ABCD, f):
    s = force_2_strain(e, mu, f)
    s1 = s[0]
    s2 = s[1]
    s3 = s[2]
    a = ABCD[0]
    b = ABCD[1]
    c = ABCD[2]
    d = ABCD[3]

    i1 = np.sum(s)
    j2 = ((s1 - s2) ** 2 + (s1 - s3) ** 2 + (s2 - s3) ** 2) / 6
    fa = 1.0
    fb = -(b * np.sqrt(j2) + c * s1 + d * i1)
    fc = -a * j2
    estrain = (-fb + np.sqrt(fb ** 2 - 4 * fa * fc)) / (2 * fa)
    return estrain


def equiv_strain(ABCD, s):
    s1 = s[0]
    s2 = s[1]
    s3 = s[2]
    a = ABCD[0]
    b = ABCD[1]
    c = ABCD[2]
    d = ABCD[3]
    i1 = np.sum(s)
    j2 = ((s1 - s2) ** 2 + (s1 - s3) ** 2 + (s2 - s3) ** 2) / 6
    fa = 1.0
    fb = -(b * np.sqrt(j2) + c * s1 + d * i1)
    fc = -a * j2
    estrain = (-fb + np.sqrt(fb ** 2 - 4 * fa * fc)) / (2 * fa)
    return estrain


if __name__ == "__main__":
    e = 3.14e10
    mu = 0.167
    ft = 3.47e6
    ct = 0.126
    ABCD = Solve(e, mu, ft, ct)
    print('{0:10.5f},{1:10.5f},{2:10.5f},{3:10.5f}'.format(ABCD[0], ABCD[1], ABCD[2], ABCD[3]))

    # uniaxial-tension
    f = np.array([ft, 0, 0])
    ef = equiv_strain_f(e, mu, ft, ABCD, f)
    print(ef)
    s = force_2_strain(e, mu, f)
    ef = equiv_strain(ABCD, s)
    print(ef)

    # uniaxial-compress
    f = np.array([0, 0, -ft / ct])
    ef = equiv_strain_f(e, mu, ft, ABCD, f)
    print(ef)
    s = force_2_strain(e, mu, f)
    ef = equiv_strain(ABCD, s)

    print(ef)
