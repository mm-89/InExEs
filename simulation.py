import posture as ps
import sun_ray_direction as srd
import datetime
import time

class Simulation:

	def __init__(self, 
				start_date, 
				end_date, 
				timestep, 
				posture, 
				source_light
				):

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

		self.day_of_beginning = (datetime.date(start_date[0],
												start_date[1],
												start_date[2]) - \
									datetime.date(start_date[0], 
													1,
													1)).days

		self.start_second = start_date[5]
		self.timestep = timestep
		self.posture = ps.Posture(posture)
		self.source_light = source_light 

		#some information for users
		print("start date is: ", self.start_date.strftime("%b %d %Y %H:%M:%S"))
		print("end date is:   ", self.end_date.strftime("%b %d %Y %H:%M:%S"))
		print("Posture that has to be simulated is: ", posture)

	def make_simulation(self):

		#reference data
		current_data = self.start_date
		current_day = self.day_of_beginning
		current_second = self.start_second
	
		print("Start simulation...")

		start = time.time()
		while(current_data < self.end_date):

			print("Current date of simulation: ", current_data.strftime("%b %d %Y %H:%M:%S"))

			#compute source rays direction
			ray_source_direction = self.source_light.get_sun_direction(current_day, current_second)

			ray_origins = self.posture.get_vertices_barycenter + self.posture.get_normals_minimized
			ray_direction = [ray_source_direction for i in range(len(ray_origins))]

			#just to check
			if not len(ray_origins)==len(ray_direction):
				print("Some problems occured")
				break

			#ray_tracing
			inf = self.posture.get_posture.ray.intersects_any(ray_origins=ray_origins, 
														ray_directions=ray_direction)

			current_data += datetime.timedelta(seconds=self.timestep)
			current_second += self.timestep

			if(current_second > 86400): 
				current_second = 86400 - current_second
				current_day = 1

			print("day: ", current_day)
			print("second: ", current_second)

		print("Total time of simulation: ", time.time() - start, " seconds")
			#print(current_data.time())