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

		# N rays on upper hemisphere
		ray_diff_hem, theta = mrd.random_points_hemisphere(sp.N)

		# N rays on lower hemisphere
		ray_refl_hem = [-i for i in ray_diff_hem]

		for counter, item in enumerate(faces_normals_minimized):

			# set current ray origin lenght to N
			ray_origin = [item for i in range(sp.N)]

			# compute beta for diffuse part
			# check the intersecptions
			res_diff = file.ray.intersects_any(ray_origins=ray_origin, 
												ray_directions=ray_diff_hem)
			
			integer_count_diff = 0
			for j, i in enumerate(res_diff):
				if not i:
					integer_count_diff += theta[j]
			
			integer_tot_diff = 2*mt.pi*integer_count_diff/sp.N

			# compute beta for reflect part
			# check the intersecptions
			res_refl = file.ray.intersects_any(ray_origins=ray_origin, 
												ray_directions=ray_refl_hem)
			
			integer_count_refl = 0
			for j, i in enumerate(res_refl):
				if not i:
					integer_count_refl += theta[j]
								
			integer_tot_refl = 2*mt.pi*integer_count_refl/sp.N


			beta.append(np.array([integer_tot_diff, integer_tot_refl]))


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