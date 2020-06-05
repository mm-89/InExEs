import numpy as np

import math_refl_diff as mrd
import shared_parameters as sp

#----------------------------------------------

def resh_APE(current_list, current_index):
    current_list = np.setdiff1d(current_list, np.array([current_index, -1]))
    return list(set(current_list))
    
#----------------------------------------------

def compute_skin_reflection_map(path, file, face_normals, face_centers):
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
    fileName = "input/skinRefl_" + mesh_name.rsplit(".", -1)[0] + "_" + str(2*sp.N) + ".txt"

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

        skinRefl_coeff = []

        if(sp.random_points):

            ray_directions = mrd.random_points_hemisphere(sp.N, True) + \
                            mrd.random_points_hemisphere(sp.N, False)
 
        else:
            # N rays on upper hemisphere
            ray_directions = mrd.uniform_points_hemisphere(sp.N, True) + \
                            mrd.uniform_points_hemisphere(sp.N, False) 

        # if not py_embree self intersection are not safe
        single_origin = [i + j*1e-6 for i, j in zip(face_centers, face_normals)]


    
        # matrix_comp is the matrix with every row
        # is a specific face of the mesh. Each column
        # specifies where there is a visible other face

        matrix_comp = np.zeros( shape=(len(single_origin), len(single_origin)) )
        matrix_pdot = np.zeros( shape=(len(single_origin), len(single_origin)) )
        matrix_dist = np.zeros( shape=(len(single_origin), len(single_origin)) )

        for j,item in enumerate(single_origin):
            ray_origins = [item for i in range(sp.N)]
            res = file.ray.intersects_first(ray_origins=ray_origins, ray_directions=ray_directions)
            real_list = resh_APE(res, j)
            for i in real_list:
                matrix_comp[j, i] = 1
                matrix_pdot[j, i] = abs( np.dot( face_normals[j], face_normals[i] ) )
                matrix_dist[j, i] = ( (face_centers[j, 0] - face_centers[i, 0])**2 + \
                                     (face_centers[j, 1] - face_centers[i, 1])**2 + \
                                     (face_centers[j, 2] - face_centers[i, 2])**2 )**0.5
        	
            print("Computing skin reflection ... ", 
                round(j/len(face_normals)*100,1), 
                " percent complete", end="\r")

        np.savetxt(fileName, matrix_comp)

    return np.loadtxt(fileName)