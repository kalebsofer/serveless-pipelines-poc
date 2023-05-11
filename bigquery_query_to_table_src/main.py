import functions_framework
from config import logger, LOCAL_TESTING, PROJECT_ID
from big_query import create_big_query_table_from_sql_query


# different entry points for cloud and local


@functions_framework.http
def cloud_entry_point(request):
    "Receives the request as flask request and runs the function after deployed"
    return bigquery_query_to_table_main(request)


def local_entry_point(request):
    "Receives the request as a python dict and runs the function without using decorating with functions_framework"
    return bigquery_query_to_table_main(request)


# function code
def bigquery_query_to_table_main(request):
    """Receives a json request body like the following:
    {
        'bigquery_query':"SELECT year FROM `forecasting-test-382708.dev_temp_tables.gold_test_03` LIMIT 1000",
        'result_table_name':'test_bq_query',
        'result_dataset_name': 'internal_forecast_bronze'
    }
    Once the request is received this function:
        - Runs the duckdb query
        - Creates table with results on Big Query named 'result_name' on the dataset 'result_dataset_name'

    Note: table on big query is created with option WRITE_TRUNCATE

    """

    # local testing receives the request as a dict already
    if LOCAL_TESTING == "LOCAL_WITH_CLOUD_EFFECTS":
        request_body_dict = request
    # cloud function receives request as a flask request, so need to get json out of the request
    else:
        request_body_dict = request.get_json(silent=True)

    BIGQUERY_QUERY = request_body_dict["bigquery_query"]
    RESULT_TABLE_NAME = request_body_dict["result_table_name"]
    RESULT_DATASET_NAME = request_body_dict["result_dataset_name"]

    create_big_query_table_from_sql_query(
        table_name=RESULT_TABLE_NAME,
        project=PROJECT_ID,
        dataset=RESULT_DATASET_NAME,
        sql_query=BIGQUERY_QUERY,
    )

    return {"statusCode": 200, "body": f"Big Query run as expected"}
