variable "project_name" {
  type        = string
  description = "Project name prefix for resources."
}

variable "aws_region" {
  type        = string
  description = "AWS region."
}

variable "vpc_id" {
  type        = string
  description = "VPC ID where the instance will live."
}

variable "subnet_id" {
  type        = string
  description = "Subnet ID for the instance (usually public subnet)."
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type."
  default     = "t3.medium"
}

variable "key_name" {
  type        = string
  description = "Optional EC2 key pair name for SSH. Leave empty if not using SSH."
  default     = ""
}

variable "allow_ssh" {
  type        = bool
  description = "Whether to open port 22 to ssh_cidr."
  default     = false
}

variable "ssh_cidr" {
  type        = string
  description = "CIDR allowed to SSH (only used if allow_ssh=true)."
  default     = "0.0.0.0/0"
}

variable "frontend_port" {
  type        = number
  description = "Port exposed publicly for the frontend service."
  default     = 8080
}

variable "ecr_registry" {
  type        = string
  description = "ECR registry hostname, e.g. 123456789012.dkr.ecr.us-west-2.amazonaws.com"
}

variable "ecr_repo_arns" {
  type        = list(string)
  description = "List of ECR repository ARNs that the instance can pull from."
}

variable "image_tag" {
  type        = string
  description = "Image tag to deploy (e.g., git sha)."
  default     = "latest"
}

variable "openai_api_key" {
  type        = string
  description = "OPENAI_API_KEY injected into compose env (.env). Prefer using secrets manager later."
  sensitive   = true
  default     = ""
}

variable "tags" {
  type        = map(string)
  description = "Common tags applied to resources."
  default     = {}
}
