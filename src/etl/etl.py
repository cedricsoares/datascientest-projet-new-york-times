""" ETL to retrieve data from NYT APIs"""

import logging

from constants import CONFIGURATIONS
from session import Session

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s')


if __name__ == '__main__':
    session = Session()
    selected_configurations = session.get_session_configurations(configurations=CONFIGURATIONS)
    session.run(selected_configurations=selected_configurations)
