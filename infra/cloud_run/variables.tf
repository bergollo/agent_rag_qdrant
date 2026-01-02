variable "project_id" { type = string }
variable "region"     { type = string }
variable "zone"       { type = string }

variable "gar_repo" {
  type    = string
  default = "agent-rag"
}

variable "gar_host" {
  type    = string
  default = "us-central1-docker.pkg.dev"
}

variable "vm_name" {
  type    = string
  default = "agent-rag-vm"
}

variable "machine_type" {
  type    = string
  default = "e2-small"
}

# For tighter SSH later, set this to your public IP like "1.2.3.4/32"
variable "ssh_source_ranges" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}

variable "qdrant_url" {
  type    = string
  default = "http://<QDRANT_HOST>:6333"
}

#Cloud SQL recommended format for redaction service
variable "redaction_database_url" {
  type    = string
  default = "postgresql://user:password@<REDACTION_DB_HOST>:5432/redaction_db"
}

variable "org_and_repo" {
  type     = string
  default = "bergollo/rag-stack-chatbot"
}

variable "tag" {
  type = string
  default = "latest"
}