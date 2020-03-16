from math import *
import numpy as np
import random

def polar_transform(comp):

    #compute theta
    theta = acos(comp[2])

    #compute phi
    phi = np.arctan2(comp[1], comp[0])

    return np.array([theta, phi])

#old code (it might be useful in the future)
"""
def compute_diff_radiation(N, theta, phi):

    inter_t = pi/(2*N)
    inter_p = 2*pi/N

    res = []

    for i in range(N):          #this is theta
        for j in range(N):      #this is alpha
            x = sin(i*inter_t)*cos(j*inter_p)*sin(phi) - \
                    (sin(i*inter_t)*cos(theta)*sin(j*inter_p) - \
                        cos(i*inter_t)*sin(theta))*cos(phi)

            y = sin(i*inter_t)*cos(j*inter_p)*cos(phi) + \
                    (sin(i*inter_t)*cos(theta)*sin(j*inter_p) - \
                        cos(i*inter_t)*sin(theta))*sin(phi)

            z = sin(i*inter_t)*sin(theta)*sin(j*inter_p) + \
                        cos(i*inter_t)*cos(theta)

            res.append(np.array([ x, y, z]))

    return res
"""

def matrix_rotation(theta, phi):
    #first rotation in xy axis 
    first = np.array([[cos(phi), -sin(phi), 0.],[sin(phi), cos(phi), 0.],[0., 0., 1.]])
    
    #second rotation in xz axis
    second = np.array([[cos(theta), 0., sin(theta)],[0., 1., 0.],[-sin(theta), 0., cos(theta)]])

    return np.dot(first, second)

#uniform points generation in a hemisphere
def point_hemisphere_uniform(N):

    inter_t = pi/(2*N)
    inter_p = 2*pi/N

    res = []

    for i in range(N - 1):          #this is theta
        for j in range(N):      #this is phi
            x = sin(i*inter_t)*cos(j*inter_p)

            y = sin(i*inter_t)*sin(j*inter_p)

            z = cos(i*inter_t)

            res.append(np.array([x, y, z]))

    return res

#random points generation in a hemisphere
def point_hemisphere_random(N):

    res = []

    for i in range(N*(N - 1)):  #just to have same dimensionality of uniform one
        phi = 2*pi*random.uniform(0,1)
        theta = np.arccos(random.uniform(0,1))

        x = sin(theta)*cos(phi)
        y = sin(theta)*sin(phi)
        z = (cos(theta))
    
        res.append(np.array([x, y, z]))

    return res

def make_rays_in_a_hemisphere(N, theta, phi, random=True):
    if(random):
        my_points = point_hemisphere_random(N)
    else:
        my_points = point_hemisphere_uniform(N)
  
    my_points_new = []

    for i in my_points:
        my_points_new.append(np.dot(matrix_rotation(theta, phi), i))

    return my_points_new
    
