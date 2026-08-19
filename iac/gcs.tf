resource "google_storage_bucket" "capstone_artifacts" {
  name     = var.bucket_name
  location = var.bucket_location

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false

  versioning {
    enabled = true
  }

  labels = {
    environment = "capstone"
    managed_by  = "terraform"
  }

  lifecycle {
    prevent_destroy = true
  }
}
