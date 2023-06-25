""" ETL to retrieve data from NYT APIs"""

import logging
from typing import Dict, Any

import fire
import time

from session import Session
from constants import MAX_API_CALLS, RESULTS_BY_PAGE, CONFIGURATIONS
from extract import get_books_or_movies, get_news
from load import create_index, delete_index
from utils import get_start_offset, is_start_offset_valid

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s')


def get_session_configurations(news: bool, books: bool,
                               movies: bool) -> Dict[str, Any]:
    """Build a list of configurarations to run a ETL session

        If an argument is True, its configuration will be appended
        to qreturned result.

        A configuration is a dictionary containing:
        index name, index mapping, settings

        Args:
            news (bool): If True news configuration will be appended
            books (bool): If True books configuration will be appended
            movies (bool): If True, movies configuration will be appended

        Returns:
            selected_configuurations (dict): dictionary of configurations to use
                for running an ETL session
    """
    selected_configurations = {}

    for arg_name, arg_value in locals().items():
        if arg_name == 'selected_configurations':
            continue

        if arg_value:
            selected_configurations[f'{arg_name}'] = CONFIGURATIONS[f'{arg_name}']

    logger.info(f'----- Selected configurations: \n {selected_configurations.keys()} \n')

    return selected_configurations


def run(session: Session, selected_configurations: Dict[str, Any]) -> None:
    """Run ETL session on selected configurations

        Args:
            selected_configurations (dict): dictionary of configurations to use
                for running an ETL session

        Returns:
            None
    """

    for configuration_name, configuration_params in selected_configurations.items():

        logger.info(f'----- Starts runing ETL on {configuration_name} -----')

        if (configuration_name == 'news') and (session.con.indices.exists(index='news')):
            delete_index(name=configuration_name, con=session.con)

        if not session.con.indices.exists(index=configuration_name):  # Check if index exists on Elasticsearch

            name = configuration_name
            mapping = configuration_params['mapping']
            settings = configuration_params['settings']

            create_index(con=session.con, name=name, mapping=mapping,
                         settings=settings)

        if session.is_remaining_api_calls(max_api_calls=MAX_API_CALLS):

            if configuration_name == 'news':
                get_news(session=session, max_api_calls=MAX_API_CALLS)

            else:
                get_books_or_movies(index_name=configuration_name,
                                    results_by_page=RESULTS_BY_PAGE,
                                    session=session,
                                    max_api_calls=MAX_API_CALLS)

        logger.info(f'----- ETL finished to run on {configuration_name}  -----')

    else:
        logger.warning('----- No more available api_call for the session -----')

    logger.info('----- ETL run final end -----')


if __name__ == '__main__':
    start = time.time()
    session = Session()
    selected_configurations = fire.Fire(get_session_configurations)
    run(session=session, selected_configurations=selected_configurations)
    end = time.time()
    runtime = end - start
    logger.info(f'----- ETL took {runtime} seconds to run -----')
