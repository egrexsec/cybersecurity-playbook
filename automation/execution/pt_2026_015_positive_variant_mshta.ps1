$ErrorActionPreference='Stop';$root='C:\Windows\Temp\dc1-t1218-005';New-Item -ItemType Directory $root -Force|Out-Null;$marker=Join-Path $root 'variant-marker.txt';$hta=Join-Path $root 'variant.hta'
$body=@'
<html><head><hta:application showintaskbar="no" windowstate="minimize" /><script language="VBScript">
Set s=CreateObject("WScript.Shell")
s.Run "cmd.exe /c echo benign-mshta-variant> C:\Windows\Temp\dc1-t1218-005\variant-marker.txt",0,True
window.close
</script></head></html>
'@
Remove-Item $marker,$hta,(Join-Path $root 'process-ids-variant.txt') -Force -ErrorAction SilentlyContinue;Set-Content $hta $body -Encoding Ascii; $p=Start-Process mshta.exe -ArgumentList $hta -PassThru;[string]$p.Id|Set-Content (Join-Path $root 'process-ids-variant.txt'); if(-not $p.WaitForExit(30000)){try{$p.Kill()}catch{};throw 'mshta timeout'};if(-not(Test-Path $marker)){throw 'marker missing'}
[pscustomobject]@{MarkerHash=(Get-FileHash $marker).Hash;Completed=$true}|ConvertTo-Json -Compress|Set-Content (Join-Path $root 'variant.json')
