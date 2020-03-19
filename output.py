import trimesh as tm
import numpy as np
import posture as ps

class Output:
	
	def __init__(self, posture, data):
		self.posture = ps.Posture(posture)
		self.data = data
	

		max_value = max(data)
		self.data_normalized = data/max_value
			
		self.data_rgb = []
		for j, comp in enumerate(self.data_normalized):
			self.data_rgb.append([int(self.data_normalized[j]*255), 0, 0])


	def show_data(self):
	
		new_mesh = tm.Trimesh(vertices=self.posture.get_vertices, 
								faces=self.posture.get_faces,
								process=True, 
								face_colors=self.data_rgb)	
		
		scene = tm.Scene([new_mesh])
		scene.show()

	

