import matplotlib.pyplot as plt
import lightFunctions as j
import numpy as np
mc, l = j.readIntensity("white-mercury_.png", "plot-white-mercury", "Ртутная лампа", "Белый лист")
x = np.array(j.callibration(mc))
y = np.array([578, 546, 435, 491])
N = len(x)
mx = x.sum() / N
my = y.sum() / N
a2 = np.dot(x.T, x) / N
a11 = np.dot(x.T, y) / N

kk = (a11 - mx * my) / (a2 - mx ** 2)
bb = my - kk * mx
print(kk, bb)
plt.clf()
plt.scatter(x, y)
plt.show()