import unittest
import sys

sys.path.insert(0, '../')

import trimesh as tm
from scipy.integrate import quad
from math import cos, sin, pi
import random

random.seed(12)

import beta_coefficients as bc
import shared_parameters as sp
#meshes for test

my_cube = "postures_test/cube_test.ply"
my_tetrahedron = "postures_test/tetrahedron_test.ply"

#try to open mesh for tests
my_mesh_cube = tm.load(my_cube)
my_mesh_tetrahedron = tm.load(my_tetrahedron)

# usual function for beta coefficient for zenith part ---
def integral_arg_2(theta, phi, theta_0, phi_0):
    return (sin(theta)*cos(phi)*sin(theta_0)*cos(phi_0) + \
            sin(theta)*sin(phi)*sin(theta_0)*sin(phi_0) + \
            cos(theta)*cos(theta_0))*sin(theta)

def integral_arg(theta, theta_0):
    return cos(theta_0 -theta)*sin(theta)
#--------------------------------------------------------

class Test_Beta_Coefficients(unittest.TestCase):

    def setUp(self):
        #for the cube mesh------------------------------------------
        self.beta_coeff_cube = bc.compute_beta(my_cube,
                                my_mesh_cube,
                                my_mesh_cube.face_normals,
                                my_mesh_cube.triangles_center + \
                                my_mesh_cube.face_normals*sp.normalization_factor)

        # parameter - analitical
        self.top_diff, self.top_diff_err = quad(integral_arg, 0, pi/2., args=(0.))
        self.bot_refl, self.bottom_err = quad(integral_arg, pi/2., pi, args=(pi))

        self.lat, self.lat_err = quad(integral_arg, 0, pi/2., args=(0.))
        #----------------------------------------------------------

        #for the tetrahedron mesh------------------------------------------
        self.beta_coeff_tetr = bc.compute_beta(my_tetrahedron,
                                my_mesh_tetrahedron,
                                my_mesh_tetrahedron.face_normals,
                                my_mesh_tetrahedron.triangles_center + \
                                my_mesh_tetrahedron.face_normals*sp.normalization_factor)

        #diff parameter - analitical
        self.top_diff_tr = pi*quad(integral_arg, 0, pi/2., args=(0.))[0]

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
        self.assertEqual(self.beta_coeff_cube[6, 0], 0.)

        # surface 8 diff - bot
        self.assertEqual(self.beta_coeff_cube[7, 0], 0.)

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
        self.assertEqual(self.beta_coeff_cube[2, 1], 0.)

        # surface 4 diff - top
        self.assertEqual(self.beta_coeff_cube[3, 1], 0.)

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
    """
    def test_compute_beta_coefficient_tetrahedron(self):
        # surface 1 diff - top
        self.assertAlmostEqual(self.beta_coeff_tetr[0, 0], 
                                pi*self.top_diff_tr, 
                                delta=10*self.beta_coeff_tetr[0, 2])
    """
if __name__ == '__main__':
    unittest.main()
