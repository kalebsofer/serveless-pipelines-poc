import logging
import sys
import os


PROJECT_ID = "forecasting-test-382708"
LOCAL_TESTING = os.environ.get("LOCAL_TESTING")
LOGGER_NAME = "bigquery_query_to_table"

# Logger config
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(levelname)s %(asctime)s %(name)s | %(message)s")
ch.setFormatter(formatter)
logger = logging.getLogger(LOGGER_NAME)
logger.addHandler(ch)
logger.setLevel(logging.INFO)
