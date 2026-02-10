// iam_policies.tf

// This file defines an IAM policy that allows Terraform to create and manage ECR repositories.
resource "aws_iam_policy" "ecr_manage" {
  name        = "${var.project_name}-ecr-manage"
  description = "Allow Terraform to manage ECR repositories created by this project"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "ManageECRRepos",
        Effect = "Allow",
        Action = [
          "ecr:CreateRepository",
          "ecr:DeleteRepository",
          "ecr:DescribeRepositories",
          "ecr:PutLifecyclePolicy",
          "ecr:GetLifecyclePolicy",
          "ecr:DeleteLifecyclePolicy",
          "ecr:TagResource",
          "ecr:UntagResource",
          "ecr:ListTagsForResource",
          "ecr:SetRepositoryPolicy",
          "ecr:GetRepositoryPolicy",
          "ecr:DeleteRepositoryPolicy"
        ],
        Resource = "*"
      }
    ]
  })
}
