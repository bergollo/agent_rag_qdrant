# iam_bindings.tf

# Frontend Cloud Run service made public
resource "google_cloud_run_v2_service_iam_member" "frontend_public" {
  name     = google_cloud_run_v2_service.frontend.name
  location = google_cloud_run_v2_service.frontend.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Backend Cloud Run service
resource "google_cloud_run_v2_service_iam_member" "ai_invoker_backend" {
  name     = google_cloud_run_v2_service.backend.name
  location = google_cloud_run_v2_service.backend.location
  role     = "roles/run.invoker"
  # member   = "serviceAccount:${google_service_account.run_backend.email}"
  member   = "allUsers" # Uncomment to make Backend public
}

# AI Service Cloud Run service made internal only (invokable by Backend service)
resource "google_secret_manager_secret_iam_member" "openai_access_ai" {
  secret_id = google_secret_manager_secret.openai_api_key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.run_ai.email}, serviceAccount:${google_service_account.run_backend.email}"
}

resource "google_secret_manager_secret_iam_member" "redaction_db_access_backend" {
  secret_id = google_secret_manager_secret.redaction_db_password.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.run_redaction_gate.email}, serviceAccount:${google_service_account.run_ai.email}"
}

