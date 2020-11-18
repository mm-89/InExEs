from xml.dom import minidom
import xml.etree.ElementTree as ET
import numpy as np

class AnatomicalZones:

	def __init__(self, path, posture):

		try:
			with open(path, 'rb') as xml_file :
				tree = ET.parse(xml_file)
				self.root = tree.getroot()
		except IOError:
			print("File ", path, " don't find or don't exist.")

		self.posture = posture
		self.mask = np.zeros(self.posture.number_faces, dtype=bool)

		self.zone_name = [item.attrib['name'] for item in self.root.iter('Zone')]
		self.composed_zone_name = [item.attrib['name'] for item in self.root.iter('ComposedZone')]


	def get_total_zones_name(self):
		return self.zone_name + self.composed_zone_name


	def get_zone_mask(self, zone):
		
		# Find the colors corresponding to the zone name in the xml file
		col = []
		cfound = False
				
		# Check if it is a single zone
		for element in self.root.iter('Zone'):
			if element.attrib['name']==zone:
				col.append([element.attrib['red'], element.attrib['green'],\
		   element.attrib['blue'], '255'])						
				cfound = True
				
		# If not, look for the composed zones
		if not cfound:
			for element in self.root.iter("ComposedZone"):
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
			
			ifaces = np.where((self.posture.get_faces_color==color).all(axis=1))[0]
			self.mask[ifaces] = True
			
		return self.mask