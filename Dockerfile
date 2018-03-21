FROM ubuntu:latest
ENV http_proxy=http://iproxy1.glasgow.gov.uk:1045
ENV https_proxy=http://iproxy1.glasgow.gov.uk:1045
MAINTAINER GCC Data Team
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=true
RUN . /app/env.sh
CMD ["flask", "run", "--host=0.0.0.0"]