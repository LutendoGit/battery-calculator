param(
    [int]$Port = 5001,
    [string]$BindHost = '127.0.0.1',
    [switch]$NoBrowser
)

$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$appScript = Join-Path $projectRoot 'mermaid_pdf_app.py'
$venvPython = Join-Path $projectRoot '.venv\Scripts\python.exe'

if (-not (Test-Path $appScript)) {
    throw "Standalone Mermaid app not found at: $appScript"
}

if (Test-Path $venvPython) {
    $pythonExe = $venvPython
} else {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCmd) {
        throw 'Python was not found. Create the .venv or install Python first.'
    }
    $pythonExe = $pythonCmd.Source
}

$env:MERMAID_PDF_HOST = $BindHost
$env:MERMAID_PDF_PORT = [string]$Port
$url = "http://$BindHost`:$Port/"

Write-Output "Starting standalone Mermaid PDF app..."
Write-Output "Project root: $projectRoot"
Write-Output "Python: $pythonExe"
Write-Output "URL: $url"
Write-Output 'Press Ctrl+C to stop the app.'

if (-not $NoBrowser) {
    Start-Process $url | Out-Null
}

Push-Location $projectRoot
try {
    & $pythonExe $appScript
} finally {
    Pop-Location
}