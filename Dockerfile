FROM python:slim
RUN apt-get update ; \
    apt-get upgrade -y ; \
    apt-get install -y git
RUN pip3 install git+https://github.com/nbdy/btpy
