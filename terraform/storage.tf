resource "google_storage_bucket" "functions_codebase_bucket" {
    name     = "internalforecast-functions-codebase"
    location = var.region
    force_destroy = var.allow_data_deletion_on_tf_destroy
}

resource "google_storage_bucket" "prefect_logs_bucket" {
    name     = "internalforecast-prefect_logs"
    location = var.region
    force_destroy = var.allow_data_deletion_on_tf_destroy 
}

resource "google_storage_bucket" "raw_bucket" {
    name     = "internalforecast-data-raw"
    location = var.region
    force_destroy = var.allow_data_deletion_on_tf_destroy 
}

resource "google_storage_bucket" "bronze_bucket" {
    name     = "internalforecast-data-bronze"
    location = var.region
    force_destroy = var.allow_data_deletion_on_tf_destroy 
} 

resource "google_storage_bucket" "silver_bucket" {
    name     = "internalforecast-data-silver"
    location = var.region
    force_destroy = var.allow_data_deletion_on_tf_destroy 
} 

resource "google_storage_bucket" "gold_bucket" {
    name     = "internalforecast-data-gold"
    location = var.region
    force_destroy = var.allow_data_deletion_on_tf_destroy 
} 