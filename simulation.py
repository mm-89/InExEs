import posture as ps
import sun_ray_direction as srd
import math_refl_diff as mrd
import protections as prt
from progressbar import *
import csvReader as cr
import outputOpt as opt

from visualization import Visualization

import trimesh as tm
import numpy as np
import math as mt
import datetime
import time
import csv
import os
#from tqdm import tqdm
import matplotlib as mpl
from color_map import color_map as cm
from vtkplotter import trimesh2vtk, show

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

class Simulation(Visualization):

	def __init__(self,
				start_date, 
				end_date, 
				timestep, 
				posture,
				output_name,
				latitude=None,
				read_data=False, 
				data_path=None
				):

		self.start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y %H:%M:%S')
		self.end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y %H:%M:%S')
    
		self.day_of_beginning = (self.start_date.date() - \
								datetime.date(self.start_date.year, 1, 1)).days + 1

		self.posture = ps.Posture(posture)
		
		# Try to correct the color code of the mesh which doesn't correspond to the
		# anatomical code
		#self.posture.correct_colors()

		self.beta = self.posture.get_beta[:,:2]

		self.face_centers = self.posture.get_triangles_center
		self.face_normals = self.posture.get_normals
		self.areas = self.posture.get_area_faces
		self.faces_index = np.arange(len(self.face_centers))

		self.IP = np.ones(self.posture.number_faces)

		self.simulate_anatomical_zones = False
		self.eye_sim = False

		self.name = posture

		self.output_name = output_name

		if(read_data):

			curr_input = cr.CsvReader(data_path)
			curr_input.checkDatesAndTimestep(start_date, end_date, timestep)

			self.timestep = timestep

			self.timeline = curr_input.timeline

			self.directions = curr_input.angles

			self.irr_dir = curr_input.irr_dir
			self.irr_dif = curr_input.irr_dif
			self.irr_ref = curr_input.irr_ref

			self.is_day = curr_input.is_day

		else:

			if(latitude==None):
				raise TypeError("With read_data=True latitude MUST be defined!")
	
			curr_input = srd.SunRayDirection(latitude)
			curr_input.checkDatesAndTimestep(start_date, end_date, timestep)

			self.timestep = timestep

			raise TypeError("Internal algorithm must be still finished")

			#self.directions = curr_input.angles

			#self.irr_dir = curr_input.irr_dir
			#self.irr_dif = curr_input.irr_dif
			#self.irr_ref = curr_input.irr_ref

			#self.is_day = curr_input.is_day

		if(self.name.split("/")[-2] == "eyes"):
			#for now simulation of left eye
			print("***")
			print("Eye-simulation configuration active")
			print("***")

			self.eye_sim = True
			self.set_zone_to_simulate(cm["red"])
			self.optk_out = opt.OutputOpt(self.output_name, 
										len(self.timeline),
										self.face_centers)

		if not os.path.exists("output"):
			os.mkdir("output")


	def make_simulation(self):

		#some information for users
		print("")
		print("start date is: ", self.start_date.strftime("%b %d %Y %H:%M:%S"))
		print("end date is:   ", self.end_date.strftime("%b %d %Y %H:%M:%S"))
		print("Posture that has to be simulated is: ", self.name)
		print("")
		
		if os.path.exists("output/{}_average.csv".format(self.output_name)):
			os.remove("output/{}_average.csv".format(self.output_name))

		if os.path.exists("output/{}_fullBody.csv".format(self.output_name)):
			os.remove("output/{}_fullBody.csv".format(self.output_name))
						
		# Average over the mesh
		file_out = open("output/{}_average.csv".format(self.output_name), mode='a')
		file_writer = csv.writer(file_out, delimiter=",",
    										quoting=csv.QUOTE_NONNUMERIC)
		
		# Full body results
		file_out_full = "output/{}_fullBody.txt".format(self.output_name)
		file_writer_full = open(file_out_full, 'w')

		header = ["datetime", 
					"direct intensity [J/m^2]",
					"diffuse intensity [J/m^2]",
					"reflect intensity [J/m^2]",
					"total intensity [J/m^2]"]

		#write the header
		file_writer.writerow(header)

		if (self.simulate_anatomical_zones):
			#for now just sub_files, no interset files

			for item in self.currAnatZone.get_total_zones_name():
				#delete old files
				curr_file = "output/{}_{}.csv".format(self.output_name, item)

				#delete old files
				if os.path.exists("{}".format(curr_file)):
					os.remove("{}".format(curr_file))

				#define variables
				exec("file_out_%s = open('%s', 'w')" % (item, curr_file))
				exec("file_writer_%s = csv.writer(file_out_%s, delimiter=',', \
    										quoting=csv.QUOTE_NONNUMERIC)" % (item, item))
				exec("file_writer_%s.writerow(%s)" % (item, header))

		print("Start simulation...")
		print("")


		#OSVALDO'S MODIFICATIONS FOR LOADING BAR : ----------
		#loadingBarSim = tqdm(total = self.total_timestep_of_simulation, position = 0, leave = False)
		#self.process_feedback()
		self.sim_process_bar()
		self.popup_process.update()
		
		start = time.time()

		area_tot = np.sum(self.areas)
		dimlines = len(self.timeline) + 1	
		full_body_time = np.zeros((dimlines, np.shape(self.face_centers)[0]))

		#for check anatomical zones
		check_area_NO_valid = False
	
		for k, item in enumerate(self.timeline):
				
			progress_bar(k, dimlines)
				
			# Total dose distributed on the mesh faces [J/m2]
			data_output_total = np.zeros(np.shape(self.face_centers)[0])
						
			# Direct, difffuse and reflected doses averaged over the mesh [J/m2]

			data_output_dir = np.zeros(np.shape(self.face_centers)[0])
			data_output_dif = 0
			data_output_ref = 0
				
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

			#compute only light days
			if(self.is_day[k]):	
	
				ray_directions = np.ones((np.shape(self.face_centers)[0], 3))*(-self.directions[k])
				ray_origins = self.face_centers - ray_directions*self.posture.get_max_bounds


				#compute dot product between ray direction and face normals
				proj = np.dot(self.face_normals,self.directions[k])
					
				# Set to zero if negative, i.e. coming from more than pi/2
				proj[proj<0.] = 0.
					
				#--------------------------------------------------------
				inf = self.posture.get_posture.ray.intersects_first(ray_origins=np.array(ray_origins), 
																	ray_directions=np.array(ray_directions))
				#--------------------------------------------------------

				expo_mask = (inf==self.faces_index)

				data_output_total[expo_mask] += proj[expo_mask] * self.irr_dir[k]
				data_output_total += self.beta[:,0]/mt.pi * self.irr_dif[k]
				data_output_total += self.beta[:,1]/mt.pi * self.irr_ref[k]
				data_output_total *= self.timestep
				data_output_total /= self.IP
					
				full_body_time[k] = data_output_total

				if(self.eye_sim):
					self.optk_out.save_output(self.irr_dir[k], ray_directions)

				data_output_dir[expo_mask] += proj[expo_mask]*self.areas[expo_mask]/self.IP[expo_mask]
				data_output_dif = self.beta[:,0]*self.areas/mt.pi/self.IP
				data_output_ref = self.beta[:,1]*self.areas/mt.pi/self.IP
				
			file_writer.writerow([item,
						float(self.irr_dir[k])*np.sum(data_output_dir)*self.timestep/area_tot,
						float(self.irr_dif[k])*np.sum(data_output_dif)*self.timestep/area_tot,
						float(self.irr_ref[k])*np.sum(data_output_ref)*self.timestep/area_tot,
						(float(self.irr_dir[k])*np.sum(data_output_dir) + \
						 float(self.irr_dif[k])*np.sum(data_output_dif) + \
						 float(self.irr_ref[k])*np.sum(data_output_ref))*self.timestep/area_tot])

			#anatomical zones
			if(self.simulate_anatomical_zones):

				data_partial_dir = 0
				data_partial_dif = 0
				data_partial_ref = 0

				for name in self.currAnatZone.get_total_zones_name():

					if(self.is_day[k]):

						expo_mask_anatZones = self.currAnatZone.get_zone_mask(name)

						zone_area = np.sum(self.areas[expo_mask_anatZones])

						if(zone_area != 0):

							data_partial_dir = float(self.irr_dir[k])*np.sum(data_output_dir[expo_mask_anatZones])/zone_area
							data_partial_dif = float(self.irr_dif[k])*np.sum(data_output_dif[expo_mask_anatZones])/zone_area
							data_partial_ref = float(self.irr_ref[k])*np.sum(data_output_ref[expo_mask_anatZones])/zone_area

						else: check_area_NO_valid = True

					exec("file_writer_%s.writerow([item, \
								data_partial_dir*self.timestep, \
								data_partial_dif*self.timestep, \
								data_partial_ref*self.timestep, \
								(data_partial_dir+data_partial_dif+data_partial_ref)*self.timestep])" % name)


		if(self.simulate_anatomical_zones and check_area_NO_valid): 
			print("Some zones selected don't exist! Area = 0!!!")

		np.savetxt(file_out_full, full_body_time, fmt='%4.8f')

		if(self.eye_sim):
			self.optk_out.export_file()

		#OSVALDO'S MODIFICATIONS FOR LOADING BAR : ----------
		#loadingBarSim.close()
		#self.popup_process.destroy()
		self.destroy_popup()
		self.popup_end_simulation()

		print("\nTotal time of simulation: {:.1f} seconds".format(time.time() - start))


	def set_protections(self, protection_lib, protections):
		self.IP = prt.get_IP(protection_lib, protections, self.posture)

	def set_anatomical_zones(self, path):
		self.simulate_anatomical_zones = False
		self.currAnatZone = anatZone.AnatomicalZones(path, self.posture)

	def show_one_timestep(self, date):

		# Visualize the exposed zones for one time step
		
		date_to_vis = datetime.datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
		print("You are visualizing: ", date_to_vis.strftime("%b %d %Y %H:%M:%S"))

		ind_date_to_vis = np.where( date_to_vis.strftime("%b %d %Y %H:%M:%S") == np.array(self.timeline) )[0][0]

		ray_directions = self.directions[ind_date_to_vis]

		ray_directions = -np.ones((self.posture.number_faces, 3))*ray_directions
		ray_origins = self.posture.get_triangles_center - \
		ray_directions*self.posture.get_max_bounds

		inf = self.posture.get_posture.ray.intersects_first(ray_origins= ray_origins, 
															ray_directions= ray_directions)

		expo_mask = ( inf==np.arange(self.posture.number_faces) )

		col = np.zeros((self.posture.number_faces, 3)) # Black color
		col[ expo_mask ] = [255, 255, 255] #White color
		
		vtkmeshes = trimesh2vtk(self.posture.get_posture)
		vtkmeshes.cellColors(col, cmap='Greys_r')
		show(vtkmeshes)

		# Add a ray and the reference frame
		
