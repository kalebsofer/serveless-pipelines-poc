resource "google_bigquery_dataset" "bronze_dataset" {
  dataset_id                  = "internal_forecast_bronze"
  friendly_name               = "internal_forecast"
  description                 = "Dataset to store internal forecast bronze tables"
  location                    = var.region 
  delete_contents_on_destroy  = var.allow_data_deletion_on_tf_destroy 

  access {
    role          = "OWNER"
    user_by_email = google_service_account.solution_sa.email
  }
}

resource "google_bigquery_dataset" "silver_dataset" {
  dataset_id                  = "internal_forecast_silver"
  friendly_name               = "internal_forecast"
  description                 = "Dataset to store internal forecast silver tables"
  location                    = var.region
  delete_contents_on_destroy  = var.allow_data_deletion_on_tf_destroy

  access {
    role          = "OWNER"
    user_by_email = google_service_account.solution_sa.email
  }
}

resource "google_bigquery_dataset" "gold_dataset" {
  dataset_id                  = "internal_forecast_gold"
  friendly_name               = "internal_forecast"
  description                 = "Dataset to store internal forecast gold tables"
  location                    = var.region
  delete_contents_on_destroy  = var.allow_data_deletion_on_tf_destroy  

  access {
    role          = "OWNER"
    user_by_email = google_service_account.solution_sa.email
  }
}
