locals {
  global_env = {
    ENV       = var.env
    QDRANT_URL = var.qdrant_url
    REGION    = var.region
  }
}