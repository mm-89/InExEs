# How to install InExES

**WIP we recommend to wait the release version before cloning it**

We suppose that InExES can work on every machine, but we only try on a Mac, Linux Ubuntu 16.04 and Linux Mint 19.3


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

## Docker user guide :
* First of all make sure to have [docker](https://hub.docker.com/search?q=&type=edition&offering=community&sort=updated_at&order=desc) setup on your computer
* Go on project folder
* BUILD : `docker build -t python:simulation .`
* RUN : `docker run --rm -ti python:simulation`
