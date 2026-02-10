# fix-clock.sh - fix the clock on an EC2 instance

# Check your current time
date -u
date

# Ubuntu/Debian (most common on Free Tier / Linux)
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
timedatectl status
# If systemd-timesyncd isn’t running, install NTP tools:
sudo apt update
sudo apt install -y chrony
sudo systemctl enable --now chrony
chronyc tracking


# # Amazon Linux 2
# sudo systemctl enable --now chronyd
# chronyc tracking


# AWS CLI should work now, as the clock is fixed: 
aws sts get-caller-identity