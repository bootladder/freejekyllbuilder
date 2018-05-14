FROM ubuntu:14.04

# install dependencies
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential curl

WORKDIR /opt/install
COPY ./requirements.txt  .
RUN pip install -r requirements.txt

# run app
WORKDIR /opt/freejekyllbuilder
CMD ["python","-u","server.py"]
