# outputs.tf

data "aws_region" "current" {}

output "aws_account_id" {
  value = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  value = var.aws_region
}

output "github_actions_role_arn" {
  description = "Set this as GitHub secret AWS_GITHUB_OIDC_ROLE_ARN"
  value       = aws_iam_role.github_actions_ecr_push.arn
}

output "ecr_registry" {
  description = "ECR registry host, e.g. 123456789012.dkr.ecr.us-west-2.amazonaws.com"
  value       = "${data.aws_caller_identity.current.account_id}.dkr.ecr.${var.aws_region}.amazonaws.com"
}

output "ecr_repository_urls" {
  description = "Map of repo name -> repository URL"
  value = {
    for name, repo in aws_ecr_repository.repos :
    name => repo.repository_url
  }
}
