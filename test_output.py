import posture as ps
import sun_ray_direction as srd
import output as oi

import numpy as np
import matplotlib.pyplot as plt
import trimesh as tm

#files previously simulated and mesh
my_posture = "postures/cube.ply"
my_file = "output/data.csv"
N = 2

#prepare to analisys
my_file_to_analyse = oi.Output(my_posture, my_file, N)






#plt.plot(x, data_right, label="right")
plt.plot(x, data_left, label="left")
plt.legend()
plt.show()