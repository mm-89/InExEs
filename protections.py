#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Define the protections and their relative methods using the xml library
"""

import numpy as np
import xml.etree.ElementTree as ET

def load_protections(path):		
	
	try:
		with open(path, 'rb') as xml_file :
			tree = ET.parse(xml_file)
			root = tree.getroot()
			
			# Define the clothes found in the library
			clothes_dict = {}
		
			for clothing in root.iter('Clothing'):
				name = clothing.attrib['name']
				clothes_dict[name] = []
				for zone in clothing:
					clothes_dict[name].append(zone.attrib['name'])
			
			# Define the materials found in the library
			material_dict = {}
		
			for material in root.iter('Material'):
				name = material.attrib['name']
				ip = material.attrib['IP']
				material_dict[name] = int(ip)
					
			return clothes_dict, material_dict

	except IOError:
		print("File ", path, " don't find or don't exist.")


def get_IP(protection_lib, protections, posture):
	
	IP = np.ones(posture.number_faces)
	
	# Load the protections from the librarys
	clothes_dict, material_dict = load_protections(protection_lib)
	
	# Check the active protections in the protection file
	try:
		with open(protections, 'rb') as xml_file :
			tree = ET.parse(xml_file)
			root = tree.getroot()
			
			# Find the active clothes
			for protection in root.findall("Clothing/Protection/[@active='1']"):
				name = protection.attrib['name']
				mat = protection.attrib['material']
				
				for zone in clothes_dict[name]:
					mask = posture.get_zone_mask(zone)
					IP[mask] *= material_dict[mat]
					
			# Find the active zones
			for protection in root.findall("Zone/Protection/[@active='1']"):
				zone = protection.attrib['name']
				IP_zone = protection.attrib['IP']
				
				mask = posture.get_zone_mask(zone)
				IP[mask] *= int(IP_zone)

		return IP
					
	except IOError:
		print("File ", protections, " doesn't find or doesn't exist.")
	