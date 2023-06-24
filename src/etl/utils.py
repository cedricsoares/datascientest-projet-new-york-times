"""Helpers functions"""
import logging
from typing import Optional

from elasticsearch import Elasticsearch

from session import Session


def get_elasctic_connection():
        """Generate elactic connector"""

        return Elasticsearch(hosts="http://@localhost:9200")  # To be changed if Elasticsearch will not remain locally


def is_remaining_api_calls(session: Session, max_api_calls: int) -> bool:
    """Check if it remains available NYT API calls in ETL session

    Args:
        session (Session): Used ETL session
        max_api_calls: Maximum of dailly calls allowed by the NYT API

    Returns:
        bolean: True if session.api_calls < max_api_calls else False
    """

    return True if session.api_calls < max_api_calls else False


def get_start_offset(con: Elasticsearch, endpoints_hits: int, index_name: str) -> int:
    """ Get the start_start offset parameter to build queries for books and movies

            It compares retrived hits from NYT api call to retrived hits from
            a specific Elasticsearch index

    Args:
        con (Elasticsearch): Connector object used to connect to database
        endpoints_hits (int): Retrived hits from NYT Api
        index_name (str): Name of the Elasticsearch index where documents
            are added
    """
    if not con.indices.exists(index=index_name):
        return 0
    
    return (con.count(index=index_name).get('count') + 1)


def build_query(index_name: str, api_key: str,
                start_offset: Optional[int], news_section: Optional[str],
                movies_type: Optional[str]) -> str:
    """ Build query to pass to the NYT API
        
        Query is built according to type of content we try to get data

    Args:
        index_name (str): Specify type of the content we want to retrieve
            via NYT API. Must be news, books, movies
        start_offset (int): Specify the offset number to start retriving data.
            Only used for books and movies
        news_section: Name of the news section.
            Only used for news.
        movies_type: Name of type of movies.
            Only used on movirs.

    Return:
        str: Builded querry regarding passed parameters
    """
    logging.info('----- Strat building querry for NYT API -----')

    if index_name == 'news':
        query = 'https://api.nytimes.com/svc/news/v3/content/all/{news_section}.json?&api-key={api_key}'
        logging.info(f'----- Builded querry {query} -----')
        return query

    if index_name == 'news_sections':
        query = f'https://api.nytimes.com/svc/news/v3/content/section-list.json?&api-key={api_key}'
        logging.info(f'----- Builded querry {query} -----')
        return query

    if index_name == 'books':
        query = f'https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?offset={start_offset}&api-key={api_key}'
        logging.info(f'----- Builded querry {query} -----')
        return query

    if index_name == 'movies':
        query = f'https://api.nytimes.com/svc/movies/v2/reviews/all.json?offset={start_offset}&api-key={api_key}'
        logging.info(f'----- Builded querry {query} -----')
        return query
    


