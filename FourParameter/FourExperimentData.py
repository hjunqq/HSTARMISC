# coding:utf-8
# from scipy.optimize import fsolve
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import copy
import math


# from scipy.optimize import fsolve
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


def func_A(x):
    a = 0.02009673525788955
    b = -0.029435013048995085
    c = -0.008450205656339653
    d = -0.010109011359836884
    e = 0.014565798366325098
    f = 9.40513299335634
    if x < 0:
        x = 1e-3
    # elif x > 10:
    #	x = 10
    return (a * x + b) / (1 + np.exp(-c * (x - 1))) + (d * x + e) / (1 + np.exp(-f * (x - 1)))


# a = 0.364939
# b = -1.18937
# c = 0.907646
# d = -5.99995
# e = -0.368731
# f = 1.20399
# g = -0.922274
# h = -6.19622
# return (a * x ** 2 + b * +c)/(1 + np.exp(-d * (x - 1))) + (e * x ** 2 + f * x
# + g) / (1 + np.exp(-h * (x - 1)))
def func_B(x):
    # a = -0.16782897428881352
    # b = -0.9730000946006507
    # c = -7.020691822039098
    # d = 0.02460200453416887
    # e = -1.4347611554479738
    # f = 6.682954427765515
    if x < 0:
        x = 1e-3
    # elif x > 10:
    #	x = 10
    # return (a * x + b) / (1 + np.exp(-c * (x - 1))) + (d * x + e) / (1 +
    # np.exp(-f * (x - 1)))
    a = -0.286416
    b = -0.088879
    c = -2.07362
    d = 0.102829
    e = 0.167942
    f = -0.00338822
    g = 0.00499205
    h = -0.301999
    i = 6.80777
    return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - 1))) + (e * x ** 2 + f * x + g * x ** 3 + h) / (
        1 + np.exp(-i * (x - 1)))


def func_C(x):
    # a = -0.02153527551118732
    # b = 2.5355663858325155
    # c = 7.4115221640961035
    # d = 0.16392524594632688
    # e = 2.128524377974201
    # f = -7.623861721311346
    if x < 0:
        x = 1e-3
    # elif x > 10:
    #	x = 10
    # return (a * x + b) / (1 + np.exp(-c * (x - 1))) + (d * x + e) / (1 +
    # np.exp(-f * (x - 1)))
    a = -0.00064966996450393139104896258364110858
    b = -0.01471874230115250162708742366068900838
    c = 2.52281420985764079503375333567903769367
    d = 6.35985746330645001818680405299039276126
    e = 0.13126535021691297496488602052127626195
    f = 0.05164115655525151965361124977651764453
    g = 2.14285744453289313549846638798741476404
    h = -6.52859182895695704025244797810383169775
    return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - 1))) + (e * x ** 2 + f * x + g) / (1 + np.exp(-h * (x - 1)))


def func_D(x):
    # a = -0.08133834789319161
    # b = -0.6997017831313568
    # c = -9.374092718229734
    # d = 0.007954995128243313
    # e = -0.8559987880029327
    # f = 8.991748543322572
    if x < 0:
        x = 1e-3
    # elif x > 10:
    #	x = 10
    # return (a * x + b) / (1 + np.exp(-c * (x - 1))) + (d * x + e) / (1 +
    # np.exp(-f * (x - 1)))
    a = -0.103031
    b = 0.0205204
    c = -0.710704
    d = -5.36586
    e = -0.000047795
    f = 0.00836642
    g = -0.85528
    h = 5.13352

    return (a * x ** 2 + b * x + c) / (1 + np.exp(-d * (x - 1))) + (e * x ** 2 + f * x + g) / (1 + np.exp(-h * (x - 1)))


def func_dA(x):
    if x < 0:
        x = 1e-3
    # elif x > 10:
    #	x = 10
    a = 0.02009673525788955
    b = -0.029435013048995085
    c = -0.008450205656339653
    d = -0.010109011359836884
    e = 0.014565798366325098
    f = 9.40513299335634
    return a / (1 + np.exp(-c * (-1 + x))) + d / (1 + np.exp(-f * (-1 + x))) + (c * np.exp(-c * (-1 + x)) * (
        b + a * x)) / (1 + np.exp(-c * (-1 + x))) ** 2 + (np.exp(-f * (-1 + x)) * f * (e + d * x)) / (1 + np.exp(
        -f * (-1 + x))) ** 2


def func_dB(x):
    if x < 0:
        x = 1e-3
    # elif x > 10:
    #	x = 10
    a = -0.286416
    b = -0.088879
    c = -2.07362
    d = 0.102829
    e = 0.167942
    f = -0.00338822
    g = 0.00499205
    h = -0.301999
    i = 6.80777
    dfx1 = (b + 2 * a * x) / (1 + np.exp(-d * (x - 1)))
    dfx2 = d * np.exp(-d * (x - 1)) * (c + b * x + a * x ** 2) / (1 + np.exp(-d * (x - 1))) ** 2
    dfx3 = (f + 2 * a * x) / (1 + np.exp(-h * (x - 1)))
    dfx4 = h * np.exp(-h * (x - 1)) * (g + f * x + e * x ** 2) / (1 + np.exp(-h * (x - 1))) ** 2
    return dfx1 + dfx2 + dfx3 + dfx4


def func_dC(x):
    if x < 0:
        x = 1e-3
    elif x > 10:
        x = 10
    a = 0.00113593
    b = -0.0424765
    c = 2.62133
    d = 1.47791
    e = 0.842102
    f = -0.462108
    g = 1.86184
    h = -2.2127
    dfx1 = (b + 2 * a * x) / (1 + np.exp(-d * (x - 1)))
    dfx2 = d * np.exp(-d * (x - 1)) * (c + b * x + a * x ** 2) / (1 + np.exp(-d * (x - 1))) ** 2
    dfx3 = (f + 2 * a * x) / (1 + np.exp(-h * (x - 1)))
    dfx4 = h * np.exp(-h * (x - 1)) * (g + f * x + e * x ** 2) / (1 + np.exp(-h * (x - 1))) ** 2
    return dfx1 + dfx2 + dfx3 + dfx4


