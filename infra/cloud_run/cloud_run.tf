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

      # Use Cloud Run $PORT model in the app. Usually no need to set PORT explicitly.

      env {
        name  = "AI_SERVICE_URL"
        value = google_cloud_run_v2_service.ai_service.uri
      }

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

  # if it should be private/internal like in compose:
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

resource "google_cloud_run_v2_service" "frontend" {
  name     = "frontend"
  location = var.region

  deletion_protection = false

  template {
    containers {
      image = "${var.gar_host}/${var.project_id}/${var.gar_repo}/frontend:${var.tag}"
      ports { container_port = 8080 }
      env {
        name  = "BACKEND_URL"
        value = google_cloud_run_v2_service.backend.uri
      }
    }
  }
}
