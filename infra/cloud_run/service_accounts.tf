# service_accounts.tf

# CI service account: GitHub Actions uses WIF to impersonate this to PUSH images
resource "google_service_account" "ci" {
  account_id   = "github-ci"
  display_name = "GitHub CI (push images)"
  depends_on   = [google_project_service.iam]
}

# Service account for Backend service to access Redaction DB secret
resource "google_service_account" "run_backend" {
  account_id   = "run-backend"
  display_name = "Cloud Run Backend Service"
}

# Service account for AI service to access OpenAI secret
resource "google_service_account" "run_ai" {
  account_id   = "run-ai"
  display_name = "Cloud Run AI Service"
}

resource "google_service_account" "run_redaction_gate" {
  account_id   = "run-redaction-gate"
  display_name = "Cloud Run Redaction Gate Service"
}