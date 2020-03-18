import simulation as sim
import sun_ray_direction as srd

#NAMELIST---------------------------------------------------------------

#POSTURE PARAMETERS--------------------------
#charging the posture by path

my_posture_file = "postures/head_high_res/head.ply"

#LIGHT SOURCE PARAMETERS---------------------
#it has to be defined

sun_ray_source = srd.Sun_ray_direction(latitude=20)

#SIMULATION PARAMETERS------------------------
#timestep of simulation

timestep = 60.

#POSTURE PARAMETERS--------------------------
#need start angle

start_angle = 180.

#DATA PARAMETERS------------------------------
#set start date

s_year = 2014
s_month = 9
s_day = 15
s_hour = 12
s_minute = 0
s_second = 0

#----------------------------------------
#set end date

e_year = 2014
e_month = 9
e_day = 15
e_hour = 12
e_minute = 30
e_second = 0

#-------------------------------------------------------------------------
#vector of current data

start_date = [s_year, s_month, s_day, s_hour, s_minute, s_second]
end_date = [e_year, e_month, e_day, e_hour, e_minute, e_second]

#-----------------------------------------

my_simulation = sim.Simulation(start_date, 
								end_date, 
								timestep, 
								my_posture_file, 
								sun_ray_source,
								start_angle)

#to visualize a particular timestep
#my_simulation.show_one_timestep(start_date)

#to do a whole simulation
my_simulation.make_simulation()
