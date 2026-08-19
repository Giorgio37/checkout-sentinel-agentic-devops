package main

import rego.v1

is_sandbox_release(r) if {
  r.mode == "managed"
  r.type == "terraform_data"
  r.name == "approved_release"
  r.change.after != null
}

deny contains msg if {
  r := input.resource_changes[_]
  is_sandbox_release(r)
  object.get(r.change.after.input, "approved", false) != true
  msg := "Sandbox apply requires approved=true from the human gate."
}

deny contains msg if {
  r := input.resource_changes[_]
  is_sandbox_release(r)
  object.get(r.change.after.input, "release", "") != "2.3.1"
  msg := "Sandbox apply may target release 2.3.1 only."
}

deny contains msg if {
  r := input.resource_changes[_]
  is_sandbox_release(r)
  not regex.match("^[a-f0-9]{64}$", object.get(r.change.after.input, "approval_hash", ""))
  msg := "Sandbox apply requires a valid approval SHA-256."
}

