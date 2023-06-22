import datetime
import json
import logging
import os
import time
from typing import Dict, List

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
    CReate an index in Elasticsearch database

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


def get_books(con: Elasticsearch, index_name: str, endpoint_hits: int,
                api_call_daily_index: int, offset_value: int,
                offset_factor: int, max_api_calls: int = 2,
                list_lenght: int = 2) -> None:
    """
    Get documents from books API
    
    Args

    """
    continue_loading = True

    logging.info("----- Start getting articles from newswire API -----")

    while (continue_loading):

        api_call_daily_index += 1
        continue_loading = api_call_daily_index < max_api_calls

        # Request the Api
        content = requests.get(f"https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?offset={offset_value}&api-key={API_KEY}")

        # save into the ES DB
        res = content.json()
        logging.info(f"----- Json response page regarding offset_value: {offset_value} \n {res} -----")

        docs = res['results']
        
    # Prepare the documents for bulk indexing
        actions = []
        for doc in docs:
            action = {
                "_index": index_name,
                "_source": doc
            }
            actions.append(action)

        now = datetime.datetime.now()
        logging.info(f'----- query index:{api_call_daily_index} at: {now} -----')

        # Perform the bulk indexing
        response = bulk(con, actions)

        # Check the response
        if not response[1]:
            logging.info(f'----- {api_call_daily_index * offset_factor} /35311 books saved successfully -----')
        else:
            logging.warning('----- Failed to save content. -----')

        ######################################################
        time.sleep(12)  ##### TO MODIFY ACCORDING API ALLOWANCE
        ######################################################

    logging.info('----- end of the API loop -----')



