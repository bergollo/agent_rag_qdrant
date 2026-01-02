############################
# Secrets
############################

resource "google_secret_manager_secret" "openai_api_key" {
  secret_id = "OPENAI_API_KEY"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret" "redaction_db_password" {
  secret_id = "REDACTION_DB_PASSWORD"

  replication {
    auto {}
  }
}


############################
# Secret Versions
############################

variable "openai_api_key" {
  type      = string
  sensitive = true
}

variable "redaction_db_password" {
  type      = string
  sensitive = true
}

resource "google_secret_manager_secret_version" "openai_api_key" {
  secret      = google_secret_manager_secret.openai_api_key.id
  secret_data = var.openai_api_key

  depends_on = [google_project_service.secretmanager]
}

resource "google_secret_manager_secret_version" "redaction_db_password" {
  secret      = google_secret_manager_secret.redaction_db_password.id
  secret_data = var.redaction_db_password

  depends_on = [google_project_service.secretmanager]
}
