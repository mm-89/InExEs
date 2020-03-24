import simulation as sim
import sun_ray_direction as srd
import output as op
import matplotlib.pyplot as plt

#NAMELIST---------------------------------------------------------------

#POSTURE PARAMETERS--------------------------
#charging the posture by path

my_posture_file = "head.ply"
my_posture_folder ="postures/head_high_res"

output_name = "data"

#LIGHT SOURCE PARAMETERS---------------------
#it has to be defined

sun_ray_source = srd.Sun_ray_direction(latitude=8.1)

#SIMULATION PARAMETERS------------------------
#timestep of simulation

timestep = 60.

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

#-------------------------------------------------------------------------
#vector of current data

start_date = [s_year, s_month, s_day, s_hour, s_minute, s_second]
end_date = [e_year, e_month, e_day, e_hour, e_minute, e_second]

#-----------------------------------------

my_simulation = sim.Simulation(start_date, 
								end_date, 
								timestep, 
								my_posture_folder + "/" + my_posture_file, 
								sun_ray_source,
								start_angle_theta,
								start_angle_phi,
								output_name)

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