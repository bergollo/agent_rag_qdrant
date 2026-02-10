# ecr_repositories.tf

# ECR Repositories
resource "aws_ecr_repository" "repos" {
  for_each = toset(var.repositories)

  name                 = each.value
  image_tag_mutability = var.ecr_image_tag_mutability
  force_delete         = var.ecr_force_delete

  image_scanning_configuration {
    scan_on_push = var.ecr_scan_on_push
  }

}

resource "aws_ecr_lifecycle_policy" "keep_recent" {
  for_each = var.enable_lifecycle_policy ? aws_ecr_repository.repos : {}

  repository = each.value.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last ${var.lifecycle_keep_last_n} images (any tag)"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = var.lifecycle_keep_last_n
      }
      action = { type = "expire" }
    }]
  })
}

