import posture as ps
import sun_ray_direction as srd

import trimesh as tm
import numpy as np
import datetime
import time

class Simulation:

	def __init__(self, 
                start_date, 
		    	end_date, 
				timestep, 
				posture, 
				source_light,
				start_angle
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
	    self.start_angle = start_angle

	    self.ray_origins = self.posture.get_vertices_barycenter + \
	    					self.posture.get_normals_minimized


	def make_simulation(self):

		method_red = True

		#some information for users
		print("")
		print("start date is: ", self.start_date.strftime("%b %d %Y %H:%M:%S"))
		print("end date is:   ", self.end_date.strftime("%b %d %Y %H:%M:%S"))
		print("Posture that has to be simulated is: ", self.posture)
		print("")

		#reference data
		current_data = self.start_date
		current_day = self.day_of_beginning
		current_second = self.start_second

		if(self.start_date > self.end_date):
			print("End date must me after of start date!")
	
		print("Start simulation...")
		print("")

		start = time.time()
		while(current_data < self.end_date):

			print("Current date of simulation: ", current_data.strftime("%b %d %Y %H:%M:%S"))

			#compute source rays direction
			ray_source_direction = self.source_light.get_sun_direction(current_day, current_second)

			ray_direction = [ray_source_direction for i in range(len(self.ray_origins))]

			#just to check
			if not len(self.ray_origins)==len(ray_direction):
				print("Some problems occured")
				break

			if(method_red):

				for j, comp in enumerate(self.posture.get_normals):

					proj = np.dot(np.array([comp]), np.array([ray_source_direction]).T)

					# given faces' normals and sun direction (normal as well)
					# if the dot product is negative means shadow
					if(proj > 0.):

						#ray_tracing
						inf = self.posture.get_posture.ray.intersects_any(ray_origins=np.array([self.ray_origins[j]]), 
															ray_directions=np.array([ray_source_direction]))
			else:

				inf = self.posture.get_posture.ray.intersects_any(ray_origins=self.ray_origins, 
														ray_directions=ray_direction)
		
			current_data += datetime.timedelta(seconds=self.timestep)
			current_second += self.timestep

			if(current_second > 86400): 
				current_second = 86400 - current_second
				current_day = 1

		print("Total time of simulation: ", time.time() - start, " seconds")


	def show_one_timestep(self, date, show_result=True):
		#this just to visualize
		date_to_vis = datetime.datetime(date[0], date[1], date[2], date[3], date[4], date[5])

		print("You are visualizing: ", date_to_vis.strftime("%b %d %Y %H:%M:%S"))

		number_of_days = (datetime.date(date[0],
											date[1],
											date[2]) - \
											datetime.date(date[0], 1, 1)).days

		#make rays of sun (direction)
		ray_source_direction = self.source_light.get_sun_direction(number_of_days, date[5])
		ray_direction = [ray_source_direction for i in range(len(self.ray_origins))]

		#rays tracing
		inf = self.posture.get_posture.ray.intersects_any(ray_origins=self.ray_origins, 
														ray_directions=ray_direction)

		#take only non-zero components (non-zero=not hit)
		face_nohit = np.nonzero(~inf)[0]

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

#IMPORTANT

#output_dir = "output"
#file_out = "my_test_mesh"
#extension = "ply"

#to export a mesh - it works
#tm.exchange.export.export_mesh(my_new_mesh, file_out + "." + extension)

#other important thing:
#face_nohit = np.nonzero(~inf)[0]