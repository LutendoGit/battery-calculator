Start-Sleep -Seconds 1
for ($i=0; $i -lt 12; $i++) {
    try {
        $res = Invoke-RestMethod http://127.0.0.1:4040/api/tunnels -ErrorAction Stop
        if ($res.tunnels -and $res.tunnels.Count -gt 0) {
            foreach ($t in $res.tunnels) {
                Write-Output $t.public_url
            }
            exit 0
        }
    } catch {
        Start-Sleep -Seconds 1
    }
}
Write-Output "NO_TUNNEL"
exit 1
