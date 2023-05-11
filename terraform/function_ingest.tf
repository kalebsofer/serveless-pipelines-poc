# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "ingestion_src_source" {
    type        = "zip"
    source_dir  = "../ingestion_src"
    output_path = "./tmp/ingestion_src.zip"
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "ingestion_src_zip" {
    source       = data.archive_file.ingestion_src_source.output_path
    content_type = "application/zip"

    # Append to the MD5 checksum of the files's content
    # to force the zip to be updated as soon as a change occurs
    name         = "src-${data.archive_file.ingestion_src_source.output_md5}.zip"
    bucket       = google_storage_bucket.functions_codebase_bucket.name

    # Dependencies are automatically inferred so these lines can be deleted
    depends_on   = [
        google_storage_bucket.functions_codebase_bucket,  # declared in `storage.tf`
        data.archive_file.ingestion_src_source
    ]
}

resource "google_cloudfunctions2_function" "ingestion_src" {  
  provider = google-beta
  project = var.project_id
  location  = var.region
  name = "salesforce_ingestion"  
  
  build_config {
    runtime = "python39"
    entry_point = "cloud_entry_point"
    source {
      storage_source {
        bucket = google_storage_bucket.functions_codebase_bucket.name
        object = google_storage_bucket_object.ingestion_src_zip.name
      }
    }
  }

  service_config {
    max_instance_count  = 20
    available_memory    = "1G"
    available_cpu       = "0.583"
    timeout_seconds     = 600
    service_account_email = google_service_account.solution_sa.email

    secret_environment_variables {
      project_id = var.project_id
      key     = "SALESFORCE_USERNAME"
      secret  = "SALESFORCE_USERNAME"
      version = "latest"
    }
    secret_environment_variables {
      project_id = var.project_id
      key     = "SALESFORCE_PASSWORD"
      secret  = "SALESFORCE_PASSWORD"
      version = "latest"
    }
    secret_environment_variables {
      project_id = var.project_id
      key     = "SALESFORCE_CLIENT_ID"
      secret  = "SALESFORCE_CLIENT_ID"
      version = "latest"
    }
    secret_environment_variables {
      project_id = var.project_id
      key     = "SALESFORCE_CLIENT_SECRET"
      secret  = "SALESFORCE_CLIENT_SECRET"
      version = "latest"
    }
  }

}
