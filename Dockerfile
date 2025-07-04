
FROM ubuntu:22.04

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get autoremove -y
RUN apt-get install -y python3-pip python3-dev

RUN pip3 install --upgrade pip
RUN sudo apt update
RUN sudo apt install ffmpeg
RUN streamlit cache clear
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt


WORKDIR /home/workspace
