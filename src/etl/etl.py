""" ETL to retrieve data from NYT APIs"""

import logging
import os

from constants import CONFIGURATIONS
from session import Session

logger = logging.getLogger(__name__)
logger.conifig(level=logging.INFO,
               format='%(asctime)s - %(message)s')






