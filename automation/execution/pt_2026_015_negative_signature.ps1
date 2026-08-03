Get-AuthenticodeSignature $env:WINDIR\System32\mshta.exe | Select-Object Status,StatusMessage | ConvertTo-Json -Compress
