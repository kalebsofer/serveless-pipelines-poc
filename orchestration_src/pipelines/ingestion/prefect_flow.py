from prefect import flow, task, get_run_logger
from prefect.utilities.names import generate_slug
from utils import trigger_cloud_function_with_http_post
from config import SF_OBJECTS_TO_RETRIEVE, INGESTION_FUNCTION_URL
import datetime

RAW_BUCKET_NAME = "internalforecast-data-raw"


@flow(flow_run_name="ingestion_flow__" + generate_slug(2))
def ingest_flow():
    list_of_objects = SF_OBJECTS_TO_RETRIEVE

    date = datetime.datetime.utcnow()
    for obj_name in list_of_objects:
        ingest_task.submit(obj_name=obj_name, date=date)


@task(task_run_name="ingest_task_{obj_name}_{date:%Y/%m/%d}")
def ingest_task(obj_name, date):
    prefect_logger = get_run_logger()

    my_obj = {
        "object_name": obj_name,
        "saving_option": "latest_and_historic",
        "bucket": RAW_BUCKET_NAME,
    }
    ingest_response = trigger_cloud_function_with_http_post(
        endpoint=INGESTION_FUNCTION_URL, post_body=my_obj
    )
    prefect_logger.info(
        f"Ingestion of obj: {obj_name} finished with response: {ingest_response}"
    )
