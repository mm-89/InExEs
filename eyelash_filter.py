import shared_parameters as sp
import math_refl_diff as mrd
from progressbar import *

import math as mt
import numpy as np
import random
import trimesh as tm

import time

eyelash_col  = [255, 255, 0, 255]

eye_r = [0, 0, 255, 255]
eye_l = [255, 0, 0, 255]

pos_lash_path = "postures/eyes/head_eyes_eyelashes.ply"
pos_free_path = "postures/eyes/head_eyes.ply"

pos_lash = tm.load(pos_lash_path)
pos_free = tm.load(pos_free_path)

diam = 0.1
delX = 0.3


def compute_beta_filtered():
	"""
	beta coeff only for eyes
	"""

	path = pos_lash_path.split('/')
	mesh_name = path[-1]
	fileName = "beta_coeff/beta_{}_{}.txt".format(mesh_name.rsplit(".", -1)[0], sp.N)

	#----------------------------------------------------------------------------
	face_index_eyes_lash = [k for k, item in enumerate(pos_lash.visual.face_colors) \
					if(np.array_equal(item, eye_l) or np.array_equal(item, eye_r))]

	face_center_eyes_lash = [pos_lash.triangles_center[k] for k in face_index_eyes_lash]

	face_index_eyes_free = [k for k, item in enumerate(pos_free.visual.face_colors) \
					if(np.array_equal(item, eye_l) or np.array_equal(item, eye_r))]


	face_center_eyes_free = [pos_free.triangles_center[k] for k in face_index_eyes_free]

	face_index_lashes =  [k for k, item in enumerate(pos_lash.visual.face_colors) if np.array_equal(item, eyelash_col)]
	face_normal_eyelashes = [pos_lash.face_normals[k] for k in face_index_lashes]
	#----------------------------------------------------------------------------

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
		
		dimfaces = np.shape(pos_lash.triangles_center)[0]
		
		#[0] is diffused, [1] is reflecte
		beta = np.zeros((dimfaces,4))
		
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

		bounds_no = 2*( 3*pos_lash.bounding_sphere.volume/(4*mt.pi) )**(1/3)

		# Dot product of all hem vectors with all face normals
		dot_mat_diff = np.matmul(ray_diff_hem, pos_lash.face_normals.T) # (N, number_faces)
		dot_mat_refl = np.matmul(ray_refl_hem, pos_lash.face_normals.T) # (N, number_faces)

		# Integrate for theta >= 0, so keep only positive dot products
		dot_mat_diff[dot_mat_diff<0.] = 0.
		dot_mat_refl[dot_mat_refl<0.] = 0.

		count = 0
		
		for idx_free, idx_lash, face_free, face_lash in zip(face_index_eyes_free, 
															face_index_eyes_lash,
															face_center_eyes_free,
															face_center_eyes_lash):
			
			integer_tot_diff = 0

			progress_bar(count, len(face_index_eyes_lash))

			# translate each diff_hem of face center point
			face_N = np.ones((sp.N, 3))*face_lash
			ray_origins = face_N + ray_diff_hem*bounds_no

			#ray_origins = np.ones((sp.N, 3))*(face + file.face_normals[count]*0.004)
			
			# diffuse part of beta coefficient ----------------------------------------

			#compute the intersect first with eyelash first. In this way
			#you have a lower beta coefficient, than you can only add
			#the rays passing throught eyelashes

			res_diff = pos_lash.ray.intersects_first(ray_origins=ray_origins, 
												ray_directions=-ray_diff_hem)

			res_diff_free = pos_free.ray.intersects_first(ray_origins=ray_origins, 
												ray_directions=-ray_diff_hem)			

			visi_mask = (res_diff==idx_lash)

			visi_mask_free = (res_diff_free==idx_lash)

			#---------------------
			interef_lash_diff = 0
			for normal, face in zip(face_normal_eyelashes, face_index_lashes):

				visi_mask_lash = (res_diff==face) # not enough
				visi_tmp = (res_diff_free==face_lash)
				visi_mask_lash_face = visi_tmp ^ visi_mask_lash
				tmp_tot = 1 - diam/(delX*abs(dot_mat_diff[visi_mask_lash_face, face]))
				tmp_tot[ np.isinf(tmp_tot)] = 0.
				#add external limit
				interef_lash_diff += np.sum(tmp_tot*dot_mat_diff[visi_mask_lash_face, idx_lash])
			"""

			# indici dei raggi che colpiscono la superficie j-esima dell'occhio (1-10000)
			ind_face_hitten_lash = [k for k, item in enumerate(visi_mask_free) if item]
 
			# indice delle facce della sopracciglia colpite dai raggi della superficie j-esima dell'occhio
			#ind_lash = [res_diff[k] for k in ind_face_hitten_lash if res_diff[k] in face_index_lashes]


			for normal, face in zip(face_normal_eyelashes, face_index_lashes):
				#indici dei raggi che coliscono la "face" del sopracciglio e anche 
				#la superficie j-esima dell'occhio.

				#ind_lash = [1 - dist/(delX*np.dot(normal, ray_diff_hem[k])) for k in ind_face_hitten_lash if res_diff[k] == face]
				#np.dot(ray_diff_hem[k], pos_lash.face_normals[idx_free])*

				ind_lash = np.sum([1 for k in ind_face_hitten_lash if res_diff[k] == face])
			"""
			#---------------------

			integer_tot_diff += 2*mt.pi*np.sum(dot_mat_diff[visi_mask, idx_lash])/sp.N

			#integer_tot_diff += 2*mt.pi*interef_lash_diff/sp.N
			
			var_diff = np.sum((dot_mat_diff[visi_mask, idx_lash] - \
					  integer_tot_diff/(2*mt.pi))**2) * 2*mt.pi/sp.N

			#_, _ = check(res_diff_free, res_diff)
			

			# --------------------------------------------------------------------------
			# reflective part of beta coefficient---------------------------------------

			ray_origins = face_N + ray_refl_hem*bounds_no

			res_refl = pos_lash.ray.intersects_first(ray_origins=ray_origins, 
												ray_directions=-ray_refl_hem)

			res_refl_free = pos_free.ray.intersects_first(ray_origins=ray_origins, 
												ray_directions=-ray_diff_hem)

			visi_mask = (res_refl==idx_lash)

			integer_tot_refl = 2*mt.pi*np.sum(dot_mat_refl[visi_mask, idx_lash])/sp.N
			
			var_refl = np.sum((dot_mat_refl[visi_mask, idx_lash] - \
					  integer_tot_refl/(2*mt.pi))**2) * 2*mt.pi/sp.N
			#----------------------------------------------------------------------------



			#print diff and refl ratio
			#print diff and refl standard deviations
			beta[idx_lash] = np.array([integer_tot_diff,
								integer_tot_refl,
								var_diff**0.5,
								var_refl**0.5])	

			count += 1				
			
		print('\nBeta computing took {:.1f} seconds.'.format(time.time()-start))
		
		np.savetxt(fileName, beta, fmt="%.10f")

		
		return beta