def func_dD(x):
    if x < 0:
        x = 1e-3
    elif x > 10:
        x = 10
    a = -0.103031
    b = 0.0205204
    c = -0.710704
    d = -5.36586
    e = -0.000047795
    f = 0.00836642
    g = -0.85528
    h = 5.13352
    dfx1 = (b + 2 * a * x) / (1 + np.exp(-d * (x - 1)))
    dfx2 = d * np.exp(-d * (x - 1)) * (c + b * x + a * x ** 2) / (1 + np.exp(-d * (x - 1))) ** 2
    dfx3 = (f + 2 * a * x) / (1 + np.exp(-h * (x - 1)))
    dfx4 = h * np.exp(-h * (x - 1)) * (g + f * x + e * x ** 2) / (1 + np.exp(-h * (x - 1))) ** 2
    return dfx1 + dfx2 + dfx3 + dfx4


def func_fx(x, fa, fb, fc, fd):
    # return (x ** 2 - fa) / (fb + fc + fd)
    return fa / x + fb + fc + fd


def func_dfx(x, fa, fb, fc, fd, dfa, dfb, dfc, dfd):
    # return (2 * x - dfa) / (fb + fc + fd) - (x ** 2 - fa) * (dfb + dfc + dfd) /
    # (fb + fc + fd) ** 2
    return -fa / x ** 2 + dfa / x + dfb + dfc + dfd


def linear_smooth3(inlist, outlist, n):
    if n < 3:
        for i in range(n):
            outlist[i] = inlist[i]
    else:
        outlist[0] = (5.0 * inlist[0] + 2.0 * inlist[1] - inlist[2]) / 6.0
        for i in range(1, n - 1):
            outlist[i] = (inlist[i - 1] + inlist[i] + inlist[i + 1]) / 3.0

        outlist[n - 1] = (5.0 * inlist[n - 1] + 2.0 * inlist[n - 2] - inlist[n - 3]) / 6.0


def linear_smooth5(inlist, outlist, n):
    if n < 5:
        for i in range(1, n):
            outlist[i] = inlist[i]
    else:
        outlist[0] = (3.0 * inlist[0] + 2.0 * inlist[1] + inlist[2] - inlist[4]) / 5.0
        outlist[1] = (4.0 * inlist[0] + 3.0 * inlist[1] + 2 * inlist[2] + inlist[3]) / 10.0
        for i in range(2, n - 2):
            outlist[i] = (inlist[i - 2] + inlist[i - 1] + inlist[i] + inlist[i + 1] + inlist[i + 2]) / 5.0

        outlist[n - 2] = (4.0 * inlist[n - 1] + 3.0 * inlist[n - 2] + 2 * inlist[n - 3] + inlist[n - 4]) / 10.0
        outlist[n - 1] = (3.0 * inlist[n - 1] + 2.0 * inlist[n - 2] + inlist[n - 3] - inlist[n - 5]) / 5.0


def linear_smooth7(inlist, outlist, n):
    if n < 7:
        for i in range(n):
            outlist[i] = inlist[i]
    else:
        outlist[0] = (
                         13.0 * inlist[0] + 10.0 * inlist[1] + 7.0 * inlist[2] + 4.0 * inlist[3] + inlist[4] - 2.0 *
                         inlist[
                             5] - 5.0 * inlist[6]) / 28.0

        outlist[1] = (5.0 * inlist[0] + 4.0 * inlist[1] + 3 * inlist[2] + 2 * inlist[3] + inlist[4] - inlist[6]) / 14.0

        outlist[2] = (7.0 * inlist[0] + 6.0 * inlist[1] + 5.0 * inlist[2] + 4.0 * inlist[3] + 3.0 * inlist[4] + 2.0 *
                      inlist[5] + inlist[6]) / 28.0

        for i in range(3, n - 3):
            outlist[i] = (inlist[i - 3] + inlist[i - 2] + inlist[i - 1] + inlist[i] + inlist[i + 1] + inlist[i + 2] +
                          inlist[i + 3]) / 7.0

        outlist[n - 3] = (7.0 * inlist[n - 1] + 6.0 * inlist[n - 2] + 5.0 * inlist[n - 3] + 4.0 * inlist[n - 4] + 3.0 *
                          inlist[n - 5] + 2.0 * inlist[n - 6] + inlist[n - 7]) / 28.0
        outlist[n - 2] = (
                             5.0 * inlist[n - 1] + 4.0 * inlist[n - 2] + 3.0 * inlist[n - 3] + 2.0 * inlist[n - 4] +
                             inlist[
                                 n - 5] - inlist[n - 7]) / 14.0
        outlist[n - 1] = (
                             13.0 * inlist[n - 1] + 10.0 * inlist[n - 2] + 7.0 * inlist[n - 3] + 4 * inlist[n - 4] +
                             inlist[
                                 n - 5] - 2 * inlist[n - 6] - 5 * inlist[n - 7]) / 28.0


def cubic_smooth5(inlist, outlist, n):
    if n < 5:
        for i in range(n):
            outlist[i] = inlist[i]
    else:
        outlist[0] = (69.0 * inlist[0] + 4.0 * inlist[1] - 6.0 * inlist[2] + 4.0 * inlist[3] - inlist[4]) / 70.0
        outlist[1] = (2.0 * inlist[0] + 27.0 * inlist[1] + 12.0 * inlist[2] - 8.0 * inlist[3] + 2.0 * inlist[4]) / 35.0
        for i in range(2, n - 2):
            outlist[i] = (-3.0 * (inlist[i - 2] + inlist[i + 2]) + 12.0 * (inlist[i - 1] + inlist[i + 1]) + 17.0 *
                          inlist[i]) / 35.0

        outlist[n - 2] = (
                             2.0 * inlist[n - 5] - 8.0 * inlist[n - 4] + 12.0 * inlist[n - 3] + 27.0 * inlist[
                                 n - 2] + 2.0 *
                             inlist[n - 1]) / 35.0
        outlist[n - 1] = (- inlist[n - 5] + 4.0 * inlist[n - 4] - 6.0 * inlist[n - 3] + 4.0 * inlist[n - 2] + 69.0 *
                          inlist[n - 1]) / 70.0


