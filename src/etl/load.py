"""load module"""

import logging
from typing import Any, Dict

from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


logger = logging.getLogger(__name__)
logger.conifig(level=logging.INFO,
               format='%(asctime)s - %(message)s')


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

        logger.info(f'----- Start index {name} creation -----')

        response = con.indices.create(index=name, mappings=mapping,
                                      settings=settings)
    
        if response['acknowledged']:
            logger.info(f'----- Index {name} created successfully. -----')
        else:
            logger.warning(f'----- Failed to create {name} index. -----')


def delete_index(name: str, con: Elasticsearch) -> None:
    """Drop an index in Elastiseacrh

    Args:
            con (Elasticsearch): Connector object used to connect to database
            name (str): Index name

    Return:
        None
    """

    logger.info(f'----- deleting {name} index -----')
    con.indices.delete(index=name)
    logger.info(f'----- {name} index deleted -----')


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
    logger.info('----- Start saving documents ----')
    bulk(con, bulk_list)
    logger.info('----- Finish saving documents -----')
