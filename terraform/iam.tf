resource "google_service_account" "solution_sa" {
  account_id   = "ingestion-service-account"
  display_name = "Service Account for the internal forecast solution"
}

resource "google_project_iam_member" "sa_bucket_iam" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.solution_sa.email}"
}

resource "google_project_iam_member" "sa_secrets_iam" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${google_service_account.solution_sa.email}"
}

resource "google_project_iam_member" "sa_cloud_function_invoker" {
  project = var.project_id
  role    = "roles/cloudfunctions.invoker"
  member  = "serviceAccount:${google_service_account.solution_sa.email}"
}

# Cloud function 2nd gen needs invoker to have cloud run invoker role
resource "google_project_iam_member" "sa_run_invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.solution_sa.email}"
}

resource "google_project_iam_member" "sa_iam_big_query" {
  project = var.project_id
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.solution_sa.email}"
}
