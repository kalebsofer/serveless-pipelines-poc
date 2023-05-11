import functions_framework
from config import BUCKET_TO_SAVE_PREFECT_DB
from prefect import flow
from prefect.utilities.names import generate_slug
from storage import upload_local_file_to_bucket
from pipelines.ingestion.prefect_flow import ingest_flow
from pipelines.raw_to_bronze.prefect_flow import raw_to_bronze_flow
from pipelines.bronze_to_silver.prefect_flow import bronze_to_silver_flow
from pipelines.silver_to_gold.prefect_flow import silver_to_gold_flow
from utils import pipeline_completion_handler


@functions_framework.http
def cloud_entry_point(request):
    "Receives the request as flask request and runs the function after deployed"

    try:
        result = orchestrate_pipelines(request)
    finally:
        upload_local_file_to_bucket(
            bucket_name=BUCKET_TO_SAVE_PREFECT_DB,
            source_file_name="/tmp/.prefect/prefect.db",
            destination_blob_name="prefect.db",
        )

    return result


def local_entry_point(request):
    "Receives the request as a python dict and runs the function without using decorating with functions_framework"
    return orchestrate_pipelines(request)


@flow(flow_run_name="orchestration__" + generate_slug(2))
def orchestrate_pipelines(request):
    "A prefect flow that orchestrates other flows"


    # ingestion
    ingestion_final_state = ingest_flow(return_state=True)    
    pipeline_completion_handler(
        pipeline_name="INGESTION", 
        is_completed=ingestion_final_state.is_completed()
    )

    # raw_to_bronze pipeline
    raw_to_bronze_final_state = raw_to_bronze_flow(return_state=True)
    pipeline_completion_handler(
        pipeline_name="RAW TO BRONZE", 
        is_completed=raw_to_bronze_final_state.is_completed()
    )
   
    # bronze_to_silver
    bronze_to_silver_final_state = bronze_to_silver_flow(return_state=True)
    pipeline_completion_handler(
        pipeline_name="BRONZE TO SILVER", 
        is_completed=bronze_to_silver_final_state.is_completed()
    )

    # silver_to_gold
    silver_to_gold_final_state = silver_to_gold_flow(return_state=True)
    pipeline_completion_handler(
        pipeline_name="SILVER TO GOLD", 
        is_completed=silver_to_gold_final_state.is_completed()
    )

    return {"statusCode": 200, "body": "All functions finished without errors"}
