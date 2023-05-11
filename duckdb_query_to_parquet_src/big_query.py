from google.cloud import bigquery
from config import logger

client = bigquery.Client()


def create_big_query_table_from_parquet(table_name, project, dataset, blob_uri):
    "Creates a big query table ingesting a parquet file from bucket"

    table_id = f"{project}.{dataset}.{table_name}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.PARQUET,
    )
    load_job = client.load_table_from_uri(blob_uri, table_id, job_config=job_config)
    load_job.result()  # Waits for the job to complete.
    destination_table = client.get_table(table_id)
    logger.info(f"Loaded table {table_id} it has {destination_table.num_rows} rows.")
