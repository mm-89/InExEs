import unittest
import sys

sys.path.insert(0, '../')

import math as mt
import numpy as np
import random

import math_refl_diff as mrd

# --IMPORTANT--------------------------------------
# random points generator has shown
# some unstability durint "scale" test
# and consistency, so it'd better to use
# uniform points algorithm. For this reason
# random points algorithm hasn't been tested yet
#--------------------------------------------------

#set the seed for random function
#DON'T TOUCH THIS
random.seed(12)

#delta range to determine relative
#difference between 2 values approximation
#(to avoid FAILED because of approx)
deltaRange = 1e-9

# value of points generated
# over of a hemisphere
max_value = 10

class Test_Math_Refl_Diff(unittest.TestCase):


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

		#to test uniform points up hemisphere function - 10 points
		self.uniform_points_hemisphere_up = [[ 0.00000000e+00, 9.65925826e-01, -2.58819045e-01],
											[ 0.00000000e+00, 7.07106781e-01, -7.07106781e-01],
											[ 7.07106781e-01, 7.07106781e-01, -4.32978028e-17],
											[ 8.65956056e-17, 7.07106781e-01, 7.07106781e-01],
											[-7.07106781e-01, 7.07106781e-01, 1.29893408e-16],
											[ 0.00000000e+00, 2.58819045e-01, -9.65925826e-01],
											[ 9.18650051e-01, 2.58819045e-01, -2.98487496e-01],
											[ 5.67756956e-01, 2.58819045e-01, 7.81450409e-01],
											[-5.67756956e-01, 2.58819045e-01, 7.81450409e-01],
											[-9.18650051e-01, 2.58819045e-01, -2.98487496e-01]]
														
		
		self.uniform_points_hemisphere_down = [[0.0, -0.25881904510252063, -0.9659258262890683], 
											[0.9186500513499989, -0.25881904510252063, -0.29848749562898547], 
											[0.5677569555011357, -0.25881904510252063, 0.7814504087735196], 
											[-0.5677569555011355, -0.25881904510252063, 0.7814504087735198], 
											[-0.918650051349999, -0.25881904510252063, -0.2984874956289853], 
											[0.0, -0.7071067811865475, -0.7071067811865476], 
											[0.7071067811865476, -0.7071067811865475, -4.329780281177467e-17], 
											[8.659560562354934e-17, -0.7071067811865475, 0.7071067811865476], 
											[-0.7071067811865476, -0.7071067811865475, 1.29893408435324e-16], 
											[0.0, -0.9659258262890683, -0.2588190451025206]]

		"""
		#to test random points up hemisphere function - 10 points
		self.random_points_hemisphere_up = [[-0.39227895168153176, 0.9097713373105905, -0.13576942909115547], 
											[0.39670411375856746, 0.3202606134375247, -0.8602668107091253], 
											[0.6377575648931711, 0.2441567359292883, 0.7305154185380952], 
											[-0.00980903553049295, 0.9407725854409976, 0.33889633415636455], 
											[-0.9384732326821453, 0.33737772664635596, -0.07378523634210679], 
											[-0.7314024667925357, 0.2772240276252587, 0.6230547889849043], 
											[-0.49010539598482095, 0.7821120541747423, -0.3848342962121839], 
											[0.9660173519390404, 0.15101620872945692, 0.20977268757792392], 
											[0.7025112545873513, 0.7094091400136472, -0.056715158848434304], 
											[0.7722156398001051, 0.33306674420696963, -0.541063350774642]]


			
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
		"""

	def test_from_cartesian_to_polar(self):
		#test right axes
		self.assertEqual( list(mrd.from_cartesian_to_polar(self.x_ax)), self.east )
		self.assertEqual( list(mrd.from_cartesian_to_polar(self.y_ax)), self.zenith )
		self.assertEqual( list(mrd.from_cartesian_to_polar(self.z_ax)), self.south )
		
		#test mixed axes
		self.assertListAlmostEqual( list(mrd.from_cartesian_to_polar(self.xy_ax)), self.xy_ax_polar, delta=deltaRange )
		self.assertListAlmostEqual( list(mrd.from_cartesian_to_polar(self.xz_ax)), self.xz_ax_polar, delta=deltaRange )
		self.assertListAlmostEqual( list(mrd.from_cartesian_to_polar(self.yz_ax)), self.yz_ax_polar, delta=deltaRange )
		self.assertListAlmostEqual( list(mrd.from_cartesian_to_polar(self.xyz_ax)), self.xyz_ax_polar, delta=deltaRange )
		
	
	def test_from_polar_to_cartesian(self):
		#test right axes
		self.assertListAlmostEqual( list(mrd.from_polar_to_cartesian(self.south_degree[0], self.south_degree[1])), 
																	self.z_ax, delta=deltaRange )
		self.assertListAlmostEqual( list(mrd.from_polar_to_cartesian(self.east_degree[0], self.east_degree[1])), 
																	self.x_ax, delta=deltaRange )
		self.assertListAlmostEqual( list(mrd.from_polar_to_cartesian(self.zenith_degree[0], self.zenith_degree[1])), 
																	self.y_ax, delta=deltaRange )

	
		#test mixed axes
		self.assertListAlmostEqual( list(mrd.from_polar_to_cartesian(self.xy_ax_polar_degree[0], self.xy_ax_polar_degree[1])), 
       															self.xy_ax, delta=deltaRange )
		self.assertListAlmostEqual( list(mrd.from_polar_to_cartesian(self.xz_ax_polar_degree[0], self.xz_ax_polar_degree[1])),
        														self.xz_ax, delta=deltaRange )
		self.assertListAlmostEqual( list(mrd.from_polar_to_cartesian(self.yz_ax_polar_degree[0], self.yz_ax_polar_degree[1])), 
       															self.yz_ax, delta=deltaRange )
		self.assertListAlmostEqual( list(mrd.from_polar_to_cartesian(self.xyz_ax_polar_degree[0], self.xyz_ax_polar_degree[1])), 
       															self.xyz_ax, delta=deltaRange )


	def test_uniform_points_hemisphere_up(self):
		#test direction (theta is implicit)
		self.assertMatrixAlmostEqual( mrd.uniform_points_hemisphere(N=max_value, diff=True), 
                                    self.uniform_points_hemisphere_up, delta=deltaRange)


	def test_uniform_points_hemisphere_dpwn(self):
		#test direction (theta is implicit)
		self.assertMatrixAlmostEqual( mrd.uniform_points_hemisphere(N=max_value, diff=False), 
                                    self.uniform_points_hemisphere_down, delta=deltaRange)						
	
	"""
	def test_random_points_hemisphere_up(self):
		#test direction (theta is implicit)
		self.assertMatrixAlmostEqual( mrd.random_points_hemisphere(N=max_value, diff=True), 
                                    self.random_points_hemisphere_up, delta=deltaRange)
	
	def test_random_points_hemisphere_down(self):
		#test direction (theta is implicit)
		self.assertEqual(np.around(mrd.random_points_hemisphere(N=max_value,diff=False)[0],
									approx).tolist(), 
                                    self.random_points_hemisphere_down.tolist())	
	"""
	#------------------------------------------------------------------------
	# this is needed because, as far as I know,
	# there is not AlmostEqual for list
	def assertListAlmostEqual(self, list1, list2, delta):
		self.assertEqual(len(list1), len(list2))
		for a, b in zip(list1, list2):
			self.assertAlmostEqual(a, b, delta=delta)
	
	def assertMatrixAlmostEqual(self, mtrx1, mtrx2, delta):
		self.assertEqual(np.array(mtrx1).shape[0], np.array(mtrx2).shape[0])
		self.assertEqual(np.array(mtrx1).shape[1], np.array(mtrx2).shape[1])
		for x, y in zip(mtrx1, mtrx2):
			self.assertListAlmostEqual(x, y, delta)
	#------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
