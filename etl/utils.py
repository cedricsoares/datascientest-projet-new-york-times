"""Helpers functions"""
import logging
from typing import Optional
import requests

from elasticsearch import Elasticsearch
from constants import RESULTS_BY_PAGE

#from session import Session

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s')


def get_elasctic_connection():
    """Generate elactic connector"""

    return Elasticsearch(hosts="http://@localhost:9200")  # To be changed if Elasticsearch will not remain locally


def get_endpoint_hits(con: Elasticsearch, api_key: str, index_name: str) -> int:
    """get amount of endpoint hits from NYT Api for books or movies
            it executes a querry with offset = 0 to get amount of hits.
            it consumes one NYT api call
    Args:
        con (Elasticsearch): Connector object used to connect to database
        api_key (str): Used Api key to connect to NYT Api

        index_name (str): Name of the Elasticsearch index where documents
            are added
    Returns:
        endpoint_hits (int): Amount of endpoint hits returned by NTY Api
    """
    query = build_query(index_name=index_name, api_key=api_key, start_offset=0)
    content = requests.get(query)

    res = content.json()
    endpoint_hits = res['num_results']

    return endpoint_hits


def get_start_offset(con: Elasticsearch, index_name: str,
                     endpoint_hits: int) -> int:
    """ Get the start_start offset parameter to build queries for books and movies

            If checks on a specific index_name how many docuemnts are stored
            in Elastisearch

    Args:
        con (Elasticsearch): Connector object used to connect to database
        index_name (str): Name of the Elasticsearch index where documents
            are added
        endpoint_hits (int): Amount of endpoints hits retrieved by NYT Api
    """
    if not con.indices.exists(index=index_name):
        return 0

    res = con.count(index=index_name).get('count')

    if res == 0:
        return 0

    if res % RESULTS_BY_PAGE == 0:
        return res + RESULTS_BY_PAGE

    else:
        return res // RESULTS_BY_PAGE


def is_start_offset_valid(start_offset: int, results_by_page: int) -> bool:
    """Check if start offset is valid

        On NYT Api offset increments by same number that RESULTS_BY_PAGE constant.
        It means that start_offset % RESULTS_BY_PAGE == 0.

        Args:
            strat_offset (int): start_offset used to build queries for books or movies
                and movies
            results_by_page (int): Number of returned by NY Times Api documents
                per results page

        Returns:
            bool : True if start_offset % RESULTS_BY_PAGE == 0 else False
    """

    return True if start_offset % RESULTS_BY_PAGE == 0 else False


def build_query(index_name: str, api_key: Optional[str], start_offset: int = 0,
                news_section: str = '') -> str:
    """ Build query to pass to the NYT API

        Query is built according to type of content we try to get data

    Args:
        index_name (str): Specify type of the content we want to retrieve
            via NYT API. Must be news, books, movies
        start_offset (int): Specify the offset number to start retriving data.
            Only used for books and movies
        news_section: Name of the news section.
            Only used for news.

    Return:
        str: Builded querry regarding passed parameters
    """
    logger.info('----- Strat building querry for NYT API -----')

    if index_name == 'news':
        query = f'https://api.nytimes.com/svc/news/v3/content/all/{news_section}.json?&api-key={api_key}'
        logger.info(f'----- Builded querry for {index_name}-----')
        return query

    if index_name == 'news_sections':
        query = f'https://api.nytimes.com/svc/news/v3/content/section-list.json?&api-key={api_key}'
        logger.info(f'----- Builded querry for {index_name} -----')
        return query

    if index_name == 'books':
        query = f'https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?offset={start_offset}&api-key={api_key}'
        logger.info(f'----- Builded querry {index_name} -----')
        return query

    if index_name == 'movies':
        query = f'https://api.nytimes.com/svc/movies/v2/reviews/all.json?offset={start_offset}&api-key={api_key}'
        logger.info(f'----- Builded querry {index_name} -----')
        return query

    else:
        return " "
