import unittest
import sys

sys.path.insert(0, '../')

import csv
import numpy as np
from math import pi, sqrt

import simulation as sim
from math_refl_diff import from_polar_to_cartesian as fpc

# EXPLANATION OF THIS TEST (michele.marro@unige.ch)
#blablabla
#--------------------------------------------------

delta_range_dir = 1e-14
delta_range = 1e-4

# CUBE parameters for simulation---------------

my_posture_file_cube = "postures_test/cube_test.ply"
output_name_cube = "this_test_cube"
input_test = "input_irradiance/input_test.csv"
timestep = 60.
latitude = 45.
start_date  = '01/01/2009 00:01:00'
end_date    = '01/02/2009 00:00:00'

my_sim_cube = sim.Simulation(start_date, 
			end_date, 
			timestep, 
			my_posture_file_cube,
			output_name_cube,
			latitude=latitude,
			read_data=True,
			data_path=input_test)
#-----------------------------------------
# TETRAHEDRON parameters for simulation---

my_posture_file_tetr = "postures_test/tetrahedron_test.ply"
output_name_tetr = "this_test_tetrahedron"
input_test = "input_irradiance/input_test.csv"
timestep = 60.
latitude = 45.
start_date  = '01/01/2009 00:01:00'
end_date    = '01/02/2009 00:00:00'

my_sim_tetr = sim.Simulation(start_date, 
			end_date, 
			timestep, 
			my_posture_file_tetr,
			output_name_tetr,
			latitude=latitude,
			read_data=True,
 			data_path=input_test)
		
#-----------------------------------------						
my_sim_cube.make_simulation()
my_sim_tetr.make_simulation()
#-----------------------------------------

def open_output(path):

	with open("output/" + path + "_average" + ".csv", mode='r') as csv_file:

		next(csv_file)
		data = np.array([i for i in csv.reader(csv_file, delimiter=",")])

		rad_dir = data[:, 1].astype(float)
		rad_dif = data[:, 2].astype(float)
		rad_ref = data[:, 3].astype(float)

	return rad_dir, rad_dif, rad_ref


def open_sunDir_input(path):
	"""
	Notes: it gives zenith and azimuth
	"""

	with open(path, mode='r') as csv_file:

		next(csv_file)
		data_read = np.array([i for i in csv.reader(csv_file, delimiter=",")])
		zenith = data_read[:, 1].astype(float)
		azimuth = data_read[:, 2].astype(float)

		polar_output = fpc(zenith, azimuth)

		return polar_output

#-----------------------------------------

def make_refl_diff_cube(vec):
	res = np.zeros(len(vec))
	res[ vec!=0. ] = 0.5
	return res

#-----------------------------------------

def make_refl_diff_tetr(vec):
	res = np.zeros(len(vec))
	res[ vec!=0. ] = 0.5
	return res

#-----------------------------------------

def simulate_face(directions, face_normal):
	res = np.dot(directions, face_normal)
	res[ directions[:, 1]<0. ] = 0.	#only day light
	res[ res<0. ] = 0.				#remove shadows
	return res


# MAIN CLASS

class TestGeneral(unittest.TestCase):

	def setUp(self):

		directions = open_sunDir_input(input_test)

		# charge data for cube --------------------------------------------
		self.cube_dir, self.cube_dif, self.cube_ref = open_output(output_name_cube) #simulated by InExES

		cube_faces = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]

		rad_cub_tmp = np.array([simulate_face(directions, i) for i in cube_faces])
		self.rad_cub_fin = np.sum(rad_cub_tmp, 0)/6.

		self.diff_cube = make_refl_diff_cube(self.cube_dif)
		self.refl_cube = make_refl_diff_cube(self.cube_ref)

		#------------------------------------------------------------------
		# charge data for tetrahedron--------------------------------------
		
		self.tetr_dir, self.tetr_dif, self.tetr_ref = open_output(output_name_tetr)

		tetr_faces = [[1./sqrt(3), 1./sqrt(3), -1./sqrt(3)], 
					[-1./sqrt(3), 1./sqrt(3), 1./sqrt(3)], 
					[1./sqrt(3), -1./sqrt(3), 1./sqrt(3)], 
					[-1./sqrt(3), -1./sqrt(3), -1./sqrt(3)]]

		rad_tet_tmp = np.array([simulate_face(directions, i) for i in tetr_faces])
		self.rad_tet_fin = np.sum(rad_tet_tmp, 0)/4.

		self.diff_tetr = make_refl_diff_tetr(self.tetr_dif)
		self.refl_tetr = make_refl_diff_tetr(self.tetr_ref)
		
		#------------------------------------------------------------------

    # CUBE--------------

	def test_simulation_direct_cube(self):
		self.assertListAlmostEqual(self.cube_dir/60., self.rad_cub_fin, delta=delta_range_dir)


	def test_simulation_diffuse_cube(self):
		self.assertListAlmostEqual(self.cube_dif/60., self.diff_cube, delta=delta_range)


	def test_simulation_reflect_cube(self):
		self.assertListAlmostEqual(self.cube_ref/60., self.refl_cube, delta=delta_range)

	# TETRAHEDRON--------

	def test_simulation_direct_tetr(self):
		self.assertListAlmostEqual(self.tetr_dir/60., self.rad_tet_fin, delta=delta_range_dir)


	def test_simulation_diffuse_tetr(self):
		self.assertListAlmostEqual(self.tetr_dif/60., self.diff_tetr, delta=delta_range)


	def test_simulation_reflect_tetr(self):
		self.assertListAlmostEqual(self.tetr_ref/60., self.refl_tetr, delta=delta_range)

	#------------------------------------------------------------------------
	# this is needed because, as far as I know,
	# there is not AlmostEqual for list
	def assertListAlmostEqual(self, list1, list2, delta):
		self.assertEqual(len(list1), len(list2))
		for a, b in zip(list1, list2):
			self.assertAlmostEqual(a, b, delta=delta)

if __name__ == '__main__':
    unittest.main()
