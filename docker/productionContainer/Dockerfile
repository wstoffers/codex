FROM python:3-slim

#Set working directory
WORKDIR /home/sandbox
COPY . /home/sandbox

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080