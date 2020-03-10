# How to install InExES

We suppose that InExES can work on every machine, but we only try on a Mac, Linux Ubuntu 16.04 and Linux Mint


## Prerequisite

**Python 3.5** or newer 

## Install instructions

    git clone https://github.com/mm-89/InExEs.git
	pip3 install trimesh
	pip3 install Rtree
	pip3 install shapely

## Librairies problems

You may face some problems reguarding libraries installation. Where is some solutions.
* Cannot install Rtree on mac or Linux :
	 * MAC : `pip install "rtree>=0.8,<0.9"`
	 * Linux : `sudo apt install python3-rtree`

* Missing C lib on mac (just after the Rtree problem) :
	*  `brew install spatialindex`

* Any missing librairies like **scipy**,**shapely**,**networkx**,**piglet**
	* `pip3 install "librairie_name"`

## Start the simulation

* `python3 main.py`