import math as mt

class Sun_ray_direction:

	def __init__(self, latitude=45.):
		self.latitude = float(latitude)


	def set_latitude(self, latitude):
		self.latitude = float(latitude)


	def get_sun_zenith_angle(self, day, radiant=True):
		"""
		if False it gives sexagesimal angle
		"""
		k = 1.
		if not radiant:
			k = 180./mt.pi
		return sun_zenith_angle(day)*k


	def get_sun_direction(self, day, second):

		#in this way the noon is exactely in the mid
		#of the day (43200 s)
		norm_time = mt.pi*(second/43200. - 1.)

		x_comp = - mt.cos(sun_zenith_angle(day))*mt.sin(norm_time)
		y_comp = mt.sin(sun_zenith_angle(day))*mt.cos(self.latitude) - \
					mt.cos(sun_zenith_angle(day))*mt.sin(self.latitude)*mt.cos(norm_time)
		z_comp = mt.cos(sun_zenith_angle(day))*mt.cos(self.latitude)*mt.cos(norm_time) + \
					mt.sin(sun_zenith_angle(day))*mt.sin(self.latitude)

		#in trimesh axis are inverted like: x->z, y->x, z->y

		return z_comp, x_comp, y_comp

def sun_zenith_angle(day):
	"""
	day is a int from 1 to 365
	"""
	if(day<1 or day>365):
		print("Please, insert a valid value of DAY variable")

	return mt.asin(0.39795*mt.cos(0.98563*(day - 173)*mt.pi/180.))