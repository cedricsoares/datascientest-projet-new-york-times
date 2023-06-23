import datetime
import json
import logging
import os
import time
from typing import Dict, List, Optional 

import requests
from constants import (API_CALL_DAILY_INDEX, BOOKS_MAPPING, END_POINT_HITS,
                       INDEXES_SETTINGS, INDEXEXES_NAMES, NEWSWIRE_MAPPING,
                       OFFSET_FACTOR)

from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

load_dotenv()

API_KEY = os.getenv("API_KEY")


def get_elactic_connection():
    """Generate elactic connector """

    return Elasticsearch(hosts="http://@localhost:9200")  # To be changed if Elasticsearch will not remain locally


def create_index(con: Elasticsearch, name: str,
    mapping: Dict[str, Dict[str, str]],
    settings: Dict[str, int]) -> None:

    """ 
    Create an index in Elasticsearch database

    Args:
        con (Elasticsearch): Connector object used to connect to database
        name (str): Index name
        mapping (dict): Index mapping
        settings (dict): Index settings

    Returns:
        None
    """

    logging.info(f'----- Star index {name} creation -----')

    response = con.indices.create(index=name, mappings=mapping,
                                    settings=settings)
   
    if response['acknowledged']:
        logging.info(f'----- Index {name} created successfully. -----')
    else:
        logging.warning(f'----- Failed to create {name} index. -----')


def build_query(index_name: str, api_key: str, 
                start_offset: Optional[int], news_section: Optional[str],
                movies_type: Optional[str]) -> str:
    """
    Build query to pass to the NYT API
    orccording to type of content we try to get data

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

    if index_name == 'books':
        query = f'https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?offset={start_offset}&api-key={api_key}'
        logging.info(f'----- Builded querry {query} -----')
        return query

    if index_name == 'movies':
        query = f'https://api.nytimes.com/svc/movies/v2/reviews/{movies_type}.json?offset={start_offset}&api-key={api_key}'
        logging.info(f'----- Builded querry {query} -----')
        return query


def get_books_or_movies(con: Elasticsearch, index_name: str, endpoint_hits: int,
                start_offset: int, results_by_page: int,
                max_api_calls: int) -> None:
    """
    Get documents from books API

    Args:
        con (Elasticsearch): Connector object used to connect to database
        content_type (str): Name of the Elasticsearch index where documents
            are added
        enpoint_hits (int): Number of returned hits from NYT API books
        start_offset (int): Offset number to pass to the API call in
            order to specify where to start retrieving data
        results_by_page (int): Number of results of each reponse from NYT API calls
        max_api_calls (int): Maximum of dailly calls allowed by the NYT API

    Returns:
        None


    """

    logging.info("----- Start getting articles from newswire API -----")

    api_calls = 1

    while (api_calls < max_api_calls):

        now = datetime.datetime.now()
        logging.info(f'----- query starts at offset:{api_calls} at: {now} -----')


        # Request the Api
        content = requests.get(f"")

        # save into the ES DB
        res = content.json()
        logging.info(f"----- Json response page regarding start_offset: {start_offset} \n {res} -----")

        docs = res['results']
        
    # Prepare the documents for bulk indexing
        actions = []
        for doc in docs:
            action = {
                "_index": index_name,
                "_source": doc
            }
            actions.append(action)

        # Perform the bulk indexing
        response = bulk(con, actions)

        # Check the response
        if not response[1]:
            saved_books = api_calls * results_by_page
            logging.info(f'----- {saved_books} books saved successfully  -----')
            logging.info(f'----- Remaining books save regarding endpoints hits: {endpoint_hits - saved_books} -----')
        else:
            logging.warning('----- Failed to save content. -----')

        start_offset += results_by_page

        api_calls += 1

        ######################################################
        time.sleep(12)  ##### TO MODIFY ACCORDING API ALLOWANCE
        ######################################################

        logging.info(f'----- Next offset to use on API call: {start_offset} -----')



    

    

    



