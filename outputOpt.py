import numpy as np

import os

import sys

try:

	sys.path.insert(1, 'head_models')

	import eye_param

except:
	print("No head_models folder found!")


class OutputOpt:
	"""
	Class for output needed
	to be provided for
	Optometrika
	"""

	def __init__(self, name_sim, tot_time, face_centers):

		self.name_sim = name_sim
		self.tot_time = tot_time
		self.tot_face = np.shape(face_centers)[0]
		self.face_centers = face_centers

		if os.path.exists("output/{}_eyes_left.txt".format(name_sim)):
				os.remove("output/{}_eyes_left.txt".format(name_sim))

		self.optk_writer = "output/{}_eyes_left.txt".format(name_sim)

		# data to be saved
		# in order:
		# 1- irradiance 
		# 2- ray direction x
		# 3- ray direction y
		# 4- ray direction z
		# 5- point origin x
		# 6- point origin y
		# 7- point origin z

		self.output_optk = np.zeros(( tot_time*self.tot_face , 7))

	def save_output(self, irr_dir, direction):

		k = 0

		# initialization 
		origins = np.ones((self.tot_face, 3))

		# N equal irradiance values
		irr = np.ones((self.tot_face,1))*irr_dir

		# translation into optical axis
		center_points = np.array(self.face_centers) - \
						np.ones((self.tot_face, 3))*eye_param.tr_f_l

		# origins are defined at 1 meter (1000mm)
		# in front of the cornea
		origins[:, 0] = center_points[:, 0] + \
						(direction[:, 0]/direction[:, 2])*(1000. - center_points[:, 2])
		origins[:, 1] = center_points[:, 1] + \
						(direction[:, 1]/direction[:, 2])*(1000. - center_points[:, 2])
		origins[:, 2] = 1000.

		merged_info = np.concatenate((irr, direction, origins), axis=1)

		start_index = k*np.shape(self.face_centers)[0]
		end_index = (k+1)*np.shape(self.face_centers)[0]

		self.output_optk[start_index:end_index, :] = merged_info

		k += 1


	def export_file(self):

		np.savetxt(self.optk_writer, 
					self.output_optk, 
					fmt='%4.8f')		

