import posture as ps
import sun_ray_direction as srd
import output as oi

import numpy as np
import matplotlib.pyplot as plt

#files previously simulated
my_posture = "postures/head_high_res/head.ply" 
my_file = "output/data_60.txt"

#prepare to analisys
my_file_to_analyse = oi.Output(my_posture, my_file)

#if you want to show just a timestep
#my_file_to_analyse.show_one_timestep(1)

data = my_file_to_analyse.get_data_matrix


select_face_to_plot_left = [80, 81, 82, 83, 84, 85]				#left eye
select_face_to_plot_right = [166, 167, 168, 169, 170, 171]		#right eyeprope
tot_len = len(select_face_to_plot_right)

#to be sure that selected faces are correct
#my_file_to_analyse.show_selected_faces(select_face_to_plot_left)


x = [i for i in range(len(data[:, 0]))]		#total timestep of simulation

data_left = []
data_right = []

for item in x:
	data_right.append(sum(data[item, 166:171])/tot_len)
	data_left.append(sum(data[item, 80:85])/tot_len)



plt.plot(x, data_right, label="right")
plt.plot(x, data_left, label="left")
plt.legend()
plt.show()