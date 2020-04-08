import posture as ps
import sun_ray_direction as srd
import math_refl_diff as mrd

import trimesh as tm
import numpy as np
import math as mt
import datetime
import time
import csv
import os

class Simulation:

	def __init__(self,
				start_date, 
				end_date, 
				timestep, 
				posture,
				N,
				output_name,
				latitude=None,
				read_data= False, 
				data_path=None,
				):

		self.start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y %H:%M:%S')
		self.end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y %H:%M:%S')
    
		
		first_day_of_year = datetime.date(self.start_date.year, 1, 1)
		self.day_of_beginning = (self.start_date.date() - first_day_of_year).days + 1

		self.posture = ps.Posture(posture, N)

		self.start_angle_azimuth = 0.

		self.read_data = read_data

		if(self.read_data):

			self.data = []
			self.timestep = 60.

			try:

				with open(data_path, mode='r') as csv_file:

					#to avoid to read header
					next(csv_file)

					#charge data line numpy array
					self.data = np.array([i for i in csv.reader(csv_file, delimiter=",",
															 quoting=csv.QUOTE_NONNUMERIC)])
					#REMEBER: probably this last matrix is a string

		    		#check if the data exists
					if(is_data_exists_in_file(self.start_date, self.data)==False or \
						is_data_exists_in_file(self.end_date, self.data)==False):
						print("Selected dates does not exist in the file ", data_path)
					else:
						self.start_row_data = select_rows_in_file(self.start_date, self.data)
						self.end_row_data = select_rows_in_file(self.end_date, self.data)
						print(type(self.start_row_data), type(self.end_row_data))
						self.total_timestep_of_simulation = self.end_row_data - self.start_row_data

						#to avoid negative values
						self.data = repair_data(self.data)
			

			except IOError:

				print("File ", data_path, " don't found or don't exist.")
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

		self.ray_origins = self.posture.get_vertices_barycenter + \
	    					self.posture.get_normals_minimized

		self.output_name = output_name


	def make_simulation(self):

		#note: True for now doesn't well work
		method_red = False

		#some information for users
		print("")
		print("start date is: ", self.start_date.strftime("%b %d %Y %H:%M:%S"))
		print("end date is:   ", self.end_date.strftime("%b %d %Y %H:%M:%S"))
		print("Posture that has to be simulated is: ", self.name)
		print("")

		if(self.start_date > self.end_date):
			print("End date must me after of start date!")


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
		#file_writer.writerow( ["datetime", *[i for i in range(len(self.ray_origins))]] )
		file_writer.writerow(["datetime", 
							"direct intensity [J/m²]",
							"diffuse intensity [J/m²]",
							"reflect intensity [J/m²]",
							"total intensity [J/m²]"])

		print("Start simulation...")
		print("")

		k = 0

		start = time.time()

		if(self.read_data):

			current_line = self.start_row_data
			data_update = self.start_date

			while(current_line < self.end_row_data + 1):

				print("Current date of simulation: ", 
					data_update.strftime("%b %d %Y %H:%M:%S"))

				data_output_dir = np.zeros(shape=len(self.ray_origins))
				data_output_dif = np.zeros(shape=len(self.ray_origins))
				data_output_ref = np.zeros(shape=len(self.ray_origins))
				
				print("Percent complete: ", round(k/self.total_timestep_of_simulation*100,1))

				#compute source rays direction
				ray_source_direction = mrd.from_polar_to_cartesian(self.data[current_line, data_map["zenith"]], \
									self.data[current_line, data_map["azimuth"]] - self.start_angle_azimuth)
				
				#Here put the algorithm to split at te next light day
				if(True):

					ray_direction = [ray_source_direction for i in range(len(self.ray_origins))]

					#just to check
					if not len(self.ray_origins)==len(ray_direction):
						print("Some problems occured")
						break

					#compute dot product between ray direction and face normals
					proj = np.dot(self.posture.get_normals, np.array([ray_source_direction]).T)

					inf = self.posture.get_posture.ray.intersects_any(ray_origins=self.ray_origins, 
																ray_directions=ray_direction)

					for j, comp in enumerate(inf):
						if not comp:
	
							data_output_dir[j] = self.data[current_line, data_map["uvdirect"]]*abs(proj[j])*self.timestep*\
									self.posture.get_area_faces[j]/(self.data[current_line, data_map["zenith"]]*mt.pi/180.)

						data_output_dif[j] = self.data[current_line, data_map["uvdiffuse"]]*self.timestep*\
										self.posture.get_area_faces[j]*self.posture.get_beta[j,0]

						data_output_ref[j] = self.data[current_line, data_map["uvreflect"]]*self.timestep*\
										self.posture.get_area_faces[j]*self.posture.get_beta[j,1]


				file_writer.writerow([data_update.strftime("%b %d %Y %H:%M:%S"), 
									sum(data_output_dir)/self.posture.get_total_area,
									sum(data_output_dif)/self.posture.get_total_area,
									sum(data_output_ref)/self.posture.get_total_area,
									(sum(data_output_dir) + sum(data_output_dif) + sum(data_output_ref))/self.posture.get_total_area
									])
			
				data_update += datetime.timedelta(seconds=self.timestep)
				current_line += 1

				k += 1

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
				
				print("Percent complete: ", round(k/self.total_timestep_of_simulation*100,1))

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
					proj = np.dot(self.posture.get_normals, np.array([ray_source_direction]).T)

					if(method_red):

						inf = []
							
						for j, lis in enumerate(proj):

							# given faces' normals and sun direction (normal as well)
							# if the dot product is negative means shadow
							if(lis > 0.):
								#ray_tracing
								inf.append( self.posture.get_posture.ray.intersects_any(ray_origins=np.array([self.ray_origins[j]]), 
																		ray_directions=np.array([ray_source_direction])) )
							else:
								inf.append(False)
											
							#means the face j
							#this is cumulative irradiance dose (energy -> J/Hz)
							data_output_dir[j] += self.source_light.get_daily_sun_irradiance(current_day, current_second)*\
												abs(proj[j])*self.posture.get_area_faces[j]*self.timestep
			
					else:

						inf = self.posture.get_posture.ray.intersects_any(ray_origins=self.ray_origins, 
																		ray_directions=ray_direction)

						for j, comp in enumerate(inf):
							if not comp:
								
								data_output_dir[j] = self.source_light.get_daily_sun_irradiance(current_day, current_second)*\
											abs(proj[j])*self.timestep*self.posture.get_area_faces[j]

							data_output_dif[j] = self.source_light.get_daily_sun_irradiance(current_day, current_second)*\
											0.2*abs(proj[j])*self.timestep*self.posture.get_area_faces[j]*\
											self.posture.get_beta[j,0]

							data_output_ref[j] = self.source_light.get_daily_sun_irradiance(current_day, current_second)*\
											0.05*abs(proj[j])*self.timestep*self.posture.get_area_faces[j]*\
											self.posture.get_beta[j,1]


				file_writer.writerow([current_data.strftime("%b %d %Y %H:%M:%S"), 
									sum(data_output_dir)/self.posture.get_total_area,
									sum(data_output_dif)/self.posture.get_total_area,
									sum(data_output_ref)/self.posture.get_total_area,
									(sum(data_output_dir) + sum(data_output_dif) + sum(data_output_ref))/self.posture.get_total_area
									])
				

				current_data += datetime.timedelta(seconds=self.timestep)
				current_second += self.timestep

				if(current_second > 86400): 
					current_second = 86400 - current_second
					current_day += 1

				k += 1

		print("Total time of simulation: ", time.time() - start, " seconds")



	def show_one_timestep(self, date, show_result=True):

		method_red = False

		#this just to visualize
		date_to_vis = datetime.datetime.strptime(date, '%m/%d/%Y %H:%M:%S')

		print("You are visualizing: ", date_to_vis.strftime("%b %d %Y %H:%M:%S"))

		first_day_of_year = datetime.date(self.start_date.year, 1, 1)
		self.day_of_beginning = (self.start_date.date() - first_day_of_year).days + 1

		current_second = self.start_date.second + self.start_date.minute*60 + self.start_date.hour*3600
		current_day = self.day_of_beginning

		#make rays of sun (direction)
		if(self.read_data):
			ray_source_direction = 	mrd.from_polar_to_cartesian(self.data[self.start_row_data, data_map["zenith"]], \
									self.data[self.start_row_data, data_map["azimuth"]] - self.start_angle_azimuth)
			print(ray_source_direction)
		else:
			ray_source_direction = 	self.source_light.get_sun_direction(current_day, current_second)
			print(ray_source_direction)

		#ay_source_direction = [0, 1, 0]

		ray_direction = [ray_source_direction for i in range(len(self.ray_origins))]

		if(method_red):

			inf = []
			proj = np.dot(self.posture.get_normals, np.array([ray_source_direction]).T)
			
			for j, lis in enumerate(proj):

				# given faces' normals and sun direction (normal as well)
				# if the dot product is negative means shadow
				if(lis < 0.):
					#ray_tracing
					inf.append( self.posture.get_posture.ray.intersects_any(ray_origins=np.array([self.ray_origins[j]]), 
														ray_directions=np.array([ray_source_direction])) )
				else:
					inf.append(False)

		else:

			#rays tracing
			inf = self.posture.get_posture.ray.intersects_any(ray_origins=self.ray_origins, 
															ray_directions=ray_direction)

		#take only non-zero components (non-zero=not hit)
		#face_nohit = np.nonzero(~inf)[0]

		#to highlithg illuminated comparet to in shadow faces
		
		black_col = [0, 0, 0]
		white_col = [255, 255, 255]

		#set white if the component is false (no hit)
		#or set black if the component is true (hit some faces)
		col_ver = []
		for comp in inf:
			if not comp:
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

		if(show_result): scene.show()


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

			tm.exchange.export.export_mesh(my_new_mesh, "output/" + fileName + \
												"_" + item + ".ply")

	def set_start_angles(self, angle):
		self.start_angle_azimuth = angle*mt.pi/180.

