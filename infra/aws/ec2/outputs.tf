output "instance_id" {
  value = aws_instance.app.id
}

output "public_ip" {
  value = aws_instance.app.public_ip
}

output "public_dns" {
  value = aws_instance.app.public_dns
}

output "frontend_url" {
  value = "http://${aws_instance.app.public_dns}:${var.frontend_port}"
}

output "ssh_command" {
  value = (
    var.key_name != ""
    ? "ssh -i <path-to-your-key.pem> ec2-user@${aws_instance.app.public_dns}"
    : "SSH key_name not set (var.key_name)."
  )
}
