resource "google_compute_instance" "agent_rag" {
  name         = var.vm_name
  machine_type = var.machine_type
  zone         = var.zone
  tags         = ["agent-rag"]

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 30
    }
  }

  network_interface {
    network = "default"
    access_config {} # allocate external IP
  }

  service_account {
    email  = google_service_account.vm.email
    scopes = ["cloud-platform"]
  }

  # OS Login at instance-level too
  metadata = {
    enable-oslogin = "TRUE"
  }

  metadata_startup_script = file("${path.module}/startup.sh")

  depends_on = [
    google_project_service.compute,
    google_compute_project_metadata_item.enable_oslogin,
    google_project_iam_member.vm_ar_reader
  ]
}