def get_value(curve, vtype, ratio):
    """
    type = 0		Up
    type = 1		Down
    """
    peak_strain = 0
    peak_stress = 0
    peak_index = 0
    nrange = len(curve)
    for i in range(nrange):
        ival = curve[i]
        if np.abs(peak_stress) < np.abs(ival[1]):
            peak_stress = ival[1]
            peak_strain = ival[0]
            peak_index = i

    y = ratio * np.abs(peak_stress)

    if vtype == 0:
        xp = []
        yp = []
        for i in range(peak_index + 1):
            xp.append(curve[i][0])
            yp.append(np.abs(curve[i][1]))
        x = np.interp(y, yp, xp)
    elif vtype == 1:
        xp = []
        yp = []
        for i in range(nrange - 1, peak_index - 1, -1):
            xp.append(curve[i][0])
            yp.append(np.abs(curve[i][1]))
        if y >= yp[0]:
            x = np.interp(y, yp, xp)
        else:
            x = (xp[0] - xp[1]) / (yp[0] - yp[1]) * (y - yp[1]) + xp[1]
    return x


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


def theta(s, s0):
    s1 = s[0]
    s2 = s[1]
    s3 = s[2]
    i1 = np.sum(s)
    j2 = ((s1 - s2) ** 2 + (s1 - s3) ** 2 + (s2 - s3) ** 2) / 6
    em = i1 / 3
    ksi = np.sqrt(2) * em / s0
    r = np.sqrt(2 * j2) / s0
    costheta = min((3 * s1 - i1) / (2 * np.sqrt(3 * j2)), 1)
    itheta = math.acos(costheta) * 180 / np.pi
    return ksi, r, itheta


def equiv_strain(ABCD, s, s_uniaxial):
    s1 = s[0]
    s2 = s[1]
    s3 = s[2]
    a = ABCD[0]
    b = ABCD[1]
    c = ABCD[2]
    d = ABCD[3]
    i1 = np.sum(s)
    j2 = ((s1 - s2) ** 2 + (s1 - s3) ** 2 + (s2 - s3) ** 2) / 6
    # fa = 1.0
    # fb = -(b * np.sqrt(j2) + c * s1 + d * i1)
    # fc = -a * j2
    # estrain1 = (-fb + np.sqrt(fb ** 2 - 4 * fa * fc)) / 2
    # estrain2 = (-fb - np.sqrt(fb ** 2 - 4 * fa * fc)) / 2
    # if a>0 :
    #	return estrain1,estrain2
    # else:
    #	return estrain2,estrain1
    fa = a * j2
    fb = b * np.sqrt(j2)
    fc = c * s1
    fd = d * i1
    BCD = fb + fc + fd
    # estrain = (s_uniaxial ** 2 - fa) / BCD
    estrain = fa / s_uniaxial + BCD
    return estrain, 0


def equiv_strain_linear(ABCD, s, s_uniaxial):
    s1 = s[0]
    s2 = s[1]
    s3 = s[2]
    a = ABCD[0]
    b = ABCD[1]
    c = ABCD[2]
    d = ABCD[3]
    i1 = np.sum(s)
    j2 = ((s1 - s2) ** 2 + (s1 - s3) ** 2 + (s2 - s3) ** 2) / 6
    fa = a * j2
    fb = b * np.sqrt(j2)
    fc = c * s1
    fd = d * i1
    BCD = fb + fc + fd
    estrain = (s_uniaxial ** 2 - fa) / BCD
    delta = BCD ^ 2 - 4 * fa
    return delta, estrain  ##,0


