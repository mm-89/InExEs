from xml.dom import minidom

class AnatomicalZones:

    def __init__(self, path):
        print("***")
        print("\n Anatomical Zones used \n")
        print("***")
        print("whatch out!")
        print("Sperimental code: twice timestep in the csv file")
        print("Need to be fix, with colour detection")
        print("***")
        document_read = minidom.parse(path)

        #this is all ComposedZone
        items = document_read.getElementsByTagName('ComposedZone')

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

    def get_total_zones_name(self):
        return self.zone_name + self.sub_zone_name
