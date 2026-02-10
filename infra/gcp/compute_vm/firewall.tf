resource "google_compute_firewall" "agent_rag_ingress" {
  name    = "agent-rag-ingress"
  network = "default"

  allow {
    protocol = "tcp"
    # 22 SSH, 8080 frontend, 8000 backend, 8002 redaction, 6333 qdrant (optional public)
    ports = ["22", "8080", "8000", "8002", "6333"]
  }

  source_ranges = var.ssh_source_ranges
  target_tags   = ["agent-rag"]

  depends_on = [google_project_service.compute]
}
