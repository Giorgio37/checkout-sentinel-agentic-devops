variable "project_id" {
  description = "GCP project ID used for the lab."
  type        = string
}

variable "region" {
  description = "Default GCP region for provider operations."
  type        = string
  default     = "us-central1"
}

variable "bucket_location" {
  description = "GCS location for the capstone artifact bucket."
  type        = string
  default     = "US"
}

variable "bucket_name" {
  description = "Globally unique GCS bucket name, such as capstone-artifacts-my-project."
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9._-]{1,61}[a-z0-9]$", var.bucket_name))
    error_message = "bucket_name must be 3-63 characters and use lowercase letters, digits, dots, underscores, or hyphens."
  }
}
