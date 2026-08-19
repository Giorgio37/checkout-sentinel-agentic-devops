param(
  [Parameter(Mandatory = $true)][string]$TerraformPath,
  [Parameter(Mandatory = $true)][string]$ConftestPath
)

$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
$IacRoot = Join-Path (Split-Path -Parent $PSScriptRoot) "iac"
Push-Location $IacRoot
try {
  & $TerraformPath fmt -check -recursive
  if ($LASTEXITCODE -ne 0) { throw "terraform fmt failed." }
  & $TerraformPath init -backend=false
  if ($LASTEXITCODE -ne 0) { throw "terraform init failed." }
  & $TerraformPath validate
  if ($LASTEXITCODE -ne 0) { throw "terraform validate failed." }
  & $ConftestPath test fixtures/tfplan-pass.json --policy policy
  if ($LASTEXITCODE -ne 0) { throw "Compliant policy fixture was rejected." }
  & $ConftestPath test fixtures/tfplan-fail.json --policy policy
  if ($LASTEXITCODE -eq 0) { throw "Non-compliant policy fixture was not blocked." }
  Write-Host "IaC verification passed: Terraform validated and OPA allow/deny behavior is correct."
}
finally {
  Pop-Location
}

