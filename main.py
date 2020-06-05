import simulation as sim
from color_map import color_map as cm

#-------------------------------------------
#------------------NAMELIST-----------------
#-------------------------------------------
#POSTURE PARAMETERS--------------------------
#choosing and charging the posture

my_data_file = "input/irradiance_2009.csv"

my_posture_file = "postures/body_low_res/baby.ply"

output_name = "baby_armL"

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
start_date  = '01/01/2009 00:01:00'
end_date    = '01/02/2009 00:01:00'

#-------------------------------------------------------------------------

my_simulation = sim.Simulation(start_date, 
								end_date, 
								timestep, 
								my_posture_file,
								output_name,
								latitude=latitude,
								read_data=True,
								data_path=my_data_file,
								loop_on_faces=True		#0:faces;1:vertices
								)

#my_simulation.set_start_angle(start_angle_azimuth)

#to make sure how your mesh is orientated in the space----
#my_simulation.export_reference_frame()

#to visualize a particular timestep-----------------------
#my_simulation.show_one_timestep(start_date)

my_simulation.set_zone_to_simulate(cm["arm1"])

#to make a whole simulation---------------------------------
my_simulation.make_simulation()
