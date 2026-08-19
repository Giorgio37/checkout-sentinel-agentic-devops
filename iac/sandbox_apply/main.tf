terraform {
  required_version = ">= 1.6.0"
}

variable "approved" {
  description = "Whether the exact sandbox release was approved by a human."
  type        = bool
}

variable "approval_hash" {
  description = "SHA-256 of the approved cloud plan."
  type        = string

  validation {
    condition     = can(regex("^[a-f0-9]{64}$", var.approval_hash))
    error_message = "approval_hash must be a lowercase SHA-256 digest."
  }
}

resource "terraform_data" "approved_release" {
  input = {
    release       = "2.3.1"
    environment   = "capstone-sandbox"
    approved      = var.approved
    approval_hash = var.approval_hash
  }
}

output "applied_release" {
  description = "Auditable sandbox apply result."
  value       = terraform_data.approved_release.output
}

