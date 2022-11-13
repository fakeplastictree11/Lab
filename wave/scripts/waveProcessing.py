import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator


def drop_point(adc):
    for i in range(len(adc)):
        if abs(adc[i] - adc[0]) >= 5:
            return i


h = np.array([20, 40, 60, 80, 100, 120])  #Калибровочные массивы
adc = np.array([np.mean(np.loadtxt('20 mm.txt', dtype=float)), np.mean(np.loadtxt('40 mm.txt', dtype=float)),
                np.mean(np.loadtxt('60 mm.txt', dtype=float)), np.mean(np.loadtxt('80 mm.txt', dtype=float)),
                np.mean(np.loadtxt('80 mm.txt', dtype=float)), np.mean(np.loadtxt('120 mm.txt', dtype=float))])

adc1 = np.loadtxt('wave40mm.txt', dtype=int)  #Массивы значений АЦП и времени для каждого из трёх уровней жидкости
adc2 = np.loadtxt('wave80mm.txt', dtype=int)
adc3 = np.loadtxt('wave120mm.txt', dtype=int)

L = 1.451  #Длина кювета в метрах
duration1 = 15.03  #Длительности эксперимента
duration2 = 15.02
duration3 = 15.01
t1 = np.arange(duration1/adc1.size, duration1 + 0.001, duration1/adc1.size)  #Массивы времени
t2 = np.arange(duration2/adc2.size, duration2 + 0.001, duration2/adc2.size)
t3 = np.arange(duration3/adc3.size, duration3 + 0.001, duration3/adc3.size)

h1 = np.polyval(np.polyfit(adc, h, 3), adc1)  #Перевод значений АЦП в уровень жидкости (мм)
h2 = np.polyval(np.polyfit(adc, h, 3), adc2)
h3 = np.polyval(np.polyfit(adc, h, 3), adc3)

T1 = duration1/adc1.size * (drop_point(adc1) + 1)  #Примерные моменты времени, в которые волна достигла датчика
T2 = duration2/adc2.size * (drop_point(adc2) + 1)
T3 = duration3/adc3.size * (drop_point(adc3) + 1)
print(T1, T2, T3)

u1 = L / T1  #Скорости распространения волн
u2 = L / T2
u3 = L / T3
print(u1, u2, u3)

log_u = np.array([math.log10(u1), math.log10(u2), math.log10(u3)])
log_h = np.array([math.log10(h1[0] * 0.001), math.log10(h2[0] * 0.001), math.log10(h3[0] * 0.001)])
sigma_k = 1 / (len(log_h) ** 0.5) * ((np.mean(log_u ** 2) - np.mean(log_u) ** 2) / (np.mean(log_h ** 2) - np.mean(log_h) ** 2) - np.polyfit(log_h, log_u, 1)[0] ** 2) ** 0.5  #Погрешности коэффициента наклона и свободного члена
sigma_b = sigma_k * (np.mean(log_h ** 2) - np.mean(log_h) ** 2) ** 0.5
print(sigma_k, sigma_b)

fig, ax = plt.subplots(1, 2, figsize=(15, 10), dpi=400)  #Построение графиков
ax[0].plot(t1, h1, color='b', label='h1(t), h1 = 40 мм')
ax[0].plot(t2, h2, color='g', label='h2(t), h2 = 80 мм')
ax[0].plot(t3, h3, color='r', label='h3(t), h3 = 120 мм')
ax[0].set_xlabel('t, с', fontsize=12)
ax[0].set_ylabel('h, мм', fontsize=12)
ax[1].scatter(log_h, log_u, color='midnightblue', label='log(u)(log(h))')
ax[1].plot(log_h, np.polyval(np.polyfit(log_h, log_u, 1), log_h), label='Результат фитирования')
ax[1].set_xlabel('log(h)', fontsize=12)
ax[1].set_ylabel('log(u)', fontsize=12)

ax[0].xaxis.set_major_locator(MultipleLocator(2))
ax[0].xaxis.set_minor_locator(AutoMinorLocator(4))
ax[0].yaxis.set_major_locator(MultipleLocator(20))
ax[0].yaxis.set_minor_locator(AutoMinorLocator(4))
ax[0].tick_params(which='major', width=1.0)
ax[0].tick_params(which='major', length=10)
ax[0].tick_params(which='minor', width=1.0)
ax[0].tick_params(which='minor', length=5)
ax[0].set_xlim(0, 16)
ax[0].set_ylim(0, 120)

ax[0].legend(fontsize=15)
ax[1].legend(fontsize=15)

ax[0].grid(which='major', linewidth=0.5)
ax[0].grid(which='minor', linewidth=0.5)
ax[0].set_title('Зависимость уровня воды в сосуде от времени', fontsize=15, wrap=True)
ax[1].grid(linewidth=0.5)
ax[1].set_title('Зависимость логарифма скорости распространения волны от логарифма начальной глубины жидкости в сосуде', fontsize=15, wrap=True)
ax[0].text(9.5, 100, 'u1 = {:.3f} м/с'.format(u1), fontsize=15, wrap=True)
ax[0].text(9.5, 95, 'u2 = {:.3f} м/с'.format(u2), fontsize=15, wrap=True)
ax[0].text(9.5, 90, 'u3 = {:.3f} м/с'.format(u3), fontsize=15, wrap=True)
ax[1].text(-1.41, 0.075, 'k = {:.3f}%c{:.3f}'.format(np.polyfit(log_h, log_u, 1)[0], sigma_k) % 177, fontsize=15, wrap=True)
ax[1].text(-1.41, 0.06, 'b = {:.3f}%c{:.3f}'.format(np.polyfit(log_h, log_u, 1)[1], sigma_b) % 177, fontsize=15, wrap=True)

fig.savefig('velocity.png')
plt.show()
