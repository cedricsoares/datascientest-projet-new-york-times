"""load module"""

import logging
from typing import Any, Dict

from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


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
