# AWS Monorepo Infrastructure – Lessons Learned

This README captures the practical knowledge from setting up:

* ECR repositories via Terraform
* GitHub Actions OIDC push to ECR
* EC2 host running the full stack with Docker Compose

---

## 1) ECR + GitHub Actions OIDC (most common pitfalls)

### Trust policy must match the **exact** GitHub token

`sts:AssumeRoleWithWebIdentity` fails when any of these don’t match:

* `aud` must be **sts.amazonaws.com**
* `sub` must match the real workflow trigger

  * Branch push:
    `repo:ORG/REPO:ref:refs/heads/<branch>`
  * Tag push:
    `repo:ORG/REPO:ref:refs/tags/<tag>`
  * PR events use a different `sub` and will NOT match branch rules.

**If you get:**

> Not authorized to perform sts:AssumeRoleWithWebIdentity

Check in this order:

1. Secret `AWS_GITHUB_OIDC_ROLE_ARN` points to the correct role
2. `allowed_branches` includes the branch actually running
3. `github_org` / `github_repo` exactly match `GITHUB_REPOSITORY`
4. Audience = `sts.amazonaws.com`
5. Workflow has:

```yaml
permissions:
  id-token: write
  contents: read
```

---

## 2) GitHub build issues unrelated to AWS

Error:

> pulling image moby/buildkit:buildx-stable-1 … 500 Internal Server Error

Cause: Docker Hub outage from `docker/setup-buildx-action`.

**Fix:** remove buildx if not using multi-arch:

```yaml
# Delete this step
- uses: docker/setup-buildx-action@v3
```

Plain `docker build` + `docker push` is enough.

---

## 3) Terraform structure conventions

### Where things belong

* `ecr_repositories.tf` – only ECR resources
* `iam_roles_github_oidc.tf` – OIDC provider + role
* `iam_policies.tf` – policy JSON
* `iam_attachments.tf` – role → policy bindings
* `ec2/` – runtime host and compose deployment

### Do NOT create IAM policy “for Terraform itself”

Terraform cannot grant permissions to the identity running it.
Your local user/role must already have IAM rights outside Terraform.

---

## 4) EC2 deployment lessons

### Networking

* Need **real** `vpc_id` and `subnet_id`.
* Easiest: auto-discover default VPC via data sources.

### Instance type

* Free-tier accounts block `t3.medium`.
* Start with:

```hcl
instance_type = "t3.micro"
```

but expect memory pressure with:

* frontend
* Nest backend
* FastAPI AI
* MCP
* Qdrant

### Security

* Expose only frontend port publicly.
* Backend/AI/Qdrant stay internal to Docker network.
* Prefer SSM over SSH when possible.

---

## 5) Docker Compose on EC2

### Image format (ECR)

```
<ECR_REGISTRY>/<repo>:<tag>
```

Example env:

```
ECR_REGISTRY=123456.dkr.ecr.us-west-2.amazonaws.com
TAG=latest
```

### Instance IAM needs only PULL rights

* `ecr:GetAuthorizationToken` on `*`
* Pull actions scoped to repo ARNs

---

## 6) Debug checklist

### OIDC assume-role failure

* Print GitHub token claims to compare `sub`
* Confirm branch/tag trigger
* Verify role ARN secret
* Check audience

### EC2 apply failures

* “Malformed VPC” → placeholder IDs
* “Not free tier” → use `t3.micro`

### Build failures

* Docker Hub 500 → remove buildx

---

## 7) Next improvements

* Move `OPENAI_API_KEY` to SSM/Secrets Manager
* Add ALB + HTTPS instead of public EC2 port
* Add log collection (CloudWatch agent)
* Add health-based auto-recovery

