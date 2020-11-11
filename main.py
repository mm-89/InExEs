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
#POSTURE PARAMETERS-------------------------
#choosing and charging the posture

my_data_file = "input_irradiance/irradiance_2009.csv"

my_posture_file = "postures/head_high_res/head.ply"

output_name = "head"

# PROTECTIONS PARAMETERS---------------------

protection_lib = "protections/protections_lib.xml"
protections = "protections/protections.xml"

# ANATOMICAL ZONES---------------------------

anat_zones = "anatomical_zones/anatomical_zones.xml"

#SIMULATION PARAMETERS-----------------------
#timestep of simulation

timestep = 60.

#GEO PARAMETERS------------------------------

latitude = 40.

#DATA PARAMETERS-----------------------------
#set start date

#--------------mm-dd-yyyy-hh-mm-ss
start_date  = '01/01/2009 00:01:00'
end_date    = '01/01/2009 23:59:00'

#---------------------------------------------
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


	#my_simulation.set_protections(protection_lib, protections)

	#my_simulation.set_anatomical_zones(anat_zones)

	#to make sure how your mesh is orientated in the space----
	#my_simulation.export_reference_frame()

	#to visualize a particular timestep-----------------------
	#my_simulation.show_one_timestep(start_date)

	#to rotate the mesh during a simulation
	#my_simulation.rotate_mesh_during_simulation()

	#to simulate a particular color
	#my_simulation.set_zone_to_simulate(cm["red"])

	#to make a whole simulation---------------------------------
	#my_simulation.make_simulation() 

	#to visualize radiance received on 3D mesh-----------------
	#my_simulation.show_one_timestep_received(600)

else:
	
	#-------------------------------------------
	#------------------GUI-----------------
	#-------------------------------------------
	window = gui.Root()
	window.mainloop()
