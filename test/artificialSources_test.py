import unittest
import sys

sys.path.insert(0, '../')

import numpy as np

import artificialSources as arts

class Test_Artificial_Sources(unittest.TestCase):

	#cube can actually receive light
	#for a point source located in (0, 0, 1)
	#on two surfaces. Anyway, for simmetry
	#results are both the same and it's enough
	#to check the irradiance on one surface
	face_active = 10
	coordinate_point_soruce = np.array([0, 0, 10])

	def setUp(self):

		artificial_scenario = arts.ArtificialSource("postures_test/cube_test.ply")

		#test a point in the space for 1 second
		artificial_scenario.add_point_source(self.coordinate_point_soruce, 1, 1)
		artificial_scenario.make_simulation()

		center_trg = artificial_scenario.triangles_center[self.face_active]

		self.output_inexes = artificial_scenario.irr_rcv[self.face_active]

		#output from physics
		self.output_physics = 1/np.linalg.norm(self.coordinate_point_soruce - center_trg)**2


	def test_source_point(self):
		# surface 1 diff - lateral
		self.assertAlmostEqual(self.output_inexes, 
								self.output_physics, 
								delta=1e-4)	


if __name__ == '__main__':
		unittest.main()
