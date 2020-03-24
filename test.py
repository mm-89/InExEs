import sun_ray_direction as srd
import matplotlib.pyplot as plt


my_d = srd.Sun_ray_direction(latitude=45.)

day = [1, 101, 201, 365]
second = [0., 21600., 43200., 64600., 86400.]

t_day = []
for i in day:
    t_day.append(my_d.get_sun_irradiance_in_a_day(i))

t_second = []
for i in second:
    t_second.append(my_d.get_daily_sun_irradiance(1, i))

print(t_day, "\n", t_second)s
