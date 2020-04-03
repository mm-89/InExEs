from math import *
import numpy as np
import random


def from_cartesian_to_polar(comp):
    """
    Note: comp is a versor
    """
    #compute theta
    theta = acos(comp[2])
    #compute phi
    phi = np.arctan2(comp[1], comp[0])

    return np.array([theta, phi])


def from_polar_to_cartesian(zenith, azimuth):
    """
    Note: comp[0] has to be zenith angle
    while comp[1] has to be azimuth angle
    """
    zenith = zenith*pi/180.
    azimuth = azimuth*pi/180.
    x = sin(zenith)*cos(azimuth + pi/2.)
    y = sin(zenith)*sin(azimuth + pi/2)
    z = cos(zenith)
    
    #according to the trimesh reference
    #frame we have the following modification:

    #  x -> x; y -> z; z -> -y

    #azimuth = 0 towards north

    return x, z, -y


def matrix_rotation(theta, phi):
    #first rotation in xy axis 
    first = np.array([[cos(phi), -sin(phi), 0.],[sin(phi), cos(phi), 0.],[0., 0., 1.]])
    
    #second rotation in xz axis
    second = np.array([[cos(theta), 0., sin(theta)],[0., 1., 0.],[-sin(theta), 0., cos(theta)]])

    return np.dot(first, second)
    

def rotation_matrix_3D_xy(angle):
	"""
	Classical rotational 3D matrix around z-axis 
	of angle "angle" (counterclockwise)
	"""
	return np.array([[cos(angle), -sin(angle), 0],
					[sin(angle), cos(angle), 0],
					[0, 0, 1]])


def rotation_matrix_3D_yz(angle):
	"""
	Classical rotational 3D matrix around x-axis 
	of angle "angle" (counterclockwise)
	"""
	return np.array([[1, 0, 0],
					[0, cos(angle), -sin(angle)],
					[0, sin(angle), cos(angle)]])


def rotation_matrix_3D_xz(angle):
	"""
	Classical rotational 3D matrix around y-axis 
	of angle "angle" (counterclockwise)
	"""
	return np.array([[cos(angle), 0, sin(angle)],
					[0, 1, 0],
					[-sin(angle), 0, cos(angle)]])


def point_hemisphere_uniform(N):
    """ 
    Ref. Markus Deserno 2004
    """
    res = []

    n_c = 0
    m_theta = int(round((pi*N/4)**0.5))

    d_theta = pi/m_theta
    d_phi = 4*pi/(d_theta*N)

    for i in range(m_theta):
        theta = pi*(i + 0.5)/(2*m_theta)
        m_phi = int(round(2*pi*sin(theta)/d_phi))

        for j in range(m_phi):
            phi = 2*pi*j/m_phi

            x = sin(theta)*cos(phi)
            y = sin(theta)*sin(phi)
            z = cos(theta)
    
            res.append(np.array([x, y, z]))
            n_c += 1
    
    return res[:N]


def point_hemisphere_random(N):
	"""
	Simple Inverse transform sampling 
	for pseudo-random number sampling
	"""
	
	res = []

	for i in range(N):
		phi = 2*pi*random.uniform(0,1)
		theta = np.arccos(random.uniform(0,1))

		x = sin(theta)*cos(phi)
		y = sin(theta)*sin(phi)
		z = cos(theta)
    
		res.append(np.array([x, y, z]))

	return res


def make_rays_in_a_hemisphere(N, theta, phi, random):

    if(random):
        my_points = point_hemisphere_random(N)
    else:
        my_points = point_hemisphere_uniform(N)
  
    my_points_new_diff = []
    my_points_new_refl = []

    N_dif = 0
    N_ref = 0

    for i in my_points:
        tmp = np.dot(matrix_rotation(theta, phi), i)
        if(tmp[2]>=0.):
            my_points_new_diff.append(tmp)
            N_dif += 1
        else:
            my_points_new_refl.append(tmp)
            N_ref += 1

    if((N_dif + N_ref) != N):
        print("Some problem occured in BETA coefficient computing!")

    return my_points_new_diff, my_points_new_refl, N_dif, N_ref