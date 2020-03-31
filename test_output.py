import posture as ps
import sun_ray_direction as srd
import output as oi

import numpy as np
import matplotlib.pyplot as plt
import trimesh as tm

#files previously simulated
N = 2
my_posture = "male_eyesballs_reduced_faces_color.ply"
my_file = "output/data_new_face_PAPER.txt"

#prepare to analisys
my_file_to_analyse = oi.Output(my_posture, my_file, N)

mesh = tm.load(my_posture)

k = 0
num = []
for j, item in enumerate(mesh.visual.face_colors):
		if(item[0]==255):
			num.append(j)
			k += 1

print("tot: ", k)


#if you want to show just a timestep
#my_file_to_analyse.show_one_timestep(1)

data = my_file_to_analyse.get_data_matrix


#select_face_to_plot_left = [80, 81, 82, 83, 84, 85]				#left eye
#select_face_to_plot_right = [166, 167, 168, 169, 170, 171]		#right eyeprope


#to be sure that selected faces are correct
#my_file_to_analyse.show_selected_faces(select_face_to_plot_left)

select_face_to_plot_left = []
for i in num:
	select_face_to_plot_left.append(mesh.visual.face_colors[i])

tot_len = len(select_face_to_plot_left)

my_data = [i for i in range(479, 1044)]

x = [i for i in range(len(data[:, 0]))]		#total timestep of simulation

data_left = []
#data_right = []

print(data)

for item in x:
	data_left.append(sum(data[item, 479:1044])/tot_len)




#plt.plot(x, data_right, label="right")
plt.plot(x, data_left, label="left")
plt.legend()
plt.show()