import numpy as np

import math_refl_diff as mrd
import shared_parameters as sp
from progressbar import *

import time 

#----------------------------------------------

def resh_APE(current_list, current_index):
    current_list = np.setdiff1d(current_list, np.array([current_index, -1]))
    return list(set(current_list))
    
#----------------------------------------------

def compute_skin_reflection_map(path, file):
    """
    Generate skin reflection map (matrix NxN 
    where N is the number of faces) for 
    a specific posture (file).

    Parameters:
    ------------
    path :   str
        name of the posture
        in order to save the 
        right referement

    file :   str
        posture previously 
        charged using posture
        class

    faces_normals : (N, 3) float
        cartesian coordinates [x, y, z] of N
        triangles normals of the posture 
    
    faces_centers : (N, 3) float
        cartesian coordinates [x, y, z] of N
        triangles centers of the posture 

    Returns:
    -----------
    ???
    """

    path = path.split('/')
    mesh_name = path[-1]
    fileName = "input_skinRefl/skinRefl_{}_{}.txt".format(mesh_name.rsplit(".", -1)[0], sp.N)

    try:
        with open(fileName) as f:
            print("SkinRefl file found")

            #upload data
            skinRefl_coeff = np.loadtxt(fileName)

            if(len(skinRefl_coeff)==0):
                print("File of Beta coefficient corrupeted")
                print("Total number of read lines are: ", len(skinRefl_coeff))

            return skinRefl_coeff

    except IOError:
        #If not we ask user for an N value, compute beta and create a beta coeff file
        print("No skinRefl file found for this N value, a new skinRefl file will be created please wait")
        start = time.time()

        skinRefl_coeff = []

        if(sp.random_points):
            # N rays over all of directions
            ray_directions = mrd.random_points_hemisphere(sp.N, True) + \
                            mrd.random_points_hemisphere(sp.N, False)
 
        else:
            # N rays over all of directions
            ray_directions = mrd.uniform_points_hemisphere(sp.N, True) + \
                            mrd.uniform_points_hemisphere(sp.N, False) 

        # if not py_embree self intersection are not safe
        single_origin = [i + j*1e-4 for i, j in zip(file.triangles_center, file.face_normals)]
    
        # matrix_comp is the matrix with each row
        # is a specific face of the mesh. Each column
        # specifies where there is a visible other face

        matrix_actv = np.zeros((len(single_origin), len(single_origin)))
        matrix_pdot = np.zeros((len(single_origin), len(single_origin)))
        matrix_dist = np.zeros((len(single_origin), len(single_origin)))

        for j,item in enumerate(single_origin):

            progress_bar(j, np.shape(single_origin)[0])

            ray_origins = np.ones((sp.N, 3))*item

            res = file.ray.intersects_first(ray_origins=ray_origins, ray_directions=ray_directions)
            real_list = resh_APE(res, j)

            mask = ( real_list == np.arange(len(single_origin)) )

            matrix_actv[j, mask] = 1
            matrix_pdot[j, :] = abs( np.dot( file.face_normals, file.face_normals[j] ) )
            matrix_dist[j, :] = np.sqrt( np.sum( (np.ones((len(single_origin), 3))*file.triangles_center[j] - \
                                file.triangles_center)**2 , axis=1 ))

        print('\nSkinRefl took {:.1f} seconds.'.format(time.time()-start))
        
        np.savetxt(fileName, matrix_comp)

    return np.loadtxt(fileName)