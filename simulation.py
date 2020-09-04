import posture as ps
import sun_ray_direction as srd
import math_refl_diff as mrd
import input_data_handle as idh
import data_map as dm
import color_map as cm
import shared_parameters as sp

import trimesh as tm
import numpy as np
import math as mt
import datetime
import time
import csv
import os
from tqdm import tqdm

from tkinter import *
from tkinter import ttk
import tkinter as tk
import gui as ui
#--------------- IMPORT FOR PYEMBREE TESTS ---------------
"""from copy import deepcopy

from pyembree import __version__ as _ver
from pyembree import rtcore_scene
from pyembree.mesh_construction import TriangleMesh

from pkg_resources import parse_version

from .ray_util import contains_points

from .. import util
from .. import caching
from .. import intersections

from ..constants import log_time"""
#--------------- IMPORT FOR PYEMBREE TESTS END ---------------

class Simulation:

	def __init__(self,
				start_date, 
				end_date, 
				timestep, 
				posture,
				output_name,
				latitude=None,
				read_data= False, 
				data_path=None
				):

		self.start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y %H:%M:%S')
		self.end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y %H:%M:%S')
    
		self.day_of_beginning = (self.start_date.date() - \
								datetime.date(self.start_date.year, 1, 1)).days + 1

		self.posture = ps.Posture(posture)
		self.beta = self.posture.get_beta

		self.start_angle_azimuth = 0.

		self.read_data = read_data

		if(self.read_data):

			self.data = []
			self.timestep = 60

			try:

				with open(data_path, mode='r') as csv_file:

					#to avoid to read header
					next(csv_file)

					#charge data line numpy array
					self.data = np.array([i for i in csv.reader(csv_file, delimiter=",",
															 quoting=csv.QUOTE_NONNUMERIC)])
					#REMEBER: probably this last matrix is a string

		    		#check if the data exists
					if(idh.is_data_exists_in_file(self.start_date, self.data)==False or \
						idh.is_data_exists_in_file(self.end_date, self.data)==False):
						print("Selected dates does not exist in the file ", data_path)
					else:
						self.start_row_data = idh.select_rows_in_file(self.start_date, self.data)
						self.end_row_data = idh.select_rows_in_file(self.end_date, self.data)
						self.total_timestep_of_simulation = self.end_row_data - self.start_row_data

						#to avoid negative values
						self.data = idh.repair_data(self.data)
			

			except IOError:

				print("File ", data_path, " don't find or don't exist.")
				print("With read data=True the file MUST be specified")

		else:

			self.timestep = timestep
			self.total_timestep_of_simulation = (self.end_date - self.start_date).total_seconds()/timestep
			if not latitude:
				print("Warning: you MUST define latitude without reading data")
			else:
				self.latitude = latitude*mt.pi/180.
				self.source_light = srd.Sun_ray_direction(latitude=self.latitude)

		self.name = posture

		self.ray_origins = self.posture.get_triangles_center
		self.face_normals = self.posture.get_normals
		self.areas = self.posture.get_area_faces
		self.faces = [i for i in range(len(self.posture.get_faces))]

		self.output_name = output_name


	def make_simulation(self):

		#some information for users
		print("")
		print("start date is: ", self.start_date.strftime("%b %d %Y %H:%M:%S"))
		print("end date is:   ", self.end_date.strftime("%b %d %Y %H:%M:%S"))
		print("Posture that has to be simulated is: ", self.name)
		print("")

		if(self.start_date > self.end_date):
			print("End date must me greater of start date!")


		#irradiance_data
		#BE CAREFUL! if the data will be cumulative, 
		#you have to move this vector outside this cycle!
		#data_output_dir = np.zeros(shape=len(self.ray_origins))
		#data_output_dif = np.zeros(shape=len(self.ray_origins))
		#data_output_ref = np.zeros(shape=len(self.ray_origins))
		
		if os.path.exists("output/" + self.output_name + ".csv"):
			os.remove("output/" + self.output_name + ".csv")

		file_out = open("output/" + self.output_name + ".csv", mode='a')
		file_writer = csv.writer(file_out, delimiter=",",
    										quoting=csv.QUOTE_NONNUMERIC)

		#write the header
		file_writer.writerow(["datetime", 
							"direct intensity [J/m^2]",
							"diffuse intensity [J/m^2]",
							"reflect intensity [J/m^2]",
							"total intensity [J/m^2]"])

		print("Start simulation...")
		print("")

		if sp.GUI_window:
			#OSVALDO'S MODIFICATIONS FOR LOADING BAR : ----------
			#loadingBarSim = tqdm(total = self.total_timestep_of_simulation, position = 0, leave = False)
			#self.process_feedback()
			self.sim_process_bar()
			self.popup_process.update()
		

		acc = 0

		start = time.time()

		if(self.read_data):

			current_line = self.start_row_data
			data_update = self.start_date

			while(current_line < self.end_row_data + 1):

				print("Current date of simulation: ", 
					data_update.strftime("%b %d %Y %H:%M:%S"))

				data_output_dir = 0
				data_output_dif = 0
				data_output_ref = 0

				rad_dir = 0
				rad_dif = 0
				rad_ref = 0 
				
				print("Percent complete: ", round(acc/self.total_timestep_of_simulation*100,1))
				#OSVALDO'S MODIFICATIONS FOR LOADING BAR : ----------
				#loadingBarSim.set_description("Simulating...".format(k))
				#loadingBarSim.update(1)
				'''if(round(k/self.total_timestep_of_simulation*100,1).is_integer()):
					self.update_value_process_bar(k/self.total_timestep_of_simulation*100)
					self.labelPercentage['text'] = "Percentage complete : " + str(round(k/self.total_timestep_of_simulation*100,1)) + "%"
				'''	
				#UPDATE POPUP FEEDBACK
				'''self.labelTimestep['text'] = "Current timestep : " + str(data_update.strftime("%b %d %Y %H:%M:%S"))
				self.labelPercentage2['text'] = "Percentage complete : " + str(round(k/self.total_timestep_of_simulation*100,1)) + "%"
				self.popupFeedback.update()'''


				#compute source rays direction
				ray_source_direction = mrd.from_polar_to_cartesian(self.data[current_line, dm.data_map["zenith"]], \
									self.data[current_line, dm.data_map["azimuth"]] - self.start_angle_azimuth)

				#compute only light days
				if(self.data[current_line, dm.data_map["zenith"]]<90.):
				
					ray_directions = [-ray_source_direction for item in range(len(self.ray_origins))]

					ray_origins = [i - j*sp.translation_factor*self.posture.get_max_bounds for i, j in zip(self.ray_origins, ray_directions)]

					#just to check
					if not len(ray_origins)==len(ray_directions):
						print("Some problems occured")
						break
			
					#compute dot product between ray direction and face normals
					proj = np.dot(self.face_normals, ray_source_direction)

					#--------------------------------------------------------
					inf = self.posture.get_posture.ray.intersects_first(ray_origins=np.array(ray_origins), 
																		ray_directions=np.array(ray_directions))
					#--------------------------------------------------------

					for k, (j, comp) in enumerate(zip(self.faces, inf)):
						if(comp==j):
							data_output_dir += abs(proj[k])*self.areas[k]

						data_output_dif += self.beta[k,0]*self.areas[k]/mt.pi

						data_output_ref += self.beta[k,1]*self.areas[k]/mt.pi
							
					rad_dir = self.data[current_line, dm.data_map["uvdirect"]]
					rad_dif = self.data[current_line, dm.data_map["uvdiffuse"]]
					rad_ref = self.data[current_line, dm.data_map["uvreflect"]]

				file_writer.writerow([data_update.strftime("%b %d %Y %H:%M:%S"),
							rad_dir*data_output_dir*self.timestep/sum(self.areas),
							rad_dif*data_output_dif*self.timestep/sum(self.areas),
							rad_ref*data_output_ref*self.timestep/sum(self.areas),
							(rad_dir*data_output_dir + \
							 rad_dif*data_output_dif + \
							 rad_ref*data_output_ref)*self.timestep/sum(self.areas)
									])
				
				data_update += datetime.timedelta(seconds=self.timestep)
				current_line += 1

				acc += 1
			if sp.GUI_window:
				#OSVALDO'S MODIFICATIONS FOR LOADING BAR : ----------
				#loadingBarSim.close()
				#self.popup_process.destroy()
				self.destroy_popup()
				self.popup_end_simulation()
		

		else:

			#reference data
			current_data = self.start_date
			current_day = self.day_of_beginning
			current_second = self.start_date.second + self.start_date.minute*60 + self.start_date.hour*3600

			while(current_data < self.end_date):

				print("Current date of simulation: ", 
					current_data.strftime("%b %d %Y %H:%M:%S"))

				data_output_dir = np.zeros(shape=len(self.ray_origins))
				data_output_dif = np.zeros(shape=len(self.ray_origins))
				data_output_ref = np.zeros(shape=len(self.ray_origins))

				rad_dir = 0
				
				print("Percent complete: ", round(acc/self.total_timestep_of_simulation*100,1))


				#compute source rays direction
				ray_source_direction = self.source_light.get_sun_direction(current_day, current_second)
				
				#check if it is daylight or not
				if(self.source_light.is_day(current_day, current_second)):

					ray_direction = [ray_source_direction for i in range(len(self.ray_origins))]

					#just to check
					if not len(self.ray_origins)==len(ray_direction):
						print("Some problems occured")
						break

					#compute dot product between ray direction and face normals
					proj = np.dot(self.face_normals, np.array([ray_source_direction]).T)

					inf = self.posture.get_posture.ray.intersects_any(ray_origins=self.ray_origins, 
																		ray_directions=ray_direction)

					for j, comp in enumerate(inf):
						if not comp:
								
							data_output_dir[j] = abs(proj[j])*self.timestep*self.areas[j]

						data_output_dif[j] = self.timestep*self.areas[j]*self.beta[j,0]

						data_output_ref[j] = self.timestep*self.areas[j]*self.beta[j,1]

						rad_dir = self.source_light.get_daily_sun_irradiance(current_day, current_second)
					
				file_writer.writerow([current_data.strftime("%b %d %Y %H:%M:%S"), 
							rad_dir*sum(data_output_dir)*self.timestep/sum(self.areas),
							0.2*rad_dir*sum(data_output_dif)*self.timestep/sum(self.areas),
							0.05*rad_dir*sum(data_output_ref)*self.timestep/sum(self.areas),
									rad_dir*(sum(data_output_dir) + \
									0.2*sum(data_output_dif) + \
									0.05*sum(data_output_ref))*self.timestep/sum(self.areas)
									])
				

				current_data += datetime.timedelta(seconds=self.timestep)
				current_second += self.timestep

				if(current_second > 86400): 
					current_second = 86400 - current_second
					current_day += 1

				acc += 1

		print("Total time of simulation: ", time.time() - start, " seconds")



	def show_one_timestep(self, date):
		print("date : ", date, type(date))

		#this just to visualize
		date_to_vis = datetime.datetime.strptime(date, '%m/%d/%Y %H:%M:%S')

		print("You are visualizing: ", date_to_vis.strftime("%b %d %Y %H:%M:%S"))

		self.day_of_beginning = (self.start_date.date() - \
								datetime.date(self.start_date.year, 1, 1)).days + 1

		current_second = self.start_date.second + self.start_date.minute*60 + self.start_date.hour*3600
		current_day = self.day_of_beginning


		#make rays of sun (direction)
		if(self.read_data):
			ray_source_direction = 	mrd.from_polar_to_cartesian(self.data[self.start_row_data, dm.data_map["zenith"]], \
									self.data[self.start_row_data, dm.data_map["azimuth"]] - self.start_angle_azimuth)
		else:
			ray_source_direction = 	self.source_light.get_sun_direction(current_day, current_second)

		ray_direction = np.array([-ray_source_direction for i in range(len(self.ray_origins))])
		
		ray_origins = np.array([i - j*sp.translation_factor*self.posture.get_max_bounds for i,j in zip(self.ray_origins, ray_direction)])

		#rays tracing
		inf = self.posture.get_posture.ray.intersects_first(ray_origins=ray_origins, 
														ray_directions=ray_direction)

		#take only non-zero components (non-zero=not hit)
		#face_nohit = np.nonzero(~inf)[0]

		#to highlithg illuminated comparet to in shadow faces
		
		black_col = [0, 0, 0]
		white_col = [255, 255, 255]

		#set white if the component is false (no hit)
		#or set black if the component is true (hit some faces)
		col_ver = []
		for j, comp in enumerate(inf):
			if(comp==j):
				col_ver.append(white_col)
			else:
				col_ver.append(black_col)

		#try to re-write a mesh
		my_new_mesh = tm.Trimesh(vertices=self.posture.get_vertices, 
								faces=self.posture.get_faces,
								process=True, 
								face_colors=col_ver)

		#if you want to visualize a ray
		#ray_visualize = tm.load_path(np.hstack((
		#ray_origins[100],
		#ray_origins[100] + ray_direction[100])).reshape(-1, 2, 3))

		scene = tm.Scene([
						my_new_mesh,
						#ray_visualize
						])

		scene.show()


	def set_start_angle(self, angle):
		self.start_angle_azimuth = angle*mt.pi/180.


	def show_one_timestep_input_irradiace(self, date):
		pass



	def export_reference_frame(self):

		path = self.name.split('/')
		mesh_name = path[-1]
		fileName = mesh_name.rsplit(".", -1)[0]

		centre = [[0, 0, 0] for i in range(len(self.ray_origins))]

		info_map = {"zenith": [0, 1, 0],
					"south": [0, 0, 1],
					"east": [1, 0, 0]}

		black_col = [0, 0, 0]
		other_color = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

		for k, item in enumerate(info_map):
			ray_direction = [info_map.get(item) for i in range(len(self.ray_origins))]
			inf = self.posture.get_posture.ray.intersects_any(ray_origins=self.ray_origins, 
																ray_directions=ray_direction)

			col_ver = []
			for comp in inf:
				if not comp:
					col_ver.append(other_color[k])
				else:
					col_ver.append(black_col)

			my_new_mesh = tm.Trimesh(vertices=self.posture.get_vertices, 
									faces=self.posture.get_faces,
									process=True, 
									face_colors=col_ver)

			tm.exchange.export.export_mesh(my_new_mesh, "output/" + "ref_frame_" + \
												fileName + "_" + item + ".ply")

		#OSVALDO'S GUI MODIFICATIONS
		if sp.GUI_window:
			self.popupmsg("Reference frame exported successfully !")

		


	
	def set_zone_to_simulate(self, RGB_map):
		"""
		Prototype: with this instance I'd like to
		select just a part f mesh (for example eyes)
		and avoid a simulation with 100% of original
		mesh - TO TEST
		Need to re-initialize beta coefficients 
		vector too - (previous error - TO TEST)
		"""
		vec_id = []
		ver = False
		compon_RGB = int(len(RGB_map) / 4)

		for k, item in enumerate(self.posture.get_faces_color):
			for i in range(compon_RGB):
				if(np.array_equal(item, RGB_map[i*4 : 4 + i*4])): 
					vec_id.append(k)
					ver = True

		if not ver:
			raise TypeError("No face/vertex with this color!")

		new_vector = []
		for item in vec_id:
			new_vector.append(self.ray_origins[item])
		self.ray_origins = new_vector

		new_normals_vector = []
		for item in vec_id:
			new_normals_vector.append(self.face_normals[item])
		self.face_normals = new_normals_vector

		new_beta_vector = np.zeros(shape=(len(vec_id), 2))
		for i, item in enumerate(vec_id):
			new_beta_vector[i] = self.beta[item, 0:2]
		self.beta = new_beta_vector

		new_area_vector = np.zeros(shape=len(vec_id))
		for i, item in enumerate(vec_id):
			new_area_vector[i] = self.areas[item]
		self.areas = new_area_vector

		new_faces_vector = []
		for item in vec_id:
			new_faces_vector.append(item)
		self.faces = new_faces_vector


	#GUI PROGRESS BAR :
	def sim_process_bar(self):
		self.popup_process = Tk()
		self.popup_process.wm_title("Simulation process...")
		#self.progressBar = ttk.Progressbar(self.popup_process, orient = 'horizontal', length = 286, mode = 'determinate')
		#self.progressBar['maximum'] = 100
		self.stopBtn = Button(self.popup_process, text="Stop Simulation", command = self.destroy_popup)
		#self.progressBar.grid(column = 1, row = 1, pady = 10)
		self.stopBtn.grid(column = 1, row = 2)

		self.labelPercentage = Label(self.popup_process, text="Simulation is processing, you can follow the progress on your terminal !")
		self.labelPercentage.grid(column = 1, row = 3, pady = 10)

	def destroy_popup(self):
    		self.popup_process.destroy()

	def popup_end_simulation(self):
		self.popupEnd = Toplevel()
		self.popupEnd.wm_title("Simulation done !")
		self.labelEnd = ttk.Label(self.popupEnd, text="Simulation ended succesfully")
		self.labelEnd.grid(column = 0 , row = 1, pady = 10)

		self.btnEnd = ttk.Button(self.popupEnd, text="Close", command = self.popupEnd.destroy)
		self.btnEnd.grid(column = 0, row = 2)
		self.popupEnd.update()

	def popupmsg(self,msg):
		popup = Tk()
		popup.wm_title("Success !")
		label = ttk.Label(popup, text=msg)
		label.pack(side="top", fill="x", pady=10)
		B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
		B1.pack()
		popup.update()

	#PLEASE DO NOT ERASE CAN BE USEFULL !
	'''def update_value_process_bar(self, value):
		self.progressBar['value'] = value
		self.progressBar.update()


	def process_feedback(self):
		self.popupFeedback = Toplevel()
		self.popupFeedback.wm_title("Simulation process...")
		self.labelTimestep = ttk.Label(self.popupFeedback, text="Current timestep : ")
		self.labelTimestep.grid(column = 0 , row = 1, pady = 10)

		self.labelPercentage2 = ttk.Label(self.popupFeedback, text="Percentage complete : ")
		self.labelPercentage2.grid(column = 0, row = 2, pady = 10)

		self.Btnstop = ttk.Button(self.popupFeedback, text="Stop Simulation", command = self.destroy_popup)
		self.Btnstop.grid(column = 0, row = 3)'''
