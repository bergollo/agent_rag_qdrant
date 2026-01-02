# outputs.tf

# Output the CI service account email
output "ci_service_account_email" {
  value = google_service_account.ci.email
}

# Output the Run Backend service account email
output "run_backend_service_account_email" {
  value = google_service_account.run_backend.email
}

# Output the Run AI service account email
output "run_ai_service_account_email" {
  value = google_service_account.run_ai.email
}

output "run_redaction_gate_service_account_email" {
  value = google_service_account.run_redaction_gate.email
}

# Output the GAR repository name
output "gar_repo" {
  value = google_artifact_registry_repository.agent_rag.repository_id
}

# Output the GAR repository location
output "gar_location" {
  value = google_artifact_registry_repository.agent_rag.location
}

# Output the Workload Identity Federation provider name for GitHub Actions
output "github_wif_provider" {
  value       = google_iam_workload_identity_pool_provider.github.name
  description = "Use this as GCP_WIF_PROVIDER in GitHub Actions"
}

# Output the Cloud Run service URLs
output "frontend_url" {
  value = google_cloud_run_v2_service.frontend.uri
}
output "backend_url" {
  value = google_cloud_run_v2_service.backend.uri
}
output "ai_service_url" {
  value = google_cloud_run_v2_service.ai_service.uri
}
