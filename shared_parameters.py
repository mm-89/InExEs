#These shared parameters are as not important as 
#those in the namelist, anyway they can change
#simulations' results.

#N: number of points generated on the hemisphere
#for beta coefficients computation

#normalizazion factor: to set rays origins different
#from faces' centers. Speed of beta coefficients 
#computed change with this parameter, as well as 
#the precision 

N = 10000
translation_factor = 2.
normalization_factor = 4 # ----> to take it off
random_points = False
