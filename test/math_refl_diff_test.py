import unittest
import sys

sys.path.insert(0, '../')

import math as mt
import numpy as np
import random

import math_refl_diff as mrd

#-Some parameters to set--------------

#value after comma to approximate
approx = 8

#seed for test random function. BE CAREFUL: don't touch this!!!!
seed = 12

#max value of component generated 
#for random functions
max_value = 10

#-------------------------------------

#set the seed for random function
random.seed(seed)

#-Class test--------------------------

class Test_Math_Refl_Diff(unittest.TestCase):

	maxDiff = None

	def setUp(self):

		#to test right axes orientation - cartesian
		self.x_ax = [1, 0, 0]   #east	
		self.y_ax = [0, 1, 0]   #zenith
		self.z_ax = [0, 0, 1]   #south

		#to test mix axes orientation - cartesian
		self.xy_ax = [1/mt.sqrt(2), 1/mt.sqrt(2), 0]
		self.xz_ax = [1/mt.sqrt(2), 0 ,	1/mt.sqrt(2)]
		self.yz_ax = [0, 1/mt.sqrt(2), 1/mt.sqrt(2)]
		self.xyz_ax = [1/2., 1/mt.sqrt(2), 1/2.]

		#to test right axes orientation - polar
		self.east = [mt.pi/2., mt.pi/2.]
		self.zenith = [0., 0.]
		self.south = [mt.pi/2., mt.pi]

		#to test mixed axes orientation - polar
		self.xy_ax_polar = [mt.pi/4., mt.pi/2.]
		self.xz_ax_polar = [mt.pi/2., 3*mt.pi/4.]
		self.yz_ax_polar = [mt.pi/4., mt.pi]
		self.xyz_ax_polar = [mt.pi/4., 3*mt.pi/4.]

		#to test right axes orientation - polar DEGREE
		self.east_degree = [90., 90.]
		self.zenith_degree = [0., 0.]
		self.south_degree = [90., 180.]		

		#to test mixed axes orientation - polar DEGREE
		self.xy_ax_polar_degree = [45., 90.]
		self.xz_ax_polar_degree = [90., 135.]
		self.yz_ax_polar_degree = [45., 180.]
		self.xyz_ax_polar_degree = [45., 135.]

		#to test random points up hemisphere function - 10 points
		self.random_points_hemisphere_up = np.array([[0.50712857, 0.80473546, 0.30857974],
													[-0.02443153, 0.99957302, -0.01602729],
													[0.36938968, 0.13306896, -0.91969773],
													[-0.00798329, 0.98980603, 0.14219804],
													[-0.08046879, 0.08360529, -0.99324465],
													[0.40071245, 0.78705783, -0.46900907],
													[0.35377831, 0.88189113, -0.31162307],
													[-0.17558993, 0.96719166, 0.18359867],
													[-0.076124, 0.99674829, 0.02641921],
													[0.84333793, 0.28547446, -0.45528615]])
													
		#to test random points low hemisphere function - 10 points
		self.random_points_hemisphere_down = np.array([[0.08153061, -0.85871426, 0.50592744],
													[-0.84360415, -0.22212766, 0.4888674],
													[0.05670855, -0.55524954, -0.82974821],
													[0.29017347, -0.95595363, 0.04418164],
													[-0.54558532, -0.81036014, 0.21366586],
													[-0.18135721, -0.86179651, 0.47372601],
													[0.60967885, -0.6374903, -0.4710603],
													[0.12536274, -0.98911257, -0.07707471],
													[0.10142727, -0.95977497, -0.26181007],
													[0.21332578, -0.88151034, -0.42122634]])


	def test_from_cartesian_to_polar(self):
		#test right axes
		self.assertListEqual(list(mrd.from_cartesian_to_polar(self.x_ax)), self.east)
		self.assertListEqual(list(mrd.from_cartesian_to_polar(self.y_ax)), self.zenith)
		self.assertListEqual(list(mrd.from_cartesian_to_polar(self.z_ax)), self.south)

		#test mixed axes
		self.assertListEqual(list(np.around(mrd.from_cartesian_to_polar(self.xy_ax), approx)), 
															list(np.around(self.xy_ax_polar, approx)))
		self.assertListEqual(list(np.around(mrd.from_cartesian_to_polar(self.xz_ax), approx)), 	
															list(np.around(self.xz_ax_polar, approx)))
		self.assertListEqual(list(np.around(mrd.from_cartesian_to_polar(self.yz_ax), approx)),
															list(np.around(self.yz_ax_polar, approx)))
		self.assertListEqual(list(np.around(mrd.from_cartesian_to_polar(self.xyz_ax), approx)), 
															list(np.around(self.xyz_ax_polar, approx)))

	def test_from_polar_to_cartesian(self):
		#test right axes
		self.assertListEqual(list(np.around(mrd.from_polar_to_cartesian(self.south_degree[0], 
        														self.south_degree[1]), approx)), 
                                                                self.z_ax)
		self.assertListEqual(list(np.around(mrd.from_polar_to_cartesian(self.east_degree[0], 
        														self.east_degree[1]), approx)), self.x_ax)
		self.assertListEqual(list(np.around(mrd.from_polar_to_cartesian(self.zenith_degree[0], 
        														self.zenith_degree[1]), approx)), self.y_ax)

		#test mixed axes
		self.assertListEqual(list(np.around(mrd.from_polar_to_cartesian(self.xy_ax_polar_degree[0],
       															self.xy_ax_polar_degree[1]), approx)), 
       													list(np.around(self.xy_ax, approx)))
		self.assertListEqual(list(np.around(mrd.from_polar_to_cartesian(self.xz_ax_polar_degree[0],
        														self.xz_ax_polar_degree[1]), approx)),
        												list(np.around(self.xz_ax, approx)))
		self.assertListEqual(list(np.around(mrd.from_polar_to_cartesian(self.yz_ax_polar_degree[0],
       															self.yz_ax_polar_degree[1]), approx)), 
       													list(np.around(self.yz_ax, approx)))
		self.assertListEqual(list(np.around(mrd.from_polar_to_cartesian(self.xyz_ax_polar_degree[0],
       															self.xyz_ax_polar_degree[1]), approx)), 
       													list(np.around(self.xyz_ax, approx)))
	
	                            
	def test_random_points_hemisphere_up(self):
		#test direction (theta is implicit)
		self.assertEqual(np.around(mrd.random_points_hemisphere(N=max_value, diff=True)[0],
									approx).tolist(), 
                                    self.random_points_hemisphere_up.tolist())
	
	def test_random_points_hemisphere_down(self):
		#test direction (theta is implicit)
		self.assertEqual(np.around(mrd.random_points_hemisphere(N=max_value,diff=False)[0],
									approx).tolist(), 
                                    self.random_points_hemisphere_down.tolist())	
    
if __name__ == '__main__':
    unittest.main()
