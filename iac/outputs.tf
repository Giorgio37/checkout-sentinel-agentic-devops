output "bucket_name" {
  description = "Name of the protected capstone artifact bucket."
  value       = google_storage_bucket.capstone_artifacts.name
}

output "bucket_url" {
  description = "Google Cloud Storage URL for the bucket."
  value       = google_storage_bucket.capstone_artifacts.url
}
