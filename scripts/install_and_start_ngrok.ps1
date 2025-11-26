$zip = Join-Path $env:USERPROFILE 'Downloads\ngrok-stable-windows-amd64.zip'
Write-Output "Downloading ngrok..."
Invoke-WebRequest -Uri "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip" -OutFile $zip -UseBasicParsing
Write-Output "Extracting to C:\tools\ngrok ..."
if (-Not (Test-Path 'C:\tools\ngrok')) { New-Item -ItemType Directory -Path 'C:\tools\ngrok' | Out-Null }
Expand-Archive -Path $zip -DestinationPath 'C:\tools\ngrok' -Force
$ngrokPath = 'C:\tools\ngrok\ngrok.exe'
if (-Not (Test-Path $ngrokPath)) { Write-Error 'ngrok executable not found after extraction.'; exit 1 }
Write-Output "Starting ngrok from $ngrokPath ..."
Start-Process -FilePath $ngrokPath -ArgumentList 'http','5000','--log=stdout' -WindowStyle Hidden -PassThru | Out-Null
Start-Sleep -Seconds 2
$found = $false
for ($i=0; $i -lt 20; $i++) {
    try {
        $res = Invoke-RestMethod http://127.0.0.1:4040/api/tunnels -ErrorAction Stop
        if ($res.tunnels -and $res.tunnels.Count -gt 0) {
            foreach ($t in $res.tunnels) { Write-Output "PUBLIC_URL: $($t.public_url)" }
            $found = $true
            break
        }
    } catch {
        Start-Sleep -Seconds 1
    }
}
if (-Not $found) { Write-Output "NO_TUNNEL"; exit 1 } else { exit 0 }
