import unittest
import sys

sys.path.insert(0, '../')

import sun_ray_direction as srd

class TestGeneral(unittest.TestCase):

    def setUp(self):
        self.my_direction = srd.Sun_ray_direction(latitude=45.)
        self.day = [1, 101, 201, 365]
        self.second = [0., 21600., 43200., 64600., 86400.]

        self.sun_declination_angle = []
        self.sun_direction = []

        for day in self.day:
            self.sun_declination_angle.append(self.my_direction.get_sun_declination_angle(day, radiant=True))

        for second in self.second:
            self.sun_direction.append(self.my_direction.get_sun_direction(1, second))


        #------------------------
        self.t_day = []
        for i in self.day:
            self.t_day.append(self.my_direction.get_sun_irradiance_in_a_day(i))

        self.t_second = []
        for i in self.second:
            self.t_second.append(self.my_direction.get_daily_sun_irradiance(1, i))
        #------------------------


        self.sun_declination_angle_result = [-0.40179266949827525, 0.13642380371241053, 0.3608504130787583, -0.4030586458307827]
        self.sun_direction_result = [(1.1271176621663314e-16, 0.3742663459328221, -0.9273212508629862), 
                                    (0.9203614160026178, -0.27652745246508204, -0.2765274524650819),
                                    (-0.0, -0.927321250862986, 0.3742663459328222), 
                                    (-0.9202640711492827, -0.2859925308612656, -0.2670623740688984), 
                                    (-1.1271176621663314e-16, 0.3742663459328221, -0.9273212508629862)]

        self.irradiance_in_a_day_result = [1408.1649685107734, 1354.34110497443, 1318.1157031757266, 1408.171373022052]
        self.daily_sun_irradiance_result = [0.0, 0.0, 527.0287572351348, 0.0, 0.0]


    def test_sun_zenith_angle(self):
        self.assertListEqual(self.sun_declination_angle_result, self.sun_declination_angle)


    def test_sun_direction(self):
        self.assertListEqual(self.sun_direction_result, self.sun_direction)


    def test_get_sun_irradiance_in_a_day(self):
        self.assertListEqual(self.irradiance_in_a_day_result, self.t_day)


    def test_get_daily_sun_irradiance(self):
        self.assertListEqual(self.daily_sun_irradiance_result, self.t_second)


if __name__ == '__main__':
    unittest.main()
