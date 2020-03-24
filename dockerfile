# Python 3.6.7

FROM python:3.6

COPY requirements.txt /app/

WORKDIR /app

RUN pip install --upgrade pip && \
    pip3 install --upgrade setuptools && \
    pip3 install --no-cache-dir -r requirements.txt && \
    pip install rtree==0.8.3 && \
    apt-get update && apt-get -y install libspatialindex-dev

COPY . /app
CMD ["python3", "main.py"]