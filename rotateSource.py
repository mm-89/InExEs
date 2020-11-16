import math_refl_diff as mrd
import csv
from math import cos

import numpy as np

class RotateSource:

	input_angles_rotation = "input_irradiance/angles_rotation.csv"

	try:

		with open(input_angles_rotation, mode='r') as csv_file:

			#to avoid to read header
			next(csv_file)

			data =  np.array([i for i in csv.reader(csv_file, delimiter=",")])

			timeline = data[:, 0]

			angles_tmp = data[:, 1:]


	except:
		raise TypeError("File {} doesn't find or doesn't exist.".format(input_irradiance_path))


	def __init__(self, timeline_list):

		self.angles = np.zeros((len(timeline_list), 2))
		for k, item in enumerate(timeline_list):
			if( item == self.timeline[k] ):
				self.angles[k] = self.angles_tmp[k]


	def update_beta_coefficients(self, datestep, beta_coefficients, face_normals):
		
		angle = np.radians(self.angles[datestep, 0])
		
		angles = np.zeros(len(face_normals))*angle

		angle_normals =  mrd.from_cartesian_to_polar(face_normals[:, 0],
													face_normals[:, 1],
													face_normals[:, 2]) 

		beta_coefficients[:, 0] *= (1 + np.cos(angle_normals[:, 0] - angles))/2
		
		return beta_coefficients


	def update_direction(self, datestep, direction):

		x_angle = np.radians(self.angles[datestep, 0])
		y_angle = np.radians(self.angles[datestep, 1])

		first_rot = np.dot( mrd.rotation_matrix_3D_xz(x_angle), direction )
		second_rot = np.dot( mrd.rotation_matrix_3D_xy(y_angle), first_rot )

		return second_rot