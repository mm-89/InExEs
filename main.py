import simulation as sim
import sun_ray_direction as srd
import posture as ps
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
#my_posture_file = "postures/head_high_res/male_eyeballs_meshlab.ply"

output_name = "data"

#SIMULATION PARAMETERS------------------------
#timestep of simulation

timestep = 60.

#GEO PARAMETERS----------------------------

latitude = 46.8

#POSTURE PARAMETERS--------------------------
#need start angle

start_angle_azimuth = 0.

#DATA PARAMETERS------------------------------
#set start date

#--------------mm-dd-yyyy-hh-mm-ss
start_date  = '01/01/2010 12:00:00'
end_date    = '01/02/2010 12:00:00'

#BETA COEFFICIENT
#spread points on a hemisphere

N = 2

#-------------------------------------------------------------------------

#Initialize classes ------------------------------------------------------

posture = ps.Posture(my_posture_file,N)

#sun_ray_source = srd.Sun_ray_direction(latitude=latitude)

#-----------------------------------------

my_simulation = sim.Simulation(start_date, 
								end_date, 
								timestep, 
								posture,
								output_name,
								latitude=latitude,
								read_data=False,
								data_path=my_data_file,
								)

#my_simulation.set_start_angle(start_angle_azimuth)

#to visualize a particular timestep
#my_simulation.show_one_timestep(start_date)

#to do a whole simulation
my_simulation.make_simulation()
