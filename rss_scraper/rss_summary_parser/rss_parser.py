from datetime import datetime
import urllib.parse

import feedparser
from bs4 import BeautifulSoup
from newspaper import Article

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
        self.link = entry['link']
        self.source = urllib.parse.urlparse(self.link).netloc.split(".")[1].capitalize()
        if self.source == "Com":
            self.source = urllib.parse.urlparse(self.link).netloc
        if entry.get("content", None) == None:
            self.scrape_content()
        elif self.source.upper() in ["NYTIMES", "WASHINGTONPOST", "NPR", "LATIMES",
         "WSJ", "FOREIGNPOLICY.COM"]:
            self.scrape_content()
        else:
            self.text = BeautifulSoup(entry["content"][0]['value'], features="html.parser").get_text()
        self.title = entry['title'].replace('"', "")
        try:
            self.authors = [f"{author['name']}" for author in entry['authors']]
        except: 
            self.authors = [self.source]
        try:
            parsed_data = entry["published_parsed"]
            self.published = f"{parsed_data.tm_year}-{parsed_data.tm_mon.rjust(2, '0')}-{parsed_data.tm_mday}"
        except:
            self.published = datetime.now().strftime("%Y-%m-%d")
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

    def scrape_content(self):
        article = Article(self.link)
        article.download()
        article.parse()
        self.text = article.text
