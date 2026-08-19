# Approved Terraform Sandbox Apply

This module provides a no-cost, local `terraform_data` apply so the approval-to-apply workflow can be demonstrated when the course GCP project's billing account is unavailable. It does not substitute for or claim a successful cloud deployment.

The workflow generates both approved and denied plans, runs Conftest against each, and applies only the approved plan. The input stores release, environment, approval state, and the approved cloud-plan SHA-256 in Terraform state.

