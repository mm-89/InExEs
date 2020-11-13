from xml.dom import minidom
import xml.etree.ElementTree as ET
import numpy as np

class AnatomicalZones:

	def __init__(self, path, posture):
		print("***")
		print("Anatomical Zones used")
		print("***")
		print("Whatch Out!")
		print("Sperimental code: it needs to be reviewed!")
		print("***")

		self.posture = posture
		self.path = path

		document_read = minidom.parse(path)

		#this is all ComposedZone
		items = document_read.getElementsByTagName('Zone')
		items2 = document_read.getElementsByTagName('ComposedZone')

		self.colors = []
		self.names = []

		#!!!!!! to add activation state
		self.names = [item.getAttribute("name") for item in items]
		self.colors = [ [ int(item.getAttribute("red")),
						int(item.getAttribute("blue")),
						int(item.getAttribute("green")), 255] for item in items]
		self.names2 = [item2.getAttribute("name") for item2 in items2]
		"""
		item = document_read.getElementsByTagName('ComposedZone')
		print( item[2].getElementsByTagName("Zone")[6].getAttribute("name") )

		self.zone_name = []
		self.sub_zone_name = []

		self.colors_vector = []

		for item in items:
			activation = item.getAttribute("active")
			self.zone_name.append(item.getAttribute("name"))
			if ( activation == '1' ):
				for comp in item.getElementsByTagName('Zone'):
					sub_activation = comp.getAttribute("active")
					self.sub_zone_name.append(comp.getAttribute("name"))
					if ( sub_activation == '1' ):
						red = comp.getAttribute("red")
						green = comp.getAttribute("green")
						blue = comp.getAttribute("blue")
						self.colors_vector.append([int(red), int(blue), int(green), 255])
		"""


	def get_total_zones_name(self):
		return self.names + self.names2


	def get_zone_mask(self, zone):
		
		mask = np.zeros(self.posture.number_faces, dtype=bool)
		
		# Find the colors corresponding to the zone name in the xml file
		col = []
		cfound = False
		
		try:
			with open(self.path, 'rb') as xml_file :
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
					
					ifaces = np.where((self.posture.get_faces_color==color).all(axis=1))[0]
					mask[ifaces] = True
					
				return mask
						
		except IOError:
			print("File ", protections, " don't find or don't exist.")	
