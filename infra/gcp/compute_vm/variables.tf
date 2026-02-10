variable "project_id" { type = string }
variable "region"     { type = string }
variable "zone"       { type = string }

variable "gar_repo" {
  type    = string
  default = "agent-rag"
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
  type     = string
  default = "bergollo/rag-stack-chatbot"
}
