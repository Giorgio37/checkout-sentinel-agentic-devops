param(
  [string]$PythonPath = "python"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $ProjectRoot
try {
  & $PythonPath -m pytest
  if ($LASTEXITCODE -ne 0) { throw "Unit tests failed." }

  & $PythonPath -m checkout_sentinel.orchestrator prepare | Out-Null
  if ($LASTEXITCODE -ne 0) { throw "Pipeline preparation failed." }

  & $PythonPath -m checkout_sentinel.orchestrator deploy 2>&1 | Out-Null
  if ($LASTEXITCODE -eq 0) { throw "Approval guard failed: unapproved deployment was allowed." }

  Write-Host "Verification passed: tests passed, evidence prepared, and unapproved deployment was blocked."
}
finally {
  Pop-Location
}

