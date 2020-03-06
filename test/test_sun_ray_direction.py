import unittest
import sys

sys.path.insert(0, '../')

import sun_ray_direction as srd

class TestGeneral(unittest.TestCase):

    def setUp(self):
        self.my_direction = srd.sun_ray_direction(year=2000, month=1, day=1, timestep=60., lat=45.)
        self.day = [1, 101, 201, 365]
        self.second = [0., 21600., 43200., 64600., 86400.]

        self.sun_zenith_angle = []
        self.sun_direction = []

        for day in self.day:
            self.my_direction.set_day(day)
            self.sun_zenith_angle.append(self.my_direction.get_sun_zenith_angle(radiant=True))

        for second in self.second:
            self.my_direction.set_second(second)
            self.sun_direction.append(self.my_direction.get_sun_direction())


        self.sun_zenith_angle_result = [-0.4020678653270671, 0.13015447130214178, 0.3604253746313337, -0.40365834939723066]
        self.sun_direction_result = [(-2.252444374665204e-16, -0.9888553336509976, 0.1488795792241976),\
                                    (1.126222187332602e-16, 0.5761778322823071, -0.817324357636833), \
                                    (-0.0, -0.9888553336509976, 0.1488795792241976), \
                                    (-0.026747185869122933, 0.5758467887062064, -0.8171199813887997), \
                                    (2.252444374665204e-16, -0.9888553336509976, 0.1488795792241976)]


    def test_sun_zenith_angle(self):
        self.assertListEqual(self.sun_zenith_angle_result, self.sun_zenith_angle)

    def test_sun_direction(self):
        self.assertListEqual(self.sun_direction, self.sun_direction_result)



if __name__ == '__main__':
    unittest.main()
