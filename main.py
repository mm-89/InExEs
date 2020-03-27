import simulation as sim
import sun_ray_direction as srd
import posture as ps

import os
import csv
import time
import output as op
import matplotlib.pyplot as plt
import trimesh as tm

#-------------------------------------------
#------------------NAMELIST-----------------
#-------------------------------------------

#POSTURE PARAMETERS--------------------------
#choosing and charging the posture

my_data_file = "input/irradiance_2009.csv"

my_posture_file = "postures/head_high_res/head.ply"

output_name = "data"

#SIMULATION PARAMETERS------------------------
#timestep of simulation

timestep = 60.

#GEO PARAMETERS----------------------------

latitude = 8.1

#POSTURE PARAMETERS--------------------------
#need start angle

start_angle_theta = 0.
start_angle_phi = 180.

#DATA PARAMETERS------------------------------
#set start date

s_year = 2010
s_month = 7
s_day = 11
s_hour = 7
s_minute = 0
s_second = 0

#----------------------------------------
#set end date

e_year = 2010
e_month = 7
e_day = 11
e_hour = 17
e_minute = 0
e_second = 0

#BETA COEFFICIENT
#spread point on a hemisphere

N = 2

#-------------------------------------------------------------------------
#vector of current data

start_date = [s_year, s_month, s_day, s_hour, s_minute, s_second]
end_date = [e_year, e_month, e_day, e_hour, e_minute, e_second]

#Initialize classes ------------------------------------------------------

posture = ps.Posture(my_posture_file,N)

sun_ray_source = srd.Sun_ray_direction(latitude=latitude)

#-----------------------------------------

my_simulation = sim.Simulation(start_date, 
								end_date, 
								timestep, 
								posture, 
								sun_ray_source,
								start_angle_theta,
								start_angle_phi,
								output_name
								)

#to visualize a particular timestep
#my_simulation.show_one_timestep(start_date)

#to do a whole simulation
my_simulation.make_simulation()


#TO GIVE UP
#one day
"""
data = []
for i in range(86400):
	projz = sun_ray_source.get_sun_direction(1,i)
	data.append(projz)

time = [i for i in range(len(data))]

plt.plot(time, data)
plt.show()
"""
