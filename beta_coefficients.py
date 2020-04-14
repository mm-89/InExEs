import shared_parameters as sp
import math_refl_diff as mrd

import math as mt
import numpy as np

def compute_beta(path, file, faces_normals_minimized, angles_normals):
	path = path.split('/')
	mesh_name = path[-1]
	fileName = "input/beta_" + mesh_name.rsplit(".", -1)[0] + "_" + str(sp.N) + ".txt"
	try:
		with open(fileName) as f:
			print("Beta file found")

			#upload data
			beta_coeff = np.loadtxt(fileName)

			if(len(beta_coeff)==0):
				print("File of Beta coefficient corrupeted")
				print("Total number of read lines are: ", len(beta_coeff))

			return beta_coeff

	except IOError:
		#If not we ask user for an N value, compute beta and create a beta coeff file
		print("No beta file found for this N value, a new beta file will be created please wait")

		ray_dir = []

		#[0] is diffused, [1] is reflecte
		beta = []

		for counter, comp in enumerate(faces_normals_minimized):
						
			ray_dir_diff, ray_dir_refl, N_diff, N_refl = mrd.make_rays_in_a_hemisphere(sp.N, 
																angles_normals[counter][0], 
																angles_normals[counter][1], 
																random=sp.hemispherical_random_generator)

			#necessary to cut solid angle on face horizon
			tmp_coeff_solid_angle = (1 + mt.cos(angles_normals[counter][0]))/2.

			#to avoid singularities
			if(N_diff>0):
				ray_ori_diff = [comp for i in range(N_diff)]
				res_diff = file.ray.intersects_any(ray_origins=ray_ori_diff, 
													ray_directions=ray_dir_diff)
				cpt_false_diff = np.nonzero(~res_diff)[0]

			if(N_refl>0):
				ray_ori_refl = [comp for i in range(N_refl)]
				res_refl = file.ray.intersects_any(ray_origins=ray_ori_refl, 
															ray_directions=ray_dir_refl)
				cpt_false_refl = np.nonzero(~res_refl)[0]

			if(N_diff>0 and N_refl>0):
				beta.append(np.array([len(cpt_false_diff)*tmp_coeff_solid_angle/N_diff/mt.pi, 
										len(cpt_false_refl)*(1 - tmp_coeff_solid_angle)/N_refl/mt.pi]))

			elif(N_diff==0):
				beta.append(np.array([0, len(cpt_false_refl)*(1 - tmp_coeff_solid_angle)/N_refl/mt.pi]))

			elif(N_refl==0):
				beta.append(np.array([len(cpt_false_diff)*tmp_coeff_solid_angle/N_diff/mt.pi, 0]))

			print("Computing beta ... ", 
				round(counter/len(faces_normals_minimized)*100,1), 
				" percent complete", end="\r")

		np.savetxt(fileName, beta, fmt="%.10f")
		return np.loadtxt(fileName)