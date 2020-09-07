import simulation as sim
from color_map import color_map as cm
import sun_ray_direction as srd
import posture as ps
import output as op

import shared_parameters as sp

import gui

import matplotlib.pyplot as plt
import trimesh as tm

from tkinter import *
#-------------------------------------------
#------------------NAMELIST-----------------
#-------------------------------------------
#POSTURE PARAMETERS--------------------------
#choosing and charging the posture

my_data_file = "input/irradiance_2009.csv"

#my_posture_file = "postures/cube.ply"
my_posture_file = "postures/body_high_res/baby.ply"

output_name = "eyelash_random_2"

#SIMULATION PARAMETERS------------------------
#timestep of simulation

timestep = 60.

#GEO PARAMETERS----------------------------

latitude = 40.

#SIM POSTURE PARAMETERS--------------------------
#need start angle

start_angle_azimuth = 0.

#DATA PARAMETERS------------------------------
#set start date

#--------------mm-dd-yyyy-hh-mm-ss
start_date  = '01/01/2009 12:01:00'
end_date    = '01/07/2009 22:39:00'

#-------------------------------------------------------------------------
    
#USE IF YOU WANT TO USE THE PROGRAMM WITHOUT GUI

if not sp.GUI_window:

	my_simulation = sim.Simulation(start_date, 
								end_date, 
								timestep, 
								my_posture_file,
								output_name,
								latitude=latitude,
								read_data=True,
								data_path=my_data_file
								)


	#my_simulation.set_start_angle(start_angle_azimuth)

	#to make sure how your mesh is orientated in the space----
	#my_simulation.export_reference_frame()

	#to visualize a particular timestep-----------------------
	#my_simulation.show_one_timestep(start_date)

	#my_simulation.set_zone_to_simulate(cm["green"])

	#to make a whole simulation---------------------------------
	#my_simulation.make_simulation() 

else:
	
	#-------------------------------------------
	#------------------GUI-----------------
	#-------------------------------------------
	window = gui.Root()
	window.mainloop()
