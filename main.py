import simulation as sim
import sun_ray_direction as srd
import posture as ps
import output as op

import matplotlib.pyplot as plt
import trimesh as tm

from tkinter import *

#-------------------------------------------
#------------------GUI-----------------
#-------------------------------------------

window = Tk()

window.title("Welcome to LikeGeeks app")

lbl = Label(window, text="InExES", font=("Arial Bold", 32))

window.geometry('500x500')

lbl.grid(column=0, row=0)





#-------------------------------------------
#------------------NAMELIST-----------------
#-------------------------------------------

#POSTURE PARAMETERS--------------------------
#choosing and charging the posture

my_data_file = "input/try.csv"

my_posture_file = "postures/cube.ply"
#my_posture_file = "postures/head_high_res/male_eyeballs_meshlab.ply"

output_name = "data"

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
start_date  = '01/01/2009 12:00:00'
end_date    = '01/02/2009 12:00:00'

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
								read_data=False,
								data_path=my_data_file,
								)

#my_simulation.set_start_angle(start_angle_azimuth)

#to make sure how your mesh is orientated in the space----
my_simulation.export_reference_frame()

#to visualize a particular timestep-----------------------
#my_simulation.show_one_timestep(start_date)

#to make a whole simulation---------------------------------
def sim():
	my_simulation.make_simulation()

def show_mesh():
	mesh = tm.load(my_posture_file)
	mesh.show()

btn = Button(window, text="start simualation", bg ="green", command=sim)
btn.grid(column=1, row=0)
btn_show = Button(window, text="show mesh", bg ="green", command=show_mesh)
btn_show.grid(column=1, row=1)
window.mainloop()

