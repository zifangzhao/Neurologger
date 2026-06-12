param(
    [string]$InstanceId = "USB\VID_0483&PID_572A\2004BF1A0800"
)

$ErrorActionPreference = "Stop"
$logPath = Join-Path $PSScriptRoot "reenumerate-device.log"

Start-Transcript -Path $logPath -Append | Out-Null

try {
    Write-Host "Removing device $InstanceId"
    pnputil /remove-device $InstanceId

    Start-Sleep -Seconds 1

    Write-Host "Scanning devices"
    pnputil /scan-devices

    Start-Sleep -Seconds 2

    Write-Host "Enumerating interfaces after scan"
    pnputil /enum-interfaces /instanceid $InstanceId /properties
}
finally {
    Stop-Transcript | Out-Null
}
