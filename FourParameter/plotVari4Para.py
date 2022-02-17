import matplotlib.pylab as plt
import numpy as np

with plt.xkcd():
    fig = plt.figure()
    ax = fig.add_axes((0.1, 0.2, 0.8, 0.7))
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.xticks([])
    plt.yticks([])
    ax.set_ylim([0, 1.2])
    ax.set_xlim([0, 6])
    data_x = np.linspace(0, 6, 100)
    data_y = np.zeros(100)
    a = 2.0
    for i in range(100):
        i_x = data_x[i]
        if i_x < 1:
            data_y[i] = a * i_x + (3 - 2 * a) * i_x ** 2 + (a - 2) * i_x ** 3
        else:
            data_y[i] = i_x / (a * (i_x - 1) ** 2 + i_x)

    plt.plot(data_x, data_y, 'g')
    plt.xlabel('strain')
    plt.ylabel('stress')
    plt.annotate(
        r'$f_t,E$ Peak Value',
        xy=(1, 1), arrowprops=dict(arrowstyle='->'), xytext=(0.5, 1.2))

    x = data_x[30]
    y = data_y[30]
    newE_x = np.array([0, x])
    newE_y = np.array([0, y])
    plt.plot(newE_x, newE_y, 'r-.')
    plt.annotate(
        "Damage\n" + r'$f_t^*=E^*\varepsilon^*$',
        xy=(x, y), arrowprops=dict(arrowstyle='->'), xytext=(x + 0.5, y))
    plt.annotate(
        r'$E^*=(1-d)^2E$', xy=(x, y),
        xytext=(0.9, 0.25))

plt.show()
# plt.savefig('Vari4Par.png')
