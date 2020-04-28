import shared_parameters as sp
import math_refl_diff as mrd

import math as mt
import numpy as np
import random

def compute_beta(path, file, face_normals, faces_normals_minimized):
	"""
	Generate beta coefficient (see
	guidelines) for a specific posture.

	Parameters:
	------------
	path :   str
		name of the posture
		in order to save the 
		right referement

	file :   str
		posture previously 
		charged using posture
		class

	faces_normals : (N, 3) float
		cartesian coordinates [x, y, z] of N
		triangles normals of the posture 
	
	faces_normals_minimized : (N, 3) float
		cartesian coordinates [x, y, z] of N
		triangles normals of the posture 
		previously normalized

	Returns:
	-----------
	beta_coeff : (N, 2) float
		beta coefficient for each
		face of the posture. First
		component is the diffused one,
		second is the reflected one.
	"""
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

		#[0] is diffused, [1] is reflecte
		beta = []

		# transform face normal vectors from cartesian to polar
		angles_normals = [mrd.from_cartesian_to_polar(item) for item in face_normals]

		for counter, comp in enumerate(faces_normals_minimized):
						
			ray_dir_diff, ray_dir_refl, \
			N_diff, N_refl = mrd.make_rays_in_a_hemisphere(angles_normals[counter][0], 
															angles_normals[counter][1], 
																)

			frac_solid_angle_diff = solid_angle_factor(angles_normals[counter][0])
			frac_solid_angle_refl = 1 - frac_solid_angle_diff

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
				beta.append(np.array([len(cpt_false_diff)*frac_solid_angle_diff/N_diff/mt.pi, 
										len(cpt_false_refl)*frac_solid_angle_refl/N_refl/mt.pi]))

			elif(N_diff==0):
				beta.append(np.array([0, len(cpt_false_refl)*frac_solid_angle_refl/N_refl/mt.pi]))

			elif(N_refl==0):
				beta.append(np.array([len(cpt_false_diff)*frac_solid_angle_diff/N_diff/mt.pi, 0]))

			print("Computing beta ... ", 
				round(counter/len(faces_normals_minimized)*100,1), 
				" percent complete", end="\r")

		np.savetxt(fileName, beta, fmt="%.10f")
		return np.loadtxt(fileName)

	return np.array(res), res_theta


def solid_angle_factor(angle):
	"""
	Fraction of upper hemisphere
	visible from a surface
	of normal inclined of an
	angle "angle" compare 
	to the horizon.

	Parameters:
	------------
	angle : (, 1)   float
		angle between the zenith
		vector (horizon) and the 
		normal of current plane

	Returns:
	-----------
	factor : (, 1)   float
		fraction of visible
		hemisphere from 0 
		to 1
	"""
	factor = (1 + mt.cos(angle))/2
	return factor