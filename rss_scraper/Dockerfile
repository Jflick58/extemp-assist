# INSTALL PYTHON IMAGE
FROM python:3.8

#VARS
ARG ES_HOST=""
ENV ES_HOST=$ES_HOST

ARG ES_TOKEN=""
ENV ES_TOKEN=$ES_TOKEN

# INSTALL REQUIREMENTS
RUN mkdir /app
COPY ./requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

#COPY REPO TO CONTAINER
COPY . /app

ENTRYPOINT ["python"]

CMD ["rss_to_elasticsearch.py"]