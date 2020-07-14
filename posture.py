import beta_coefficients as bc
import math_refl_diff as mrd
import shared_parameters as sp

import trimesh as tm
import sys
import numpy as np

class Posture:

	def __init__(self, my_file):
		self.path = my_file
		self.my_file = tm.load(my_file, 
                                use_embree=sp.py_embree,
                                process=sp.process,
                                validate=sp.validate)


		if(True):
			self.beta_coeff = bc.compute_beta(self.path,
											self.my_file,
											self.my_file.face_normals,
											self.my_file.triangles_center)
		else:
			self.beta_coeff = bc.compute_beta(self.path,
											self.my_file,
											self.my_file.vertex_normals,
											self.vertices_normals_minimized)
			

	def get_angles_from_normals(self):
		return self.angles_normals


	def show_posture(self):
		self.my_file.show()


	def plyTests(self):
		self.my_file.remove_degenerate_faces()
		self.my_file.remove_duplicate_faces()
		self.my_file.remove_infinite_values()
		self.my_file.remove_unreferenced_vertices()
		v = self.my_file.is_volume
		w = self.my_file.is_winding_consistent
		wa = self.my_file.is_watertight
		if(not v) or (not w) or (not wa):
			self.my_file.fill_holes()
			if(not v) or (not w) or (not wa):
				print("Mesh is corrupted")
				sys.exit()
				
				
	@property
	def get_posture(self):
		return self.my_file


	@property
	def get_normals(self):
		return self.my_file.face_normals


	@property
	def get_area_faces(self):
		return self.my_file.area_faces


	@property
	def get_total_area(self):
		return self.my_file.area


	@property
	def get_normals_minimized(self):
    		return self.normals_minimized


	@property
	def get_vertices_normals_minimized(self):
		return self.vertices_normals_minimized


	@property
	def get_beta(self):
		return self.beta_coeff


	@property
	def get_faces(self):
		return self.my_file.faces
	
	
	@property
	def get_vertices(self):
		return self.my_file.vertices


	@property
	def get_triangles_center(self):
		return self.my_file.triangles_center


	@property
	def get_faces_color(self):
		return self.my_file.visual.face_colors


	@property
	def get_vertices_color(self):
		return self.my_file.visual.vertex_colors


	@property
	def get_vertex_faces(self):
		return self.my_file.vertex_faces


	@property
	def get_vertex_normals(self):
		return self.my_file.vertex_normals

	
	@property
	def get_max_bounds(self):
		return np.linalg.norm(self.my_file.bounds[1])
	
