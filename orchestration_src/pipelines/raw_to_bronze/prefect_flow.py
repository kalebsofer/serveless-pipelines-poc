from prefect import flow, task, get_run_logger
from prefect.utilities.names import generate_slug
from config import DUCKDB_QUERY_TO_PARQUET_FUNCTION_URL
from utils import trigger_cloud_function_with_http_post, multiple_files_yaml_loader
import datetime


@flow(flow_run_name="raw_to_bronze__" + generate_slug(2))
def raw_to_bronze_flow():
    date = datetime.datetime.utcnow()
    pipeline_list = multiple_files_yaml_loader(
        path_pattern="pipelines/raw_to_bronze/transforms/*.yaml"
    )

    for item in pipeline_list:
        raw_to_bronze_task.submit(
            bronze_pipeline_item=item, date=date, item_result_name=item["result_name"]
        )


@task(task_run_name="raw_to_bronze_task_{item_result_name}_{date:%Y/%m/%d}")
def raw_to_bronze_task(bronze_pipeline_item, date, item_result_name):
    prefect_logger = get_run_logger()
    raw_to_bronze_response = trigger_cloud_function_with_http_post(
        endpoint=DUCKDB_QUERY_TO_PARQUET_FUNCTION_URL,
        post_body=bronze_pipeline_item,
    )
    prefect_logger.info(
        f"Item {bronze_pipeline_item['result_name']} of bronze pipeline finished with response: {raw_to_bronze_response}"
    )
