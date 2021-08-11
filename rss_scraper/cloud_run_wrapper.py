from flask import Flask
import os
from rss_to_elasticsearch import rss_feeds_job

app = Flask(__name__)

@app.route('/')
def wrapper():
    """GCP Cloud Run requires the ability to listen to HTTP requests. This is just a wrapper for that. 

    :return: [description]
    :rtype: [type]
    """
    rss_feeds_job()
    return "okay", 200


if __name__ == "__main__":
  app.run(host='0.0.0.0',port=int(os.environ.get('PORT',8080)))