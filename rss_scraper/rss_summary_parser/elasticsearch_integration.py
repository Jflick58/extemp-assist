from elastic_enterprise_search import AppSearch
import elastic_transport

from typing import List

class Elasticsearch_Integration:

    def __init__(self, app_search_host: str,
                       app_search_token:str,
                       engine_name:str=None,
                       create_engine_if_not_exists=True):

        """Class to handle Elasticsearch connectivity and operations

        :param app_search_host: URL of AppSearch host
        :type app_search_host: str
        :param app_search_token: Searhc token
        :type app_search_token: str
        :param engine_name: Name of intended ES Engine, defaults to None
        :type engine_name: str, optional
        :param create_engine_if_not_exists: If the passed engine does not exist, create it., defaults to True
        :type create_engine_if_not_exists: bool, optional
        :raises ConnectionError: Engine does not exist
        """

        self.client = Elasticsearch_Integration.authenticate(app_search_host, app_search_token)
        self.engine = engine_name
        if not self.engine_exists():
            if not create_engine_if_not_exists:
                raise ConnectionError(f"{self.engine} does not exist")
            else: 
                self.create_engine()
        

    @staticmethod
    def authenticate(host:str, token:str):
        """Authenticate to ElasticSearch AppSearch

        :param host: host url
        :type host: str
        :param token: search token
        :type token: str
        :return: AppSearch connection
        """
        app_search = AppSearch(host,http_auth=token)
        return app_search

    def engine_exists(self):
        """Check if a given engine exists on the host

        :return: Does engine exist?
        :rtype: Bool
        """
        try:
            self.client.get_engine(engine_name=self.engine)
            return True
        except elastic_transport.exceptions.NotFoundError:
            return False
    
    def create_engine(self):
        """Create a new ES Engine
        """
        self.client.create_engine(
            engine_name=self.engine,
            language="en",
        )

    def index_documents(self, documents:List[dict]):
        """Index new documents

        :type documents: List[dict]
        """
        self.client.index_documents(
            engine_name=self.engine,
            documents=documents)



