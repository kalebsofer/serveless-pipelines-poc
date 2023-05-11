resource "google_cloud_scheduler_job" "job" {
  name             = "daily_orchestration_funcion"
  description      = "triggers the cloud function 2nd gen that orchestrates our pipeline"
  schedule         = "10 10 * * *"
  time_zone        = "Europe/London"
  attempt_deadline = "1200s"

  retry_config {
    retry_count = 0
  }

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions2_function.function_orchestrate.service_config[0].uri
    body        = base64encode("{\"name\":\"bla\"}")
    headers =   {"Content-Type": "application/json"}
    oidc_token  {
        service_account_email =  google_service_account.solution_sa.email
    }

  }
}