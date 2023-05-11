from prefect import flow, task, get_run_logger
from prefect.utilities.names import generate_slug
from config import DUCKDB_QUERY_TO_PARQUET_FUNCTION_URL
from utils import trigger_cloud_function_with_http_post, multiple_files_yaml_loader
import datetime


@flow(flow_run_name="silver_to_gold__" + generate_slug(2))
def silver_to_gold_flow():
    date = datetime.datetime.utcnow()

    # Step 01
    step_01_list = multiple_files_yaml_loader(
        path_pattern="pipelines/silver_to_gold/transforms/step_01/*.yaml"
    )
    results_step_01 = []
    for item in step_01_list:
        results_step_01.append(
            silver_to_gold_task.submit(
                gold_pipeline_item=item, date=date, item_result_name=item["result_name"]
            )
        )

    # Step 02
    for result in results_step_01:
        result.wait()

    step_02_list = multiple_files_yaml_loader(
        path_pattern="pipelines/silver_to_gold/transforms/step_02/*.yaml"
    )
    for item in step_02_list:
        silver_to_gold_task.submit(
            gold_pipeline_item=item, date=date, item_result_name=item["result_name"]
        )


@task(task_run_name="silver_to_gold_task_{item_result_name}_{date:%Y/%m/%d}")
def silver_to_gold_task(gold_pipeline_item, date, item_result_name):
    prefect_logger = get_run_logger()
    response = trigger_cloud_function_with_http_post(
        endpoint=DUCKDB_QUERY_TO_PARQUET_FUNCTION_URL,
        post_body=gold_pipeline_item,
    )
    prefect_logger.info(
        f"Item {gold_pipeline_item['result_name']} of bronze pipeline finished with response: {response}"
    )
