// apis.tf

// Enable the Artifact Registry API
resource "google_project_service" "artifactregistry" {
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

// Enable the IAM API
resource "google_project_service" "iam" {
  service            = "iam.googleapis.com"
  disable_on_destroy = false
}

// Enable the IAM Service Account Credentials API
resource "google_project_service" "iamcredentials" {
  service            = "iamcredentials.googleapis.com"
  disable_on_destroy = false
}

// Enable the Security Token Service API
resource "google_project_service" "sts" {
  service            = "sts.googleapis.com"
  disable_on_destroy = false
}

// Enable the Secret Manager API
resource "google_project_service" "secretmanager" {
  service            = "secretmanager.googleapis.com"
  disable_on_destroy = false
}


# Enable the Cloud Run Admin API
resource "google_project_service" "cloud_run_api" {
  service = "run.googleapis.com"
  # Optional: Keep the service enabled if the Terraform resource is destroyed
  disable_on_destroy = false
}