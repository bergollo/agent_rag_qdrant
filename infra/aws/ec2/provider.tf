provider "aws" {
  region = var.aws_region

  default_tags {
    tags = merge(
      {
        ManagedBy = "terraform"
        Project   = var.project_name
        Module    = "ec2-compose"
      },
      var.tags
    )
  }
}
