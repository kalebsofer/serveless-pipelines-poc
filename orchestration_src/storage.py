from google.cloud import storage
from config import logger
from datetime import datetime


def upload_local_file_to_bucket(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    upload_date = datetime.now().strftime("%Y/%m/%d/%Hh%Mm")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"{upload_date}/{destination_blob_name}")
    blob.upload_from_filename(source_file_name)
    logger.info(f"File '{destination_blob_name}' uploaded to bucket '{bucket_name}'.")
