resource "google_artifact_registry_repository" "agent_rag" {
  location      = var.region
  repository_id = var.gar_repo
  format        = "DOCKER"
  depends_on    = [google_project_service.artifactregistry]
}