#		ray_or = self.posture.get_triangles_center[100]-ray_directions[100]*3
#		ray_visualize = tm.load_path(np.hstack((
#		ray_or,
#		ray_or + ray_directions[100])).reshape(-1, 2, 3))

#		xaxis = tm.load_path(np.array([[1,0,0],[2,0,0]]).reshape( 2, 3))
#		yaxis = tm.load_path(np.array([[1,0,0],[1,1,0]]).reshape( 2, 3))
#		zaxis = tm.load_path(np.array([[1,0,0],[1,0,1]]).reshape( 2, 3))
		
#		scene = tm.Scene([
#						my_new_mesh,
#						ray_visualize,
#							xaxis, yaxis, zaxis
#						])

#		bounds_no = float(np.linalg.norm(self.posture.get_posture.extents[0]))
#		scene.set_camera(angles=(0.,0.,0.), distance=4.*bounds_no, fov=(30.,50.))

#		scene = tm.Scene([my_new_mesh])
#		scene.show()


	def show_face_colors(self):

		print("You are visualizing the anatonomical zones.")
		
		# show the zone color
		col = self.posture.get_faces_color
		
		#try to re-write a mesh
		my_new_mesh = tm.Trimesh(vertices=self.posture.get_vertices, 
								faces=self.posture.get_faces,
								process=True, 
								face_colors=col)

		my_new_mesh.export(file_obj='postures/{}_new-face-colors.ply'.format(self.output_name), file_type='ply')
		
		scene = tm.Scene([my_new_mesh])
		scene.show()
		
		
	def show_IP(self):
		
		# Show where there is protection
		IP_vis = self.IP-1
		norm = mpl.colors.Normalize(vmin=np.amin(IP_vis), vmax=np.amax(IP_vis))
		
		scalarMap = cm.ScalarMappable(norm=norm, cmap=cm.get_cmap('jet'))
		
		#try to re-write a mesh
		my_new_mesh = tm.Trimesh(vertices=self.posture.get_vertices, 
								faces=self.posture.get_faces,
								process=True, 
								face_colors=scalarMap.to_rgba(IP_vis))

		my_new_mesh.export(file_obj='{}{}_IP.ply'.format(self.output_file, self.output_name), file_type='ply')

		scene = tm.Scene([my_new_mesh])

