FROM ubuntu:latest

# Setup python in container
RUN apt update
RUN apt -y install python3
RUN apt -y install python3-pip

# Download required library
RUN apt -y install libgeos++-dev

# Download required python imports
RUN pip3 install numpy
RUN pip3 install numpy-stl
RUN pip3 install shapely
RUN pip3 install progress
RUN pip3 install Pillow

# Create directory and copy source files
RUN mkdir /pytracer
COPY ./main.py /pytracer/main.py
COPY ./LangEngine.py /pytracer/LangEngine.py
COPY ./Engine3D.py /pytracer/Engine3D.py
COPY ./ImageEngine.py /pytracer/ImageEngine.py
COPY ./PathingEngine.py /pytracer/PathingEngine.py
COPY ./QuadTree.py /pytracer/QuadTree.py

# Execute script
WORKDIR /pytracer
CMD [ "python3", "main.py" ]