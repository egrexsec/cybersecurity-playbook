$ErrorActionPreference = 'Stop'
schtasks.exe /Query /TN '\Microsoft\Windows\PushToInstall\Registration' | Out-Host
