# iam_roles_github_oidc.tf

data "aws_caller_identity" "current" {}

resource "aws_iam_openid_connect_provider" "github" {
  url             = "https://token.actions.githubusercontent.com"
  thumbprint_list = var.github_oidc_thumbprints
  client_id_list  = [var.github_oidc_audience]
}

locals {
  github_branch_subs = [
    for b in var.allowed_branches :
    "repo:${var.github_org}/${var.github_repo}:ref:refs/heads/${b}"
  ]

  github_tag_subs = [
    for t in var.allowed_tags :
    "repo:${var.github_org}/${var.github_repo}:ref:refs/tags/${t}"
  ]

  github_sub_patterns = concat(local.github_branch_subs, local.github_tag_subs)
}

resource "aws_iam_role" "github_actions_ecr_push" {
  name = "${var.project_name}-github-actions-ecr-push"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid    = "GitHubOIDCAssumeRole"
      Effect = "Allow"
      Principal = { Federated = aws_iam_openid_connect_provider.github.arn }
      Action = [
        "sts:AssumeRoleWithWebIdentity"
        # ,"sts:TagSession" # optional
      ]
      Condition = {
        StringEquals = {
          "token.actions.githubusercontent.com:aud" = var.github_oidc_audience
        }
        StringLike = {
          "token.actions.githubusercontent.com:sub" = local.github_sub_patterns
        }
      }
    }]
  })
}
