FROM ubuntu:22.04

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get autoremove -y
RUN apt-get install -y python3-pip python3-dev

RUN pip3 install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r requirements.txt
RUN streamlit run src/01_login.py

WORKDIR /home/workspace