def equiv_strain_delta(s, s_uniaxial, pe):
    def fx(x):
        a = func_A(x)
        b = func_B(x)
        c = func_C(x)
        d = func_D(x)
        fa = a * j2
        fb = b * np.sqrt(j2)
        fc = c * s1
        fd = d * i1
        # fx1 = (x - fa / (s_uniaxial[100] ** 2) / x - (fb + fc + fd) / s_uniaxial[100])
        # fx2 = x ** 2 - (fb + fc + fd) / s_uniaxial[100] * x - fa / (s_uniaxial[100] ** 2)
        # fx3 = (x ** 2 - fa / (s_uniaxial[100] ** 2)) / ((fb + fc + fd) / s_uniaxial[100]) - x
        # fx4 = (fb + fc + fd) / s_uniaxial[100] + fa / s_uniaxial[100] ** 2 / x - fa / s_uniaxial[100] ** 2 / (x - (fb + fc + fd) / s_uniaxial[100])
        fx5 = x ** 3 - fa / (s_uniaxial[100] ** 2) * x - (fb + fc + fd) / s_uniaxial[100] * x ** 2
        return fx5

    def faix(x):
        a = func_A(x)
        b = func_B(x)
        c = func_C(x)
        d = func_D(x)
        fa = a * j2
        fb = b * np.sqrt(j2)
        fc = c * s1
        fd = d * i1
        fx1 = (fb + fc + fd) / s_uniaxial[100] * x + fa / s_uniaxial[100] ** 2
        fx2 = (fa / s_uniaxial[100] ** 2 / x + (fb + fc + fd) / s_uniaxial[100]) ** 2
        return fx1

    def dfaix(x):
        a = func_A(x)
        b = func_B(x)
        c = func_C(x)
        d = func_D(x)
        da = func_dA(x)
        db = func_dB(x)
        dc = func_dC(x)
        dd = func_dD(x)
        fa = a * j2
        fb = b * np.sqrt(j2)
        fc = c * s1
        fd = d * i1
        dfa = da * j2
        dfb = db * np.sqrt(j2)
        dfc = dc * s1
        dfd = dd * i1
        dfx1 = (fb + fc + fd) / s_uniaxial[100] + dfa / s_uniaxial[100] ** 2 + x * ((dfb + dfc + dfd) / s_uniaxial[100])
        dfx2 = 2 * (fa / s_uniaxial[100] ** 2 / x + (fb + fc + fd) / s_uniaxial[100]) * (
            -fa / s_uniaxial[100] ** 2 / x ** 2 + dfa / s_uniaxial[100] ** 2 / x + (dfb + dfc + dfd) / s_uniaxial[100])
        return dfx1

    s1 = s[0]
    s2 = s[1]
    s3 = s[2]
    i1 = np.sum(s)
    j2 = ((s1 - s2) ** 2 + (s1 - s3) ** 2 + (s2 - s3) ** 2) / 6.
    es = 0

    ##### 弦截法
    # x0 = pe / s_uniaxial[100]
    # x1 = 1.1*x0
    # for i in range(1000):
    #	fx0 = fx(x0)
    #	fx1 =fx(x1)
    #	x2 = x1-fx1/(fx1-fx0)*(x1-x0)
    #	delta = ((x2-x1)/x1)**2
    #	if delta <1e-10:
    #		es = x2*s_uniaxial[100]
    #		break
    #	else:
    #		x0 = x1
    #		x1 = x2
    ####抛物线法
    # x0 = pe / s_uniaxial[100]+0.001
    # x1 = x0 + 0.02
    # x2 = x0+0.01
    ##x2 = pe / s_uniaxial[100]+0.005
    ##if x2 == 0:
    ##	x2 = 0.005
    ###if x2>1:
    ###	x2 = max(1,x2-0.2)

    ##x0 = x2-0.0009
    ##x1 = x2+0.0009

    # es = 0
    # for i in range(200):
    #	fx0 = fx(x0)
    #	fx1 = fx(x1)
    #	fx2 = fx(x2)
    #	fx2x1 = (fx2 - fx1) / (x2 - x1)
    #	fx1x0 = (fx1 - fx0) / (x1 - x0)
    #	fx2x1x0 = (fx2x1 - fx1x0) / (x2 - x0)
    #	fa = fx2
    #	fb = fx2x1 + fx2x1x0 * (x2 - x1)
    #	fc = fx2x1x0
    #	fdelta = fb**2-4*fa*fc
    #	if fdelta<=0:
    #		x3 = max(0,-fb/(2*fa))
    #		#break
    #	else:
    #		sgn = np.sign(fb)
    #		x3 = (x2 - 2 * fx2 / (fb + sgn * np.sqrt(fdelta)))
    #	es = x3 * s_uniaxial[100]
    #	if x2 != 0:
    #		delta = ((x3-x2)/x2)**2
    #	else:
    #		delta = x3**2
    #	if delta <1e-10:
    #		break
    #	else:
    #		x0 = x1
    #		x1 = x2
    #		x2 = x3

    ##二重弦截法
    # x0 = pe / s_uniaxial[100]
    # if x0 == 0:
    #	x0 = x0 +0.001
    # x1 = x0+0.001
    # for i in range(200):
    #	fx0 = fx(x0)
    #	fx1 = fx(x1)
    #	x2 = x1-(x1-x0)*fx1/(fx1-fx0)
    #	fx2 = fx(x2)
    #	x2 = x1-(x2-x1)*fx1/(fx2-fx1)
    #	delta = ((x2-x1)/x1)**2
    #	if delta <1e-10:
    #		es = x2*s_uniaxial[100]
    #		break
    #	else:
    #		x0 = x1
    #		x1 = x2

    ##平行弦
    # if pe < s_uniaxial[100]:
    #	pe = s_uniaxial[100]
    # x0 = pe / s_uniaxial[100]
    # x1 = 1.1*x0
    # for i in range(1000):
    #	fx0 = fx(x0)
    #	fx1 = fx(x1)
    #	x2 = x1-fx1/(fx1-fx0)
    #	fx2 = fx(x2)
    #	x2 = x2-fx2/(fx1-fx0)
    #	delta = ((x2-x1)/x1)**2
    #	if delta <1e-10:
    #		es = x2*s_uniaxial[100]
    #		break
    #	else:
    #		x0 = x1
    #		x1 = x2

    ##新的两点迭代法
    # x0 = pe / s_uniaxial[100]
    # if x0<=0:
    #	x0 = 0.001
    # x1 = x0+0.01
    # for i in range(200):
    #	fx0 = fx(x0)
    #	fx1 = fx(x1)
    #	x05 = (x0+x1)/2
    #	fx05 =fx(x05)
    #	x2 = x1-(x1-x0)*fx(1)/(3*fx1-4*fx05+fx0)
    #	delta = ((x2-x1)/x1)**2
    #	if delta <1e-10:
    #		es = x2*s_uniaxial[100]
    #		break
    #	else:
    #		x0 = x1
    #		x1 = x2

    #####################解非线性风场的一个非线性迭代法
    # if pe < s_uniaxial[100]*0.1:
    #	pe = s_uniaxial[100]*0.1
    # x0 = pe / s_uniaxial[100]
    # x1 = 1.2*x0
    # for i in range(100):
    #	fx0 = fx(x0)
    #	fx1 = fx(x1)
    #	x2 = x1 -x1*fx1/(x1*(fx1-fx0)/(x1-x0)+fx1)
    #	delta = ((x2-x1)/x1)**2
    #	if delta <1e-10:
    #		es = x2*s_uniaxial[100]
    #		break
    #	else:
    #		x0 = x1
    #		x1 = x2
    #################################
    # if pe < s_uniaxial[100]*0.1:
    #	pe = s_uniaxial[100]*0.1
    # x0 = pe
    # for i in range(200):
    #	fx = faix(x0)
    #	dfx = dfaix(x0)
    #	x1 = (dfx+np.sqrt(dfx**2+4*(dfx*x0-fx)) )/2
    #	delta = ((x1-x0)/x0)**2
    #	if delta <1e-10:
    #		es = x1*s_uniaxial[100]
    #		break
    #	else:
    #		x0 = x1

    ###改进的Muller法
    x0 = pe / s_uniaxial[100] + 0.001
    x1 = x0 + 0.015
    x2 = (x1 - x0) * 0.618 + x0
    es = 0
    for i in range(200):
        fx0 = fx(x0)
        fx1 = fx(x1)
        fx2 = fx(x2)
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
        es = x3 * s_uniaxial[100]
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
    return es, 0


