# CI service account: GitHub Actions uses WIF to impersonate this to PUSH images
resource "google_service_account" "ci" {
  account_id   = "github-ci"
  display_name = "GitHub CI (push images)"
  depends_on   = [google_project_service.iam]
}