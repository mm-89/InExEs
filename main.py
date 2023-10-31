import simulation as sim
from color_map import color_map as cm
import sun_ray_direction as srd
import posture as ps

import gui

import matplotlib.pyplot as plt
import trimesh as tm

from tkinter import *
#-------------------------------------------
#------------------NAMELIST-----------------
#-------------------------------------------
#POSTURE PARAMETERS-------------------------
#choosing and charging the posture

my_data_file = "input_irradiance/June.csv"

my_posture_file = "postures/head_high_res/male_head.ply"

output_name = "eyelashes_test_1"

# PROTECTIONS PARAMETERS---------------------

protection_lib = "protections/protections_lib.xml"
protections = "protections/protections.xml"

#SIMULATION PARAMETERS-----------------------
#timestep of simulation

timestep = 60.

#GEO PARAMETERS------------------------------

latitude = 40.

#DATA PARAMETERS-----------------------------
#set start date

#--------------mm-dd-yyyy-hh-mm-ss
start_date  = '01/01/2009 00:01:00'
end_date    = '01/02/2009 00:01:00'

#---------------------------------------------

window = gui.Root()
window.mainloop()
