<#
.SYNOPSIS
  Sets up the TARS folder structure, creates or activates a Python 3.10 venv.

.DESCRIPTION
  1. Ensures a "tars" directory with subfolders "config" and "core".
  2. Ensures empty placeholder files exist for your TARS-based Python structure:
     config.yaml, tars_core.py, stt_engine.py, tts_engine.py, llm_integration.py, main.py,
     persona_manager.py, and tars_persona.json.
  3. Checks if a venv folder "tars-venv" exists:
       - If not, creates it with Python 3.10.
       - If yes, activates it.
#>

# --- 1) Create folder structure if missing ---
Write-Host "Checking folder structure..."

if (!(Test-Path -Path ".\tars")) {
    Write-Host "Creating folder: tars"
    New-Item -ItemType Directory -Path ".\tars" | Out-Null
}

# Subfolder: config
if (!(Test-Path -Path ".\tars\config")) {
    Write-Host "Creating folder: tars\config"
    New-Item -ItemType Directory -Path ".\tars\config" | Out-Null
}

# Subfolder: core
if (!(Test-Path -Path ".\tars\core")) {
    Write-Host "Creating folder: tars\core"
    New-Item -ItemType Directory -Path ".\tars\core" | Out-Null
}

# --- 2) Create empty files if they don't exist ---
$files = @(
    ".\tars\config\config.yaml",
    ".\tars\core\tars_core.py",
    ".\tars\core\stt_engine.py",
    ".\tars\core\tts_engine.py",
    ".\tars\core\llm_integration.py",
    ".\tars\core\persona_manager.py",
    ".\tars\main.py",
    ".\tars\tars_persona.json"
)

foreach ($file in $files) {
    if (!(Test-Path -Path $file)) {
        Write-Host "Creating empty file: $file"
        New-Item -ItemType File -Path $file | Out-Null
    }
}

Write-Host "Folder structure is ready."

# --- 3) Check or create Python 3.10 virtual environment ---
$venvPath = ".\tars-venv"
if (!(Test-Path -Path $venvPath)) {
    Write-Host "No virtual environment found. Creating with Python 3.10..."
    # Adjust to your Python 3.10 command if needed (e.g. "python3.10" or "python")
    py -3.10 -m venv $venvPath
    Write-Host "Virtual environment created at $venvPath"
} else {
    Write-Host "Virtual environment already exists at $venvPath"
}

# --- 4) Activate the virtual environment ---
Write-Host "Activating virtual environment..."
. "$venvPath\Scripts\Activate.ps1"

Write-Host "`nTARS setup complete. Virtual environment active."
