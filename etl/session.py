import logging
import os
from typing import Optional

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

from utils import get_elasctic_connection

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s')


class Session:
    """ETL Session to retrieve data

    Attributes:
        _con (Elasticsearch): Connector object used to connect to database
        _api_key (str): Used api_key to connect to NYT APIs
        _api_calls (int): Number of calls to NYT APIs during session
    """

    def __init__(self):
        """Init method for Session class

        Args:
            _con (Elasticsearch): Connector object used to connect to database
            _api_key (str): Used api_key to connect to NYT APIs
            _api_calls (int): Number of calls to NYT APIs during session

        """
        logger.info('----- Initiate ETL Session -----')
        self._con: Elasticsearch = get_elasctic_connection()
        self._api_key: Optional[str] = os.getenv("API_KEY")
        self._api_calls: int = 0

    @property
    def con(self) -> Elasticsearch:
        """_con getter"""
        return self._con

    @property
    def api_key(self) -> Optional[str]:
        """_api_key getter"""
        return self._api_key

    @property
    def api_calls(self) -> int:
        """_api_calls getter"""
        return self._api_calls

    @api_calls.setter
    def api_calls(self, new_api_calls: int) -> None:
        """_api_calls setter"""
        self._api_calls = new_api_calls

    def is_remaining_api_calls(self, max_api_calls: int) -> bool:
        """Check if it remains available NYT API calls in ETL session

        Args:
            api_calls (int): Consumed api_calls by the current session
            max_api_calls: Maximum of dailly calls allowed by the NYT API

        Returns:
            bool: True if session.api_calls < max_api_calls else False
        """

        return True if self.api_calls < max_api_calls else False
