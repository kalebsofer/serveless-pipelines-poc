# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "bigquery_query_to_table_source" {
    type        = "zip"
    source_dir  = "../bigquery_query_to_table_src"
    output_path = "./tmp/bigquery_query_to_table_src.zip"
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "bigquery_query_to_table_zip" {
    source       = data.archive_file.bigquery_query_to_table_source.output_path
    content_type = "application/zip"

    # Append to the MD5 checksum of the files's content
    # to force the zip to be updated as soon as a change occurs
    name         = "src-${data.archive_file.bigquery_query_to_table_source.output_md5}.zip"
    bucket       = google_storage_bucket.functions_codebase_bucket.name

    
    depends_on   = [
        google_storage_bucket.functions_codebase_bucket,  
        data.archive_file.bigquery_query_to_table_source
    ]
}

resource "google_cloudfunctions2_function" "bigquery_query_to_table" {  
  provider = google-beta
  project = var.project_id
  location  = var.region
  name = "bigquery_query_to_table"  
  
  build_config {
    runtime = "python39"
    entry_point = "cloud_entry_point"
    source {
      storage_source {
        bucket = google_storage_bucket.functions_codebase_bucket.name
        object = google_storage_bucket_object.bigquery_query_to_table_zip.name
      }
    }
  }

  service_config {
    max_instance_count  = 20
    available_memory    = "256M"    
    timeout_seconds     = 600
    service_account_email = google_service_account.solution_sa.email
  }

}
