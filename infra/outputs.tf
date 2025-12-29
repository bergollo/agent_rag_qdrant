output "vm_external_ip" {
  value = google_compute_instance.agent_rag.network_interface[0].access_config[0].nat_ip
}

output "vm_name" {
  value = google_compute_instance.agent_rag.name
}

output "ci_service_account_email" {
  value = google_service_account.ci.email
}

output "vm_service_account_email" {
  value = google_service_account.vm.email
}

output "gar_repo" {
  value = google_artifact_registry_repository.agent_rag.repository_id
}

output "gar_location" {
  value = google_artifact_registry_repository.agent_rag.location
}


output "github_wif_provider" {
  value = google_iam_workload_identity_pool_provider.github.name
  description = "Use this as GCP_WIF_PROVIDER in GitHub Actions"
}