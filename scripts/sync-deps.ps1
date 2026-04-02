# Sync lock files from pyproject.toml using pip-tools

param(
    [switch]$DryRun,
    [switch]$IncludeTest
)

$rootDir = Split-Path -Parent $PSScriptRoot
Set-Location $rootDir

$pipCompile = $null
if (Test-Path ".venv\Scripts\pip-compile.exe") {
    $pipCompile = ".venv\Scripts\pip-compile.exe"
}
else {
    $command = Get-Command pip-compile -ErrorAction SilentlyContinue
    if ($null -ne $command) {
        $pipCompile = "pip-compile"
    }
}

if ($null -eq $pipCompile) {
    Write-Error "pip-compile not found. Install pip-tools first: pip install pip-tools"
    exit 1
}

if ($DryRun) {
    & $pipCompile pyproject.toml --strip-extras --output-file requirements.txt --dry-run
}
else {
    & $pipCompile pyproject.toml --strip-extras --output-file requirements.txt
}
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "requirements.txt is synced with pyproject.toml" -ForegroundColor Green

if ($IncludeTest) {
    if ($DryRun) {
        & $pipCompile pyproject.toml --extra test --strip-extras --constraint requirements.txt --output-file requirements-dev.txt --dry-run
    }
    else {
        & $pipCompile pyproject.toml --extra test --strip-extras --constraint requirements.txt --output-file requirements-dev.txt
    }

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host "requirements-dev.txt is synced with pyproject.toml[test]" -ForegroundColor Green
}
