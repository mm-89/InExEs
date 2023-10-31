import math as mt
import numpy as np
import random


def from_cartesian_to_polar(item):
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
    polar_coordinates = np.array([np.arccos(item[1]),
                        np.arctan2(item[0], -item[2])])
    return polar_coordinates.T


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
 
    res = np.array([np.sin(np.radians(zenith))*np.sin(np.radians(azimuth)),
            np.cos(np.radians(zenith)),
            -np.sin(np.radians(zenith))*np.cos(np.radians(azimuth))])

    return res.T
    

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


def uniform_points_hemisphere(N, diff):
    """
    Generate N points on the upper
    hemisphere uniformly distribuited.


    Ref. Markus Deserno 2004

    Parameters:
    ------------
    N :   int
        total points number

    diff :  bool
        if True it gives N points
        on the upper hemisphere
        if False it gives N points
        on the lower hemisphere

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
    N = int(N)
    res = np.zeros((2*N,3)) # 2N to be sure if it creates more points... (?)

    n_c = 0
    m_theta = int(round((mt.pi*N/4)**0.5))

    d_theta = mt.pi/m_theta
    d_phi = 4*mt.pi/(d_theta*N)

    for i in range(m_theta):
        theta = mt.pi*(i + 0.5)/(2*m_theta)
        
        if not diff:
            theta = mt.pi*(i + 0.5)/(2*m_theta) + mt.pi/2.
            
        m_phi = int(round(2*mt.pi*mt.sin(theta)/d_phi))

        for j in range(m_phi):
            phi = 2*mt.pi*j/m_phi

            x = mt.sin(theta)*mt.sin(phi)
            y = mt.cos(theta)
            z = - mt.sin(theta)*mt.cos(phi)
    
            res[n_c] = np.array([x, y, z])
            n_c += 1
    
    return res[:N]