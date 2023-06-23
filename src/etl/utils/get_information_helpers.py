from typing import Dict, List, Optional, Any
from elasticsearch import Elasticsearch
from elastic_transport import ObjectApiResponse
from elasticsearch.helpers import bulk
import logging


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
    
def results_to_list(index_name: str,
                    results: List[Dict[str, Any]]) -> List[Dict[str, Dict[Any]]]:
    """Transform a list of documents from NTY API to dict to bulk on Elasticsearch
  
    Args:
        index_name (str): index_name to provide to bulk data to Elasticsearch
        results (list): A list of documents retrived by NYT API

    Retuns
        bulk_list (lits): A list of index_name / documents ready to bulk on Elasticsearch
    """
    logging.info(f'----- Start building bulk list for {index_name} index -----')
    actions = []
    for doc in results:
        action = {
            "_index": index_name,
            "_source": doc
        }
        actions.append(action)
    logging.info(f'----- List to bulk on Elasticsearch : \n {actions} \n -----')
    return actions


def bulk_to_elasticsearch(
        con: Elasticsearch, bulk_list: Dict[str, Dict[Any]]
        ) -> ObjectApiResponse[Any][Any]:
    """ Run Elasticsearch Bulk API with results from NYT API 
    
    Args:
        con (Elasticsearch): 
        bult_list (list): A list of documents with index_names from NYT API results

    Returns:
        ObjectApiREsponse : Response from Elasticsearh Bulk API call
    """
    logging.info('----- Start calling Elasticsearck Bulk API -----')
    bulk(con, bulk_list)
