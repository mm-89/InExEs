import simulation as sim
import posture as ps
import sun_ray_direction as srd

#NAMELIST---------------------------------------------------------------

#POSTURE PARAMETERS--------------------------
#charging the posture by path

my_posture_file = "postures/body_low_res/BabyLowRes_01.ply"

#LIGHT SOURCE PARAMETERS---------------------
#to be defined

sun_ray_source = srd.Sun_ray_direction(latitude=45)

#SIMULATION PARAMETERS------------------------
#timestep of simulation

timestep = 60.

#DATA PARAMETERS------------------------------
#set start date

s_year = 2014
s_month = 9
s_day = 15
s_hour = 0
s_minute = 0
s_second = 0

#----------------------------------------
#set end date

e_year = 2014
e_month = 9
e_day = 16
e_hour = 0
e_minute = 0
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
								sun_ray_source)

my_simulation.make_simulation()