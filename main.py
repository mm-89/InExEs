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
posture = ps.Posture(my_file)

#SUNRAYS SETUP ----------------------------------
#set the sun ray direction (one step for now)
sun_ray = srd.Sun_ray_direction()
sun_direction = sun_ray.get_sun_direction(day=1, second=43200)
#--------------------------------------------


#SHADOW MAPPING ----------------------------------
#look for intersections
ray_origins = posture.get_vertices_barycenter + posture.normals_minimized
#ray_direction = [sun_direction for i in range(len(ray_origins))]

#just to check
#if not len(ray_origins)==len(ray_direction):
#	print("Some problems occured")

#new_origins = []
#for comp in ray_origins:
#	if(np.dot(comp, sun_direction) > 0 and np.dot(comp, sun_direction) <= 1):
#		new_origins.append(comp)

#print("old lenght: ", len(ray_origins), " new lenght: ", len(new_origins))

ray_direction = [sun_direction for i in range(len(ray_origins))]

#OLD VERSION
#try to evaluate intersections 
#inf = posture.get_posture.ray.intersects_any(ray_origins=ray_origins, ray_directions=ray_direction)

#print("old lenght: ", len(new_origins), " new lenght: ", len(ray_direction))

#NEW VERSION
inf = posture.get_posture.ray.intersects_any(ray_origins=ray_origins, ray_directions=ray_direction)

#take only non-zero components (non-zero=not hit)
face_nohit = np.nonzero(~inf)[0]



#try to re-write a mesh
my_new_mesh = tm.Trimesh(vertices=posture.get_vertices, 
						faces=posture.get_faces, 
						process=True, 
						#face_colors=col_ver
						)

#IMPORTANT TO IMPLEMENTATE
#to export a mesh - it works
#tm.exchange.export.export_mesh(my_new_mesh, file_out + "." + extension)
#--------------------------------------------