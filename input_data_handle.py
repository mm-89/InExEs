import data_map as dm

import numpy as np

#to test if data selected exist in data file
def is_data_exists_in_file(date, data_read):
	#NEED to re-scale????????
	if( date.year in data_read[:, dm.data_map["year"]] \
		and date.month in data_read[:, dm.data_map["month"]] \
		and date.day in data_read[:, dm.data_map["day"]] \
		and date.hour in data_read[:, dm.data_map["hour"]] \
		and date.minute in data_read[:, dm.data_map["minute"]] ):
		return True
	else:
		return False

def select_rows_in_file(date, data_read):
	val = None
	my_vect_prop = np.array([date.year,
							date.month,
							date.day,
							date.hour,
							date.minute])
	for j, item in enumerate(data_read):
		if np.array_equal(item[:5], my_vect_prop) :
			val = j
	return val

def repair_data(data_read):
	"""
	Sometimes input data has negative values (WHY?)
	If a value is negative I have to put to zero
	"""
	print("Start to repair data")

	for j, item in enumerate(data_read[:, dm.data_map["uvglobal"]]):
		if(item < 0): data_read[j, dm.data_map["uvglobal"]] = 0

	for j, item in enumerate(data_read[:, dm.data_map["uvdiffuse"]]):
		if(item < 0): data_read[j, dm.data_map["uvdiffuse"]] = 0

	for j, item in enumerate(data_read[:, dm.data_map["uvdirect"]]):
		if(item < 0): data_read[j, dm.data_map["uvdirect"]] = 0

	for j, item in enumerate(data_read[:, dm.data_map["uvreflect"]]):
		if(item < 0): data_read[j, dm.data_map["uvreflect"]] = 0

	return data_read