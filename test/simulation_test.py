import unittest
import sys

sys.path.insert(0, '../')

import csv
import numpy as np
from math import pi

import simulation as sim
from math_refl_diff import from_polar_to_cartesian as fpc

# EXPLANATION OF THIS TEST (michele.marro@unige.ch)
#blablabla
#--------------------------------------------------

delta_range = 1e-15

# parameters for simulation---------------

my_posture_file_cube = "postures_test/cube_test.ply"
output_name_cube = "this_test_cube"
input_test = "input/input_test.csv"
timestep = 60.
latitude = 45
start_date  = '01/01/2009 00:01:00'
end_date    = '01/01/2009 23:59:00'

#----------------------------------------

# make simulation output-----------------

my_sim = sim.Simulation(start_date, 
			end_date, 
			timestep, 
			my_posture_file_cube,
			output_name_cube,
			latitude=latitude,
			read_data=True,
                        data_path=input_test)
								
my_sim.make_simulation()
#-----------------------------------------

def open_output(path):

	with open("output/" + path + ".csv", mode='r') as csv_file:

		next(csv_file)
		data = np.array([i for i in csv.reader(csv_file, delimiter=",")])
		data = np.delete(data, 0, 1)
		data = data.astype(np.float)

	return data[:, 0], data[:, 1], data[:, 2]


def open_sunDir_input(path):
	"""
	Notes: it gives zenith and azimuth
	"""

	with open(path, mode='r') as csv_file:

		next(csv_file)
		data = np.array([i for i in csv.reader(csv_file, delimiter=",",
						quoting=csv.QUOTE_NONNUMERIC)])
		return data[:, 5], data[:, 6]

#-----------------------------------------

def make_refl_diff_cube(vec):
	out = []
	for item in vec:
		if(item==0.):
			out.append( 0. )
		else:
			out.append( 0.5 )
	return out

#-----------------------------------------

def simulate_face(directions, face_normal):

	res = []
	for item in directions:

		# see this if condition in 
		# simulation class (<90). It means
		# that I want to simulate
		# just a day sun

		if(item[1]>0):
			dot_comp = np.dot(item, face_normal)

			# less than 0 means visible
			if(dot_comp < 0):
				res.append( -dot_comp )
			else:
				res.append( 0. )
		else:
			res.append( 0. )

	return res

#-----------------------------------------


# MAIN CLASS

class TestGeneral(unittest.TestCase):

	def setUp(self):

		tmp_zenith, tmp_azimuth = open_sunDir_input(input_test)

		directions = [fpc(i, j) for i, j in zip(tmp_zenith, tmp_azimuth)]

		# charge data for cube --------------------------------------------
		cube_dir, cube_dif, cube_ref = open_output(output_name_cube)

		self.cub_dir_tot = [i/60. for i in cube_dir] # output is in Joule
		self.cub_dif_tot = [i/60. for i in cube_dif] # output is in Joule
		self.cub_ref_tot = [i/60. for i in cube_ref] # output is in Joule

		cube_faces = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]

		tot_rad_cube_rcv = []
		for item in cube_faces:
			tot_rad_cube_rcv.append( simulate_face(directions, item) )

		self.rad_cub_fin = []
		for item in np.array(tot_rad_cube_rcv).T:
			self.rad_cub_fin.append( sum(item)/6 )


		self.diff_cube = make_refl_diff_cube(self.cub_dif_tot)
		self.refl_cube = make_refl_diff_cube(self.cub_ref_tot)

		#------------------------------------------------------------------

        
	def test_simulation_direct(self):
		#print(self.cub_dir_tot, self.rad_cub_fin)
		self.assertListAlmostEqual(self.cub_dir_tot, self.rad_cub_fin, delta=delta_range)


	def test_simulation_diffuse(self):
		#print(self.cub_dir_tot, self.rad_cub_fin)
		self.assertListAlmostEqual(self.cub_dif_tot, self.diff_cube, delta=1e-4)


	def test_simulation_reflect(self):
		#print(self.cub_dir_tot, self.rad_cub_fin)
		self.assertListAlmostEqual(self.cub_ref_tot, self.refl_cube, delta=1e-4)

	#------------------------------------------------------------------------
	# this is needed because, as far as I know,
	# there is not AlmostEqual for list
	def assertListAlmostEqual(self, list1, list2, delta):
		self.assertEqual(len(list1), len(list2))
		for a, b in zip(list1, list2):
			self.assertAlmostEqual(a, b, delta=delta)

if __name__ == '__main__':
    unittest.main()
