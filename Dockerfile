FROM python:slim
RUN apt update ; \
    apt upgrade -y ; \
    apt install -y python3 python3-pip python3-dev
RUN pip3 install btpy
