package main

import rego.v1

is_bucket_change(r) if {
  r.mode == "managed"
  r.type == "google_storage_bucket"
  r.change.after != null
}

versioning_enabled(after) if {
  versions := object.get(after, "versioning", [])
  some version in versions
  object.get(version, "enabled", false) == true
}

deny contains msg if {
  r := input.resource_changes[_]
  is_bucket_change(r)
  object.get(object.get(r.change.after, "labels", {}), "environment", "") != "capstone"
  msg := sprintf("Resource %s must set labels.environment to 'capstone'.", [r.address])
}

deny contains msg if {
  r := input.resource_changes[_]
  is_bucket_change(r)
  object.get(object.get(r.change.after, "labels", {}), "managed_by", "") != "terraform"
  msg := sprintf("Resource %s must set labels.managed_by to 'terraform'.", [r.address])
}

deny contains msg if {
  r := input.resource_changes[_]
  is_bucket_change(r)
  object.get(r.change.after, "uniform_bucket_level_access", false) != true
  msg := sprintf("Resource %s must enable uniform bucket-level access.", [r.address])
}

deny contains msg if {
  r := input.resource_changes[_]
  is_bucket_change(r)
  object.get(r.change.after, "public_access_prevention", "") != "enforced"
  msg := sprintf("Resource %s must enforce public access prevention.", [r.address])
}

deny contains msg if {
  r := input.resource_changes[_]
  is_bucket_change(r)
  not versioning_enabled(r.change.after)
  msg := sprintf("Resource %s must enable object versioning.", [r.address])
}
