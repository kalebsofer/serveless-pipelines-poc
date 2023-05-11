from google.cloud import storage
from config import logger


def upload_file_on_tmp_to_bucket(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename("/tmp/" + source_file_name)
    logger.info(f"File '{destination_blob_name}' uploaded to bucket '{bucket_name}'.")


def download_blob_to_tmp(bucket_name, source_blob_name, destination_file_name):
    "Downloads blob from bucket and saves at /tmp/"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename("/tmp/" + destination_file_name)
    logger.info(
        f"File '{source_blob_name}' downloaded from bucket '{bucket_name}' to tmp."
    )


def upload_blob_from_memory(bucket_name, contents, destination_blob_name):
    "Uploads contents of string as blob to the bucket."

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(contents)

    logger.info(f"File '{destination_blob_name}' uploaded to bucket '{bucket_name}'.")


def copy_blob(
    bucket_name,
    blob_name,
    destination_bucket_name,
    destination_blob_name,
):
    "Makes a copy of a blob, can be used to copy on same bucket or different ones"

    storage_client = storage.Client()
    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)
    blob_copy = source_bucket.copy_blob(
        source_blob,
        destination_bucket,
        destination_blob_name,
    )
    logger.info(
        f"Blob {source_blob.name} in bucket {source_bucket.name} copied to blob {blob_copy.name} in bucket {destination_bucket.name}."
    )
