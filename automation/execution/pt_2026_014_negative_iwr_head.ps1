try{Invoke-WebRequest -Uri 'http://127.0.0.1:9/' -Method Head -TimeoutSec 1 -ErrorAction Stop}catch{Write-Output 'expected bounded local refusal'}
