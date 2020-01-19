#!/bin/bash
shared=/home/kamil/Projects/Degree/Container/
docker build -t pytracer .
docker run -it --rm \
-v ${shared}config:/pytracer/config \
-v ${shared}images:/pytracer/images \
-v ${shared}input:/pytracer/input \
-v ${shared}output:/pytracer/output pytracer