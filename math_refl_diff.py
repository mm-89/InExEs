from math import *
import numpy as np
import random

#PARAMS : comp
#OUTPUT : array of theta and phi value 
#DESCRIPTION : get theta and phi values for ?
def from_cartesian_to_polar(comp):

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
    x = sin(zenith)*cos(azimuth)
    y = sin(zenith)*sin(azimuth)
    z = cos(zenith)
    
    return x, y, z

#PARAMS : theta, phi
#OUTPUT : 
#DESCRIPTION : 
def matrix_rotation(theta, phi):
    #first rotation in xy axis 
    first = np.array([[cos(phi), -sin(phi), 0.],[sin(phi), cos(phi), 0.],[0., 0., 1.]])
    
    #second rotation in xz axis
    second = np.array([[cos(theta), 0., sin(theta)],[0., 1., 0.],[-sin(theta), 0., cos(theta)]])

    return np.dot(first, second)


#PARAMS : N
#OUTPUT : 
#DESCRIPTION : perfectly uniform random point generation on a hemisphere
def point_hemisphere_uniform(N):
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



#PARAMS : N
#OUTPUT : 
#DESCRIPTION : random points generation on a hemisphere
def point_hemisphere_random(N):

    res = []

    for i in range(N):  #just to have same dimensionality of uniform one
        phi = 2*pi*random.uniform(0,1)
        theta = np.arccos(random.uniform(0,1))

        x = sin(theta)*cos(phi)
        y = sin(theta)*sin(phi)
        z = cos(theta)
    
        res.append(np.array([x, y, z]))

    return res


#PARAMS : N, theta, phi, random
#OUTPUT : 
#DESCRIPTION : 
def make_rays_in_a_hemisphere(N, theta, phi, random=True):
    if(random):
        my_points = point_hemisphere_random(N)
    else:
        my_points = point_hemisphere_uniform(N)
  
    my_points_new = []

    for i in my_points:
        my_points_new.append(np.dot(matrix_rotation(theta, phi), i))

    return my_points_new
    
