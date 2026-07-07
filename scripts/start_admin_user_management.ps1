param(
    [string]$AdminToken = '',
    [int]$Port = 5000,
    [string]$BindHost = '127.0.0.1',
    [switch]$NoBrowser
)

$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$appScript = Join-Path $projectRoot 'app.py'
$venvPython = Join-Path $projectRoot '.venv\Scripts\python.exe'

if (-not (Test-Path $appScript)) {
    throw "App entrypoint not found at: $appScript"
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

if ([string]::IsNullOrWhiteSpace($AdminToken)) {
    if ($env:ADMIN_STREAM_TOKEN) {
        $AdminToken = $env:ADMIN_STREAM_TOKEN
    } else {
        # Prompt only if not provided as parameter or existing env var.
        $AdminToken = Read-Host 'Enter ADMIN_STREAM_TOKEN for admin interface'
    }
}

if ([string]::IsNullOrWhiteSpace($AdminToken)) {
    throw 'Admin token cannot be empty.'
}

$env:ADMIN_STREAM_TOKEN = $AdminToken
$env:FLASK_RUN_HOST = $BindHost
$env:FLASK_RUN_PORT = [string]$Port
if (-not $env:FLASK_DEBUG) {
    $env:FLASK_DEBUG = '0'
}

$appUrl = "http://$BindHost`:$Port/"
$adminUrl = "http://$BindHost`:$Port/learn/admin/users?token=$AdminToken"

Write-Output 'Starting local admin user management app...'
Write-Output "Project root: $projectRoot"
Write-Output "Python: $pythonExe"
Write-Output "Host: $BindHost"
Write-Output "Port: $Port"
Write-Output "Admin page: $adminUrl"
Write-Output 'Press Ctrl+C to stop the app.'

if (-not $NoBrowser) {
    Start-Process $adminUrl | Out-Null
}

Push-Location $projectRoot
try {
    & $pythonExe $appScript
} finally {
    Pop-Location
}
