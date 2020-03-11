import trimesh as tm
import math_refl_diff as mrd
import numpy as np #not necessary

class posture:

	def __init__(self, my_file):
		self.my_file = tm.load(my_file)

		self.my_file.remove_degenerate_faces()
		self.my_file.remove_duplicate_faces()
		self.my_file.remove_infinite_values()
		self.my_file.remove_unreferenced_vertices()

		normals = self.my_file.face_normals
		new_normals = []
		for comp in normals:
			new_normals.append(mrd.polar_transform(comp))
		
		self.new_normals = new_normals

 
	def get_posture(self):
		return self.my_file


	def get_normals(self):
		return self.my_file.face_normals


	def get_area_faces(self):
		return self.my_file.area_faces


	def get_total_area(self):
		return self.my_file.area


	def get_normals_min(self, fact=1000.):
		normals_minimized = []
		fact = float(fact)
		for comp in self.my_file.face_normals:
			normals_minimized.append(comp/fact)
		return normals_minimized


	def compute_beta(self, N=20):
		ray_ori_all = self.my_file.triangles_center + \
 		self.my_file.face_normals/1000.

		ray_dir = []

		j = 0
		beta = []

		for t in ray_ori_all:

			ray_ori = []
			for i in range(N*(N - 1)):

				ray_ori.append(t)
				ray_ori=[t for i in range(N*(N - 1))]
				ray_dir =mrd.compute_diff_radiation(N, self.new_normals[j][0], \
													self.new_normals[j][1])

				res = self.my_file.ray.intersects_any(ray_origins=ray_ori, \
															ray_directions=ray_dir)

			cpt_false = len(np.nonzero(~res)[0])
			beta.append(cpt_false/(N*(N - 1)))
			print(j)
			j += 1
		return beta


	def get_faces(self):
		return self.my_file.faces


	def get_vertices(self):
		return self.my_file.vertices



	def get_vertices_barycenter(self):
		return self.my_file.triangles_center


	def get_angles_from_normals(self):
		return self.new_normals


	def show_posture(self):
		self.my_file.show()