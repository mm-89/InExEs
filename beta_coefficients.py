import shared_parameters as sp
import math_refl_diff as mrd

import math as mt
import numpy as np
import random

import time 

def compute_beta(path, file, face_normals, face_centers):
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
		if(sp.random_points):
			# N rays on upper hemisphere
			ray_diff_hem = mrd.random_points_hemisphere(sp.N, True)
			# N rays on lower hemisphere
			ray_refl_hem = mrd.random_points_hemisphere(sp.N, False)
		else:
			# N rays on upper hemisphere
			ray_diff_hem = mrd.uniform_points_hemisphere(sp.N, True)
			# N rays on lower hemisphere
			ray_refl_hem = mrd.uniform_points_hemisphere(sp.N, False)
		#in this case fnm is triangle centres

		bounds_no = float(np.linalg.norm(file.bounds[1]))
		tf_no = sp.translation_factor

		for count, item in enumerate(face_centers):

			# translate each diff_hem of face center point
			curr_tr_centre = [item for i in range(sp.N)]

			# diffuse part of beta coefficient ----------------------------------------
			ray_origins = [i + j*bounds_no*tf_no for i, j in zip(curr_tr_centre, np.array(ray_diff_hem))]
			ray_direction_diff_in = [-item for item in np.array(ray_diff_hem)]

			res_diff = file.ray.intersects_first(ray_origins=ray_origins, 
												ray_directions=ray_direction_diff_in)


			# parameter i: index of the first hitten
			# parameter j: boolean
			tmp_acc_comp = [k for k, i in enumerate(res_diff) if i == count]
			integer_count_diff = [np.dot(face_normals[count], ray_diff_hem[x]) for x in tmp_acc_comp]

			integer_tot_diff = 2*mt.pi*sum(integer_count_diff)/sp.N
			var_diff = 2*mt.pi*sum([ (x - integer_tot_diff/(2*mt.pi))**2 for x in  integer_count_diff])/sp.N

			# --------------------------------------------------------------------------
			# reflective part of beta coefficient---------------------------------------

			ray_origins = [i + j*bounds_no*tf_no for i, j in zip(curr_tr_centre, np.array(ray_refl_hem))]
			ray_direction_refl_in = [-item for item in np.array(ray_refl_hem)]

			res_refl = file.ray.intersects_first(ray_origins=ray_origins, 
												ray_directions=ray_direction_refl_in)

			# parameter i: index of the first hitten
			# parameter j: boolean
			tmp_acc_comp = [k for k, i in enumerate(res_refl) if i == count]
			integer_count_refl = [np.dot(face_normals[count], ray_refl_hem[x]) for x in tmp_acc_comp]

			integer_tot_refl = 2*mt.pi*sum(integer_count_refl)/sp.N
			var_refl = 2*mt.pi*sum([ (x - integer_tot_refl/(2*mt.pi))**2 for x in  integer_count_refl])/sp.N

			#----------------------------------------------------------------------------

			#print diff and refl ratio
			#print diff and refl standard deviations
			beta.append(np.array([integer_tot_diff,
								integer_tot_refl,
								var_diff**0.5,
								var_refl**0.5]))
			
			print("Computing beta ... ", 
				round(count/len(face_normals)*100,1), 
				" percent complete", end="\r")
			
		np.savetxt(fileName, beta, fmt="%.10f")
	return np.loadtxt(fileName)

def test_my(vector_component, current_face, count_acc):
	if vector_component == current_face:
		return count_acc
	count_acc += 1
