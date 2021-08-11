from datetime import datetime
import urllib.parse

import feedparser
from bs4 import BeautifulSoup

from . import summarize


class RSS_Parser:

    def __init__(self, url:str):
        """Parse a given URL into Entry objects

        :param url: RSS URL, usually ends in .XML
        :type url: str
        """
        self.url = url

    def parse(self):
        """Parse the given RSS feed

        :return: Feed
        :rtype: list
        """
        feed = feedparser.parse(self.url)['entries']
        return feed
        
class RSS_Entry:

    def __init__(self, entry:feedparser.util.FeedParserDict):
        """Class to handle a single RSS article

        :param entry: A single RSS article
        :type entry: feedparser.util.FeedParserDict
        """
        self.text = BeautifulSoup(entry["content"][0]['value'], features="html.parser").get_text()
        self.link = entry['link']
        self.title = entry['title'].replace('"', "")
        self.source = urllib.parse.urlparse(self.link).netloc.split(".")[1].capitalize()
        try:
            self.authors = [f"{author['name']}" for author in entry['authors']]
        except: 
            self.authors = [self.source]
        self.published = entry["published"]
        self.summary = summarize.summarize(self.text)

    def to_dict(self):
        """Cast specifc object attributes to dictionary

        :return: Attributes as dict
        :rtype: dict
        """
        attrs = {
            "id": self.title,
            "source": self.source,
            "title": self.title,
            "published": self.published,
            "authors": ', '.join(self.authors),
            "link": self.link,
            "summary": self.summary
        }
        return attrs
