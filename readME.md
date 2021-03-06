# How to install InExES

**WIP we recommend to wait the release version before cloning it**

We suppose that InExES can work on every machine, but we only tried on a Mac, Linux Ubuntu 16.04 and Linux Mint 19.3


## Prerequisite

**Python 3.5** or newer 

## Install instructions

    git clone https://github.com/mm-89/InExEs.git
    pip3 install matplotlib
	pip3 install trimesh
	pip3 install Rtree
	pip3 install shapely

## Librairies problems

You may face some problems reguarding libraries installation. Where is some solutions.
* Cannot install Rtree on mac or Linux :
	 * Mac : `pip install "rtree>=0.8,<0.9"`
	 * Linux : `sudo apt install python3-rtree` or `pip install Rtree`

* Missing C lib on mac (just after the Rtree problem) :
	*  `brew install spatialindex`

* Any missing librairies like **scipy**,**shapely**,**networkx**,**piglet**
	* `pip3 install "librairie_name"`

* No module name '_tkinter' :
	* `sudo apt install python3-tk`

## Start the simulation

* `python3 main.py`

## Deactivate Graphic User Interface (GUI)

* open the file `shared_parameters.py` and replace True with False in GUI_window parameter.

## Docker user guide :
* First of all make sure to have [docker](https://hub.docker.com/search?q=&type=edition&offering=community&sort=updated_at&order=desc) setup on your computer
* Go on project folder
* BUILD : `docker build -t python:simulation .`
* RUN : `docker run --name CONTAINER_NAME -ti python:simulation`
* Copy the beta file from the container : `sudo docker cp CONTAINER_NAME:/app/input/beta_"MESH_NAME"_"N_VALUE".txt DESTINATION_PATH`

* Warnings about the beta file copy :
	* Be sure to know which N value and mesh name you're using. Exemple of complete beta file name : `beta_head_2.txt`
	* Destination path must be the complete path ! 

## Speed up simulation process with conda :
* Install [anaconda](https://www.anaconda.com/products/individual)
* Create an conda environment : `conda create --name ENV_NAME`
* Active the conda environment : `conda activate ENV_NAME`
* Install pyembree and trimesh with conda : `conda install -c conda-forge pyembree` and `conda install -c conda-forge trimesh`
* Then you may need to install some others librairies, like matplotlib networkx pyglet scipy vtkplotter : `pip install LIBRAIRY_NAME`
* Launch the programm with : `python3 main.py` (make sure your conda env is activate)
