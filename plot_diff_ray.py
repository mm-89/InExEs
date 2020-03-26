import math_refl_diff as mrd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import *
import random

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


N = 1000

#theta has to be in interval 0 - pi
theta = pi/2.

#phi has to be in interval 0 - 2pi
phi =  0.

values = mrd.make_rays_in_a_hemisphere(N, theta, phi, random=False)
#values = mrd.point_hemisphere_lebedev(N)

x = []
y = []
z = []
res = []

for comp in values:
    x.append(comp[0])
    y.append(comp[1])
    z.append(comp[2])

ax.scatter(x, y, z, c='r', marker='o')


ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()

