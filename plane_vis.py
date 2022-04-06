import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt


fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

# x = [1, 0, 3]
#
# y = [0, 5, 5]
#
# z = [1, 3, 4]

x = [311.64066856671445, 296.5399931572099, 299.4603390340668]
y = [-186.29371211432286, -194.52231849334018, -182.26346300125607]
z = [36.277517712859435, 35.82613085381476, 34.41723732924254]


vertices = [list(zip(x,y,z))]

poly = Poly3DCollection(vertices, alpha=0.8, edgecolors='red', facecolors='green')

ax.add_collection3d(poly)

ax.set_xlim(280, 320)

ax.set_ylim(-200, -150)

ax.set_zlim(30,40)

plt.show()