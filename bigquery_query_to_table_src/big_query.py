from google.cloud import bigquery
from config import logger

client = bigquery.Client()


def create_big_query_table_from_sql_query(table_name, project, dataset, sql_query):
    "Creates a table in the specified dataset with the results of the query"

    table_id = f"{project}.{dataset}.{table_name}"
    job_config = bigquery.QueryJobConfig(
        destination=table_id, write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    query_job = client.query(sql_query, job_config=job_config)  # Make an API request.
    query_job.result()  # Wait for the job to complete.

    print("Query results loaded to the table {}".format(table_id))
