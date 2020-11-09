from xml.dom import minidom
import numpy as np

class AnatomicalZones:

    def __init__(self, path):
        print("***")
        print("Anatomical Zones used")
        print("***")
        print("Whatch Out!")
        print("Sperimental code: it needs to be reviewed!")
        print("***")
        document_read = minidom.parse(path)

        #this is all ComposedZone
        items = document_read.getElementsByTagName('Zone')

        self.colors = []
        self.names = []

        items2 = document_read.getElementsByTagName('Zone')

        #!!!!!! to add activation state
        self.names = [item.getAttribute("name") for item in items2]
        self.colors = [ [ int(item.getAttribute("red")),
                        int(item.getAttribute("blue")),
                        int(item.getAttribute("green")), 255] for item in items2]

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
        return self.zone_name + self.sub_zone_name