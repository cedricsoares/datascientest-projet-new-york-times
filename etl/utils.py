"""Helpers functions"""
import logging
from typing import List, Dict, Any, Optional
import requests

import hashlib
from elasticsearch import Elasticsearch, helpers

from constants import RESULTS_BY_PAGE

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s')


def get_elasctic_connection():
    """Generate elactic connector"""

    return Elasticsearch(hosts="http://@localhost:9200")  # To be changed if Elasticsearch will not remain locally


def get_endpoint_hits(con: Elasticsearch, api_key: str, index_name: str) -> int:
    """get amount of endpoint hits from NYT Api for books
            it executes a query with offset = 0 to get amount of hits.
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
    
    try:
        content = requests.get(query)
    except Exception as e:
        logger.warning(f"-----Error:{e}-----")

    res = content.json()
    endpoint_hits = res['num_results']

    return endpoint_hits


def get_start_offset(con: Elasticsearch, index_name: str) -> int:
    """ Get the start_start offset parameter to build queries for books and movies

            If checks on a specific index_name how many documents are stored
            in Elastisearch

    Args:
        con (Elasticsearch): Connector object used to connect to database
        index_name (str): Name of the Elasticsearch index where documents
            are added
        endpoint_hits (int): Amount of endpoints hits retrieved by NYT Api
    """
    try:
        if not con.indices.exists(index=index_name):
    except Exception as e:
        logger.warning(f"-----Error:{e}-----")
            return 0

    try:
        res = con.count(index=index_name).get('count')
    except Exception as e:
        logger.warning(f"-----Error:{e}-----")

    if res == 0:
        return 0

    if res % RESULTS_BY_PAGE == 0:
        return res

    else:
        return (res // RESULTS_BY_PAGE) * RESULTS_BY_PAGE  # It returns the previous mulitple of RESULTS_BY_PAGE


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
        str: built query regarding passed parameters
    """
    logger.info('----- Start building query for NYT API -----')

    if index_name == 'news':
        query = f'https://api.nytimes.com/svc/news/v3/content/all/{news_section}.json?&api-key={api_key}'
        logger.info(f'----- built query for {index_name}-----')
        return query

    if index_name == 'news_sections':
        query = f'https://api.nytimes.com/svc/news/v3/content/section-list.json?&api-key={api_key}'
        logger.info(f'----- built query for {index_name} -----')
        return query

    if index_name == 'books':
        query = f'https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json?offset={start_offset}&api-key={api_key}'
        logger.info(f'----- built query {index_name} -----')
        return query

    if index_name == 'movies':
        query = f'https://api.nytimes.com/svc/movies/v2/reviews/all.json?offset={start_offset}&api-key={api_key}'
        logger.info(f'----- built query {index_name} -----')
        return query

    else:
        return " "


# Method updated from provided one from Elasticsearch : https://www.elastic.co/fr/blog/how-to-find-and-remove-duplicate-documents-in-elasticsearch
# by Alexander Marquardt: https://github.com/alexander-marquardt/deduplicate-elasticsearch/blob/master/deduplicate-elaticsearch.py
def delete_duplicates(con: Elasticsearch, index_name: str) -> None:
    """Delete duplicates documents from a specific Elasticsearch index

    Args:
        con (Elasticsearch): Connector object used to connect to database
        index_name (str): Name of the index where to check if duplicated exist
            and delete then if so

    Return:
        None
    """
    logger.info(f'----- Start of drop duplicates process for {index_name}  index -----')
    keys_to_include_in_hash = get_index_keys(index_name=index_name)
    dict_of_duplicate_docs = scroll_over_all_docs(
                                                  con=con,
                                                  index_name=index_name,
                                                  keys_to_include_in_hash=keys_to_include_in_hash
                                                  )

    loop_over_hashes_and_remove_duplicates(con=con, index_name=index_name,
                                           dict_of_duplicate_docs=dict_of_duplicate_docs)

    logger.info(f'End of drop duplicates process from {index_name} -----')


def get_index_keys(index_name: str) -> List[str]:
    """Retrieve used index keys to detect duplicates

    Args:
        index_name (str): Name of the index where to check if duplicated exist
            and delete then if so

    Return:
        list: List of key to use to detect duplicates in the index_name
    """
    if index_name == 'news':
        return ['section', 'title', 'abstract', 'byline', 'source']

    if index_name == 'books':
        return ['title', 'description', 'contributor', 'contributor_note',
                'author']

    if index_name == 'movies':
        return ['byline', 'display_title', 'mpaa_rating', 'headline']


# Loop over all documents in the index, and populate the
# dict_of_duplicate_docs data structure.
def scroll_over_all_docs(con: Elasticsearch, index_name: str,
                         keys_to_include_in_hash: List[str]) -> Dict[Any, Any]:
    """Scroll over documents from specified index and retrieve duplicated
        documents

    Args:
        con (Elasticsearch): Connector object used to connect to database
        index_name (str): Name of the index where to check if duplicated exist
            and delete then if so
        keys_to_include_in_hash (list): List of key to use to detect
            duplicates in the index_name

    Returns:
        dict_of_duplicate_docs (dict): Dictionary of duplicated documents
    """
    try:
        for hit in helpers.scan(con, index=index_name):
            dict_of_duplicate_docs = {}
            combined_key = ""
            for mykey in keys_to_include_in_hash:
                combined_key += str(hit['_source'][mykey])

            _id = hit["_id"]

            hashval = hashlib.md5(combined_key.encode('utf-8')).digest()

            # If the hashval is new, then we will create a new key
            # in the dict_of_duplicate_docs, which will be
            # assigned a value of an empty array.
            # We then immediately push the _id onto the array.
            # If hashval already exists, then
            # we will just push the new _id onto the existing array
            dict_of_duplicate_docs.setdefault(hashval, []).append(_id)
    except Exception as e:
        logger.warning(f"-----Error:{e}-----")
            return dict_of_duplicate_docs

def loop_over_hashes_and_remove_duplicates(con, index_name,
                                           dict_of_duplicate_docs) -> None:
    """Loop over duplicated documents provided and delete theme via their id

    Args:
        con (Elasticsearch): Connector object used to connect to database
        index_name (str): Name of the index where to check if duplicated exist
            and delete then if so
        dict_of_duplicate_docs (dict): Dictionary of duplicated documents

    Return:
        None
    """

    # Search through the hash of doc values to see if any
    # duplicate hashes have been found
    for hashval, array_of_ids in dict_of_duplicate_docs.items():
        if len(array_of_ids) > 1:
            # Get the documents that have mapped to the current hasval
            for id in array_of_ids[1:]:
                try:
                    con.delete(index=index_name, id=id)
                except Exception as e:
                    logger.warning(f"-----Error:{e}-----")
            num_deleted_docs = len(array_of_ids[1:])
            logger.info(f'----- {num_deleted_docs} from {index_name} index -----')
        else:
            logger.info(f'----- No duplicated documents in {index_name} index -----')
            