#		bounds_no = float(np.linalg.norm(self.posture.get_posture.extents[0]))
#		scene.set_camera(angles=(-np.pi/8.,0.,0.),distance=3.3*bounds_no,\
#											    fov=(30.,50.))
		scene.show()
		
		
	def save_simu_timespan(self, begin_date, duration='00 02 00', vis_timestep=5.):
		
		try:
		
			result_path = "{}{}_fullBody.txt".format(self.output_file, self.output_name)
			
			if not os.path.exists("{}images".format(self.output_file)):
				os.mkdir("{}images".format(self.output_file))
			
			# Check if the simulation results exist
			with open(result_path, mode='r') as txt_file:
		
				begin_datetime = datetime.datetime.strptime(begin_date, '%m/%d/%Y %H:%M:%S')
				
				# duration in 'days hours minutes'
				iduration = int((float(duration[-2:])*60. + float(duration[-5:-3])*3600. + \
							float(duration[:-6])*24*3600.) / self.timestep) #in indices
				ibegin = idh.select_rows_in_file(begin_datetime, self.data)
				iend = ibegin+iduration
				
				# vis_timestep in minutes
				itimestep = int(vis_timestep*60./self.timestep)
				
				# Check if the time range requested as been simulated
				# using the indices of the full data file
				if ibegin<self.start_row_data or iend > self.end_row_data:
					print('Selected time range out of the simulated one.')
				else:
					
					# retrieve the simulated data using its own indices
					# only on the requested time range
					ibegin_sim = ibegin-self.start_row_data
					iend_sim = iend-self.start_row_data
					
					sim_res = np.array([temp.split() for temp in \
							txt_file.readlines()[ibegin_sim:iend_sim]]).astype(float)
					
					norm = mpl.colors.Normalize(vmin=0.,\
									    vmax=np.amax(sim_res)) #np.amin(sim_res)
		
					scalarMap = cm.ScalarMappable(norm=norm, cmap=cm.get_cmap('jet')) #cmap_Palwilch)
		
					fig = mpl.pyplot.figure()
					ax = fig.add_subplot(111)
					mpl.pyplot.colorbar(scalarMap, ax=ax)
					mpl.pyplot.show()
					
					data_update = begin_datetime
					
					bounds_no = float(np.linalg.norm(self.posture.get_posture.extents[0]))
						
					# Start from 0 because imported only the requested results
					for idata in range(0):#, iduration, itimestep):
						my_new_mesh = tm.Trimesh(vertices=self.posture.get_vertices, 
													faces=self.posture.get_faces,
													process=True,
													face_colors=scalarMap.to_rgba(sim_res[idata])[:,:-1])
													
						my_new_mesh.export(file_obj='{}{}_{:03d}.ply'.format(self.output_file, \
						 self.output_name, idata), file_type='ply')
						
						scene = tm.Scene([my_new_mesh])
						scene.set_camera(angles=(-np.pi/8.,0.,0.),distance=3.3*bounds_no,\
											    fov=(30.,50.))
						impng = scene.save_image()
		
						out_file = open("{}images/{}_{}.png".format(self.output_file,\
								  self.output_name, data_update.strftime("%Y %b %d %H:%M:%S")), "wb")
						out_file.write(impng)
						out_file.close()
		
						np.savetxt('{}{}_val_{:03d}.txt'.format(self.output_file,\
								  self.output_name, idata), sim_res[idata], fmt='%4.3f')
						
						data_update += datetime.timedelta(minutes=vis_timestep)
							
		except IOError:
		
			print("File {} don't find or don't exist.".format(result_path))


	def export_reference_frame(self):

		info_map = {"zenith": [0, 1, 0],
					"south": [0, 0, 1],
					"east": [1, 0, 0]}

		other_color = [[255, 0, 0], [0, 255, 0], [0, 0, 255]]

		for k, item in enumerate(info_map):

			color_storage = np.zeros((self.posture.number_faces, 3))
			curr_color = np.ones((self.posture.number_faces, 3))*other_color[k]

			ray_origins = self.posture.get_triangles_center + \
				np.ones((self.posture.number_faces, 3))*info_map.get(item)*self.posture.get_max_bounds

			ray_directions = -np.ones((self.posture.number_faces, 3))*info_map.get(item)

			inf = self.posture.get_posture.ray.intersects_first(ray_origins=ray_origins, 
																ray_directions=ray_directions)

			expo_mask = ( inf==np.arange(self.posture.number_faces) )

			color_storage[expo_mask] += curr_color[expo_mask]

			my_new_mesh = tm.Trimesh(vertices=self.posture.get_vertices, 
									faces=self.posture.get_faces,
									process=True, 
									face_colors=color_storage)

			tm.exchange.export.export_mesh(my_new_mesh, 
				"output/ref_frame_{}_{}.ply".format(self.output_name, item))

		#OSVALDO'S GUI MODIFICATIONS
		self.popupmsg("Reference frame exported successfully!")

		
	def set_zone_to_simulate(self, RGB_map):

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

		self.face_centers = [self.face_centers[item] for item in vec_id]
		self.face_normals = [self.face_normals[item] for item in vec_id]
		self.beta = np.array([self.beta[item] for item in vec_id])
		self.areas = np.array([self.areas[item] for item in vec_id])
		self.faces_index = np.copy(vec_id)
		self.IP = np.ones(np.shape(self.face_centers)[0])

		#for item in vec_id:
		#	new_vector.append(self.face_centers[item])
		#self.face_centers = new_vector

		#new_normals_vector = []
		#for item in vec_id:
		#	new_normals_vector.append(self.face_normals[item])
		#self.face_normals = new_normals_vector

		#new_beta_vector = np.zeros(shape=(len(vec_id), 2))
		#for i, item in enumerate(vec_id):
		#	new_beta_vector[i] = self.beta[item, 0:2]
		#self.beta = new_beta_vector

		#new_area_vector = np.zeros(shape=len(vec_id))
		#for i, item in enumerate(vec_id):
		#	new_area_vector[i] = self.areas[item]
		#self.areas = new_area_vector

		#new_faces_vector = []
		#for item in vec_id:
		#	new_faces_vector.append(item)
		#self.faces_index = new_faces_vector


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
