import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator


h = np.array([20, 40, 60, 80, 100, 120])
adc = np.array([np.mean(np.loadtxt('20 mm.txt', dtype=float)), np.mean(np.loadtxt('40 mm.txt', dtype=float)),
                np.mean(np.loadtxt('60 mm.txt', dtype=float)), np.mean(np.loadtxt('80 mm.txt', dtype=float)),
                np.mean(np.loadtxt('100 mm.txt', dtype=float)), np.mean(np.loadtxt('120 mm.txt', dtype=float))])
polyfit = np.polyval(np.polyfit(adc, h, 3), adc)


fig, ax = plt.subplots(figsize=(15, 10), dpi=400)
ax.scatter(adc, h, color='midnightblue', label='h(АЦП)')
ax.plot(adc, polyfit, label='Результат фитирования')
ax.set_xlabel('АЦП, ед.', fontsize=12)
ax.set_ylabel('h, мм', fontsize=12)

ax.xaxis.set_major_locator(MultipleLocator(20))
ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_major_locator(MultipleLocator(20))
ax.yaxis.set_minor_locator(AutoMinorLocator(4))
ax.tick_params(which='major', width=1.0)
ax.tick_params(which='major', length=10)
ax.tick_params(which='minor', width=1.0)
ax.tick_params(which='minor', length=5)

ax.set_xlim(50, 140)
ax.set_ylim(0, 140)
ax.legend(fontsize=15)

ax.grid(which='major', linewidth=0.5)
ax.grid(which='minor', linewidth=0.5)
ax.set_title('Зависимость уровня воды в сосуде от значений АЦП', fontsize=15, wrap=True)
ax.text(60, 130, 'Полиномиальная зависимость - многочлен 3ей степени', fontsize=15, wrap=True)

fig.savefig('level-calibration.png')
plt.show()
