"""transform module"""

import logging
from typing import Any, Dict, List


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
