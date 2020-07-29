import unittest
import sys

sys.path.insert(0, '../')

import csv

import simulation as sim

# parameters for simulation---------------

my_posture_file = "postures_test/cube_test.ply"
output_name = "this_test"
timestep = 60.
latitude = 45
start_date  = '01/01/2009 00:00:00'
end_date    = '01/02/2009 00:00:00'

#----------------------------------------

# make simulation output-----------------

my_sim = sim.Simulation(start_date, 
						end_date, 
						timestep, 
						my_posture_file,
						output_name,
						latitude=latitude,
						read_data=False)
								
my_sim.make_simulation()
#-----------------------------------------


class TestGeneral(unittest.TestCase):

	def setUp(self):

		with open(output_name + ".csv", mode='r') as csv_file:

			next(csv_file)
			data = np.array([i for i in csv.reader(csv_file, delimiter=",")])
			data = np.delete(data, 0, 1)
			data = data.astype(np.float)

			self.direct_irr = data[:, 0]
			self.diffus_irr = data[:, 1]
			self.reflec_irr = data[:, 2]
			
        
	def test_simulation(self):
		print("ciao")

