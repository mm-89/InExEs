import numpy as np
import random
import trimesh as tm


class CheckPostureColor:
	"""
	Ply files are normally colored by vertices, but
	InExES simulates radiation over faces. To use
	anatomical zone and so on we needed to translate
	colors from vertices to faces. 
	"""
	
	#old, maybe useless
	def _checkPostureColor(self, file, show=True):
		"""
		This code works in this way:
		1- take a face
		2- check the colors in each vertex
		3- if the color is the same for every vertices, 
			take this color for the face
		"""

		face_vertex_index = file.faces
		colors = file.visual.vertex_colors #[:, 0:3] #opacity doesn't matter

		acc = 0

		new_colors = np.ones(shape=(len(face_vertex_index), 4))*[150, 150, 150, 255]
		for k, item in enumerate(face_vertex_index):
			if( np.array_equal(colors[item[0]], colors[item[1]])):
				if( np.array_equal(colors[item[0]], colors[item[2]])):
					new_colors[k,:] = colors[item[0]]
					acc += 1
		
		if( show ):
			my_new_mesh = tm.Trimesh(vertices=mesh.vertices, 
									faces=mesh.faces,
									process=True, 
									face_colors=new_colors)

			scene = tm.Scene([my_new_mesh])
			scene.show()
		
		print("Total number of face with 3 equal vertices: ", acc)

		return np.array( new_colors )

	#old, maybe useless
	def _checkPostureColor_andRepair1(self, file, show=True):
		"""
		This code works in this way:
		1- take a face
		2- check the colors in each vertex
		3- if the color is the same for at least 2 vertices, 
			take this color for the face
		"""


		face_vertex_index = file.faces
		colors = file.visual.vertex_colors #[:, 0:3] #opacity doesn't matter

		acc = 0

		new_colors = np.ones(shape=(len(face_vertex_index), 4))*[150, 150, 150, 255]
		for k, item in enumerate(face_vertex_index):
			if( np.array_equal(colors[item[0]], colors[item[1]])):
					new_colors[k,:] = colors[item[0]]
					acc += 1
			elif( np.array_equal(colors[item[0]], colors[item[2]])):
					new_colors[k,:] = colors[item[0]]
					acc += 1
			elif( np.array_equal(colors[item[1]], colors[item[2]])):
					new_colors[k,:] = colors[item[0]]
					acc += 1
					

				
		
		if( show ):
			my_new_mesh = tm.Trimesh(vertices=mesh.vertices, 
									faces=mesh.faces,
									process=True, 
									face_colors=new_colors)

			scene = tm.Scene([my_new_mesh])
			scene.show()
		
		print("Total number of faces with at least 2 equal vertices: ", acc)

		return np.array( new_colors )

	def _checkPostureColor_andRepair2(self):
		"""
		This code works in this way:
		1- take a face
		2- check the colors in each vertex
		3- if the color is the same for at least 2 vertices, 
			take this color for the face
		4- if all 3 colors are different, the face color
			will be taken randomly from one of these three
		"""
	

		face_vertex_index = self.my_file.faces
		colors = self.my_file.visual.vertex_colors

		acc = 0

		new_colors = np.ones(shape=(len(face_vertex_index), 4))*[150, 150, 150, 255]
		for k, item in enumerate(face_vertex_index):
			if( np.array_equal(colors[item[0]], colors[item[1]])):
					new_colors[k,:] = colors[item[0]]
					acc += 1
			elif( np.array_equal(colors[item[0]], colors[item[2]])):
					new_colors[k,:] = colors[item[0]]
					acc += 1
			elif( np.array_equal(colors[item[1]], colors[item[2]])):
					new_colors[k,:] = colors[item[0]]
					acc += 1
			else:
				#for now I just wanna to take the first
				#index in order to avoid random meshes
				#tmp_num = random.choice([0, 1, 2])
				tmp_num = 0
				new_colors[k,:] = colors[item[tmp_num]]
				acc += 1
		
		#update the posture
		self.my_file = tm.Trimesh(vertices=self.my_file.vertices, 
									faces=self.my_file.faces,
									process=True, 
									face_colors=new_colors)
		
		#if you want to export the mesh
		#? avoid check each time???
		tm.exchange.export.export_mesh(self.my_file, "postures/head_high_res/head_repaired.ply")