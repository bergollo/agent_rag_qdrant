# AWS Terraform

---
---

## Pre-configuration before Terraform AWS Registry

Terraform can’t grant itself permissions unless that identity already has IAM rights.

Attach to user group permissions

- ECR repo creation access (under AmazonEC2ContainerRegistryPowerUser Policy)

- Attached inline policy:
```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Sid": "VisualEditor0",
			"Effect": "Allow",
			"Action": "iam:CreateOpenIDConnectProvider",
			"Resource": "*"
		}
	]
}
```

---
---

`aws configure`

---
---

That error is almost always **your machine’s clock is wrong** (or timezone/time drift). AWS request signing is time-sensitive; if your system time is ahead/behind by ~5+ minutes you’ll get `Signature expired`.

In your message, AWS is saying the signature timestamp is **earlier than AWS’s current time** by ~8–15 minutes.

## Fix: sync your system clock

### 1) Check your current time

```bash
date -u
date
```

If it’s not correct, sync it:

---

## Ubuntu/Debian (most common on Free Tier / Linux)

```bash
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
timedatectl status
```

If `systemd-timesyncd` isn’t running, install NTP tools:

```bash
sudo apt update
sudo apt install -y chrony
sudo systemctl enable --now chrony
chronyc tracking
```

---

## Amazon Linux 2 / Amazon Linux 2023

```bash
sudo systemctl enable --now chronyd
chronyc tracking
```

---

## Inside Docker container?

Containers inherit host time. Fix the **host** clock (above).
To confirm you’re in a container:

```bash
cat /proc/1/cgroup | head
```

---

## Then retry

```bash
aws sts get-caller-identity
```

---

## Also: avoid IMDS timeout in Terraform (optional but helpful)

```bash
export AWS_EC2_METADATA_DISABLED=true
```

---

## If time is correct but error persists

Two other (less common) causes:

1. **Old cached credentials with a bad timestamp**
   Run:

```bash
rm -rf ~/.aws/cli/cache
```

2. **Using temporary credentials with an expired session token**
   If you set `AWS_SESSION_TOKEN`, unset and reconfigure:

```bash
unset AWS_SESSION_TOKEN
```

---

If you paste the output of these (no secrets):

```bash
date -u
aws --version
aws configure list
```

I can tell you exactly what’s off.

---
---

You can get the real `vpc_id` and `subnet_id` from **AWS Console**, **AWS CLI**, or even **Terraform data sources**. Here are the practical ways—from easiest to most automated.

---

### Find VPC ID
### Find via AWS CLI (fastest for devs)

### List your VPCs

```bash
aws ec2 describe-vpcs --query "Vpcs[*].[VpcId,CidrBlock,IsDefault]" --output table
```

You’ll see:

```
----------------------------------------
|           DescribeVpcs               |
+--------------------+----------------+
|  vpc-0a12bc34de56  | 172.31.0.0/16  | true |
+--------------------+----------------+
```

---

### List subnets in that VPC

```bash
aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=vpc-0a12bc34de56" \
  --query "Subnets[*].[SubnetId,AvailabilityZone,CidrBlock]" \
  --output table
```

Pick one subnet ID from the result.

---

# 3) Let Terraform discover them automatically (best long-term)

You don’t actually need to hardcode anything.

Add this file in your EC2 module:

### `network_data.tf`

```hcl
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

locals {
  effective_vpc_id    = var.vpc_id != "" ? var.vpc_id : data.aws_vpc.default.id
  effective_subnet_id = var.subnet_id != "" ? var.subnet_id : data.aws_subnets.default.ids[0]
}
```

Then in your resources use:

```hcl
vpc_id    = local.effective_vpc_id
subnet_id = local.effective_subnet_id
```

👉 Now Terraform will use the **default VPC + first subnet automatically** and you can delete those values from `terraform.tfvars`.

---

# 4) Which subnet should you choose?

## If you want public access to the app

Pick a subnet that:

* Is in a VPC with an Internet Gateway
* Has a route `0.0.0.0/0 → igw-xxxx`

Usually the **default VPC subnets** already satisfy this.

## If later you want private + ALB

Then we’ll switch to:

* Private subnet for EC2
* Public ALB in public subnets
* No direct EC2 exposure


---
---