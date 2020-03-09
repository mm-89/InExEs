import trimesh as tm


class posture:

	def __init__(self, my_file):
		self.my_file = tm.load(my_file)


	def repair_posture(self):
		self.my_file.remove_degenerate_faces()
		self.my_file.remove_duplicate_faces()
		self.my_file.remove_infinite_values()
		self.my_file.remove_unreferenced_vertices()


	def compute_more_information(self):
		self.my_file.face_normals
		self.my_file.fix_normals


	def reset_color(self): #need to find a function of this kind
		pass
		
 
	def get_posture(self):
		return self.my_file


	def get_normals(self):
		return self.my_file.face_normals


	def get_area_faces(self):
		return self.my_file.area_faces


	def get_total_area(self):
		return self.my_file.area


	def get_faces(self):
		return self.my_file.faces


	def get_vertices(self):
		return self.my_file.vertices


	def get_vertices_barycenter(self):
		return self.my_file.triangles_center


	def show_posture(self):
		self.my_file.show()
