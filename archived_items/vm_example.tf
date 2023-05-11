# This was used when we were considering using Prefect on a VM for orchestration
# We decided to keep it simpler and orchestrate with a Cloud Function Gen2

resource "google_compute_instance" "prefect" {
  boot_disk {
    auto_delete = true
    device_name = "prefect"

    initialize_params {
      image = "projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20230302"
      size  = 10
      type  = "pd-balanced"
    }

    mode = "READ_WRITE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false

  labels = {
    ec-src = "vm_add-tf"
  }

  machine_type = "e2-medium"
  name         = "prefect"

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    subnetwork = "projects/forecasting-test-382708/regions/europe-west2/subnetworks/default"
  }

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
    preemptible         = false
    provisioning_model  = "STANDARD"
  }

  service_account {
    email  = "310105214006-compute@developer.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }

  shielded_instance_config {
    enable_integrity_monitoring = true
    enable_secure_boot          = false
    enable_vtpm                 = true
  }

  tags = ["prefect-server"]
  zone = "europe-west2-c"
}
