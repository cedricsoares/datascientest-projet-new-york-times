""" ETL to retrieve data from NYT APIs"""

import logging
import os

from constants import (BOOKS_MAPPING, INDEXES_SETTINGS, INDEXEXES_NAMES,
                       MAX_API_CALLS, NEWSWIRE_MAPPING, RSEULTS_BY_PAGE)
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from utils import get_elasctic_connection

load_dotenv()


class Session:
    """ETL Session to retrieve data

    Attributes:
        _con (Elasticsearch): Connector object used to connect to database
        _api_key (str): Used api_key to connect to NYT APIs
        _api_calls (int): Number of calls to NYT APIs during session
    """

    def __init__(self, con: Elasticsearch, api_key: str, api_calls:int):
        """Init method for Session class
        
        Args:
            _con (Elasticsearch): Connector object used to connect to database
            _api_key (str): Used api_key to connect to NYT APIs
            _api_calls (int): Number of calls to NYT APIs during session
        
        """
        self._con = get_elasctic_connection()
        self._api_key = os.getenv("API_KEY")
        self._api_calls = 0

    @property
    def api_calls(self):
        """_api_calls getter"""
        return self.api_calls

    @api_calls.setter
    def api_calls(self, new_api_calls: int):
        """_api_calls setter"""
        self._api_calls = new_api_calls
