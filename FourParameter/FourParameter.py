# coding:utf-8
import matplotlib.pyplot as plt
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


def solveABCD(e, mu, ft, fc, s0):
    """"""
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
    print('{0:10.5e},{1:10.5e},{2:10.5e},{3:10.5e}'.format(fa[0][0], fa[0][1], fa[0][2], fa[0][3]))
    # print('e = {0:10.5e}, ft = {1:10.5e}, s0 = {2:10.5e}'.format(e,ft,s0))
    return abcd


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
    estrain = (-fb + np.sqrt(fb ** 2 - 4 * fa * fc)) / 2
    estrain = fb ** 2 - 4 * fa * fc
    return estrain


def getdamage(e, ft, es, b, s0):
    if es < s0:
        d = 0
    else:
        d = 1 - np.sqrt(ft / (e * es) * (2 * np.exp(-b * (es - s0)) - np.exp(-2 * b * (es - s0))))
    return d


e = 3.14e10
mu = 1.67e-1
ft = 3.47e6
ct = 0.126
fc = ft / ct
s0 = ft / e
gf = 336
lch = 0.87
bb = 3 / (s0 * (2 * gf * e / lch / ft ** 2 - 1))

maxrange = 500
ABCD = np.zeros((maxrange, 4))
estrain = []
refstrain = []
damage = []
ABCD[0] = solveABCD(e, mu, ft, fc, s0)
f_uniaxial_tensile = np.array([ft, 0, 0])
s_uniaxial_tensile = force_2_strain(e, mu, f_uniaxial_tensile)
f_uniaxial_compress = np.array([0, 0, -fc])
s_uniaxial_compress = force_2_strain(e, mu, f_uniaxial_compress)
ds = s_uniaxial_compress * 0.001
dref = s_uniaxial_tensile * 0.001
de = e
for i in range(maxrange - 1):
    s_uniaxial_compress = np.add(s_uniaxial_compress, ds)
    s_uniaxial_tensile = np.add(s_uniaxial_tensile, dref)
    refstrain.append(s_uniaxial_tensile[0])
    estrain.append(equiv_strain(ABCD[0], s_uniaxial_compress))
    damage.append(getdamage(e, ft, estrain[i], bb, s0))

    ds0 = estrain[i]
    dABCD = solveABCD(e, mu, ft, fc, ds0)
    ABCD[i + 1] = dABCD

with plt.xkcd():
    plt.figure(figsize=(8, 8), dpi=80)
    p1 = plt.subplot(311)
    pa = []
    pb = []
    pc = []
    pd = []
    for dABCD in ABCD:
        pa.append(dABCD[0])
        pb.append(dABCD[1])
        pc.append(dABCD[2])
        pd.append(dABCD[3])
    plta = p1.plot(pa, 'g', label="A", linewidth=2)
    pltb = p1.plot(pb, 'r', label="B", linewidth=2)
    pltc = p1.plot(pc, 'y', label="C", linewidth=2)
    pltd = p1.plot(pd, 'm', label="D", linewidth=2)
    plt.sca(p1)
    plt.xlabel('istep')
    plt.ylabel('ABCD')
    plt.legend(loc=0)

    p2 = plt.subplot(312)
    p2.plot(estrain)
    p2.plot(refstrain)
    plt.sca(p2)
    plt.xlabel('istep')
    plt.ylabel('equiv_strain')

    p3 = plt.subplot(313)
    p3.plot(damage)
    plt.sca(p3)
    plt.xlabel('istep')
    plt.ylabel('damage')

plt.show()
# plt.savefig('VarABCD.png')
# print(ABCD)
