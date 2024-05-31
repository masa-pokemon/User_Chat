FROM ubuntu:22.04

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get autoremove -y
RUN apt-get install -y python3-pip python3-dev

RUN pip3 install --upgrade pip
COPY requirements.txt /tmp/requirements.txt
RUN pip freeze > requirements.txt
RUN pip uninstall requirements.txt
RUN pip install streamlit==1.28.1 streamlit-authenticator==0.3.2 streamlit-autorefresh==1.0.1 extra-streamlit-components==0.1.56 st-pages==0.4.5 watchdog==3.0.0 numpy==1.25.0 Pillow==9.5.0 openai
RUN streamlit run src/01_login.py

WORKDIR /home/workspace
