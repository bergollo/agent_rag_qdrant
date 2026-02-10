provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      ManagedBy   = "terraform"
      Component   = "artifact-registry"
      Repository  = "${var.github_org}/${var.github_repo}"
    }
  }
}
