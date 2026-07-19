$ErrorActionPreference='SilentlyContinue'
cmd.exe /c "regsvr32.exe /s C:\Windows\System32\shell32.dll" | Out-Host
