import math as mt
import numpy as np
import random

import shared_parameters as sp


def from_cartesian_to_polar(comp):
    """
    Convert cartesian coordinates
    of InExEs referent frame
    [x, y, z] into polar-spherical
    coordinates [zenith, azimut].

    Parameters:
    ------------
    comp :   (, 3) float
        versor cartesian coordinates
        in InExEs reference frame

    Returns:
    -----------
    polar_coordinates :   (, 2) float
        polar-spherical coordinates
        in InExEs reference frame

    """
    polar_coordinates = np.array([mt.acos(comp[1]),
                        np.arctan2(comp[0], -comp[2])])
    return polar_coordinates


def from_polar_to_cartesian(zenith, azimuth):
    """
    Convert polar atronomical coordinates
    [zenith, azimuth] into cartesian
    coordinates [x, y, z].

    Parameters:
    ------------
    zenith :   (, 1) float
        zenith angle in degree. 
        Possible values from 0°
        to 180°
    azimuth :   (, 1) float
        azimuth angle in degree. 
        Possible values from 0°
        to 360°

    Returns:
    -----------
    x : cartesian coordinate x
    y : cartesian coordinate y
    z : cartesian coordinate z

    [x, y, z] is a versor ==
    x2 + y2 + z2 = 1
    
    Note: this function has been written 
    to transform input data of the model
    and it is used only for this
    """
 
    x = mt.sin(np.radians(zenith))*mt.sin(np.radians(azimuth))
    y = mt.cos(np.radians(zenith))
    z = - mt.sin(np.radians(zenith))*mt.cos(np.radians(azimuth))

    if(x < sp.threshold): x = 0
    if(y < sp.threshold): y = 0
    if(z < sp.threshold): z = 0

    return x, y, z
    

def rotation_matrix_3D_xy(angle):
	"""
	Classical rotational 3D matrix around z-axis 
	of angle "angle" (counterclockwise)
	"""
	return np.array([[mt.cos(angle), -mt.sin(angle), 0],
					[mt.sin(angle), mt.cos(angle), 0],
					[0, 0, 1]])

def rotation_matrix_3D_yz(angle):
	"""
	Classical rotational 3D matrix around x-axis 
	of angle "angle" (counterclockwise)
	"""
	return np.array([[1, 0, 0],
					[0, mt.cos(angle), -mt.sin(angle)],
					[0, mt.sin(angle), mt.cos(angle)]])


def rotation_matrix_3D_xz(angle):
	"""
	Classical rotational 3D matrix around y-axis 
	of angle "angle" (counterclockwise)
	"""
	return np.array([[mt.cos(angle), 0, mt.sin(angle)],
					[0, 1, 0],
					[-mt.sin(angle), 0, mt.cos(angle)]])


def uniform_points_hemisphere(N):
    """
    Generate N points on the upper
    hemisphere uniformly distribuited.


    Ref. Markus Deserno 2004

    Parameters:
    ------------
    N :   int
        total points number

    Returns:
    -----------
    polar_coordinates :   (N, 3) float
        cartesian coordinates of N
        points uniformly distribuited
        on upper hemisphere

    Note1: it needs to be well orientated
    Note2: this methos sometimes cannot
    generated exaclty N points but some 
    more or less.
    """
    res = []

    n_c = 0
    m_theta = int(round((mt.pi*N/4)**0.5))

    d_theta = mt.pi/m_theta
    d_phi = 4*mt.pi/(d_theta*N)

    for i in range(m_theta):
        theta = mt.pi*(i + 0.5)/(2*m_theta)
        m_phi = int(round(2*mt.pi*mt.sin(theta)/d_phi))

        for j in range(m_phi):
            phi = 2*mt.pi*j/m_phi

            x = mt.sin(theta)*mt.sin(phi)
            y = mt.cos(theta)
            z = - mt.sin(theta)*mt.cos(phi)
    
            res.append(np.array([x, y, z]))
            res_theta.append(mt.sin(theta))
            n_c += 1
    
    return np.array(res[:N])


def random_points_hemisphere(N):
	"""
	Generate N points on the upper
	hemisphere randomly distribuited.

	Ref. any about Monte Carlo
	inverse problem

	Parameters:
	------------
	N :   int
		total points number

	Returns:
	-----------
	polar_coordinates :   (N, 3) float
		cartesian coordinates of N
		points randomly distribuited
		on upper hemisphere

	Note: it needs to be well orientated
	"""
	res = []
	res_theta = []

	for i in range(N):

		prn = random.uniform(0, 1)
		trn = random.uniform(0, 1)

		phi = 2*mt.pi*prn
		theta = np.arccos(trn)

		x = mt.sin(theta)*mt.sin(phi)
		y = mt.cos(theta)
		z = - mt.sin(theta)*mt.cos(phi)

		res.append(np.array([x, y, z]))
		res_theta.append(trn)

	return np.array(res), res_theta


def make_rays_in_a_hemisphere(theta, phi):
	"""
	Generate rays in a hemisphere
	orientated towards an angle theta
	(zenith) and an angle phi (azimuth)
	compare to the usual horizon.

	Parameters:
	------------
	theta :   float
		zenith angle

	phi :   float
		azimuth angle

	Returns:
	-----------
	my_points_new_diff :   (N, 3) float
		cartesian coordinates of N_diff points 
		on the upper hemisphere
		(diffused)

	my_points_new_refl :   (N, 3) float
		cartesian coordinates of N_refl points 
		on the lower hemisphere
		(reflected)

	N_diff :   int
		total number of points 
		distribuited on upper 
		hemisphere from initial N

	N_refl :   int
		total number of points 
		distribuited on lower 
		hemisphere from initial N
	"""
	if(sp.hemispherical_random_generator):
		my_points = random_points_hemisphere(sp.N)
	else:
		my_points = uniform_points_hemisphere(sp.N)

	my_points_new_diff = []
	my_points_new_refl = []

	N_dif = 0
	N_ref = 0
	
	for i in my_points:

		# rotate in the new reference frame
		current_vector = np.dot(rotation_matrix_3D_xz(-phi), 
						np.dot(rotation_matrix_3D_yz(-theta), i))
		
		#note: the horizon is [0, 1, 0]
		if(current_vector[1] >= 0.):
			my_points_new_diff.append(current_vector)
			N_dif += 1
		else:
			my_points_new_refl.append(current_vector)
			N_ref += 1
        
	if((N_dif + N_ref) != sp.N):
		print("Some problem occured in BETA coefficient computing!")
		
	return np.array(my_points_new_diff), \
			np.array(my_points_new_refl), N_dif, N_ref