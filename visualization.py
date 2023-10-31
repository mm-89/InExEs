from vtkplotter import trimesh2vtk, show
import numpy as np

class Visualization:

	def show_one_timestep_received(self, one_timestep):

		#row is timestep
		#column is triangle
		file_out_full = "output/{}_fullBody.txt".format(self.output_name)

		total_body_output = np.loadtxt(file_out_full)

		if (one_timestep < 0 or one_timestep > np.shape(total_body_output)[0]):
			raise TypeError("Timestep must be smaller than {}".format(np.shape(total_body_output)[0]))

		col = total_body_output[one_timestep - 1, :]

		vtkmeshes = trimesh2vtk(self.posture.get_posture)
		vtkmeshes.cellColors(col, cmap='jet')
		vtkmeshes.addScalarBar(title="J/m^2")

		show(vtkmeshes)