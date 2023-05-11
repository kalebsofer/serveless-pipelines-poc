import functions_framework
from datetime import datetime
from config import logger, LOCAL_TESTING
from storage import copy_blob, upload_blob_from_memory
from salesforce_api import create_sf_client, query_bulk

# different entry points for cloud and local


@functions_framework.http
def cloud_entry_point(request):
    "Receives the request as flask request and runs the function after deployed"
    return ingestion_main(request)


def local_entry_point(request):
    "Receives the request as a python dict and runs the function without using decorating with functions_framework"
    return ingestion_main(request)


# function code
def ingestion_main(request):
    """Receives a json request body with:
        - object_name: sales force object to ingest
        - saving_option: one of 2 options:
            'latest_only'
            'latest_and_historic'
        - bucket: bucket to save data
    example:
    {   'object_name':"Account",
        'saving_option':'latest_and_historic',
        'bucket':'internalforecast-data-bronze'
    }
    """

    # local testing receives the request as a dict already
    if LOCAL_TESTING == "LOCAL_WITH_CLOUD_EFFECTS":
        request_body_dict = request
    # cloud function receives request as a flask request, so need to get json out of the request
    else:
        request_body_dict = request.get_json(silent=True)

    OBJ_NAME = request_body_dict["object_name"]
    SAVING_OPTION = request_body_dict["saving_option"]
    BUCKET = request_body_dict["bucket"]

    sf_client = create_sf_client()
    query_result = query_bulk(sf_client=sf_client, obj_name=OBJ_NAME)
    logger.info("Bulk query finished")

    latest_file_name = f"{OBJ_NAME}/latest/data.jsonl"
    upload_blob_from_memory(
        bucket_name=BUCKET,
        contents=query_result,
        destination_blob_name=latest_file_name,
    )

    if SAVING_OPTION == "latest_and_historic":
        query_time = datetime.now().strftime("%Y/%m/%d")
        historic_file_name = f"{OBJ_NAME}/{query_time}/data.jsonl"
        copy_blob(
            bucket_name=BUCKET,
            blob_name=latest_file_name,
            destination_bucket_name=BUCKET,
            destination_blob_name=historic_file_name,
        )

    return {"statusCode": 200, "body": f"object {OBJ_NAME} ingested"}