def equiv_strain_iter(ABCD, s, s_uniaxial):
    s1 = s[0]
    s2 = s[1]
    s3 = s[2]
    i1 = np.sum(s)
    j2 = ((s1 - s2) ** 2 + (s1 - s3) ** 2 + (s2 - s3) ** 2) / 6

    nlen = len(ABCD)
    index_0 = 0
    dABCD = np.array([np.interp(index_0, range(nlen), ABCD[:, 0]),
                      np.interp(index_0, range(nlen), ABCD[:, 1]),
                      np.interp(index_0, range(nlen), ABCD[:, 2]),
                      np.interp(index_0, range(nlen), ABCD[:, 3])])
    # dABCD = ABCD[index_0]
    ds_uniaxial = np.interp(index_0, range(nlen), s_uniaxial)
    estrain_0 = equiv_strain(dABCD, s)
    index_1 = 1
    dABCD = np.array([np.interp(index_1, range(nlen), ABCD[:, 0]),
                      np.interp(index_1, range(nlen), ABCD[:, 1]),
                      np.interp(index_1, range(nlen), ABCD[:, 2]),
                      np.interp(index_1, range(nlen), ABCD[:, 3])])
    ds_uniaxial = np.interp(index_1, range(nlen), s_uniaxial)
    estrain_1 = equiv_strain(dABCD, s)
    dindex = index_1 - index_0
    for i in range(1000):
        index_2 = index_1 - (index_1 - index_0) * (estrain_1[0] - s_uniaxial[index_1]) / (estrain_1[0] - estrain_0[0])
        dABCD = np.array([np.interp(index_2, range(nlen), ABCD[:, 0]),
                          np.interp(index_2, range(nlen), ABCD[:, 1]),
                          np.interp(index_2, range(nlen), ABCD[:, 2]),
                          np.interp(index_2, range(nlen), ABCD[:, 3])])
        ds_uniaxial = np.interp(index_2, range(nlen), s_uniaxial)
        estrain_2 = equiv_strain(dABCD, s)
        delta = np.power((estrain_2[0] - estrain_1[0]) / estrain_1[0], 2)
        if delta < 1e-30:
            break
        else:
            index_0 = index_1
            index_1 = index_2
            estrain_0 = estrain_1
            estrain_1 = estrain_2
    print("{0}".format(index_2))
    return estrain_2[0], index_2


