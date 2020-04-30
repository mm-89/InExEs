# Python 3.6.7

FROM python:3.6

COPY requirements.txt /app/

WORKDIR /app

RUN pip install --upgrade pip && \
    pip3 install --upgrade setuptools && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip install rtree==0.8.3 && \
    apt-get update && apt-get -y install libspatialindex-dev && \
    pip install trimesh[easy]
    #installing anaconda
    #apt-get install -y wget bzip2 && \
    #wget https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh && \
    #bash Anaconda3-5.0.1-Linux-x86_64.sh -b && \
    #rm Anaconda3-5.0.1-Linux-x86_64.sh'''

# Set path to conda
#ENV PATH /root/anaconda3/bin:$PATH

# Updating Anaconda packages
#RUN conda update conda
#RUN conda update anaconda
#RUN conda update --all
#RUN conda install -c conda-forge pyembree

COPY . /app
CMD ["python3", "main.py"]