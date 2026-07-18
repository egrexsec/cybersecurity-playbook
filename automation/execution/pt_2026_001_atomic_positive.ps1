$ErrorActionPreference = 'Stop'
$encoded = 'U2V0LUNvbnRlbnQgLXBhdGggIiRlbnY6U3lzdGVtUm9vdC9UZW1wL2FydC1tYXJrZXIudHh0IiAtdmFsdWUgIkhlbGxvIGZyb20gdGhlIEF0b21pYyBSZWQgVGVhbSI='
reg.exe add "HKEY_CURRENT_USER\Software\Classes\AtomicRedTeam" /v ART /t REG_SZ /d $encoded /f
Invoke-Expression ([Text.Encoding]::ASCII.GetString([Convert]::FromBase64String((Get-ItemProperty 'HKCU:\Software\Classes\AtomicRedTeam').ART)))
Get-Item "$env:SystemRoot\Temp\art-marker.txt" | Select-Object FullName,Length,LastWriteTime | Format-List