#IMPORTANT

#output_dir = "output"
#file_out = "my_test_mesh"
#extension = "ply"

#to export a mesh - it works
#tm.exchange.export.export_mesh(my_new_mesh, file_out + "." + extension)

#other important thing:
#face_nohit = np.nonzero(~inf)[0]

#global map for read data

data_map = {"year": 0,
			"month": 1,
			"day": 2,
			"hour": 3,
			"minute": 4,
			"zenith": 5,
			"azimuth": 6,
			"uvglobal": 7,
			"uvdiffuse": 8,
			"uvdirect": 9,
			"uvreflect": 10}

#------------------------------

#to test if data selected exist in data file
def is_data_exists_in_file(date, data_read):
	#NEED to re-scale????????
	if( date.year in data_read[:, data_map["year"]] \
		and date.month in data_read[:, data_map["month"]] \
		and date.day in data_read[:, data_map["day"]] \
		and date.hour in data_read[:, data_map["hour"]] \
		and date.minute in data_read[:, data_map["minute"]] ):
		return True
	else:
		return False

def select_rows_in_file(date, data_read):
	val = None
	my_vect_prop = np.array([date.year,
							date.month,
							date.day,
							date.hour,
							date.minute])
	for j, item in enumerate(data_read):
		if np.array_equal(item[:5], my_vect_prop) :
			val = j
	return val

def repair_data(data_read):
	"""
	Sometimes input data has negative values (WHY?)
	If a value is negative I have to put to zero
	"""
	print("Start to repair data")

	for j, item in enumerate(data_read[:, data_map["uvglobal"]]):
		if(item < 0): data_read[j, data_map["uvglobal"]] = 0

	for j, item in enumerate(data_read[:, data_map["uvdiffuse"]]):
		if(item < 0): data_read[j, data_map["uvdiffuse"]] = 0

	for j, item in enumerate(data_read[:, data_map["uvdirect"]]):
		if(item < 0): data_read[j, data_map["uvdirect"]] = 0

	for j, item in enumerate(data_read[:, data_map["uvreflect"]]):
		if(item < 0): data_read[j, data_map["uvreflect"]] = 0

	return data_read
