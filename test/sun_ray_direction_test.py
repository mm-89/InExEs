import unittest
import sys

sys.path.insert(0, '../')

import sun_ray_direction as srd

# parameters for this test
lat = 45.
day_to_plot = [i for i in range(1, 365, 30)]
second_to_plot = [0., 21600., 43200., 64600., 86400.]

class TestGeneral(unittest.TestCase):

    def setUp(self):
        self.sun = srd.Sun_ray_direction(latitude=lat)
        self.day = day_to_plot
        self.second = second_to_plot

        self.sun_declination_angle = [self.sun.get_sun_declination_angle(x, radiant=True) for x in self.day]

        self.sun_declination_angle_result = [-0.40179266949827525, 
                                            -0.3113716922017807, 
                                            -0.1397383698648595, 
                                            0.06834168476363259, 
                                            0.2585967777059113,
                                            0.3814043432609367, 
                                            0.40473356219493506, 
                                            0.3224996791334077, 
                                            0.1561510358892609, 
                                            -0.050925111243841414, 
                                            -0.2447189086671415, 
                                            -0.37468482145501586, 
                                            -0.40692498150588097]


    def test_sun_zenith_angle(self):
        self.assertListEqual(self.sun_declination_angle_result, self.sun_declination_angle)

if __name__ == '__main__':
    unittest.main()
