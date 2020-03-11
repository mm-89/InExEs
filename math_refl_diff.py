from math import *
import numpy as np

def polar_transform(comp):
    if(comp[0]==0.):
        phi = pi/2.
    else:
        phi = atan(comp[1]/comp[0])
    if(comp[2]==0.):
        theta = pi/2.
    else:
        theta = acos(  comp[2]/(comp[0]*comp[0] + comp[1]*comp[1] + comp[2]*comp[2])**0.5  )
    return np.array([theta, phi])

def compute_diff_radiation(N, theta, phi):
    inter_t = pi/(2*N)
    inter_p = 2*pi/N

    res = []

    x = []
    y = []
    z = []

    for i in range(N - 1):          #this is theta
        for j in range(N):      #this is alpha
            x.append(sin(pi/2 - i*inter_t)*cos(j*inter_p)*sin(phi) - \
                    (sin(pi/2 - i*inter_t)*cos(theta)*sin(j*inter_p) - \
                        cos(pi/2 - i*inter_t)*sin(theta))*cos(phi))
            y.append(sin(pi/2 - i*inter_t)*cos(j*inter_p)*cos(phi) + \
                    (sin(pi/2 - i*inter_t)*cos(theta)*sin(j*inter_p) - \
                        cos(pi/2 - i*inter_t)*sin(theta))*sin(phi))
            z.append(sin(pi/2 - i*inter_t)*sin(theta)*sin(j*inter_p) + \
                        cos(pi/2 - i*inter_t)*cos(theta))

    for r in range(N*(N - 1)):
        tmp = np.array([ x[r], y[r], z[r] ])
        res.append(tmp)

    return res
