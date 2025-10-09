FROM python:3
WORKDIR /usr/src/app
RUN pip install numpy
RUN pip install requests