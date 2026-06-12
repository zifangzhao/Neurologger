param(
    [string]$InstanceId = "USB\VID_0483&PID_572A\2004BF1A0800"
)

$ErrorActionPreference = "Stop"
$logPath = Join-Path $PSScriptRoot "install-driver.log"
Start-Transcript -Path $logPath -Append | Out-Null

try {
    $infPath = Join-Path $PSScriptRoot "WILD_FS_Bridge_WinUSB.inf"
    if (-not (Test-Path $infPath)) {
        throw "INF not found: $infPath"
    }

    Write-Host "Installing local WinUSB driver package from $infPath"
    pnputil /add-driver $infPath /install

    Write-Host "Restarting device $InstanceId"
    pnputil /restart-device $InstanceId

    Write-Host "Enumerating device interfaces"
    pnputil /enum-interfaces /instanceid $InstanceId /properties
}
finally {
    Stop-Transcript | Out-Null
}
