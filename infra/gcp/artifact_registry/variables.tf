variable "project_id" { type = string }
variable "region"     { type = string }
variable "zone"       { type = string }

variable "gar_repo" {
  type    = string
  default = "agent-rag"
}

variable "org_and_repo" {
  type     = string
  default = "bergollo/rag-stack-chatbot"
}
