import unittest
import sys

sys.path.insert(0, '../')

import math as mt
import numpy as np
import random

random.seed(12)

import math_refl_diff as mrd



class Test_Math_Refl_Diff(unittest.TestCase):

    def setUp(self):

        #to test right axes orientation - cartesian
        self.x_ax = [1, 0, 0]   #east
        self.y_ax = [0, 1, 0]   #zenith
        self.z_ax = [0, 0, 1]   #south

        #to test mix axes orientation - cartesian
        self.xy_ax = [0.7071067811865475, 0.7071067811865476, 0]	#[1/mt.sqrt(2), 1/mt.sqrt(2), 0]
        self.xz_ax = [0.7071067811865476, 0, 0.7071067811865475]	#[1/mt.sqrt(2), 0 ,	1/mt.sqrt(2)]
        self.yz_ax = [0, 0.7071067811865476, 0.7071067811865475]	#[0, 1/mt.sqrt(2), 1/mt.sqrt(2)]
        self.xyz_ax = [0.5, 0.7071067811865476, 0.4999999999999999]				#[1/2., 1/mt.sqrt(2), 1/2.]

        #to test right axes orientation - polar
        self.east = [mt.pi/2., mt.pi/2]
        self.zenith = [0., 0.]
        self.south = [mt.pi/2., mt.pi]

        #to test mixed axes orientation - polar
        self.xy_ax_polar = [0.7853981633974483, 1.5707963267948966]	#[mt.pi/4, mt.pi/2.]
        self.xz_ax_polar = [1.5707963267948966, 2.356194490192345]	#[mt.pi/2., 3*mt.pi/4.]
        self.yz_ax_polar = [0.7853981633974483, 3.141592653589793]	#[mt.pi/4, mt.pi]
        self.xyz_ax_polar = [0.7853981633974483, 2.356194490192345]	#[mt.pi/4., 3*mt.pi/4.]

        #to test right axes orientation - polar DEGREE
        self.south_degree = [90., 180.]
        self.east_degree = [90., 90.]
        self.zenith_degree = [0., 0.]

        #to test mixed axes orientation - polar DEGREE
        self.xy_ax_polar_degree = [45., 90.]
        self.xz_ax_polar_degree = [90., 135.]
        self.yz_ax_polar_degree = [45., 180.]
        self.xyz_ax_polar_degree = [45., 135.]

        #to test uniform points hemisphere function - 10 points
        self.uniform_points_hemisphere = np.array([[0.0, 0.9659258262890683, -0.25881904510252074],
 										[0.0, 0.7071067811865476, -0.7071067811865475],
 										[0.7071067811865475, 0.7071067811865476, -4.329780281177466e-17],
										[8.659560562354932e-17, 0.7071067811865476, 0.7071067811865475],
										[-0.7071067811865475, 0.7071067811865476, 1.2989340843532398e-16],
										[0.0, 0.25881904510252074, -0.9659258262890683],
										[0.9186500513499989, 0.25881904510252074, -0.29848749562898547],
										[0.5677569555011357, 0.25881904510252074, 0.7814504087735196],
										[-0.5677569555011355, 0.25881904510252074, 0.7814504087735198],
										[-0.918650051349999, 0.25881904510252074, -0.2984874956289853]])

		#to test random points hemisphere function - 10 points
        self.random_points_hemisphere = np.array([[0.11987706963406297, 0.6574725026572553, 0.7438813053340938],
                                        [-0.8563771795956278, 0.14260035292536768, 0.4962693478479187],
                                        [0.06321616982738963, 0.37475449206336436, -0.9249663704971572],
                                        [0.5792726843126144, 0.8103480522350838, 0.08819972476183857],
                                        [-0.7438932075770736, 0.6014570387277332, 0.2913285538452405],
                                        [-0.2681822876309054, 0.661321085872001, 0.7005231487839155],
                                        [0.7105820342140365, 0.4400547919247699, -0.5490218144630404],
                                        [0.36062910255210806, 0.9059729815293226, -0.2217196588742885],
                                        [0.20737352397104908, 0.8188201278420804, -0.5352848025084478],
                                        [0.32832980344565055, 0.6869455040935417, -0.6483096594799512]])



    def test_from_cartesian_to_polar(self):
    	#test right axes
        self.assertListEqual(list(mrd.from_cartesian_to_polar(self.x_ax)), self.east)
        self.assertListEqual(list(mrd.from_cartesian_to_polar(self.y_ax)), self.zenith)
       	self.assertListEqual(list(mrd.from_cartesian_to_polar(self.z_ax)), self.south)

       	#test mixed axes
       	self.assertListEqual(list(mrd.from_cartesian_to_polar(self.xy_ax)), self.xy_ax_polar)
        self.assertListEqual(list(mrd.from_cartesian_to_polar(self.xz_ax)), self.xz_ax_polar)
       	self.assertListEqual(list(mrd.from_cartesian_to_polar(self.yz_ax)), self.yz_ax_polar)
       	self.assertListEqual(list(mrd.from_cartesian_to_polar(self.xyz_ax)), self.xyz_ax_polar)

    def test_from_polar_to_cartesian(self):
    	#test right axes
        self.assertListEqual(list(mrd.from_polar_to_cartesian(self.south_degree[0], 
        														self.south_degree[1])), self.z_ax)
        self.assertListEqual(list(mrd.from_polar_to_cartesian(self.east_degree[0], 
        														self.east_degree[1])), self.x_ax)
        self.assertListEqual(list(mrd.from_polar_to_cartesian(self.zenith_degree[0], 
        														self.zenith_degree[1])), self.y_ax)

       	#test mixed axes
       	self.assertListEqual(list(mrd.from_polar_to_cartesian(self.xy_ax_polar_degree[0],
       															self.xy_ax_polar_degree[1])), 
       															self.xy_ax)
        self.assertListEqual(list(mrd.from_polar_to_cartesian(self.xz_ax_polar_degree[0],
        														self.xz_ax_polar_degree[1])),
        														 self.xz_ax)
       	self.assertListEqual(list(mrd.from_polar_to_cartesian(self.yz_ax_polar_degree[0],
       															self.yz_ax_polar_degree[1])), 
       															self.yz_ax)
       	self.assertListEqual(list(mrd.from_polar_to_cartesian(self.xyz_ax_polar_degree[0],
       															self.xyz_ax_polar_degree[1])), 
       															self.xyz_ax)

    def test_uniform_points_hemisphere(self):
    	self.assertEqual(mrd.uniform_points_hemisphere(N=10).tolist(), 
                                    self.uniform_points_hemisphere.tolist())

    def test_random_points_hemisphere(self):
        self.assertEqual(mrd.random_points_hemisphere(N=10).tolist(), 
                                    self.random_points_hemisphere.tolist())

if __name__ == '__main__':
    unittest.main()
