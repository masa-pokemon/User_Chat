FROM ubuntu:22.04

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get autoremove -y
RUN RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y python3-pip python3-dev


RUN pip3 install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /home/workspace
