import simulation as sim
import sun_ray_direction as srd
import posture as ps
import output as op

import os
import matplotlib.pyplot as plt
import trimesh as tm

#-------------------------------------------
#------------------NAMELIST-----------------
#-------------------------------------------

#POSTURE PARAMETERS--------------------------
#choosing and charging the posture

my_data_file = "input/irradiance_2009.csv"

#my_posture_file = "postures/head_high_res/head.ply"
my_posture_file = "male_eyesballs_reduced_faces.ply"

output_name = "data"

#SIMULATION PARAMETERS------------------------
#timestep of simulation

timestep = 60.

#GEO PARAMETERS----------------------------

latitude = 46.8

#POSTURE PARAMETERS--------------------------
#need start angle

start_angle_theta = 0.
start_angle_phi = 0.

#DATA PARAMETERS------------------------------
#set start date

s_year = 2009
s_month = 1
s_day = 1
s_hour = 12
s_minute = 1
s_second = 0

#----------------------------------------
#set end date

e_year = 2009
e_month = 1
e_day = 1
e_hour = 12
e_minute = 40
e_second = 0

#BETA COEFFICIENT
#spread points on a hemisphere

N = 2

#-------------------------------------------------------------------------
#vector of current data

start_date = [s_year, s_month, s_day, s_hour, s_minute, s_second]
end_date = [e_year, e_month, e_day, e_hour, e_minute, e_second]

#Initialize classes ------------------------------------------------------

posture = ps.Posture(my_posture_file,N)

#sun_ray_source = srd.Sun_ray_direction(latitude=latitude)

#-----------------------------------------

my_simulation = sim.Simulation(start_date, 
								end_date, 
								timestep, 
								posture,
								start_angle_theta,
								start_angle_phi,
								output_name,
								latitude=latitude,
								read_data=False,
								data_path=my_data_file,
								)

#to visualize a particular timestep
#my_simulation.show_one_timestep(start_date)

#to do a whole simulation
my_simulation.make_simulation()