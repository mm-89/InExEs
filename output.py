import posture as ps

import trimesh as tm
import numpy as np


class Output:
	
	def __init__(self, posture, data_file, N):
		self.posture = ps.Posture(posture, N)

		self.data = []
		with open(data_file, 'r') as f:
		    for line in f:
		        if line: #avoid blank lines
		            self.data.append(float(line.strip()))
		
		dim_x = int(len(self.posture.get_faces))
		dim_y = int(len(self.data)/dim_x)

		#the the matrix of data
		#rows are faces
		#columns are timesteps
		self.data_matrix = np.reshape(self.data, (dim_y, dim_x)) 

		print("Selected data contains: \n")
		print(dim_x, " 	total number of faces")
		print(dim_y, "	total number of timesteps")
		print("")


	@property
	def get_data_matrix(self):
		return self.data_matrix


	def show_selected_faces(self, vec_of_faces):
		data_rgb = []
		for i in range(len(self.posture.get_faces)):
			data_rgb.append([0, 0, 0])
		
		for i in vec_of_faces:
			data_rgb[i] = [255, 0, 0]

		new_mesh = tm.Trimesh(vertices=self.posture.get_vertices, 
								faces=self.posture.get_faces,
								process=True, 
								face_colors=data_rgb)	
		
		scene = tm.Scene([new_mesh])
		scene.show()



	def show_one_timestep(self, timestep):

		my_personal_data = self.data_matrix[:, timestep]
		
		max_value = max(my_personal_data)
		new_personal_data = my_personal_data/max_value

		data_rgb = []
		for item in new_personal_data:
			data_rgb.append([int(item*255), 0, 0])

		new_mesh = tm.Trimesh(vertices=self.posture.get_vertices, 
								faces=self.posture.get_faces,
								process=True, 
								face_colors=data_rgb)	
		
		scene = tm.Scene([new_mesh])
		scene.show()