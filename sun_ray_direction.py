import math as mt

class Sun_ray_direction:

	def __init__(self, year=2000, month=1, day=1, second=0., timestep=60., lat=45.):
		"""
		day starts from 1 and finishes to 365
		"""
		self.year = year
		self.month = month
		self.day = day
		self.second = second
		self.timestep = timestep
		self.latitude = lat

	#PARAMS : self, year
	#OUTPUT : nothing
	#DESCRIPTION : define year value of the instance
	def set_year(self, year):
		self.year = year

	#PARAMS : self, month
	#OUTPUT : nothing
	#DESCRIPTION : define month value of the instance
	def set_month(self, month):
		self.month = month

	#PARAMS : self, day
	#OUTPUT : nothing
	#DESCRIPTION : define day value of the instance
	def set_day(self, day):
		self.day = day

	#PARAMS : self, second
	#OUTPUT : nothing
	#DESCRIPTION : define second value of the instance
	def set_second(self, second):
		self.second = second

	#PARAMS : self, timestep
	#OUTPUT : 
	#DESCRIPTION :
	def set_timestep(self, timestep):
		self.timestep = timestep

	#PARAMS : self, latitude
	#OUTPUT : 
	#DESCRIPTION :
	def set_latitude(self, lat):
		self.latitude = lat

	#PARAMS : self
	#OUTPUT : 
	#DESCRIPTION :
	def get_sun_zenith_angle(self):
		#for now I can use this one, but other parametritations exist
		self.sun_zenith_angle = mt.asin(0.39795*mt.cos(0.98563*(self.day - 173)*mt.pi/180.))

	#PARAMS : self, randiant (boolean)
	#OUTPUT : 
	#DESCRIPTION :
	def get_sun_zenith_angle(self, radiant=True):
		"""
		if False it gives sexagesimal angle
		"""
		k = 1.
		if not radiant:
			k = 180./mt.pi
		return sun_zenith_angle(self.day)*k

	#PARAMS : self
	#OUTPUT : 
	#DESCRIPTION :
	def get_sun_direction(self):

		norm_time = mt.pi*(self.second/43200. - 1.) # 0 at noon means cos=1
		return -mt.cos(sun_zenith_angle(self.day))*mt.sin(norm_time),\
				mt.sin(sun_zenith_angle(self.day))*mt.cos(self.latitude) - mt.cos(sun_zenith_angle(self.day))*mt.sin(self.latitude)*mt.cos(norm_time),\
				mt.cos(sun_zenith_angle(self.day))*mt.cos(self.latitude)*mt.cos(norm_time) + mt.sin(sun_zenith_angle(self.day))*mt.sin(self.latitude)


#PARAMS : day
#OUTPUT : 
#DESCRIPTION :
def sun_zenith_angle(day):
	"""
	day is a int from 1 to 365
	"""
	if(day<1 or day>365):
		print("Please, insert a valid value of DAY variable")

	return mt.asin(0.39795*mt.cos(0.98563*(day - 173)*mt.pi/180.))