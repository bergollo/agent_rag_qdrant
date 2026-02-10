## Terraform-managed Cloud Run services for the rag-stack components hosted in Artifact Registry.
resource "google_cloud_run_v2_service" "backend" {
  name     = "backend"
  location = var.region

  deletion_protection = false

  template {
    containers {
      image = "${var.gar_host}/${var.project_id}/${var.gar_repo}/backend:${var.tag}"

      env {
        name  = "NODE_ENV"
        value = "production"
      }

      # Cloud Run supplies the target port through the PORT env var; expose container_port for routing.
      env {
        name  = "AI_SERVICE_URL"
        value = google_cloud_run_v2_service.ai_service.uri
      }

      # Qdrant stores are shared; point both backend and AI service to the same cluster URL.
      env {
        name  = "QDRANT_URL"
        value = var.qdrant_url
      }

      # If backend needs to call redaction_gate directly:
      # env { name = "REDACTION_URL" value = google_cloud_run_v2_service.redaction_gate.uri }

      ports {
        container_port = 8080
      }
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 10
    }

    service_account = google_service_account.run_backend.email
  }
}

resource "google_cloud_run_v2_service" "ai_service" {
  name     = "ai-service"
  location = var.region

  ingress = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  deletion_protection = false

  template {
    containers {
      image = "${var.gar_host}/${var.project_id}/${var.gar_repo}/ai_service:${var.tag}"

      env {
        name  = "REDACTION_URL"
        value = google_cloud_run_v2_service.redaction_gate.uri
      }

      env {
        name  = "QDRANT_URL"
        value = var.qdrant_url
      }

      # OPENAI_API_KEY is delivered via Secret Manager so the plaintext value never appears in source control.
      env {
        name = "OPENAI_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.openai_api_key.secret_id
            version = "latest"
          }
        }
      }

      ports { container_port = 8080 }
    }

    service_account = google_service_account.run_ai.email
  }
}

resource "google_cloud_run_v2_service" "redaction_gate" {
  name     = "redaction-gate"
  location = var.region

  # Keep the redaction gate private by restricting ingress to internal traffic only.
  ingress = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  deletion_protection = false

  template {
    containers {
      image = "${var.gar_host}/${var.project_id}/${var.gar_repo}/redaction_gate:${var.tag}"

      # Make sure your app listens on $PORT (usually 8080)
      ports { container_port = 8080 }

      # Example: set DATABASE_URL appropriately (Cloud SQL recommended)
      # env { 
      #   name = "DATABASE_URL"
      #   value = var.redaction_database_url
      # }
    }

    service_account = google_service_account.run_redaction_gate.email
  }
}

locals {
  frontend_env = merge(local.global_env, {
    VITE_API_BASE_URL = google_cloud_run_v2_service.backend.uri
    BACKEND_URL       = google_cloud_run_v2_service.backend.uri
  })
}

resource "google_cloud_run_v2_service" "frontend" {
  name     = "frontend"
  location = var.region

  deletion_protection = false

  template {
    containers {
      image = "${var.gar_host}/${var.project_id}/${var.gar_repo}/frontend:${var.tag}"

      dynamic "env" {
        for_each = local.frontend_env
        content {
          name  = env.key
          value = env.value
        }
      }

      ports { container_port = 8080 }
      # Frontend calls the backend service over its Cloud Run URL.
      # env {
      #   name  = "BACKEND_URL"
      #   value = google_cloud_run_v2_service.backend.uri
      # }
    }
  }
}
