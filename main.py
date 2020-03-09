import matplotlib.pyplot as plt
import numpy as np
import trimesh as tm

import sun_ray_direction as srd
import posture as io

my_file = "postures/body_high_res/BabyHighRes_01.ply"

output_dir = "output"
file_out = "my_test_mesh"
extension = "ply"

#define and charge a posture
posture = io.posture(my_file)

posture.repair_posture()
posture.compute_more_information()

#need more information
normals = posture.get_normals()

normals_minimized = []
for comp in normals:
	normals_minimized.append(comp/1000.)

#set the sun ray direction
sun_direction = srd.sun_ray_direction(second=43000)

#look for intersections
ray_origins = posture.get_vertices_barycenter() + normals_minimized#total len is number of face
ray_direction = [sun_direction.get_sun_direction() for i in range(len(ray_origins))]

#just to check
if not len(ray_origins)==len(ray_direction):
	print("Some problems occured")

#try to evaluate intersections
inf = posture.get_posture().ray.intersects_any(ray_origins=ray_origins, ray_directions=ray_direction)

#take only non-zero components
face_nohit = np.nonzero(~inf)[0]

print("total faces not hitten: ", face_nohit)

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


ray_visualize = tm.load_path(np.hstack((
        ray_origins[100],
        ray_origins[100] + ray_direction[100])).reshape(-1, 2, 3))

scene = tm.Scene([
        my_new_mesh,
        ray_visualize])

scene.show()
