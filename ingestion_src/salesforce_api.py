from simple_salesforce import Salesforce
import os
import json
from config import (
    logger,
    SALESFORCE_USERNAME,
    SALESFORCE_PASSWORD,
    SALESFORCE_CLIENT_ID,
    SALESFORCE_CLIENT_SECRET,
    SALESFORCE_DOMAIN,
)


def create_sf_client():
    "Creates salesforce client from secrets in OS env and returns it"

    sf_client = Salesforce(
        username=SALESFORCE_USERNAME,
        password=SALESFORCE_PASSWORD,
        consumer_key=SALESFORCE_CLIENT_ID,
        consumer_secret=SALESFORCE_CLIENT_SECRET,
        domain=SALESFORCE_DOMAIN,
    )

    return sf_client


def query_bulk(sf_client, obj_name: str):
    """Query all fields and all records against a given object
    Returns records as JSONL inside a string variable
    """

    desc = getattr(sf_client, obj_name).describe()

    field_names = [field["name"] for field in desc["fields"]]
    if obj_name in ["KimbleOne__Resource__c", "KimbleOne__ActivityAssignment__c"]:
        pii = [
            "Name",
            "NameAndPrimaryRole__c",
            "KimbleOne__FirstName__c",
            "KimbleOne__LastName__c",
        ]
        field_names = [i for i in field_names if i not in pii]

    query = "SELECT {} FROM {}".format(",".join(field_names), obj_name)
    query_result = sf_client.query_all(query)

    jsonlines_str = ""
    for entry in query_result["records"]:
        entry.pop("attributes")
        jsonlines_str += json.dumps(entry) + "\n"

    logger.info(f"Retrieved object: {obj_name}, size: {query_result['totalSize']}")

    return jsonlines_str
