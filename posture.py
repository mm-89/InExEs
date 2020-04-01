import math_refl_diff as mrd

import trimesh as tm
import numpy as np
import math as mt
import time
import sys

class Posture:

	def __init__(self, my_file, N):
		self.path = my_file
		self.my_file = tm.load(my_file)
		self.N = N

		normals = self.my_file.face_normals
		angles_normals = []
		for comp in normals:
			angles_normals.append(mrd.from_cartesian_to_polar(comp))
		
		self.angles_normals = angles_normals
		self.normals_minimized = self.my_file.face_normals/1000.
		
		self.compute_beta(random=True)
    		
    		
	def compute_beta(self, random):
			path = self.path.split('/')
			mesh_name = path[-1]
			fileName = "input/beta_" + mesh_name.rsplit(".", -1)[0] + "_" + str(self.N) + ".txt"
			try:
				with open(fileName) as f:
					print("Beta file found")

					#We put the file content = to beta coeff value
					self.betaCoeff = f.readlines()

					if(len(self.betaCoeff)==0):
						print("File of Beta coefficient corrupeted")
						print("Total number of read lines are: ", len(self.betaCoeff))
					return
			except IOError:
				#If not we ask user for an N value, compute beta and create a beta coeff file
				print("No beta file found for this N value, a new beta file will be created please wait")
						
				ray_ori_all = self.my_file.triangles_center + self.normals_minimized

				ray_dir = []

				#[0] is diffused, [1] is reflecte
				beta = []

				angles = self.angles_normals

				for counter, comp in enumerate(ray_ori_all):

					if(random):
						
						ray_dir_diff, ray_dir_refl, N_diff, N_refl = mrd.make_rays_in_a_hemisphere(self.N, 
																			angles[counter][0], 
																			angles[counter][1], random=True)

					else:

						ray_dir_diff, ray_dir_refl, N_diff, N_refl = mrd.make_rays_in_a_hemisphere(self.N, 
																			angles[counter][0], 
																			angles[counter][1], random=False)

					tmp_coeff_solid_angle = (1 + mt.cos(angles[counter][0]))/2.

					if(N_diff>0):
						ray_ori_diff = [comp for i in range(N_diff)]
						res_diff = self.my_file.ray.intersects_any(ray_origins=ray_ori_diff, 
																		ray_directions=ray_dir_diff)
						cpt_false_diff = np.nonzero(~res_diff)[0]
					else:
						cpt_false_diff = []

					if(N_refl>0):
						ray_ori_refl = [comp for i in range(N_refl)]
						res_refl = self.my_file.ray.intersects_any(ray_origins=ray_ori_refl, 
																		ray_directions=ray_dir_refl)
						cpt_false_refl = np.nonzero(~res_refl)[0]
					else:
						cpt_false_refl = []

					if(N_diff>0 and N_refl>0):
						beta.append(np.array([len(cpt_false_diff)/N_diff, 
												len(cpt_false_diff)*(1 - tmp_coeff_solid_angle)/N_refl]))
					elif(N_diff==0):
						beta.append(np.array([0, len(cpt_false_diff)*(1 - tmp_coeff_solid_angle)/N_refl]))

					elif(N_refl==0):
						beta.append(np.array([len(cpt_false_diff)*tmp_coeff_solid_angle/N_diff, 0]))

					print("Computing beta ... ", 
						round(counter/len(ray_ori_all)*100,1), 
						" percent complete", end="\r")

				np.savetxt(fileName, beta, fmt="%.10f")
				self.betaCoeff = beta
				

	def get_angles_from_normals(self):
		return self.angles_normals


	def set_normals_minimized(self, fact=0.001):
		return self.face_normals*fact


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
	def get_beta(self):
		return self.betaCoeff


	@property
	def get_faces(self):
		return self.my_file.faces
	
	
	@property
	def get_vertices(self):
		return self.my_file.vertices


	@property
	def get_vertices_barycenter(self):
		return self.my_file.triangles_center

