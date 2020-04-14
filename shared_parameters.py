#These shared parameters are as not important as 
#those in the namelist, anyway they can change
#simulations' results.

#N: number of points generated on the hemisphere
#for beta coefficients computation

#hemispherical random generator: beta coefficients
#can be computed via random way (Monte Carlo) or
#uniformilly distribuited [the second converges
#much faster than first]

#normalizazion factor: to set rays origins different
#from faces' centers. Speed of beta coefficients 
#computed change with this parameter, as well as 
#the precision 

N = 600
hemispherical_random_generator = False
normalization_factor = 1e-3