#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""Lösung der Laplace-Gleichung für ein rechteckiges Gebiet mit vorgegebenen
Randbedingungen.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from LaplaceFortran import iterate

# Größe des Rechtecks:
xLength = 10
yLength = 5

step = 0.05 # Step-Weite

# erlaubten Fehler setzen:
maxDiff = 1E-4

# Array-Größe aus Längen und Step berechnen:
xSamples = xLength/step
ySamples = yLength/step

# Array erzeugen:
V = np.zeros([ySamples, xSamples])

# Randbedingungen:
V[0,:] = 5 # V = V_0 auf dem linken Rand

# lustige Sinus- und Cosinus-RB:
V[0,:] = np.sin(2*np.pi*np.linspace(0, 1., xSamples)) # Sinus auf dem Rand
V[-1,:] = -np.sin(2*np.pi*np.linspace(0, 1., xSamples))
V[:,0] = -np.sin(2*np.pi*np.linspace(0, 1., ySamples))
V[:,-1] = +np.sin(2*np.pi*2*np.linspace(0, 1., ySamples))

# Iteration (nach Fortran ausgelagert):
V = iterate(V, maxDiff)

# Plotten:
fig = plt.figure()
ax = fig.gca(projection='3d', aspect="equal")

xValues = np.linspace(0, xLength, xSamples)
yValues = np.linspace(0, yLength, ySamples)
XX, YY = np.meshgrid(xValues, yValues)

ax.plot_surface(XX, YY, V, cmap=plt.cm.hot)
ax.set_xlabel("$x$")
ax.set_ylabel("$y$")
ax.set_zlabel("$V$")
plt.show()

plt.imshow(V)
plt.colorbar()
plt.show()
