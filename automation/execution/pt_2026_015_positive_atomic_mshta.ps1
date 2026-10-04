$ErrorActionPreference='Continue'
$guid='8707a805-2b76-4f32-b1c0-14e558205772'
$atomicYaml='C:\Tools\AtomicRedTeam\atomics\T1218.005\T1218.005.yaml'
if(-not (Select-String -LiteralPath $atomicYaml -SimpleMatch $guid -Quiet)){throw 'Pinned Atomic UUID not present in staged definition'}
$root='C:\Windows\Temp\dc1-t1218-005';New-Item -ItemType Directory $root -Force|Out-Null
$start=(Get-Date).ToUniversalTime();$arg='about:<hta:application><script language="VBScript">Close(Execute("CreateObject(""Wscript.Shell"").Run%20""powershell.exe%20-nop%20-Command%20Write-Host%20Detection%20Cycle%201;Start-Sleep%20-Seconds%201"""))</script>'
try{$p=Start-Process "$env:WINDIR\System32\mshta.exe" -ArgumentList ('"{0}"' -f $arg) -PassThru -ErrorAction Stop;[string]$p.Id|Set-Content (Join-Path $root 'process-ids-atomic.txt');if(-not$p.WaitForExit(20000)){try{$p.Kill()}catch{};throw 'timeout'};$started=$true;$exit=$p.ExitCode}catch{$started=$false;$exit=$null;$launchError=$_.Exception.Message}
Start-Sleep 2
$defender=@(Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Windows Defender/Operational';StartTime=$start} -ErrorAction SilentlyContinue|Where-Object {$_.Id -in 1116,1117 -and $_.Message -match 'mshta'})
$result=[pscustomobject]@{AtomicGuid=$guid;ProcessStarted=$started;ExitCode=$exit;PreventiveEvents=$defender.Count;Outcome=$(if(-not$started -and $defender.Count){'prevented'}elseif($started){'executed'}else{'failed-unconfirmed'});Completed=$true}
$result|ConvertTo-Json -Compress|Set-Content (Join-Path $root 'positive.json');$result|ConvertTo-Json -Compress
