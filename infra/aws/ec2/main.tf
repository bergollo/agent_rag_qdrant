data "aws_ami" "al2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_instance" "app" {
  ami                    = data.aws_ami.al2023.id
  instance_type          = var.instance_type
  subnet_id              = var.subnet_id
  vpc_security_group_ids = [aws_security_group.app.id]
  iam_instance_profile   = aws_iam_instance_profile.ec2_profile.name
  key_name               = var.key_name

  user_data = templatefile("${path.module}/user_data.sh", {
    aws_region    = var.aws_region
    ecr_registry  = var.ecr_registry
    tag           = var.image_tag
    openai_key    = var.openai_api_key
  })

  tags = {
    Name = "${var.project_name}-compose"
  }
}
