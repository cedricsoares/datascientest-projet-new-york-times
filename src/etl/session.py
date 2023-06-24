from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from utils import get_elasctic_connection
import os
import logging


load_dotenv()
logger = logging.getLogger(__name__)


class Session:
    """ETL Session to retrieve data

    Attributes:
        _con (Elasticsearch): Connector object used to connect to database
        _api_key (str): Used api_key to connect to NYT APIs
        _api_calls (int): Number of calls to NYT APIs during session
    """

    def __init__(self, _con: Elasticsearch, _api_key: str, _api_calls:int, ):
        """Init method for Session class
        
        Args:
            _con (Elasticsearch): Connector object used to connect to database
            _api_key (str): Used api_key to connect to NYT APIs
            _api_calls (int): Number of calls to NYT APIs during session
        
        """
        logger.info('----- Initiate Session -----')
        self._con = get_elasctic_connection()
        self._api_key = os.getenv("API_KEY")
        self._api_calls = 0

    @property
    def con(self):
        """_con getter"""
        return self._con
    
    @property
    def api_key(self):
        """_api_key getter"""
        return self._api_key

    @property
    def api_calls(self):
        """_api_calls getter"""
        return self._api_calls

    @api_calls.setter
    def api_calls(self, new_api_calls: int):
        """_api_calls setter"""
        self._api_calls = new_api_calls
