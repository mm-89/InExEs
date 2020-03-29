import math as mt
import numpy as np
import datetime
import time
import csv

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

class Sun_ray_direction:

	def __init__(self, read_data= False, data_path=None, latitude=None):


		self.read_data = read_data

		if(self.read_data):

			self.data = []
			#self.timestep = 60.

			with open(data_path, mode='r') as csv_file:

				#to avoid to read header
				next(csv_file)

				#charge data line numpy array
				self.data = np.array([i for i in csv.reader(csv_file, delimiter=",",
													 quoting=csv.QUOTE_NONNUMERIC)])

		else:

			#self.timestep = timestep
			if not latitude:
				print("Warning: you MUST define latitude without reading data")
			else:
				self.latitude = latitude*mt.pi/180.

		#is_data_exists_in_file(self.start_date, self.end_date, self.data)
		"""
		self.start_date = datetime.datetime(start_date[0],
												start_date[1],
												start_date[2],
												start_date[3],
												start_date[4],
												start_date[5])
		self.end_date = datetime.datetime(end_date[0],									
												end_date[1],
												end_date[2],
												end_date[3],
												end_date[4],
												end_date[5])

		self.start_day = (datetime.date(start_date[0],
												start_date[1],
												start_date[2]) - \
												datetime.date(start_date[0], 1,	1)).days

		self.total_timestep_of_simulation = (self.end_date - \
											self.start_date).total_seconds()/timestep
		
		self.start_hour = start_date[3]
		self.start_minute = start_date[4]
		self.start_second = start_date[5]
		self.timestep = timestep
		"""
	"""
	@property
	def get_start_date(self):
		return self.start_date


	@property
	def get_end_date(self):
		return self.end_date


	@property
	def get_start_day(self):
		return self.get_start_day


	@property
	def get_start_hour(self):
		return self.get_start_hour
	

	@property
	def get_start_minute(self):
		return self.get_start_minute
	
	
	@property
	def get_start_second(self):
		return self.get_start_second
	

	@property
	def get_total_timestep_of_simulation(self):
		return self.get_self.total_timestep_of_simulation
	"""

	@property
	def get_read_data(self):
		return self.data


	def set_latitude(self, latitude):
		if(self.read_data):
			print("You must select read_data=False to select latitude!")
		else:
			self.latitude = latitude*mt.pi/180.


	def get_sun_declination_angle(self, day, radiant=True):
		"""
		if False it gives sexagesimal angle
		"""
		k = 1.
		if not radiant:
			k = 180./mt.pi
		return sun_declination_angle(day)*k


	def get_sun_direction(self, day, second):
		""""
		reference: ...
		z -> zenith
		y -> towards North pole
		x -> towards East
		"""

		#in this way the noon is exactely in the mid
		#of the day (43200 s)
		norm_time = mt.pi*(second/43200. - 1.)

		x_comp = - mt.cos(sun_declination_angle(day))*mt.sin(norm_time)
		y_comp = mt.sin(sun_declination_angle(day))*mt.cos(self.latitude) - \
					mt.cos(sun_declination_angle(day))*mt.sin(self.latitude)*mt.cos(norm_time)
		z_comp = mt.cos(sun_declination_angle(day))*mt.cos(self.latitude)*mt.cos(norm_time) + \
					mt.sin(sun_declination_angle(day))*mt.sin(self.latitude)

		#in trimesh axis are inverted like: x->z, y->x, z->y

		return x_comp, y_comp, z_comp

	def is_day(self, day, second):
		norm_time = mt.pi*(second/43200. - 1.)

		sza = mt.cos(sun_declination_angle(day))*mt.cos(self.latitude)*mt.cos(norm_time) + \
					mt.sin(sun_declination_angle(day))*mt.sin(self.latitude)
		if(sza>0.): 
			return True 
		else: 
			return False
		

	def get_sun_irradiance_in_a_day(self, day):
		#Irradiance is W/m2...
		#solar_constant
		s0 = 1362 # W/m2 at the top of the atmosphere
		return sun_irradiance_in_a_day(s0, day)


	def get_daily_sun_irradiance(self, day, second):
		#Irradiance is W/m2...
		#solar_constant
		s0 = 1362
		norm_time = mt.pi*(second/43200. - 1.)
		total_day = sun_irradiance_in_a_day(s0, day)
		sza =	mt.cos(sun_declination_angle(day))*mt.cos(self.latitude)*mt.cos(norm_time) + \
					mt.sin(sun_declination_angle(day))*mt.sin(self.latitude)
		if(sza<0.):
			return 0.
		else:
			return total_day*sza


def sun_declination_angle(day):
	"""
	day is a int from 1 to 365
	"""
	if(day<1 or day>365):
		print("Please, insert a valid value of DAY variable")

	#return mt.asin(0.39795*mt.cos(0.98563*(day - 173)*mt.pi/180.))
	return -23.44*mt.pi/180.*mt.cos(mt.pi/180.*360./365.*(day + 10))

def sun_irradiance_in_a_day(s0, day):
	return s0*(1 + 0.0339*mt.cos(2*mt.pi*day/365.25))


#to test if data selected exist in data file
def is_data_exists_in_file(start_date, end_date, data_read):

	if( start_date.year in data_read[:, data_map["year"]] \
		and start_date.month in data_read[:, data_map["month"]] \
		and start_date.day in data_read[:, data_map["day"]] \
		and start_date.hour in data_read[:, data_map["hour"]] \
		and start_date.minute in data_read[:, data_map["minute"]] ):
		print("SI")
	else:
		print("NO")