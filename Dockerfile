
FROM ubuntu:22.04

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get autoremove -y
RUN apt-get install -y python3-pip python3-dev

RUN pip3 install --upgrade pip

RUN pip3 install deepspeech>=0.9.0,<=0.9.3
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
RUN pip install pyaudio

WORKDIR /home/workspace
