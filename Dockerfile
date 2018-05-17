FROM jekyll/jekyll


RUN apk update
RUN apk add py-pip 
RUN apk add python-dev
RUN apk add curl

WORKDIR /opt/install
COPY ./requirements.txt  .
RUN pip install -r requirements.txt

RUN apk add zip

USER jekyll
# run app
WORKDIR /opt/freejekyllbuilder
CMD ["python","-u","server.py"]
