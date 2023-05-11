import logging
import sys
import os

BUCKET_TO_SAVE_PREFECT_DB = "internalforecast-prefect_logs"

SF_OBJECTS_TO_RETRIEVE = [
    "Account",
    "KimbleOne__Resource__c",
    "KimbleOne__ResourceType__c",
    "KimbleOne__BusinessUnit__c",
    "KimbleOne__ActivityAssignment__c",
    "KimbleOne__DeliveryElement__c",
    "Opportunity",
    "KimbleOne__OpportunitySource__c",
    "KimbleOne__Proposal__c",
    "KimbleOne__ProposalItem__c",
    "KimbleOne__DeliveryGroup__c",
    "KimbleOne__ActivityAssignmentDemand__c",
    "KimbleOne__ResourcedActivity__c",
    "KimbleOne__ReferenceData__c",
]

LOCAL_TESTING = os.environ.get("LOCAL_TESTING")

# We retrieve the following 2 env variables that is set in
#  this cloud function during the Terraform Deployment
INGESTION_FUNCTION_URL = os.environ.get("INGESTION_FUNCTION_URL")
DUCKDB_QUERY_TO_PARQUET_FUNCTION_URL = os.environ.get(
    "DUCKDB_QUERY_TO_PARQUET_FUNCTION_URL"
)


LOGGER_NAME = "orchestration function"

# Logger
ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s     | %(levelname)s | %(name)s | %(message)s", "%H:%M:%S"
)
ch.setFormatter(formatter)
logger = logging.getLogger(LOGGER_NAME)
logger.addHandler(ch)
logger.setLevel(logging.INFO)
