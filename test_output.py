import output as oi
import posture as ps
import matplotlib.pyplot as plt


#files previously simulated and mesh
my_posture = "special_postures/face_without_eyebrows.ply"
my_file = "output/face_january_without_eyebrows.csv"

#prepare to analisys
my_file_to_analyse = oi.Output(my_posture, my_file)

vec_color_id = my_file_to_analyse.get_id_color([255, 0, 0, 255])

#my_file_to_analyse.show_selected_faces(id_vector)