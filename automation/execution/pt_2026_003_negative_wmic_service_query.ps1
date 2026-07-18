Get-WmiObject Win32_Service -Filter "Name='Spooler'" | Select-Object Name,State,StartMode | Format-List
