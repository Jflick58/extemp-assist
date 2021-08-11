import re
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class RSS_Feeds(Base):
    """ORM class for the RSS feeds table
    """

    __tablename__ = "RSS_Feeds"

    id = Column(Integer, Sequence('rss_id_seq'),primary_key=True)
    url = Column(String)  

def create_database():
    """Create a new empty database
    """
    engine = create_engine("sqlite:///rss_summary_parser/rss.db", echo=False)
    Base.metadata.create_all(engine)

def add_rss_feed(rss_feed_url:str): 
    """Add a new RSS feed to the RSS_Feeds table

    :param rss_feed_url: URL of RSS Feed
    :type rss_feed_url: str
    """
    session = create_session("sqlite:///rss_summary_parser/rss.db")
    new_feed = RSS_Feeds(url=rss_feed_url)
    session.add(new_feed)
    session.commit()

def create_session(db_url:str):
    """Create SQL Alchemy Session via a Engine

    :param db_url: SQlAlchemy Connection URL
    :type db_url: str
    :return: session
    :rtype: sqlalchemy session
    """
    engine = create_engine(db_url, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def get_all_feeds():
    """Get all RSS feed URLS

    :return: list of RSS URLs
    :rtype: list
    """
    session = create_session("sqlite:///rss_summary_parser/rss.db")
    results = session.query(RSS_Feeds.url).distinct(RSS_Feeds.url).all()
    results = [result[0] for result in results]
    return results
    

    
            
