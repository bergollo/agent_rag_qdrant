variable "project_name" {
  description = "A short name used to prefix AWS resources."
  type        = string
  default = "rag-stack-chatbot"
}

variable "aws_region" {
  description = "AWS region to deploy into."
  type        = string
  default     = "us-east-1"
}

variable "repositories" {
  description = "ECR repositories to create (service names)."
  type        = list(string)
  default = [ "agent_rag_qdrant" ]
}

variable "github_org" {
  description = "GitHub org/user that owns the repo."
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name."
  type        = string
}

variable "allowed_branches" {
  description = "Branches allowed to assume the CI role."
  type        = list(string)
  default     = ["main", "dev"]
}

variable "github_oidc_audience" {
  description = "GitHub OIDC audience. aws-actions typically uses sts.amazonaws.com."
  type        = string
  default     = "sts.amazonaws.com"
}

variable "ecr_image_tag_mutability" {
  description = "MUTABLE or IMMUTABLE tags."
  type        = string
  default     = "MUTABLE"
}

variable "ecr_scan_on_push" {
  description = "Enable ECR scan on push."
  type        = bool
  default     = true
}

variable "ecr_force_delete" {
  description = "Allow Terraform to delete repos even if images exist."
  type        = bool
  default     = false
}

variable "enable_lifecycle_policy" {
  description = "Whether to create a lifecycle policy to keep only the most recent images."
  type        = bool
  default     = true
}

variable "lifecycle_keep_last_n" {
  description = "Number of recent images to keep in the lifecycle policy."
  type        = number
  default     = 10
}

variable "github_oidc_thumbprints" {
  type    = list(string)
  default = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

variable "allowed_tags" {
  description = "GitHub tags allowed to assume the CI role."
  type        = list(string)
  default     = ["latest"]
}