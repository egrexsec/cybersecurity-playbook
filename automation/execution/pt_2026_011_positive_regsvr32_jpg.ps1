$ErrorActionPreference='SilentlyContinue'
$dst='C:\Windows\Temp\pt-2026-011-shell32.jpg'
$marker='C:\Windows\Temp\pt-2026-011-jpg.txt'
Copy-Item 'C:\Windows\System32\shell32.dll' $dst -Force
cmd.exe /c "regsvr32.exe /s $dst"
Set-Content -Path $marker -Value ([string](Test-Path $dst))
Get-Item $marker | Select-Object FullName,Length,LastWriteTime | Format-List
