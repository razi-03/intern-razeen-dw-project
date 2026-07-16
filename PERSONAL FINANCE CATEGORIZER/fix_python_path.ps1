# 🔧 Automatic Python Fix Script for Windows
# Run this in PowerShell to fix the PATH issue

Write-Host "🔍 Searching for system Python installation..." -ForegroundColor Cyan

# Search for Python installations
$pythons = @()

# Check common locations
$commonPaths = @(
    "C:\Program Files\Python312",
    "C:\Program Files\Python311",
    "C:\Program Files\Python310",
    "C:\Python312",
    "C:\Python311",
    "C:\Python310"
)

foreach ($path in $commonPaths) {
    if (Test-Path "$path\python.exe") {
        Write-Host "✅ Found: $path" -ForegroundColor Green
        $pythons += $path
    }
}

# Search user AppData
$userPython = Get-ChildItem -Path "$env:LOCALAPPDATA\Programs\Python" -ErrorAction SilentlyContinue | 
    Where-Object { Test-Path "$($_.FullName)\python.exe" } |
    Select-Object -ExpandProperty FullName

if ($userPython) {
    Write-Host "✅ Found: $userPython" -ForegroundColor Green
    $pythons += $userPython
}

if ($pythons.Count -eq 0) {
    Write-Host "`n❌ No system Python found!" -ForegroundColor Red
    Write-Host "`n📥 Download Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "   ⚠️  CHECK 'Add Python to PATH' during installation!" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n🔧 Creating virtual environment..." -ForegroundColor Cyan

# Use first found Python
$pythonPath = $pythons[0]
$pythonExe = "$pythonPath\python.exe"

# Create venv
& $pythonExe -m venv finance_venv

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to create venv" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Virtual environment created" -ForegroundColor Green

# Activate venv
Write-Host "`n📦 Activating virtual environment..." -ForegroundColor Cyan
& .\finance_venv\Scripts\Activate.ps1

Write-Host "`n📥 Installing packages..." -ForegroundColor Cyan
pip install -r finance_requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ SUCCESS! All packages installed!" -ForegroundColor Green
    Write-Host "`n🚀 Now run:" -ForegroundColor Yellow
    Write-Host "   python finance_01_categorizer.py" -ForegroundColor Cyan
    Write-Host "   streamlit run finance_05_dashboard.py" -ForegroundColor Cyan
} else {
    Write-Host "`n❌ Installation failed" -ForegroundColor Red
    exit 1
}
