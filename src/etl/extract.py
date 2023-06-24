"""Extract module"""


import logging
import time
from datetime import datetime
from typing import List

import requests
from load import bulk_to_elasticsearch
from session import Session
from transform import results_to_list
from utils import build_query, is_remaining_api_calls, get_start_offset

logger = logging.getLogger(__name__)
logger.conifig(level=logging.INFO,
               format='%(asctime)s - %(message)s')


def get_news(session: Session, max_api_calls: int) -> None:
    """Run entire process to get news data from NYT API

            It runs get_news_sections() to get section and get_news_data()
            if it remains any NYT API calls in the ETL Session

    Args:
        session (Session): Used ETL session
        max_api_calls (int): Maximum of dailly calls allowed by the NYT API  

    Returns:
        None
    """
    sections = get_news_sections(session=session)

    if (is_remaining_api_calls(session=session, max_api_calls=max_api_calls)):
        get_news_data(session=session, sections=sections)


def get_news_sections(session: Session) -> List(str):
        """ Get list of news section from NYT API

        Args:
            session (Session): Used ETL session

        Returns:
            sections (list): List of news sections retrieved from NYT API
        """
        logger.info('----- Retrieving news sections -----')
        query = build_query(index_name='news_sections',
                            api_key=session.api_key)
        results = requests.get(query)
        sections = [item['section'] for item in results.json()['results']]
        logger.info(f'----- News sections: \n {sections} \n')

        session.api_calls += 1

        return sections


def get_news_data(session: Session, sections: List[str]) -> None:
    """Get news documents from NYT newswire API

    Args:
        session (Session): Used ETL session
        sections (list): List of news sections
    
    Returns:
        None
    """

    logger.info('----- Start geting news data from NYT API -----')

    for section in sections:

        logger.info(f'----- Start retriving data from section: {section} -----')

        # Request the Api
        query = build_query(index_name='news', news_section=section,
                            api_key=session.api_key)
        content = requests.get(query)

        # save into the ES DB
        res = content.json()
        logger.info(f'----- Retrieved results: \n {res} \n -----')       

        docs = res['results']

        # Prepare the documents for bulk indexing
        actions = results_to_list(index_name='news', results=docs)

        # Perform the bulk indexing
        response = bulk_to_elasticsearch(con=session.con, bulk_list=actions)

        # Check the response
        if not response[1]:
            print(f'{section} saved successfully')
        else:
            print('Failed to save content.')

        session.api_calls += 1
        
        ######################################################
        time.sleep(13) ##### TO MODIFY ACCORDING API ALLOWANCE
        #################### 5 requests max per minute ######
        ######################################################


def get_books_or_movies(index_name: str,
                        results_by_page: int, session: Session,
                        max_api_calls: int) -> None:
    """Get books or movies documents from books API
        For both logic is the same due to API calls limites

    Args:
        index_name (str): Name of the Elasticsearch index where documents
            are added
        results_by_page (int): Number of results of each reponse from NYT API calls
        session (Session): Used ETL session
        max_api_calls (int): Maximum of dailly calls allowed by the NYT API

    Returns:
        None
    """
    logger.info(f'----- Start getting {index_name} from NYT API -----')

    internal_api_calls = 0

    while (is_remaining_api_calls(session=session, max_api_calls=max_api_calls)):

        now = datetime.datetime.now()
        logger.info(f'----- Number of NYT API calls {internal_api_calls} \n -----')
        logger.info(f'----- query starts at offset:{internal_api_calls} at: {now} -----')

        # Request the Api
        query = build_query(index_name=index_name, start_offset=start_offset)
        content = requests.get(query)

        # save into the ES DB
        res = content.json()
        endpoint_hits = res['num_results']

        start_offset = get_start_offset(con=session.con, endpoints_hits=endpoint_hits,
                                        index_name=index_name)

        logger.info(f"----- Json response page regarding start_offset: {start_offset} \n {res} -----")

        docs = res['results']
        actions = results_to_list(index_name=index_name, results=docs)

        # Perform the bulk indexing
        response = bulk_to_elasticsearch(con=session.con, bulk_list=actions)

        # Check the response
        if not response[1]:
            saved_books = internal_api_calls * results_by_page
            logger.info(f'----- {saved_books} books saved successfully  -----')
            logger.info(f'----- Remaining books save regarding endpoints hits: {endpoint_hits - saved_books} -----')
        else:
            logger.warning('----- Failed to save content. -----')

        start_offset += results_by_page

        session.api_calls += 1
        internal_api_calls += 1

        ######################################################
        time.sleep(12)  ##### TO MODIFY ACCORDING API ALLOWANCE
        ######################################################

    logger.info(f'----- Next offset to use on API call: {start_offset} -----')
