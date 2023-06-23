import datetime
import json
import logging
import os
import time
from typing import Dict, List, Tuple, Optional, Any

import requests
from constants import (API_CALL_DAILY_INDEX, BOOKS_MAPPING, END_POINT_HITS,
                       INDEXES_SETTINGS, INDEXEXES_NAMES, NEWSWIRE_MAPPING,
                       OFFSET_FACTOR)
from elasticsearch import Elasticsearch
from utils.get_information_helpers import (build_query, results_to_list, 
                                           bulk_to_elasticsearch)

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_CALLS = 0


def get_elactic_connection():
    """Generate elactic connector """

    return Elasticsearch(hosts="http://@localhost:9200")  # To be changed if Elasticsearch will not remain locally


def create_index(con: Elasticsearch, name: str,
    mapping: Dict[str, Dict[str, str]],
    settings: Dict[str, int]) -> None:

    """Create an index in Elasticsearch database

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


def get_news_sections(con: Elasticsearch, api_key: str, 
                          api_calls: int) -> Tuple(List(str), int):
    """ Get list of news section from NYT API

    Args:
        con (Elasticsearch): Connector object used to connect to database
        api_key (str): Used NYT api key to retrieve data
        api_call (int): Number of API calls

    Returns:
        sections (list): List of news sections retrieved from NYT API
        api_calls (int): number of calls done by the script
    """
    logging.info('----- Retrieving news sections -----')
    query = build_query(index_name='news_sections', api_key=api_key)
    results = requests.get(query)
    sections = [item['section'] for item in results.json()['results']]
    logging.info(f'----- News sections: \n {sections} \n')

    api_calls += 1

    return sections, api_calls


def get_books_or_movies_data(con: Elasticsearch, index_name: str,
                start_offset: int, results_by_page: int, api_cals: int,
                max_api_calls: int, api_key: str) -> int:
    """Get books or movies documents from books API
        For both logic is the same due to API calls limites

    Args:
        con (Elasticsearch): Connector object used to connect to database
        content_type (str): Name of the Elasticsearch index where documents
            are added
        enpoint_hits (int): Number of returned hits from NYT API books
        start_offset (int): Offset number to pass to the API call in
            order to specify where to start retrieving data
        api_calls (int): Number of API calls since start of the script 
        results_by_page (int): Number of results of each reponse from NYT API calls
        max_api_calls (int): Maximum of dailly calls allowed by the NYT API
        api_key (str): Used NYT api key to retrieve data

    Returns:
        api_calls (int): number api calls used by the function
    """
    logging.info(f'----- Start getting {index_name} from NYT API -----')

    while (api_calls < max_api_calls):

        now = datetime.datetime.now()
        logging.info(f'----- Number of NYT API calls {api_calls} \n -----')
        logging.info(f'----- query starts at offset:{api_calls} at: {now} -----')


        # Request the Api
        query = build_query(index_name=index_name, start_offset=start_offset)
        content = requests.get(query)

        # save into the ES DB
        res = content.json()
        endpoint_hits = res['num_results']

        logging.info(f"----- Json response page regarding start_offset: {start_offset} \n {res} -----")

        docs = res['results']
        actions = results_to_list(index_name=index_name, results=docs)

        # Perform the bulk indexing
        response = bulk_to_elasticsearch(con, actions)

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
        
        return api_cals


