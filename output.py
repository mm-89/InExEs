import posture as ps

import trimesh as tm
import numpy as np
import csv


class Output:
	
	def __init__(self, posture, data_file, N):

		self.posture = ps.Posture(posture, N)
		self.data_file = data_file

		self.data = []
		with open(self.data_file, mode='r') as csv_file:

			#to avoid to read header
			next(csv_file)

			#charge data line numpy array STR
			self.data = np.array([i for i in csv.reader(csv_file, delimiter=",",
															 quoting=csv.QUOTE_NONNUMERIC)])

		#delete first column and transform matrix of all floating points
		self.data = np.delete(self.data, 0, 1)
		self.data = self.data.astype(np.float)

		#to review
		print("")
		print("********************")
		print("")
		print("Total vertices: \t %s" % len(self.data[0,:]))
		print("Total timesteps: \t %s" % len(self.data))
		print("")
		print("********************")
		print("")


	@property
	def get_data_matrix(self):
		return self.data


	def get_id_color(self, color_rgb):
		vec_id = []
		for k, item in enumerate(self.posture.get_faces_color):
			if(np.array_equal(item,color_rgb)): vec_id.append(k)
		return vec_id


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

		my_data = self.data[timestep]
		
		max_value = max(my_data)
		my_data_norm = my_personal_data/max_value

		data_rgb = []
		for item in my_data_norm:
			data_rgb.append([int(item*255), 0, 0])

		new_mesh = tm.Trimesh(vertices=self.posture.get_vertices, 
								faces=self.posture.get_faces,
								process=True, 
								face_colors=data_rgb)	
		
		scene = tm.Scene([new_mesh])
		scene.show()
