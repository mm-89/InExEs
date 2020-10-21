import math as mt
import numpy as np
import datetime as dt

class SunRayDirection:

	def __init__(self, latitude):
		self.latitude = np.radians(latitude)


	def get_sun_declination_angle(self, day):
		return sun_declination_angle(day)


	def checkDatesAndTimestep(self, start_date, end_date, timestep):
		"""
		Note: start and end date are strings.
		"""
		s_date = dt.datetime.strptime(start_date, '%m/%d/%Y %H:%M:%S')
		e_date = dt.datetime.strptime(end_date, '%m/%d/%Y %H:%M:%S')

		if(s_date > e_date):
			raise TypeError("End date MUST be greter or equal to start date!")

		self.tot_timestep = int((e_date - s_date).total_seconds()/timestep)
		
		self.timeline = [(s_date + dt.timedelta(seconds=timestep*i)).strftime("%b %d %Y %H:%M:%S") \
							for i in range(self.tot_timestep + 1)]
		

	def get_sun_direction(self, day, second):
		"""
		reference frame:
		z -> zenith
		y -> towards North pole
		x -> towards East

		Ref: Sproul 2006
		"""

		#in this way the noon is exactely in the mid
		#of the day (43200 s)
		norm_time = mt.pi*(second/43200. - 1.)

		x_comp = - np.cos(sun_declination_angle(day))*np.sin(norm_time)
		y_comp = np.sin(sun_declination_angle(day))*np.cos(self.latitude) - \
					np.cos(sun_declination_angle(day))*np.sin(self.latitude)*np.cos(norm_time)
		z_comp = np.cos(sun_declination_angle(day))*np.cos(self.latitude)*np.cos(norm_time) + \
					np.sin(sun_declination_angle(day))*np.sin(self.latitude)

		#in trimesh axis are inverted like: x->z, y->x, z->y
		#for such reference frame
		#we need x -> x; y -> z; z -> -y
		#IMPORTANT: so, mesh faces towards South

		return x_comp, z_comp, - y_comp


	def is_day(self, day, second):
		norm_time = mt.pi*(second/43200. - 1.)

		sza = mt.cos(sun_declination_angle(day))*mt.cos(self.latitude)*mt.cos(norm_time) + \
					mt.sin(sun_declination_angle(day))*mt.sin(self.latitude)
		if(sza>0.): 
			return True 
		else: 
			return False
		

def sun_declination_angle(day):
	"""
	day is a int from 1 to 365
	"""
	if(day<1 or day>365):
		raise TypeError("Please, insert a valid value of DAY variable")

	#ref: Ismail 2016
	#return 23.45*mt.pi/180.*mt.sin((284 + day)*360/365*mt.pi/180.))

	#ref: 
	#return mt.asin(0.39795*mt.cos(0.98563*(day - 173)*mt.pi/180.))

	#ref:
	return -23.44*mt.pi/180.*mt.cos(mt.pi/180.*360./365.*(day + 10))