from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from utils import get_elasctic_connection
import os
import logging
from typing import List, Dict, Any
import click
from constants import CONFIGURATIONS, MAX_API_CALLS, RESULTS_BY_PAGE
from extract import get_news, get_books_or_movies
from load import create_index
from utils import is_remaining_api_calls

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

    @click.option("--news", default=False, help="Set True to run ETL on news")
    @click.option("--books", default=False, help="Set True to run ETL on books")
    @click.option("--movies", default=False, help="Set True to run ETL on movies")
    @staticmethod
    def get_session_confifurations(
                                    news: bool, 
                                    books: bool, 
                                    movies: bool,
                                    configurations: Dict[str, Dict[str, Any]]
                                ) -> Dict[str, Any]:
        """Build a list of configurarations to run a ETL session

            If an argument is True, its configuration will be appended
            to re returned result.

            A configuration is a dictionary containing:
            index name, index mapping, settings

            Args:
                news (bool): If True news configuration will be appended
                books (bool): If True books configuration will be appended
                movies (bool): If true, movies configuration will be appended

            Returns:
                selected_configuurations (dict): dictionary of configurations to use
                    for running an ETL session
        """
        selected_configurations = {}
        for arg_name, arg_value in locals().items():
            if arg_name == 'configurations':
                continue

            if arg_value:
                selected_configurations[f'{arg_name}'] = configurations[f'{arg_name}']

        logger.info(f'----- Selected configurations: \n {configurations.keys()} \n')

        return selected_configurations
    
    def run(self, selected_configurations: Dict[str, Any]) -> None:
        """Run ETL session on selected configurations
        
            Args:
                selected_configurations (dict): dictionary of configurations to use
                    for running an ETL session

            Returns:
                None
        """

        for configuration_name, configuration_params in selected_configurations.items():

            logger.info(f'----- Starts runing ETL on {configuration_name} -----')

            if configuration_name == 'news':
                drop_index(index_name=index_name, session=session) #TODO: code method in load module

            if not self.con.indices.exists(index=configuration_name): # Check if an index exists on Elasticsearch
                
                name = configuration_name
                mapping = configuration_params['mapping']
                settings = configuration_params['settings']

                create_index(con=self.con, name=name, mapping=mapping,
                             settings=settings)
            
            if is_remaining_api_calls(session=self, max_api_call=MAX_API_CALLS):

                if configuration_name == 'news':
                    get_news(session=self, max_api_calls=MAX_API_CALLS)

                else:
                    get_books_or_movies(index_name=configuration_name,
                                        results_by_page=RESULTS_BY_PAGE,
                                         session=self,
                                         max_api_calls=MAX_API_CALLS)

            logger.info(f'----- ETL finished to run on {configuration_name}  -----')

        logger.info('----- ETL run final end -----')

