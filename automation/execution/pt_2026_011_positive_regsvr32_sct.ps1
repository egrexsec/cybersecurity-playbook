$ErrorActionPreference='SilentlyContinue'
$dir='C:\Windows\Temp\pt-2026-011'
$path=Join-Path $dir 'empty.sct'
$marker='C:\Windows\Temp\pt-2026-011-sct.txt'
New-Item -ItemType Directory -Path $dir -Force | Out-Null
$lines=@('<scriptlet>','<registration progid="PT2026011" classid="{AAAA1111-0000-0000-0000-0000FEEDACDC}"></registration>','<script language="JScript"></script>','</scriptlet>')
Set-Content -Path $path -Value $lines -Encoding ascii
cmd.exe /c "regsvr32.exe /s /u /i:$path scrobj.dll"
Set-Content -Path $marker -Value ([string](Test-Path $path))
Get-Item $marker | Select-Object FullName,Length,LastWriteTime | Format-List
