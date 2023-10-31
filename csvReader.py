import csv
import numpy as np
import datetime as dt
import math_refl_diff as mrd

class CsvReader:

	def __init__(self, input_irradiance_path):

		try:

			with open(input_irradiance_path, mode='r') as csv_file:

				#to avoid to read header
				next(csv_file)

				data =  np.array([i for i in csv.reader(csv_file, delimiter=",")])

		except:
			raise TypeError("File {} doesn't find or doesn't exist.".format(input_irradiance_path))


		#to check the input has 6 columns
		if ( np.shape(data.T)[0] != 6):
			raise TypeError("Input file format is not correct!")

		try:

			#self.datetime = [dt.datetime.strptime(i, '%b %d %Y %H:%M:%S') for i in data[:, 0]]
			self.datetime = data[:, 0]
			self.other_data = data[: , 1:7]

		except:
			print("Something gone wrong setting dates input file.")


	def checkDatesAndTimestep(self, start_date, end_date, timestep):
		"""
		Note: start and end date are strings.
		"""
		s_date = dt.datetime.strptime(start_date, '%m/%d/%Y %H:%M:%S')
		e_date = dt.datetime.strptime(end_date, '%m/%d/%Y %H:%M:%S')

		if(s_date > e_date):
			raise TypeError("End date MUST be greter or equal to start date!")
		if not s_date.strftime("%b %d %Y %H:%M:%S") in self.datetime:
			raise TypeError("Start date doesn't find in input file!")
		if not e_date.strftime("%b %d %Y %H:%M:%S") in self.datetime:
			raise TypeError("End date doesn't find in input file!")

		s_date_row = np.where( s_date.strftime("%b %d %Y %H:%M:%S") == np.array(self.datetime))[0][0]
		e_date_row = np.where( e_date.strftime("%b %d %Y %H:%M:%S") == np.array(self.datetime))[0][0]

		#check the timestep is always the same
		diff_btw = [(dt.datetime.strptime(i, '%b %d %Y %H:%M:%S') - \
					dt.datetime.strptime(j, '%b %d %Y %H:%M:%S')).seconds \
					for i,j in zip(self.datetime[s_date_row+1 : e_date_row], 
								self.datetime[s_date_row : e_date_row-1])]

		#ind is the interval 
		ind, occ = np.unique( np.array(diff_btw), return_counts=True)

		if ( len(ind) != 1 or len(occ) != 1):
			raise TypeError("Time duration between dates in input file is not equal!")
		if ( occ[0] != e_date_row - s_date_row - 1):
			raise TypeError("Some problem occur in reading input file")

		self.start_date = s_date
		self.end_date = e_date

		if(timestep % ind[0] != 0):
			raise TypeError("Timestep is not equal or multiple of that one in input file!")

		mult_timetep = int(timestep/ind[0])

		self.timeline = self.datetime[s_date_row:e_date_row + 1:mult_timetep]

		try:
			angles_tmp = (self.other_data[s_date_row:e_date_row + 1:mult_timetep, 0:2]).astype(np.float)

		except:
			print("Float conversion didn't work for this angles data!")

		#set in radiant form
		self.angles = mrd.from_polar_to_cartesian(angles_tmp[:, 0], angles_tmp[:, 1])

		self.is_day = angles_tmp[:,0]<=90.

		try:

			self.irr_dir = (self.other_data[s_date_row:e_date_row + 1:mult_timetep, 2]).astype(np.float)
			self.irr_dif = (self.other_data[s_date_row:e_date_row + 1:mult_timetep, 3]).astype(np.float)
			self.irr_ref = (self.other_data[s_date_row:e_date_row + 1:mult_timetep, 4]).astype(np.float)

		except:
			print("Float conversion didn't work for this irradiance data!")

		#remove eventual negative numbers
		self.irr_dir[self.irr_dir<0.] = 0.
		self.irr_dif[self.irr_dif<0.] = 0.
		self.irr_ref[self.irr_ref<0.] = 0.
