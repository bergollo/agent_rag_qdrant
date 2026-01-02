variable "project_id" { type = string }
variable "region"     { type = string }
variable "zone"       { type = string }

variable "env" {
  type    = string
  default = "dev"
}

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


variable "org_and_repo" {
  type    = string
  default = "bergollo/rag-stack-chatbot"
}

variable "tag" {
  type    = string
  default = "latest"
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

# Frontend metadata
variable "FRONTEND_NAME" {
  type    = string
  default = "RAG Stack Chatbot"
}
variable "FRONTEND_PORT" {
  type    = string
  default = "8080"
}


# Backend metadata
variable "BACKEND_NAME" {
  type    = string
  default = "RAG Stack Chatbot Backend"
}
variable "BACKEND_ENV" {
  type    = string
  default = "development"
}


# AI Service metadata
variable "AI_SERVICE_NAME" {
  type    = string
  default = "AI Service Stub"
}
variable "AI_SERVICE_ENV" {
  type    = string
  default = "development"
}
# Required for OpenAI chat + embeddings
variable "OPENAI_API_KEY" {
  type    = string
  default = "..."
}


# Redaction Gate MCP URL
variable "REDACTION_GATE_NAME" {
  type    = string
  default = "Redaction Gate MCP"
}
variable "REDACTION_GATE_TOKEN" {
  type    = string
  default = "dev-token"
}

# Redaction DB credentials
variable "REDACTION_DB_USER" {
  type    = string
  default = "redaction_user"
}
variable "REDACTION_DB_NAME" {
  type    = string
  default = "redaction_db"
}
variable "REDACTION_DB_PASSWORD" {
  type    = string
  default = "..."
}

# Vector store connection
variable "QDRANT_API_KEY" {
  type    = string
  default = "..."
}