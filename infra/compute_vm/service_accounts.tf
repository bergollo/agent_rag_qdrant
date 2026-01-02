# CI service account: GitHub Actions uses WIF to impersonate this to PUSH images
resource "google_service_account" "ci" {
  account_id   = "github-ci"
  display_name = "GitHub CI (push images)"
  depends_on   = [google_project_service.iam]
}

# VM service account: attached to the VM to PULL images
resource "google_service_account" "vm" {
  account_id   = "agent-rag-vm"
  display_name = "Agent RAG VM (pull images)"
  depends_on   = [google_project_service.iam]
}
