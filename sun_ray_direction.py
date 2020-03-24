import math as mt

class Sun_ray_direction:

	def __init__(self, latitude=45.):
		self.latitude = latitude*mt.pi/180.


	def set_latitude(self, latitude):
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
