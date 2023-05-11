import functions_framework
from datetime import datetime
from config import logger, LOCAL_TESTING, PROJECT_ID
from storage import download_blob_to_tmp, copy_blob, upload_file_on_tmp_to_bucket
from duckdb_tools import run_sql_save_res_to_parquet
from big_query import create_big_query_table_from_parquet


# different entry points for cloud and local
@functions_framework.http
def cloud_entry_point(request):
    "Receives the request as flask request and runs the function after deployed"
    return duckdb_query_to_parquet_main(request)


def local_entry_point(request):
    "Receives the request as a python dict and runs the function without using decorating with functions_framework"
    return duckdb_query_to_parquet_main(request)


# function code
def duckdb_query_to_parquet_main(request):
    """The structure of a request is as follows:
    {   'duckdb_query':"SELECT * FROM read_json_auto('/tmp/Account/latest/data.jsonl', maximum_object_size=104857600,sample_size=100000,auto_detect=true)",
        'data_sources': [
            {'data_source_path_and_name':'Account/latest/data.jsonl',
            'data_source_bucket':'internalforecast-data-raw'},
        ],
        'result_name':'Account',
        'result_bucket':'internalforecast-data-bronze',
        'saving_option':'latest_and_historic',
        'create_bigquery_table': 'TRUE',
        'bigquery_dataset_name': 'internal_forecast_bronze'
    }

    Once the request is received this function:
        - Downloads all data sources to /tmp/
        - Runs the duckdb query
        - Saves result as parquet in /tmp/
        - Uploads result to: bucket/result_name/latest/data.parquet
        - (optionally) Makes historic copy of data in bucket with following naming:
             bucket/result_name/year/month/date/data.parquet
        - (optionally) creates table on big query named 'result_name' with results

    Note 1: All items in the data sources list will be downloaded to /tmp/ in the function
     your query will have to read them from there

    Note 2: the table on big query is created with option WRITE_TRUNCATE
    """

    # local testing receives the request as a dict already
    if LOCAL_TESTING == "LOCAL_WITH_CLOUD_EFFECTS":
        request_body_dict = request
    # cloud function receives request as a flask request, so need to get json out of the request
    else:
        request_body_dict = request.get_json(silent=True)

    DUCKDB_QUERY = request_body_dict["duckdb_query"]
    DATASOURCES_LIST = request_body_dict["data_sources"]
    RESULT_NAME = request_body_dict["result_name"]
    RESULT_BUCKET = request_body_dict["result_bucket"]
    SAVING_OPTION = request_body_dict["saving_option"]
    CREATE_BIGQUERY_TABLE = request_body_dict["create_bigquery_table"]
    if CREATE_BIGQUERY_TABLE == "TRUE":
        BIGQUERY_DATASET_NAME = request_body_dict["bigquery_dataset_name"]

    for datasource in DATASOURCES_LIST:
        download_blob_to_tmp(
            bucket_name=datasource["data_source_bucket"],
            source_blob_name=datasource["data_source_path_and_name"],
            destination_file_name=datasource["data_source_path_and_name"],
        )

    run_sql_save_res_to_parquet(
        sql_query=DUCKDB_QUERY, output_filename=RESULT_NAME + ".parquet"
    )

    upload_file_on_tmp_to_bucket(
        bucket_name=RESULT_BUCKET,
        source_file_name=RESULT_NAME + ".parquet",
        destination_blob_name=f"{RESULT_NAME}/latest/data.parquet",
    )

    if SAVING_OPTION == "latest_and_historic":
        query_day = datetime.now().strftime("%Y/%m/%d")
        copy_blob(
            bucket_name=RESULT_BUCKET,
            blob_name=f"{RESULT_NAME}/latest/data.parquet",
            destination_bucket_name=RESULT_BUCKET,
            destination_blob_name=f"{RESULT_NAME}/{query_day}/data.parquet",
        )

    # Create big query table with data from the file
    if CREATE_BIGQUERY_TABLE == "TRUE":
        blob_uri = f"gs://{RESULT_BUCKET}/{RESULT_NAME}/latest/data.parquet"
        create_big_query_table_from_parquet(
            table_name=RESULT_NAME,
            project=PROJECT_ID,
            dataset=BIGQUERY_DATASET_NAME,
            blob_uri=blob_uri,
        )

    return {"statusCode": 200, "body": f"Query run as expected"}
