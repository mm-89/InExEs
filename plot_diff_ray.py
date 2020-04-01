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
theta = pi/9.

#phi has to be in interval 0 - 2pi
phi =  pi/3.

my_points_new_diff, my_points_new_refl, N_dif, N_ref = mrd.make_rays_in_a_hemisphere(N, theta, phi, random=False)
#values = mrd.point_hemisphere_lebedev(N)

x_diff = []
y_diff = []
z_diff = []

x_refl = []
y_refl = []
z_refl = []


for comp in my_points_new_diff:
    x_diff.append(comp[0])
    y_diff.append(comp[1])
    z_diff.append(comp[2])

for comp in my_points_new_refl:
    x_refl.append(comp[0])
    y_refl.append(comp[1])
    z_refl.append(comp[2])

ax.scatter(x_diff, y_diff, z_diff, c='r', marker='o')
#ax.scatter(x_refl, y_refl, z_refl, c='r', marker='o')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()

