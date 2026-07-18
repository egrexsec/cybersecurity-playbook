$ErrorActionPreference = 'Stop'
$bytes = [Text.Encoding]::Unicode.GetBytes('Set-Content -Path "$env:SystemRoot\Temp\variant-marker.txt" -Value "Hello from modified variant"')
$b64 = [Convert]::ToBase64String($bytes)
Invoke-Expression ([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($b64)))
Get-Item "$env:SystemRoot\Temp\variant-marker.txt" | Select-Object FullName,Length,LastWriteTime | Format-List
