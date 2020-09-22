#These shared parameters are as not important as 
#those in the namelist, anyway they can change
#simulations' results.

#N: number of points generated on the hemisphere
#for beta coefficients computation

#normalizazion factor: to set rays origins different
#from faces' centers. Speed of beta coefficients 
#computed change with this parameter, as well as 
#the precision 

#		py_embree - TO TEST (something changes)
#		 if True, Trimesh can use py_embree
#		 raytracing, faster than the normal one

#      	process
#        if True, Nan and Inf values will be removed
#        immediately and vertices will be merged

#		validate
#        If True, degenerate and duplicate faces will be
#        removed immediately, and some functions will alter
#        the mesh to ensure consistent results.
#

GUI_window = False

N = 10000
translation_factor = 2.
random_points = False

py_embree = True
process = True
validate = False
