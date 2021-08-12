from rss_summary_parser.elasticsearch_integration import Elasticsearch_Integration
from rss_summary_parser.rss_parser import RSS_Parser, RSS_Entry
from rss_summary_parser. database import get_all_feeds

import multiprocessing
import logging 
import sys
import os 
import traceback
import time

logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s - RSS Scraper: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO)

def RSS_to_ElasticSearch(link:str):
    """Core method to parse an RSS feed, summarize the articles, and index them in ElasticSearch

    :param link: RSS URL, often ends in .XML
    :type link: str
    """
    es_host = os.environ["ES_HOST"]
    es_token = os.environ["ES_TOKEN"]

    logging.info(f"Starting job for {link}")
    rss = RSS_Parser(link)
    logging.info(f"Grabbing RSS feed at {link}")
    entries = rss.parse()
    logging.info(f"Parsing RSS Feed from {link}")
    parsed_entries = []
    for entry in entries:
        try: 
            parsed_entries.append(RSS_Entry(entry).to_dict())
        except BaseException as e:
            logging.info(str(e))
            logging.info(traceback.format_exc())
            continue
    logging.info("Connecting to ElasticSearch...")
    es = Elasticsearch_Integration(es_host, es_token, "extemp-assist")
    logging.info("Connected to ElasticSearch.")
    logging.info(f"Indexing {len(parsed_entries)} articles with ElasticSearch")
    if len(parsed_entries) == 0:
        logging.info(f"Couldn't get entries for {link}")
        return
    es.index_documents(parsed_entries)
    logging.info(f"Job complete for {link}")

def rss_feeds_job():
    """Method to retrieve all RSS feeds and run them in pararell batches of 4 concurrent processes. 
    """
    feeds = get_all_feeds()
    pool = multiprocessing.Pool(8)
    pool.map(RSS_to_ElasticSearch, feeds)



if __name__ == '__main__':
    rss_feeds_job()


