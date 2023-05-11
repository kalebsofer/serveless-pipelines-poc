import logging
import sys
import os


PROJECT_ID = "forecasting-test-382708"
LOCAL_TESTING = os.environ.get("LOCAL_TESTING")
LOGGER_NAME = "ingestion_function"

# Do not change the Sales Force items: they are received via secret env
#  variables during terraform deployment. Note that these secrets need
#  to be created manually on your GCP Secrets Manager before the TF deployment
SALESFORCE_USERNAME = os.environ.get("SALESFORCE_USERNAME")
SALESFORCE_PASSWORD = os.environ.get("SALESFORCE_PASSWORD")
SALESFORCE_CLIENT_ID = os.environ.get("SALESFORCE_CLIENT_ID")
SALESFORCE_CLIENT_SECRET = os.environ.get("SALESFORCE_CLIENT_SECRET")
SALESFORCE_DOMAIN = "test"

# Logger config
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(levelname)s %(asctime)s %(name)s | %(message)s")
ch.setFormatter(formatter)
logger = logging.getLogger(LOGGER_NAME)
logger.addHandler(ch)
logger.setLevel(logging.INFO)
