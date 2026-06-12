param(
    [string]$InstanceId = "USB\VID_0483&PID_572A\2004BF1A0800",
    [string]$InterfaceGuid = "{6C303587-B774-4A8B-8AFF-20557620207A}"
)

$ErrorActionPreference = "Stop"
$logPath = Join-Path $PSScriptRoot "register-guid.log"
$instanceSuffix = ($InstanceId -split '\\')[-1]
$keyPath = "HKLM:\SYSTEM\CurrentControlSet\Enum\USB\VID_0483&PID_572A\$instanceSuffix"

Start-Transcript -Path $logPath -Append | Out-Null

try {
    Write-Host "Writing DeviceInterfaceGUIDs under $keyPath"
    New-ItemProperty -Path $keyPath -Name "DeviceInterfaceGUIDs" -PropertyType MultiString -Value $InterfaceGuid -Force | Out-Null

    Write-Host "Verifying registry value"
    Get-ItemProperty -Path $keyPath | Format-List FriendlyName,Service,DeviceInterfaceGUIDs

    Write-Host "Restarting device $InstanceId"
    pnputil /restart-device $InstanceId

    Write-Host "Enumerating device interfaces"
    pnputil /enum-interfaces /instanceid $InstanceId /properties
}
finally {
    Stop-Transcript | Out-Null
}
