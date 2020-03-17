import trimesh as tm
import math_refl_diff as mrd
import numpy as np
import time


np.set_printoptions(suppress=True) #I dunno if now it is necessary

class Posture:

	def __init__(self, my_file):
		self.my_file = tm.load(my_file)

		normals = self.my_file.face_normals
		angles_normals = []
		for comp in normals:
			angles_normals.append(mrd.polar_transform(comp))
		
		self.angles_normals = angles_normals
		self.normals_minimized = self.my_file.face_normals/1000.
		start = time.time()
		self.compute_beta(random=False)
		print(time.time() - start)

	@property
	def get_posture(self):
		return self.my_file

	@property
	def get_normals(self):
		return self.my_file.face_normals


	def get_area_faces(self):
		return self.my_file.area_faces


	def get_total_area(self):
		return self.my_file.area

	@property
	def get_normals_minimized(self):
		return self.normals_minimized


	def compute_beta(self, random=True):
    	#Try to find a beta_coefficient file
		try:
			with open('input/beta_coefficient.txt') as f:
				print(f.readlines())
				#We put the file content = to beta coeff value
				self.betaCoeff = f.readlines()
				print(self.betaCoeff)
				return
		except IOError:
			#If not we ask user for an N value, compute beta and create a beta coeff file
			print("No beta file found")
			print("You will need to define a N value, press enter for default value (default value N = 5)")
			value = input("N value : ")
			if value == '': 
				N = 5 #DEFAULT VALUE OF BETA
			else:
				N = int(value)
			print("You choose N =", N)
					
			ray_ori_all = self.my_file.triangles_center + self.normals_minimized

			ray_dir = []
			beta = []

			angles = self.angles_normals
			
			if(random):
				for counter, t in enumerate(ray_ori_all):

					ray_ori = [t for i in range(N)]
					ray_dir = mrd.make_rays_in_a_hemisphere(N, angles[counter][0],
																angles[counter][1], random=True)

					res = self.my_file.ray.intersects_any(ray_origins=ray_ori,
															ray_directions=ray_dir)
					cpt_false = np.nonzero(~res)[0]
					beta.append(len(cpt_false)/N)

					print("Computing beta ... ", 
						round(counter/len(ray_ori_all)*100,1), 
						" percent complete", end="\r")

			else:

				for counter, comp in enumerate(ray_ori_all):

					ray_ori = [comp for i in range(N)]
					ray_dir = mrd.make_rays_in_a_hemisphere(N, angles[counter][0], 
																angles[counter][1], random=False)

					res = self.my_file.ray.intersects_any(ray_origins=ray_ori, 
															ray_directions=ray_dir)
				
					cpt_false = np.nonzero(~res)[0]
					beta.append(len(cpt_false)/N)

					print("Computing beta ... ", 
						round(counter/len(ray_ori_all)*100,1), 
						" percent complete", end="\r")

			print(beta)
			with open('input/beta_coefficient.txt', 'w+') as f:
				for line in beta:
						f.write(str(line))

			self.betaCoeff = beta
			



	def get_faces(self):
		return self.my_file.faces


	def get_vertices(self):
		return self.my_file.vertices



	def get_vertices_barycenter(self):
		return self.my_file.triangles_center


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
    	


