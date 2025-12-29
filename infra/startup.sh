#!/bin/bash
set -eux

apt-get update
apt-get install -y ca-certificates curl gnupg lsb-release

install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
> /etc/apt/sources.list.d/docker.list

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

systemctl enable docker
systemctl start docker

mkdir -p /opt/agent-rag
chmod 755 /opt/agent-rag


# Install Google Cloud SDK
apt-get install -y apt-transport-https ca-certificates gnupg curl
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
  | sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list
apt-get update
apt-get install -y google-cloud-cli
# Authenticate Docker to Google Container Registry
gcloud auth configure-docker us-central1-docker.pkg.dev --quiet


# NOTE:
# We do NOT bake secrets or compose here.
# After the VM is up, you will SCP:
#   - docker-compose.prod.yml
#   - .env.prod
# Then run docker compose manually the first time.
