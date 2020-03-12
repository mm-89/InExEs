import matplotlib.pyplot as plt
import numpy as np
import trimesh as tm

import sun_ray_direction as srd
import posture as ps
import math_refl_diff as mrd

import time

#PARAMETER ----------------------------------
my_file = "postures/head_high_res/head.ply"

output_dir = "output"
file_out = "my_test_mesh"
extension = "ply"
#--------------------------------------------

#POSTURES SETUP ----------------------------------
#define and charge a posture
posture = ps.posture(my_file)

#need normals
normals = posture.get_normals()

#minimized them to avoid extra intersections
normals_minimized = posture.get_normals_min()
#--------------------------------------------

#SUNRAYS SETUP ----------------------------------
#set the sun ray direction (one step for now)
sun_ray = srd.sun_ray_direction(second=400)
sun_direction = sun_ray.get_sun_direction()
#--------------------------------------------


#SHADOW MAPPING ----------------------------------
#look for intersections
ray_origins = posture.get_vertices_barycenter() + normals_minimized
ray_direction = [sun_direction for i in range(len(ray_origins))]

#just to check
if not len(ray_origins)==len(ray_direction):
	print("Some problems occured")

#try to evaluate intersections
inf = posture.get_posture().ray.intersects_any(ray_origins=ray_origins, ray_directions=ray_direction)

#take only non-zero components (non-zero=not hit)
face_nohit = np.nonzero(~inf)[0]

#to highlithg illuminated comparet to in shadow faces
black_col = [0, 0, 0]
white_col = [255, 255, 255]

col_ver = []
for comp in inf:
	if not comp:
		col_ver.append(white_col)
	else:
		col_ver.append(black_col)

if(len(col_ver)==len(posture.get_faces())):
	print("Program is working")

#try to re-write a mesh
my_new_mesh = tm.Trimesh(vertices=posture.get_vertices(), faces=posture.get_faces(), \
				process=True, face_colors=col_ver)

#to export a mesh - it works
tm.exchange.export.export_mesh(my_new_mesh, file_out + "." + extension)
#--------------------------------------------

#BETA COEFICIENT ----------------------------------
#try to compute beta coefficient
start = time.time()
posture.compute_beta(N=5)
print(time.time() - start)
#--------------------------------------------


#DISPLAY 3D VISUALISATION ----------------------------------
"""
#visualize current mesh
ray_visualize = tm.load_path(np.hstack((
        ray_origins[100],
        ray_origins[100] + ray_direction[100])).reshape(-1, 2, 3))

scene = tm.Scene([
        my_new_mesh,
        ray_visualize])

scene.show()
"""