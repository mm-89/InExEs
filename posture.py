import beta_coefficients as bc
import math_refl_diff as mrd

from checkPostureColor import CheckPostureColor

import trimesh as tm
from vtkplotter import trimesh2vtk, show
import sys
import numpy as np
import xml.etree.ElementTree as ET
from math import pi

#Theo's MOD
zone_path = "anatomical_zones/anatomical_zones.xml"

class Posture(CheckPostureColor):

	def __init__(self, my_file):
		self.path = my_file
		self.my_file = tm.load(my_file, use_embree=False)

		self._checkPostureColor_andRepair()

		self.beta_coeff = bc.compute_beta(self.path, self.my_file)

		# double ray of the bounding sphere
		self.max_bounds = 2*( 3*self.my_file.bounding_sphere.volume/(4*pi) )**(1/3)
	
		self.number_faces = np.shape(self.my_file.triangles_center)[0]
		
		self.number_vertices = np.shape(self.my_file.vertices)[0]
			

	def show_posture(self):
		self.my_file.show()


	def show_beta_coefficients(self, beta_coeff):
		"""
		beta_coeff can be diff or refl
		"""
		if( beta_coeff == 'diff' ):
			this_beta = self.beta_coeff[:, 0]
		elif( beta_coeff == 'refl'):
			this_beta = self.beta_coeff[:, 1]
		else:
			raise TypeErro("Value not recognise! It can be 'diff' or 'refl'")

		this_beta = this_beta/pi

		vtkmeshes = trimesh2vtk(self.my_file)
		vtkmeshes.cellColors(this_beta, cmap='jet', vmin=0., vmax=1.)
		vtkmeshes.addScalarBar(title="Beta coefficients")

		show(vtkmeshes)


	def plyTests(self):
		self.my_file.remove_degenerate_faces()
		self.my_file.remove_duplicate_faces()
		self.my_file.remove_infinite_values()
		self.my_file.remove_unreferenced_vertices()
		v = self.my_file.is_volume
		w = self.my_file.is_winding_consistent
		wa = self.my_file.is_watertight
		if( (not v) or (not w) or (not wa) ):
			self.my_file.fill_holes()
			if( (not v) or (not w) or (not wa) ):
				print("Mesh is corrupted")
				sys.exit()
				
				
	@property
	def get_posture(self):
		return self.my_file


	@property
	def get_normals(self):
		return self.my_file.face_normals


	@property
	def get_area_faces(self):
		return self.my_file.area_faces


	@property
	def get_total_area(self):
		return self.my_file.area


	@property
	def get_beta(self):
		return self.beta_coeff


	@property
	def get_faces(self):
		return self.my_file.faces
	
	
	@property
	def get_vertices(self):
		return self.my_file.vertices


	@property
	def get_triangles_center(self):
		return self.my_file.triangles_center


	@property
	def get_faces_color(self):
		return self.my_file.visual.face_colors


	@property
	def get_vertices_color(self):
		return self.my_file.visual.vertex_colors


	@property
	def get_vertex_faces(self):
		return self.my_file.vertex_faces

	@property
	def get_vertex_normals(self):
		return self.my_file.vertex_normals

	
	@property
	def get_max_bounds(self):
		return 2*( 3*self.my_file.bounding_sphere.volume/(4*pi) )**(1/3)


	def correct_colors(self):
		
		col = []
		try:
			with open(zone_path, 'rb') as xml_file :
				tree = ET.parse(xml_file)
				root = tree.getroot()
				
				for element in root.iter('Zone'):
					col.append([element.attrib['red'], element.attrib['green'],\
				   element.attrib['blue'], '255'])					
		except IOError:
			print("File ", protections, " doesn't find or doesn't exist.")		

		col = np.array(col).astype(int)
		
		if np.unique(self.get_faces_color, axis=0).shape != col.shape:
			print('Some colors are undefined. Start correcting colors...')
		
			new_face_colors = np.copy(self.get_faces_color).astype(int)
			
			for iface in range(self.number_faces):
				imin = np.argmin(np.sum((col-new_face_colors[iface])**2, axis=1))
				new_face_colors[iface] = col[imin]
				
			self.my_file.visual.face_colors = new_face_colors
			


	def get_zone_mask(self, zone):
		
		mask = np.zeros(self.number_faces, dtype=bool)
		
		# Find the colors corresponding to the zone name in the xml file
		col = []
		cfound = False
		
		try:
			with open(zone_path, 'rb') as xml_file :
				tree = ET.parse(xml_file)
				root = tree.getroot()
				
				# Check if it is a single zone
				for element in root.iter('Zone'):
					if element.attrib['name']==zone:
						col.append([element.attrib['red'], element.attrib['green'],\
				   element.attrib['blue'], '255'])						
						cfound = True
						
				# If not, look for the composed zones
				if not cfound:
					for element in root.iter("ComposedZone"):
						if element.attrib['name'] == zone:
							for child in element:
								
								#check if the child is a composed zone
								if child.tag=='Zone':
									col.append([child.attrib['red'],\
					  child.attrib['green'], child.attrib['blue'], '255'])
								else:
									for grandchild in child:
										col.append([grandchild.attrib['red'],\
					   grandchild.attrib['green'], grandchild.attrib['blue'], '255'])									

				# Convert to face index using the face colors of the mesh
				for color in col:
					color = np.array([int(i) for i in color])
					
					ifaces = np.where((self.get_faces_color==color).all(axis=1))[0]
					mask[ifaces] = True
					
				return mask
						
		except IOError:
			print("File ", protections, " don't find or don't exist.")		
