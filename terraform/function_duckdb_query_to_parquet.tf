# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "duckdb_query_to_parquet_source" {
    type        = "zip"
    source_dir  = "../duckdb_query_to_parquet_src"
    output_path = "./tmp/duckdb_query_to_parquet_src.zip"
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "duckdb_query_to_parquet_zip" {
    source       = data.archive_file.duckdb_query_to_parquet_source.output_path
    content_type = "application/zip"

    # Append to the MD5 checksum of the files's content
    # to force the zip to be updated as soon as a change occurs
    name         = "src-${data.archive_file.duckdb_query_to_parquet_source.output_md5}.zip"
    bucket       = google_storage_bucket.functions_codebase_bucket.name

    # Dependencies are automatically inferred so these lines can be deleted
    depends_on   = [
        google_storage_bucket.functions_codebase_bucket,  # declared in `storage.tf`
        data.archive_file.duckdb_query_to_parquet_source
    ]
}

resource "google_cloudfunctions2_function" "duckdb_query_to_parquet" {  
  provider = google-beta
  project = var.project_id
  location  = var.region
  name = "duckdb_query_to_parquet"  
  
  build_config {
    runtime = "python39"
    entry_point = "cloud_entry_point"
    source {
      storage_source {
        bucket = google_storage_bucket.functions_codebase_bucket.name
        object = google_storage_bucket_object.duckdb_query_to_parquet_zip.name
      }
    }
  }

  service_config {
    max_instance_count  = 20
    available_memory    = "1G"
    available_cpu       = "0.583"
    timeout_seconds     = 600
    service_account_email = google_service_account.solution_sa.email
  }

}
