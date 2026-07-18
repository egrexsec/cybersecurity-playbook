$ErrorActionPreference = 'Stop'
Get-ItemProperty -Path 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run' | Select-Object PSPath | Format-List
