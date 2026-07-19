$ErrorActionPreference='SilentlyContinue'
reg.exe query "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" | Out-Host
