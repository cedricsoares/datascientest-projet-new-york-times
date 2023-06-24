"""Helpers functions"""
import logging
from typing import Optional

from elasticsearch import Elasticsearch


def get_elasctic_connection():
        """Generate elactic connector """

        return Elasticsearch(hosts="http://@localhost:9200")  # To be changed if Elasticsearch will not remain locally


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
