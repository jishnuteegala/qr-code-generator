# PowerShell setup script for QR Code Generator
# This automates the setup process on Windows

Write-Host "QR Code Generator - Setup Script" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8+ from https://www.python.org" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path .venv) {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv .venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to activate. You may need to run:" -ForegroundColor Red
    Write-Host "  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Verify sample input file
Write-Host ""
Write-Host "Checking sample input file..." -ForegroundColor Yellow
if (Test-Path input\contacts.xlsx) {
    Write-Host "✓ Sample input file exists" -ForegroundColor Green
} else {
    Write-Host "⚠ Sample input file not found at input\contacts.xlsx" -ForegroundColor Yellow
    Write-Host "  You'll need to create your own Excel file with a 'Phone' column" -ForegroundColor Yellow
}

# Success message
Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Quick start commands:" -ForegroundColor Cyan
Write-Host "  python generate_qr_code_images.py                    # Generate with defaults"
Write-Host "  python generate_qr_code_images.py --help             # View all options"
Write-Host "  python generate_qr_code_images.py --payload-format vcard --filename-template '{Name}'"
Write-Host ""
Write-Host "Remember to activate the virtual environment before running:"
Write-Host "  .venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host ""
