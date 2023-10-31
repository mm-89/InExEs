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

	#able to visualize colors on mesh, not a Posture class though
#	def _checkPostureColor_show(self, file, show=True):

#		face_vertex_index = file.faces
#		colors = file.visual.vertex_colors #[:, 0:3] #opacity doesn't matter

#		acc = 0

#		new_colors = np.ones(shape=(len(face_vertex_index), 4))*[150, 150, 150, 255]
#		for k, item in enumerate(face_vertex_index):
#			if( np.array_equal(colors[item[0]], colors[item[1]])):
#				if( np.array_equal(colors[item[0]], colors[item[2]])):
#					new_colors[k,:] = colors[item[0]]
#					acc += 1
		
#		if( show ):
#			my_new_mesh = tm.Trimesh(vertices=mesh.vertices, 
#									faces=mesh.faces,
#									process=True, 
#									face_colors=new_colors)

#			scene = tm.Scene([my_new_mesh])
#			scene.show()
		
#		print("Total number of face with 3 equal vertices: ", acc)

#		return np.array( new_colors )

	#old, maybe useless
#	def _checkPostureColor_andRepair_alter(self):

#		face_vertex_index = self.my_file.faces
#		colors = self.my_file.visual.vertex_colors

#		acc = 0

#		new_colors = np.ones(shape=(len(face_vertex_index), 4))*[150, 150, 150, 255]
#		for k, item in enumerate(face_vertex_index):
#			if( np.array_equal(colors[item[0]], colors[item[1]])):
#					new_colors[k,:] = colors[item[0]]
#					acc += 1
#			elif( np.array_equal(colors[item[0]], colors[item[2]])):
#					new_colors[k,:] = colors[item[0]]
#					acc += 1
#			elif( np.array_equal(colors[item[1]], colors[item[2]])):
#					new_colors[k,:] = colors[item[0]]
#					acc += 1
		
#		self.my_new_mesh = tm.Trimesh(vertices=self.my_file.vertices, 
#									faces=self.my_file.faces,
#									process=True, 
#									face_colors=new_colors)


	def _checkPostureColor_andRepair(self):

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
		
		self.my_new_mesh = tm.Trimesh(vertices=self.my_file.vertices, 
									faces=self.my_file.faces,
									process=True, 
									face_colors=new_colors)



