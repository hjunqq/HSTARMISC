import numpy as np
from matplotlib import pyplot as plt

for i in range(0, MAXSTEP):
    stressx = stressx + STEPSIZE
    stressy = -STEPSIZE
    for j in range(0, MAXSTEP):
        stressy = stressy + STEPSIZE
        stressz = -STEPSIZE
        for k in range(0, MAXSTEP):
            stressz = stressz + STEPSIZE
            tI1 = calcI1(stressx, stressy, stressz)
            tJ2 = calcJ2(stressx, stressy, stressz)
            tyieldf = calcF(tI1, ycon)
            tsqrtJ2 = np.sqrt(tJ2)
            tdiff = abs(tsqrtJ2 - tyieldf)
            if tdiff < TOL:
                sigx[count] = stressx
                sigy[count] = stressy
                sigz[count] = stressy
                I1[count] = tI1
                sqrtJ2[count] = tsqrtJ2
                diff[count] = tdiff
                count = count + 1

X = np.outer(sigx[0:count], sigx[0:count])
Y = np.outer(sigy[0:count], sigy[0:count])
Z = np.outer(sigz[0:count], sigz[0:count])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
main()
