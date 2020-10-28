import trimesh as tm
import numpy as np
import math as mt
from vtkplotter import trimesh2vtk, show

from scipy.spatial.distance import cdist

from progressbar import *

def dirc_cos(v1, v2):
	"""
	Note: v1 and v2 -> (n, 3)
	
	norm = np.linalg.norm(v2 - v1)

	x = (v2[0] - v1[0])/norm
	y = (v2[1] - v1[1])/norm
	z = (v2[2] - v1[2])/norm
	"""
	return (v2 - v1)/np.linalg.norm(v2 - v1)


def translate_mesh(translate_vec, curr_mesh):

	translation_matrix = [ [1, 0, 0, translate_vec[0]], 
									[0, 1, 0, translate_vec[1]],
									[0, 0, 1, translate_vec[2]],
									[0, 0, 0, 1] ]

	curr_vertices = np.append( np.array(curr_mesh.vertices), np.ones((len(curr_mesh.vertices),1)), axis=1 )
	new_vertices = np.dot( translation_matrix, curr_vertices.T).T
	new_vertices = np.delete(new_vertices, 3, 1)
	return tm.Trimesh(vertices=new_vertices, faces=curr_mesh.faces, process=True)


class ArtificialLight:

	n_plane = 25

	def __init__(self, posture):

		self.myPosture = tm.load(posture)

		self.triangles_center = self.myPosture.triangles_center
		self.triangles_normal = np.array(self.myPosture.face_normals)
		self.triangle_area = np.array(self.myPosture.area_faces)


	def add_point_source(self, coordinates, irradiance_level, total_time):

		self.origin = [coordinates]
		sphere = tm.creation.icosphere(subdivisions=3, radius=0.5, color=[255, 255, 255])
		self.posture_of_sources = translate_mesh(coordinates, sphere)

		self.irr = irradiance_level
		self.total_time = total_time


	def add_extended_source(self, path, coordinates, irradiance_level, total_time):

		posture_of_sources = tm.load(path)

		self.posture_of_sources = translate_mesh(coordinates,	posture_of_sources)
		self.origin = self.posture_of_sources.triangles_center

		self.irr = irradiance_level
		self.total_time = total_time


	def show_scenario(self):

		vtkmeshes = trimesh2vtk(self.myPosture)
		vtksource = trimesh2vtk(self.posture_of_sources)

		show(vtkmeshes, vtksource)


	def make_simulation(self):

		self.irr_rcv = np.zeros(len(self.triangles_center))
		
		for k, source_point in enumerate(self.origin):

			progress_bar(k, len(self.origin))

			ray_origins = np.ones((len(self.triangles_center), 3))*source_point
			dot_prod = np.dot(self.triangles_normal, source_point)

			directions = [dirc_cos(source_point, i) for i in self.triangles_center]
			distances = np.array([np.linalg.norm(source_point - i) for i in self.triangles_center])

			# diffuse part of beta coefficient ----------------------------------------
			res = self.myPosture.ray.intersects_first(ray_origins=ray_origins, 
														ray_directions=directions)
			
			#ind = np.unique( res_diff, return_counts=False)
			#print(ind)
			#ind = np.delete(ind, np.where( ind==-1 ))
			

			self.irr_rcv[ res ] += self.irr*self.total_time*np.abs( dot_prod[ res ] )/distances[ res ]**2/len(self.origin)


	def show_results(self, show_sources=True):

		vtkmeshes = trimesh2vtk(self.myPosture)

		vtkmeshes.cellColors(self.irr_rcv, cmap='jet')
		vtkmeshes.addScalarBar(title="J/m^2")

		if(show_sources):
			vtksource = trimesh2vtk(self.posture_of_sources)
			show(vtkmeshes, vtksource)
		else:
			show(vtkmeshes)


posture = "postures/head_high_res/head.ply"
total_time = 60.
coordinates = [50, 0, 40] #x, y, z
irr = 100

lightScenario = ArtificialLight(posture)
lightScenario.add_point_source(coordinates, irr, total_time)
#lightScenario.add_extended_source("artificial_sources/TV_screens/screen40_1024.ply", coordinates, irr, total_time)
lightScenario.make_simulation()
lightScenario.show_results(show_sources=False)