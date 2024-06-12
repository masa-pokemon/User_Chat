FROM ubuntu:22.04

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get autoremove -y
RUN apt-get install -y python3-pip python3-dev

RUN pip3 freeze > uninstall.txt
RUN pip3 uninstall -y -r uninstall.txt 

RUN pip3 install --upgrade pip
RUN deepspeech>=0.9.0,<=0.9.3
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /home/workspace
