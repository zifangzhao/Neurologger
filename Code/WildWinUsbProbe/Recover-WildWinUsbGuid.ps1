$cli = 'C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe'
$start = 0x08000000
$total = 0x80000
$chunk = 0x2000
$outPath = Join-Path $PSScriptRoot '..\wild_flash_08000000_0807ffff.bin'
$outPath = [System.IO.Path]::GetFullPath($outPath)

if (-not (Test-Path $cli)) {
    throw "STM32CubeProgrammer CLI not found at: $cli"
}

$bytes = New-Object System.Collections.Generic.List[byte]
for ($offset = 0; $offset -lt $total; $offset += $chunk) {
    $addr = $start + $offset
    $size = [Math]::Min($chunk, $total - $offset)
    $text = & $cli -c port=SWD mode=HOTPLUG -r8 ('0x{0:X8}' -f $addr) ('0x{0:X}' -f $size) 2>&1 | Out-String
    foreach ($line in ($text -split "`r?`n")) {
        if ($line -match '^0x[0-9A-Fa-f]{8}\s*:\s*(.+)$') {
            foreach ($hex in ($matches[1] -split '\s+' | Where-Object { $_ -match '^[0-9A-Fa-f]{2}$' })) {
                $bytes.Add([Convert]::ToByte($hex, 16))
            }
        }
    }
}

[System.IO.File]::WriteAllBytes($outPath, $bytes.ToArray())
Write-Host "Wrote flash sample to $outPath"

$ascii = [System.Text.Encoding]::ASCII.GetString($bytes.ToArray())
$unicode = [System.Text.Encoding]::Unicode.GetString($bytes.ToArray())

function Show-Hit {
    param(
        [string]$Label,
        [string]$Value
    )

    $a = $ascii.IndexOf($Value)
    $u = $unicode.IndexOf($Value)
    if ($a -ge 0 -or $u -ge 0) {
        Write-Host ("{0}: ASCII={1} Unicode={2}" -f $Label, $a, $u)
    }
}

Show-Hit 'Product string' 'WILD USB FS Bridge'
Show-Hit 'Interface string' 'WinUSB Stream'
Show-Hit 'MSFT100 marker' 'MSFT100'
Show-Hit 'Ext prop name' 'DeviceInterfaceGUIDs'

$guidPattern = '[0-9A-Fa-f]{8}\-[0-9A-Fa-f]{4}\-[0-9A-Fa-f]{4}\-[0-9A-Fa-f]{4}\-[0-9A-Fa-f]{12}'
$guidHits = [regex]::Matches($ascii + "`n" + $unicode, $guidPattern) |
    ForEach-Object { $_.Value } |
    Select-Object -Unique

if ($guidHits) {
    Write-Host "GUID hits:"
    $guidHits | ForEach-Object { Write-Host "  $_" }
} else {
    Write-Host 'No GUID strings found.'
}
