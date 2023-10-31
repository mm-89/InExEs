import math_refl_diff as mrd
from progressbar import *

import math as mt
import numpy as np
import random

import time

def compute_beta(path, file):
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
	_N = int(1e16)
	path = path.split('/')
	mesh_name = path[-1]
	fileName = "beta_coeff/beta_{}_{}.txt".format(mesh_name.rsplit(".", -1)[0], _N)

	try:
		with open(fileName) as f:
			print("Beta file found")

			#upload data
			beta_coeff = np.loadtxt(fileName)

			if(len(beta_coeff)==0):
				print("File of Beta coefficient corrupeted")
				print("Total number of read lines are: {}".format(np.shape(beta_coeff)[0]))

			return beta_coeff

	except IOError:
		#If not we ask user for an N value, compute beta and create a beta coeff file
		print("No beta file found for this N value, a new beta file will be created please wait")
		start = time.time()
		
		dimfaces = np.shape(file.triangles_center)[0]
		
		#[0] is diffused, [1] is reflecte
		beta = np.zeros((dimfaces,4))
		

		# N rays on upper hemisphere
		ray_diff_hem = mrd.uniform_points_hemisphere(_N, True)
		# N rays on lower hemisphere
		ray_refl_hem = mrd.uniform_points_hemisphere(_N, False)

		bounds_no = 2*( 3*file.bounding_sphere.volume/(4*mt.pi) )**(1/3)

		# Dot product of all hem vectors with all face normals
		dot_mat_diff = np.matmul(ray_diff_hem, file.face_normals.T) # (N, number_faces)
		dot_mat_refl = np.matmul(ray_refl_hem, file.face_normals.T) # (N, number_faces)

		# Integrate for theta >= 0, so keep only positive dot products
		dot_mat_diff[dot_mat_diff<0.] = 0.
		dot_mat_refl[dot_mat_refl<0.] = 0.
		
		for count, face in enumerate(file.triangles_center):

			progress_bar(count, np.shape(file.triangles_center)[0])

			# translate each diff_hem of face center point
			face_N = np.ones((_N, 3))*face
			ray_origins = face_N + ray_diff_hem*bounds_no
			
			# diffuse part of beta coefficient ----------------------------------------
			res_diff = file.ray.intersects_first(ray_origins=ray_origins, 
												ray_directions=-ray_diff_hem)
			visi_mask = (res_diff==count)

			integer_tot_diff = 2*mt.pi*np.sum(dot_mat_diff[visi_mask, count])/_N
			
			var_diff = np.sum((dot_mat_diff[visi_mask, count] - \
					  integer_tot_diff/(2*mt.pi))**2) * 2*mt.pi/_N
			

			# --------------------------------------------------------------------------
			# reflective part of beta coefficient---------------------------------------

			ray_origins = face_N + ray_refl_hem*bounds_no

			res_refl = file.ray.intersects_first(ray_origins=ray_origins, 
												ray_directions=-ray_refl_hem)

			visi_mask = (res_refl==count)

			integer_tot_refl = 2*mt.pi*np.sum(dot_mat_refl[visi_mask, count])/_N
			
			var_refl = np.sum((dot_mat_refl[visi_mask, count] - \
					  integer_tot_refl/(2*mt.pi))**2) * 2*mt.pi/_N
			#----------------------------------------------------------------------------

			#print diff and refl ratio
			#print diff and refl standard deviations
			beta[count] = np.array([integer_tot_diff,
								integer_tot_refl,
								var_diff**0.5,
								var_refl**0.5])
			
		print('\nBeta computing took {:.1f} seconds.'.format(time.time()-start))
		
		np.savetxt(fileName, beta, fmt="%.10f")

		
		return beta
