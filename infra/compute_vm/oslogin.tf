# Enable OS Login at project-level
resource "google_compute_project_metadata_item" "enable_oslogin" {
  key   = "enable-oslogin"
  value = "TRUE"

  depends_on = [google_project_service.compute, google_project_service.oslogin]
}