def ABCD_curve():
    def data_init_two():
        y1.set_data([], [])
        y2.set_data([], [])
        y3.set_data([], [])
        y4.set_data([], [])
        y5.set_data([], [])
        y6.set_data([], [])
        y7.set_data([], [])
        y8.set_data([], [])
        return y1, y2, y3, y4, y5, y6, y7, y8,

    def animate_two(data):
        estrain_UT = []
        estrain_UC = []
        estrain_BC = []
        estrain_TC = []
        for i in range(200):
            s_uniaxial_tensile = np.array([UT[i], -mu * UT[i], -mu * UT[i]])
            s_uniaxial_compress = np.array([-UC[i] * mu, -UC[i] * mu, UC[i]])
            s_biaxial_compress = np.array([BC_1[i], BC_2[i], BC_3[i]])
            s_triaxial_compress = np.array([TC_1[i], TC_2[i], TC_3[i]])
            if i > 0:
                x = s_uniaxial[data] / s_uniaxial[100]
                a = func_A(x)
                b = func_B(x)
                c = func_C(x)
                d = func_D(x)
                dABCD = np.array([a, b, c, d])
                estrain_UT.append(equiv_strain(dABCD, s_uniaxial_tensile, s_uniaxial[i]))
                estrain_UC.append(equiv_strain(dABCD, s_uniaxial_compress, s_uniaxial[i]))
                estrain_BC.append(equiv_strain(dABCD, s_biaxial_compress, s_uniaxial[i]))
                estrain_TC.append(equiv_strain(dABCD, s_triaxial_compress, s_uniaxial[i]))
            else:
                estrain_UT.append([0, 0])
                estrain_UC.append([0, 0])
                estrain_BC.append([0, 0])
                estrain_TC.append([0, 0])
        x = []
        ya = []
        yb = []
        x = np.linspace(0, 199, 200)
        for s in estrain_UT:
            ya.append(s[0])
            yb.append(s[1])
        y1.set_data(x, ya)
        y2.set_data(x, yb)
        ya = []
        yb = []
        x = np.linspace(0, 199, 200)
        for s in estrain_UC:
            ya.append(s[0])
            yb.append(s[1])
        y3.set_data(x, ya)
        y4.set_data(x, yb)
        ya = []
        yb = []
        x = np.linspace(0, 199, 200)
        for s in estrain_BC:
            ya.append(s[0])
            yb.append(s[1])
        y5.set_data(x, ya)
        y6.set_data(x, yb)
        ya = []
        yb = []
        x = np.linspace(0, 199, 200)
        for s in estrain_TC:
            ya.append(s[0])
            yb.append(s[1])
        y7.set_data(x, ya)
        y8.set_data(x, yb)
        return y1, y2, y3, y4, y5, y6, y7, y8,

    UT1_curve = np.loadtxt('Mazars\\Uniaxial_T.txt')
    US1_curve = np.loadtxt('Mazars\\Uniaxial_S1.txt')
    # BS1_curve = np.loadtxt('Mazars\\Biaxial_S1.txt')
    # BS2_curve = np.loadtxt('Mazars\\Biaxial_S2.txt')
    # BS3_curve = np.loadtxt('Mazars\\Biaxial_S3.txt')
    BS1_curve = np.loadtxt('Mazars\\kupfer_S1.txt')
    BS2_curve = np.loadtxt('Mazars\\kupfer_S1.txt')
    BS3_curve = np.loadtxt('Mazars\\kupfer_S2.txt')
    TS1_curve = np.loadtxt('Mazars\\Tri_Eq1.txt')
    TS2_curve = np.loadtxt('Mazars\\Tri_Eq1.txt')
    TS3_curve = np.loadtxt('Mazars\\Tri_Eq3.txt')

    e = 2.69e10
    mu = 1.67e-1
    ft = 2.954e6

    UT = []
    UC = []
    BC_1 = []
    BC_2 = []
    BC_3 = []
    TC_1 = []
    TC_2 = []
    TC_3 = []
    ndiv = 100

    for i in range(ndiv):
        iratio = i / ndiv
        itype = 0
        iut = get_value(UT1_curve, itype, iratio)
        UT.append(iut)
        iuc = get_value(US1_curve, itype, iratio)
        UC.append(iuc)
        ibc_1 = get_value(BS1_curve, itype, iratio)
        BC_1.append(ibc_1)
        ibc_2 = get_value(BS2_curve, itype, iratio)
        BC_2.append(ibc_2)
        ibc_3 = get_value(BS3_curve, itype, iratio)
        BC_3.append(ibc_3)
        itc_1 = get_value(TS1_curve, itype, iratio)
        TC_1.append(itc_1)
        itc_2 = get_value(TS2_curve, itype, iratio)
        TC_2.append(itc_2)
        itc_3 = get_value(TS3_curve, itype, iratio)
        TC_3.append(itc_3)
    for i in range(ndiv):
        iratio = 1. - i / ndiv
        itype = 1
        iut = get_value(UT1_curve, itype, iratio)
        UT.append(iut)
        iuc = get_value(US1_curve, itype, iratio)
        UC.append(iuc)
        ibc_1 = get_value(BS1_curve, itype, iratio)
        BC_1.append(ibc_1)
        ibc_2 = get_value(BS2_curve, itype, iratio)
        BC_2.append(ibc_2)
        ibc_3 = get_value(BS3_curve, itype, iratio)
        BC_3.append(ibc_3)
        itc_1 = get_value(TS1_curve, itype, iratio)
        TC_1.append(itc_1)
        itc_2 = get_value(TS2_curve, itype, iratio)
        TC_2.append(itc_2)
        ibc_3 = get_value(TS3_curve, itype, iratio)
        TC_3.append(itc_3)

    ut_s = UT
    linear_smooth7(UT, ut_s, ndiv * 2)
    uc_s = UC
    linear_smooth7(UC, uc_s, ndiv * 2)
    bc_1s = BC_1
    linear_smooth7(BC_1, bc_1s, ndiv * 2)
    bc_2s = BC_2
    linear_smooth7(BC_2, bc_2s, ndiv * 2)
    bc_3s = BC_3
    linear_smooth7(BC_3, bc_3s, ndiv * 2)
    tc_1s = TC_1
    linear_smooth7(TC_1, tc_1s, ndiv * 2)
    tc_2s = TC_2
    linear_smooth7(TC_2, tc_2s, ndiv * 2)
    tc_3s = TC_3
    linear_smooth7(TC_3, tc_3s, ndiv * 2)

    ABCD = np.zeros((ndiv * 2, 4))
    s_uniaxial = np.zeros((ndiv * 2))

    estrain_UT = []
    estrain_UC = []
    estrain_BC = []
    estrain_TC = []

    file = open('strain.txt', 'w')
    for i in range(ndiv * 2):
        s_uniaxial_tensile = np.array([UT[i], -mu * UT[i], -mu * UT[i]])
        s_uniaxial_compress = np.array([-UC[i] * mu, -UC[i] * mu, UC[i]])
        s_biaxial_compress = np.array([BC_1[i], BC_2[i], BC_3[i]])
        s_triaxial_compress = np.array([TC_1[i], TC_2[i], TC_3[i]])
        # file_path.write('{0:10.5e},{1:10.5e},{2:10.5e},{3}\n'.format(s_uniaxial_tensile[0],s_uniaxial_tensile[1],s_uniaxial_tensile[2],i))
        # file_path.write('{0:10.5e},{1:10.5e},{2:10.5e},{3}\n'.format(s_uniaxial_compress[0],s_uniaxial_compress[1],s_uniaxial_compress[2],i))
        file.write('{0:10.5e},{1:10.5e},{2:10.5e},{3}\n'.format(s_biaxial_compress[0], s_biaxial_compress[1],
                                                                s_biaxial_compress[2], i))
        # file_path.write('{0:10.5e},{1:10.5e},{2:10.5e},{3}\n'.format(s_triaxial_compress[0],s_triaxial_compress[1],s_triaxial_compress[2],i))
        fa = np.zeros((4, 4))
        fb = np.array([1, 1, 1, 1])
        s0 = s_uniaxial_tensile[0]

        if i > 0:
            fa[0] = value_in_function(s_uniaxial_tensile, s0)
            fa[1] = value_in_function(s_uniaxial_compress, s0)
            fa[2] = value_in_function(s_biaxial_compress, s0)
            fa[3] = value_in_function(s_triaxial_compress, s0)
            # fb = theta(s_uniaxial_tensile,s0)
            # file_path.write('{0:10.5e},{1:10.5e},{2:10.5e},{3}\n'.format(fb[0],fb[1],fb[2],i))
            # fb = theta(s_uniaxial_compress,s0)
            # file_path.write('{0:10.5e},{1:10.5e},{2:10.5e},{3}\n'.format(fb[0],fb[1],fb[2],i))
            # fb = theta(s_biaxial_compress,s0)
            # file_path.write('{0:10.5e},{1:10.5e},{2:10.5e},{3}\n'.format(fb[0],fb[1],fb[2],i))
            # fb = theta(s_triaxial_compress,s0)
            # file_path.write('{0:10.5e},{1:10.5e},{2:10.5e},{3}\n'.format(fb[0],fb[1],fb[2],i))
            #
            fb = np.array([1, 1, 1, 1])
            fb = np.linalg.solve(fa, fb)

            # fb[0] = fb[0]/s0
            # fb = np.divide(fb,s0)
            ABCD[i] = fb
            s_uniaxial[i] = s0
            # file_path.write('{0},{1},{2},{3},{4}\n'.format(fb[0], fb[1], fb[2], fb[3], s0))
            # print('{0:10.5e},{1:10.5e},{2:10.5e},{3:10.5e}'.format(fa[0][0],fa[0][1],fa[0][2],fa[0][3]))
            # print('{0:10.5e},{1:10.5e},{2:10.5e},{3:10.5e}'.format(fa[1][0],fa[1][1],fa[1][2],fa[1][3]))
            # print('{0:10.5e},{1:10.5e},{2:10.5e},{3:10.5e}'.format(fa[2][0],fa[2][1],fa[2][2],fa[2][3]))
            # print('{0:10.5e},{1:10.5e},{2:10.5e},{3:10.5e}'.format(fa[3][0],fa[3][1],fa[3][2],fa[3][3]))
            # estrar_square[i] = s0*s0
            # fc = np.dot(fa,fb)

    file.close()

    ############################################################# animal
    ############################################################# ############################################
    ##def animation_plot():
    # fig = plt.figure(figsize=(16,16),dpi=80)
    # ax1 = plt.subplot(221)
    ##ax1.set_ylim([0,2e-3])
    ##ax1.set_axes(xlim=(0,200),ylim=(0,1.5e-3))
    # ax1.plot(s_uniaxial)
    # y1, = ax1.plot([],[],label='ut')
    # y2, = ax1.plot([],[],label='ut')
    # ax1.set_title('UT')
    # ax2 = plt.subplot(222)
    ##ax2.set_ylim([0,2e-3])
    # ax2.plot(s_uniaxial)
    # y3, = ax2.plot([],[],label='uc')
    # y4, = ax2.plot([],[],label='uc')
    # ax2.set_title('UC')
    # ax3 = plt.subplot(223)
    ##ax3.set_ylim([0,2e-3])
    # ax3.plot(s_uniaxial)
    # y5, = ax3.plot([],[],label='bc')
    # y6, = ax3.plot([],[],label='bc')
    # ax3.set_title('BC')
    # ax4 = plt.subplot(224)
    ##ax4.set_ylim([0,2e-3])
    # ax4.plot(s_uniaxial)
    # y7, = ax4.plot([],[],label='tc')
    # y8, = ax4.plot([],[],label='tc')
    # ax4.set_title('TC')
    # animl =	manimation.FuncAnimation(fig,animate_two,init_func=data_init_two,frames=ndiv	* 2, interval=20, blit=True)
    # plt.legend()
    # plt.rcParams['animation.ffmpeg_path'] = 'ffmpeg\\bin\\ffmpeg.exe'
    # plt.rcParams['animation.mencoder_path'] = 'mplayer\\mencoder.exe'
    # FFwriter = manimation.FFMpegWriter()
    # Menwriter = manimation.MencoderWriter()
    # metadata = dict(title='Movie Test', artist='Matplotlib',
    #				comment='Movie support!')
    ##animl.save('FixABCD_two.mp4',writer=FFwriter,metadata=metadata)
    # plt.show()
    ##animation_plot()
    ############################################################# animal
    ############################################################# ############################################

    # estrain_UT.append([0,0])
    # estrain_UC.append([0,0])
    # estrain_BC.append([0,0])
    # estrain_TC.append([0,0])
    # for i in range(ndiv * 2 - 1):
    #	s_uniaxial_tensile = np.array([UT[i + 1],-mu * UT[i + 1],-mu * UT[i + 1]])
    #	s_uniaxial_compress = np.array([-UC[i + 1] * mu,-UC[i + 1] * mu,UC[i + 1]])
    #	s_biaxial_compress = np.array([BC_1[i + 1],BC_2[i + 1],BC_3[i + 1]])
    #	s_triaxial_compress = np.array([TC_1[i + 1],TC_2[i + 1],TC_3[i + 1]])
    #	x = s_uniaxial[i] / s_uniaxial[100]
    #	a = func_A(1)
    #	b = func_B(1)
    #	c = func_C(1)
    #	d = func_D(1)
    #	dABCD = np.array([a,b,c,d])
    #	estrain_UT.append(equiv_strain(dABCD,s_uniaxial_tensile, s_uniaxial[i]))
    #	estrain_UC.append(equiv_strain(dABCD,s_uniaxial_compress, s_uniaxial[i]))
    #	estrain_BC.append(equiv_strain(dABCD,s_biaxial_compress, s_uniaxial[i]))
    #	estrain_TC.append(equiv_strain(dABCD,s_triaxial_compress, s_uniaxial[i]))

    # i = 10
    # s0 = s_uniaxial[i]
    # print("{0}".format(s0))
    # s_uniaxial_tensile = np.array([UT[i],-mu * UT[i],-mu * UT[i]])
    # s_uniaxial_compress = np.array([-UC[i] * mu,-UC[i] * mu,UC[i]])
    # s_biaxial_compress = np.array([BC_1[i],BC_2[i],BC_3[i]])
    # s_triaxial_compress = np.array([TC_1[i],TC_2[i],TC_3[i]])
    # print("{0}".format(equiv_strain_delta(s_uniaxial_tensile,
    # s_uniaxial,s_uniaxial[i-1])))
    ##estrain_UT.append(equiv_strain_delta(s_uniaxial_tensile,
    ##s_uniaxial,s_uniaxial[i-1]))
    # print("{0}".format(equiv_strain_delta(s_uniaxial_compress,
    # s_uniaxial,s_uniaxial[i-1])))
    ##estrain_UC.append(equiv_strain_delta(s_uniaxial_compress,
    ##s_uniaxial,s_uniaxial[i-1]))
    # print("{0}".format(equiv_strain_delta(s_biaxial_compress,
    # s_uniaxial,s_uniaxial[i-1])))
    ##estrain_BC.append(equiv_strain_delta(s_biaxial_compress,
    ##s_uniaxial,s_uniaxial[i-1]))
    # print("{0}".format(equiv_strain_delta(s_triaxial_compress,
    # s_uniaxial,s_uniaxial[i-1])))
    ##estrain_TC.append(equiv_strain_delta(s_triaxial_compress,
    ##s_uniaxial,s_uniaxial[i-1]))

    # estrain_UT.append([0,0])
    # estrain_UC.append([0,0])
    # estrain_BC.append([0,0])
    # estrain_TC.append([0,0])
    # for i in range(ndiv * 2):
    #	s_uniaxial_tensile = np.array([UT[i],-mu * UT[i],-mu * UT[i]])
    #	s_uniaxial_compress = np.array([-UC[i] * mu,-UC[i] * mu,UC[i]])
    #	s_biaxial_compress = np.array([BC_1[i],BC_2[i],BC_3[i]])
    #	s_triaxial_compress = np.array([TC_1[i],TC_2[i],TC_3[i]])
    #	#print("{0},{1},{2},{3}".format(s_biaxial_compress[0],s_biaxial_compress[1],s_biaxial_compress[2],i))
    #	estrain_UT.append(equiv_strain_delta(s_uniaxial_tensile,	s_uniaxial,estrain_UT[i][0]))
    #	estrain_UC.append(equiv_strain_delta(s_uniaxial_compress,	s_uniaxial,estrain_UC[i][0]))
    #	estrain_BC.append(equiv_strain_delta(s_biaxial_compress,	s_uniaxial,estrain_BC[i][0]))
    #	estrain_TC.append(equiv_strain_delta(s_triaxial_compress,	s_uniaxial,estrain_TC[i][0]))

    # with plt.xkcd():
    #	plt.figure(figsize=(8,8),dpi=80)
    #	p1 = plt.subplot(111)
    #	x = []
    #	for s in s_uniaxial:
    #		x.append(s)
    #	pa = []
    #	pb = []
    #	pc = []
    #	pd = []
    #	for dABCD in ABCD:
    #		pa.append(dABCD[0])
    #		pb.append(dABCD[1])
    #		pc.append(dABCD[2])
    #		pd.append(dABCD[3])
    #		#file_path.write('{0:10.5e},{1:10.5e},{2:10.5e},{3:10.5e}\n'.format(dABCD[0],dABCD[1],dABCD[2],dABCD[3]))
    #	plta = p1.plot(x,pa,'g',label="A",linewidth=1)
    #	pltb = p1.plot(x,pb,'r',label="B",linewidth=1)
    #	pltc = p1.plot(x,pc,'y',label="C",linewidth=1)
    #	pltd = p1.plot(x,pd,'m',label="D",linewidth=1)
    #	plt.sca(p1)
    #	plt.xlabel('istep')
    #	plt.ylabel('ABCD')
    #	#plt.axvline(100)
    #	plt.legend()
    # plt.show()
    # file_path.close()


    # with plt.xkcd():
    plt.figure(figsize=(8, 8), dpi=80)
    x = []
    y = []
    yp = []
    for ivar in UT1_curve:
        x.append(ivar[0])
        y.append(ivar[1])
    yp = y
    # linear_smooth7(y,yp,len(y))
    plt.plot(x, y, label='UT')
    # plt.plot(x,yp,label='UT_P_3')

    x = []
    y = []
    for ivar in US1_curve:
        x.append(ivar[0])
        y.append(ivar[1])
    # linear_smooth7(y,y,len(y))
    plt.plot(x, y, label='UC')

    x = []
    y = []
    for ivar in BS1_curve:
        x.append(ivar[0])
        y.append(ivar[1])
    # linear_smooth7(y,y,len(y))
    plt.plot(x, y, label='BC')

    x = []
    y = []
    for ivar in BS3_curve:
        x.append(ivar[0])
        y.append(ivar[1])
    # linear_smooth7(y,y,len(y))
    plt.plot(x, y, label='BC')

    x = []
    y = []
    for ivar in TS1_curve:
        x.append(ivar[0])
        y.append(ivar[1])
    # linear_smooth7(y,y,len(y))
    plt.plot(x, y, label='TC')

    x = []
    y = []
    for ivar in TS3_curve:
        x.append(ivar[0])
        y.append(ivar[1])
    # linear_smooth7(y,y,len(y))
    plt.plot(x, y, label='TC')

    plt.legend(loc=0)
    plt.show()

    # with plt.xkcd():
    plt.figure(figsize=(8, 8), dpi=80)
    p1 = plt.subplot(111)
    # p2 = plt.subplot(222)
    # p3 = plt.subplot(223)
    # p4 = plt.subplot(224)
    x = []
    y = []
    z = []
    for ivar in estrain_UT:
        x.append(ivar[0])
        y.append(ivar[1])
        z.append((ivar[0] + ivar[1]) / 2)
    p1.plot(x, 'b-1', label='utx')
    # p1.plot(y,label='ut')
    # plt.axvline(100)
    # plt.legend(loc=0)
    # plt.plot(z,label='z')
    x = []
    y = []
    z = []
    for ivar in estrain_UC:
        x.append(ivar[0])
        y.append(ivar[1])
        z.append((ivar[0] + ivar[1]) / 2)
    p1.plot(x, 'g-2', label='ucx')
    ##p1.plot(y,label='ucy')
    ##plt.legend(loc=0)
    x = []
    y = []
    z = []
    for ivar in estrain_BC:
        x.append(ivar[0])
        y.append(ivar[1])
        z.append((ivar[0] + ivar[1]) / 2)
    p1.plot(x, 'r-3', label='bcx')
    ##p1.plot(y,label='bcy')
    ##plt.legend(loc=0)
    x = []
    y = []
    z = []
    for ivar in estrain_TC:
        x.append(ivar[0])
        y.append(ivar[1])
        z.append((ivar[0] + ivar[1]) / 2)
    p1.plot(x, 'm-4', label='tcx')
    # p1.plot(y,label='tcy')
    # plt.plot(estrain_UT,label='estrain_UT')
    # plt.plot(estrain_UC,label='estrain_UC')
    # plt.plot(estrain_BC,label='estrain_BC')
    # plt.plot(estrain_TC,label='estrain_TC')
    plt.legend(loc=0)
    plt.show()


ABCD_curve()
print('Finish')
