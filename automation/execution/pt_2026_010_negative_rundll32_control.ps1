$ErrorActionPreference='SilentlyContinue'
Start-Process rundll32.exe -ArgumentList 'shell32.dll,Control_RunDLL appwiz.cpl'
Start-Sleep -Seconds 3
Get-Process rundll32 -ErrorAction SilentlyContinue | Select-Object -First 3 ProcessName,Id | Format-List
Get-Process explorer -ErrorAction SilentlyContinue | Select-Object -First 1 ProcessName,Id | Format-List
