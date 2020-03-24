import simulation as sim
import sun_ray_direction as srd
import os
import csv
import time
import output as op
import matplotlib.pyplot as plt

#NAMELIST---------------------------------------------------------------
#TESTS FOR CSV FILES---------------------------------------------------------------
annee = []
mois = []
jours = []
heures =  []
minutes = []
seconds = []
zeniths = []
azimuts = []
uvglobals = []
uvdiffuses = []
uvdirects = []
uvreflects = []

start = time.time()
with open('input/csv_data/irradiance 2009 example.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file)
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			print(f'Column names are {", ".join(row)}')
			line_count += 1
		annee.append({row["anne"]})
		mois.append({row["mois"]})
		jours.append({row["jour"]})
		heures.append({row["heure"]})

		minutes.append({row["min"]})
		seconds.append({row["sec"]})
		zeniths.append({row["zenith"]})
		azimuts.append({row["azimut"]})

		uvglobals.append({row["uvglobal"]})
		uvdiffuses.append({row["uvdiffuse"]})
		uvdirects.append({row["uvdirect"]})
		uvreflects.append({row["uvreflected"]})
		line_count += 1
	print(f'Processed {line_count} lines.')

print("Time taken to get all informations from CSV file : ",time.time() - start)


#POSTURE PARAMETERS--------------------------
#choosing and charging the posture by path
meshes = os.listdir("postures/head_high_res")
for i in range(len(meshes)):
	print("(", i, ")", meshes[i])

file_number = input("Choose the mesh with the associate number ( x ) ")
my_posture_file = "postures/head_high_res/"+meshes[int(file_number)]

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
								my_posture_file, 
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