# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "orchestration_source" {
    type        = "zip"
    source_dir  = "../orchestration_src"
    output_path = "./tmp/orchestration_function.zip"
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "orchestration_src_zip" {
    source       = data.archive_file.orchestration_source.output_path
    content_type = "application/zip"

    # Append to the MD5 checksum of the files's content
    # to force the zip to be updated as soon as a change occurs
    name         = "src-${data.archive_file.orchestration_source.output_md5}.zip"
    bucket       = google_storage_bucket.functions_codebase_bucket.name

    # Dependencies are automatically inferred so these lines can be deleted
    depends_on   = [
        google_storage_bucket.functions_codebase_bucket,  # declared in `storage.tf`
        data.archive_file.orchestration_source
    ]
}

resource "google_cloudfunctions2_function" "function_orchestrate" {  
  provider = google-beta
  project = var.project_id
  location  = var.region
  name = "orchestrate_pipelines"  
  
  build_config {
    runtime = "python310"
    entry_point = "cloud_entry_point" 
    source {
      storage_source {
        bucket = google_storage_bucket.functions_codebase_bucket.name
        object = google_storage_bucket_object.orchestration_src_zip.name
      }
    }
  }

  service_config {
    max_instance_count  = 1
    available_memory    = "2G"
    available_cpu       = "1"    
    timeout_seconds     = 600 # Can be changed to up to 3600 if there are lots of pipelines to orchestrate
    service_account_email = google_service_account.solution_sa.email
    environment_variables = {
        INGESTION_FUNCTION_URL = google_cloudfunctions2_function.ingestion_src.service_config[0].uri
        DUCKDB_QUERY_TO_PARQUET_FUNCTION_URL = google_cloudfunctions2_function.duckdb_query_to_parquet.service_config[0].uri
    }
  }

  depends_on            = [
        google_cloudfunctions2_function.ingestion_src, 
        google_cloudfunctions2_function.duckdb_query_to_parquet
  ]
}
