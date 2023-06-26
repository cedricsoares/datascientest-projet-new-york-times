"""Extract module"""


import logging
import time
from typing import List

import requests


from session import Session
from utils import build_query, get_endpoint_hits, get_start_offset
from load import bulk_to_elasticsearch
from transform import results_to_list


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
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

    if (session.is_remaining_api_calls(max_api_calls=max_api_calls)):
        get_news_data(session=session, sections=sections, max_api_calls=max_api_calls)


def get_news_sections(session: Session) -> List[str]:
    """ Get list of news section from NYT API

    Args:
        session (Session): Used ETL session

    Returns:
        sections (list): List of news sections retrieved from NYT API
    """

    logger.info('----- Retrieving news sections -----')
    query = build_query(index_name='news_sections', api_key=session.api_key)
    results = requests.get(query)
    sections = [item['section'] for item in results.json()['results']]
    logger.info(f'----- News sections: \n {sections} \n')

    session.api_calls += 1

    return sections


def get_news_data(session: Session, sections: List[str], max_api_calls: int) -> None:
    """Get news documents from NYT newswire API

    Args:
        session (Session): Used ETL session
        sections (list): List of news sections
        max_api_calls (int): Maximum of dailly calls allowed by the NYT API

    Returns:
        None
    """

    logger.info('----- Start geting news data from NYT API -----')

    for section in sections:
        if section == 'multimedia/photos': # multimedia/photos section name causes an error when sending query to NYT Api
            continue
        if session.is_remaining_api_calls(max_api_calls=max_api_calls):
            logger.info(f'----- Start retriving data from section: {section} -----')

            query = build_query(index_name='news', news_section=section,
                                api_key=session.api_key)
            content = requests.get(query)

            # save into the ES DB
            res = content.json()

            docs = res['results']
            saved_documents_request = len(docs)

            # Prepare the documents for bulk indexing
            actions = results_to_list(index_name='news', results=docs)

            bulk_to_elasticsearch(con=session.con, bulk_list=actions)

            session.api_calls += 1
            print(f'{section} : {session.api_calls}')

            ######################################################
            time.sleep(13)  ##### TO MODIFY ACCORDING API ALLOWANCE
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

    logger.info(f'----- Number of NYT API calls {session.api_calls} -----')

    endpoint_hits = get_endpoint_hits(con=session.con, api_key=session.api_key,
                                      index_name=index_name)

    internal_api_calls += 1  # A first API call is used to get endpoint_hits

    start_offset = get_start_offset(con=session.con,
                                    index_name=index_name,
                                    endpoint_hits=endpoint_hits)

    while (session.is_remaining_api_calls(max_api_calls=max_api_calls)):

        logger.info(f'----- Number of NYT API calls {session.api_calls} -----')
        logger.info(f'----- query starts at offset:{start_offset} -----')

        query = build_query(index_name=index_name, api_key=session._api_key,
                            start_offset=start_offset)

        content = requests.get(query)

        res = content.json()
        endpoint_hits = endpoint_hits = res['num_results']
        docs = res['results']
        saved_documents_request = len(docs)

        actions = results_to_list(index_name=index_name, results=docs)

        saved_documents = start_offset + saved_documents_request
        bulk_to_elasticsearch(con=session.con, bulk_list=actions)
        logger.info(f'----- Remaining documents to save regarding endpoints hits: {endpoint_hits - saved_documents} -----')

        start_offset += results_by_page

        session.api_calls += 1
        internal_api_calls += 1

        ######################################################
        time.sleep(12)  ##### TO MODIFY ACCORDING API ALLOWANCE
        ######################################################

    logger.info(f'----- Next offset to use on API call: {start_offset} -----')
