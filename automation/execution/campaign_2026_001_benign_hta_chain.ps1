$ErrorActionPreference='Stop'
$root='C:\Windows\Temp\dc1-campaign'
New-Item -ItemType Directory $root -Force|Out-Null
$source=Join-Path $root 'source.hta';$staged=Join-Path $root 'staged.hta';$marker=Join-Path $root 'campaign-marker.txt'
$pidFile=Join-Path $root 'process-ids.txt';if(Test-Path $pidFile){throw 'prior process record exists; run cleanup before reuse'};Remove-Item $source,$staged,$marker,(Join-Path $root 'result.json') -Force -ErrorAction SilentlyContinue
$body=@'
<html><head><hta:application showintaskbar="no" windowstate="minimize" /><script language="VBScript">
Set s=CreateObject("WScript.Shell")
s.Run "powershell.exe -NoProfile -NonInteractive -Command Set-Content -LiteralPath C:\Windows\Temp\dc1-campaign\campaign-marker.txt -Value benign-campaign",0,True
window.close
</script></head></html>
'@
Set-Content $source $body -Encoding Ascii
$server=Start-Job -ScriptBlock {param($file)$l=[Net.HttpListener]::new();$l.Prefixes.Add('http://127.0.0.1:18769/');$l.Start();try{$c=$l.GetContext();$b=[IO.File]::ReadAllBytes($file);$c.Response.StatusCode=200;$c.Response.ContentType='text/html';$c.Response.ContentLength64=$b.Length;$c.Response.OutputStream.Write($b,0,$b.Length);$c.Response.OutputStream.Close()}finally{$l.Stop();$l.Close()}} -ArgumentList $source
try{Start-Sleep 2;Invoke-WebRequest -Uri 'http://127.0.0.1:18769/stage.hta' -OutFile $staged -UseBasicParsing;if(-not(Wait-Job $server -Timeout 30)){throw 'server timeout'};$sourceHash=(Get-FileHash $source).Hash;$stagedHash=(Get-FileHash $staged).Hash;if($sourceHash -ne $stagedHash){throw 'staged HTA hash mismatch'};$p=Start-Process mshta.exe -ArgumentList $staged -PassThru;[string]$p.Id|Set-Content $pidFile;if(-not$p.WaitForExit(30000)){try{$p.Kill()}catch{};throw 'mshta timeout'};$deadline=(Get-Date).AddSeconds(10);do{Start-Sleep -Milliseconds 250}until((Test-Path $marker)-or(Get-Date)-gt$deadline);if(-not(Test-Path $marker)){throw 'campaign marker missing'};[pscustomobject]@{SourceHash=$sourceHash;StagedHash=$stagedHash;MarkerHash=(Get-FileHash $marker).Hash;Completed=$true}|ConvertTo-Json -Compress|Set-Content (Join-Path $root 'result.json')}finally{Get-Job|Stop-Job -ErrorAction SilentlyContinue;Get-Job|Remove-Job -Force -ErrorAction SilentlyContinue}
