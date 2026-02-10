#!/bin/bash
set -euxo pipefail

dnf -y update
dnf -y install docker
systemctl enable --now docker

# Docker Compose plugin
dnf -y install docker-compose-plugin || true

mkdir -p /opt/app
cd /opt/app

cat > .env <<EOF
ECR_REGISTRY=${ecr_registry}
TAG=${tag}
OPENAI_API_KEY=${openai_key}
EOF

# Write docker-compose file (simplest: bake it in via templatefile too)
# Alternative: use S3 / git clone / userdata heredoc.

aws ecr get-login-password --region ${aws_region} \
  | docker login --username AWS --password-stdin ${ecr_registry}

docker compose -f docker-compose.aws.yml pull
docker compose -f docker-compose.aws.yml up -d
