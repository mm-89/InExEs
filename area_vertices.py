import trimesh as tm
import numpy as np

def compute_vertex_area(vertex_faces, area_faces):
	# vertex_faces: vector of vertex with all face index 
	# of adjancy faces [-1 means nothing, just to fill the element]

	# area_faces: vector of area of each face

	vertex_area = np.zeros(shape = len(vertex_faces))

	for i, item in enumerate(vertex_faces):
		for component in item:
			if(component != -1):
				vertex_area[i] += area_faces[component]/2.
	return vertex_area