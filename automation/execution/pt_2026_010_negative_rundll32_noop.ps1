$ErrorActionPreference='SilentlyContinue'
cmd.exe /c "rundll32.exe shell32.dll,Control_RunDLL appwiz.cpl" | Out-Host
