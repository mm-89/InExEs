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

#my_posture_file = "postures/cube.ply"
my_posture_file = "postures/cube.ply"

output_name = "test"

#SIMULATION PARAMETERS------------------------
#timestep of simulation

timestep = 60.

#GEO PARAMETERS----------------------------

latitude = 40

#POSTURE PARAMETERS--------------------------
#need start angle

start_angle_azimuth = 0.

#DATA PARAMETERS------------------------------
#set start date

#--------------mm-dd-yyyy-hh-mm-ss
start_date  = '01/01/2009 00:01:00'
end_date    = '01/01/2009 07:30:00'

#BETA COEFFICIENT
#spread points on a hemisphere

N = 2

#-------------------------------------------------------------------------

my_simulation = sim.Simulation(start_date, 
								end_date, 
								timestep, 
								my_posture_file,
								N,
								output_name,
								latitude=latitude,
								read_data=True,
								data_path=my_data_file,
								)

#my_simulation.set_start_angle(start_angle_azimuth)

#to make sure how your mesh is orientated in the space----
my_simulation.export_reference_frame()

#to visualize a particular timestep-----------------------
#my_simulation.show_one_timestep(start_date)

#to make a whole simulation---------------------------------
my_simulation.make_simulation()
