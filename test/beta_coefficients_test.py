import unittest
import sys

sys.path.insert(0, '../')

import os, glob

import trimesh as tm
from scipy.integrate import quad
from math import cos, sin, atan, pi
import random

random.seed(12)

import beta_coefficients as bc

#--------------------------------------------------------
#delete previous tests

for fileHere in glob.glob("input/beta_*"):
    os.remove(fileHere)

#--------------------------------------------------------

#meshes for test ----------------------------------------

my_cube = "postures_test/cube_test.ply"
my_tetrahedron = "postures_test/tetrahedron_test.ply"

#try to open mesh for tests
my_mesh_cube = tm.load(my_cube)
my_mesh_tetrahedron = tm.load(my_tetrahedron)

#simple integral function for tetrahedron
#it comes from integral of labert law with z=sqrt(2)x
def integral_tetr(x):
    return (sin(atan(1/((2**0.5) *sin(x)))))**2

#simple integral function for cube
def integral_cube(x, theta_0):
    return cos(theta_0 - x)*sin(x)
#--------------------------------------------------------

class Test_Beta_Coefficients(unittest.TestCase):

    def setUp(self):
        #for the cube mesh------------------------------------------
        self.beta_coeff_cube = bc.compute_beta(my_cube,
                                my_mesh_cube)

        #diff and refl parameter - analitical
        self.top_diff, self.top_diff_err = quad(integral_cube, 0, pi/2., args=(0.))
        self.bot_refl, self.bottom_err = quad(integral_cube, pi/2., pi, args=(pi))

        #lateral parameter - analitical
        self.lat, self.lat_err = quad(integral_cube, 0, pi/2., args=(0.))
        #----------------------------------------------------------

        #for the tetrahedron mesh------------------------------------------
        self.beta_coeff_tetr = bc.compute_beta(my_tetrahedron,
                                my_mesh_tetrahedron)

        #diff parameter - analitical
        #divide the domain in 1/4 of sphere + 1/8 of sphere
        self.top_diff_tr = quad(integral_tetr, 0, pi)[0]/2. + \
                                pi*quad(integral_cube, 0, pi/2., args=(0.))[0]

        self.bot_diff_tr = pi/2. - quad(integral_tetr, 0, pi)[0]/2.

        #refl parameter - analitical
        self.top_refl_tr = pi/2. - quad(integral_tetr, 0, pi)[0]/2.

        self.bot_refl_tr = quad(integral_tetr, 0, pi)[0]/2. + \
                                pi*quad(integral_cube, pi/2., pi, args=(pi))[0]
        
        #----------------------------------------------------------

    def test_compute_beta_coefficient_cube(self):
        # surface 1 diff - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[0, 0], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[0, 2])

        # surface 2 diff - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[1, 0], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[1, 2])

        # surface 3 diff - top
        self.assertAlmostEqual(self.beta_coeff_cube[2, 0], 
                                2*pi*self.top_diff, 
                                delta=self.beta_coeff_cube[2, 2])

        # surface 4 diff - top
        self.assertAlmostEqual(self.beta_coeff_cube[3, 0], 
                                2*pi*self.top_diff, 
                                delta=self.beta_coeff_cube[3, 2])

        # surface 5 diff - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[4, 0], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[4, 2])

        # surface 6 diff - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[5, 0], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[5, 2])

        # surface 7 diff - bot
        self.assertAlmostEqual(self.beta_coeff_cube[6, 0], 
							0.,
							delta=self.beta_coeff_cube[6, 2])

        # surface 8 diff - bot
        self.assertAlmostEqual(self.beta_coeff_cube[7, 0], 
								0.,
								delta=self.beta_coeff_cube[7, 2])

        # surface 9 diff - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[8, 0], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[8, 2])

        # surface 10 diff - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[9, 0], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[9, 2])

        # surface 11 diff - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[9, 0], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[9, 2])

        # surface 12 diff - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[11, 0], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[11, 2])

        # surface 1 refl - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[0, 1], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[0, 3])

        # surface 2 refl - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[1, 1], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[1, 3])

        # surface 3 refl - top
        self.assertAlmostEqual(self.beta_coeff_cube[2, 1], 
								0.,
								delta=self.beta_coeff_cube[2, 2])

        # surface 4 diff - top
        self.assertAlmostEqual(self.beta_coeff_cube[3, 1], 
								0.,
								delta=self.beta_coeff_cube[4, 2])

        # surface 5 refl - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[4, 1], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[4, 3])

        # surface 6 refl - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[5, 1], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[5, 3])

        # surface 7 refl - bot
        self.assertAlmostEqual(self.beta_coeff_cube[6, 1], 
                                2*pi*self.bot_refl, 
                                delta=self.beta_coeff_cube[6, 3])

        # surface 8 refl - bot
        self.assertAlmostEqual(self.beta_coeff_cube[7, 1], 
                                2*pi*self.bot_refl, 
                                delta=self.beta_coeff_cube[7, 3])

        # surface 9 refl - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[8, 1], 
                                pi*self.lat, 
                                delta=10*self.beta_coeff_cube[8, 3])

        # surface 10 refl - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[9, 1], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[9, 3])

        # surface 11 refl - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[9, 1], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[9, 3])

        # surface 12 refl - lateral
        self.assertAlmostEqual(self.beta_coeff_cube[11, 1], 
                                pi*self.lat, 
                                delta=self.beta_coeff_cube[11, 3])


    def test_compute_beta_coefficient_tetrahedron(self):
        # surface 1 diff - top
        self.assertAlmostEqual(self.beta_coeff_tetr[0, 0], 
                                self.top_diff_tr, 
                                delta=10*self.beta_coeff_tetr[0, 2])

        # surface 2 diff - bot
        self.assertAlmostEqual(self.beta_coeff_tetr[1, 0], 
                                self.bot_diff_tr, 
                                delta=10*self.beta_coeff_tetr[1, 2])

        # surface 3 diff - top
        self.assertAlmostEqual(self.beta_coeff_tetr[2, 0], 
                                self.top_diff_tr, 
                                delta=10*self.beta_coeff_tetr[2, 2])

        # surface 4 diff - bot
        self.assertAlmostEqual(self.beta_coeff_tetr[3, 0], 
                                self.bot_diff_tr, 
                                delta=10*self.beta_coeff_tetr[3, 2])

        # surface 1 refl - top
        self.assertAlmostEqual(self.beta_coeff_tetr[0, 1], 
                                self.top_refl_tr, 
                                delta=10*self.beta_coeff_tetr[0, 2])

        # surface 2 refl - bot
        self.assertAlmostEqual(self.beta_coeff_tetr[1, 1], 
                                self.bot_refl_tr, 
                                delta=10*self.beta_coeff_tetr[1, 3])

        # surface 3 refl - top
        self.assertAlmostEqual(self.beta_coeff_tetr[2, 1], 
                                self.top_refl_tr, 
                                delta=10*self.beta_coeff_tetr[2, 3])

        # surface 4 refl - bot
        self.assertAlmostEqual(self.beta_coeff_tetr[3, 1], 
                                self.bot_refl_tr, 
                                delta=10*self.beta_coeff_tetr[3, 3])

if __name__ == '__main__':
		unittest.main()
