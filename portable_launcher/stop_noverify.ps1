$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$exe = Join-Path $root "yoko_rpa_mcp.exe"
$stubExe = Join-Path $root "dev_auth_stub.exe"
$pidFile = Join-Path $env:TEMP "yoko-dev-auth.pid"

$rpaProcesses = Get-CimInstance Win32_Process -Filter "Name='yoko_rpa_mcp.exe'"
if ($rpaProcesses) {
    try {
        Invoke-RestMethod -Uri "http://127.0.0.1:9921/shutdown" -Method Post -TimeoutSec 5 | Out-Null
    } catch {
        Write-Warning "Graceful shutdown failed; stale processes will be cleaned up."
    }

    foreach ($attempt in 1..50) {
        $rpaProcesses = Get-CimInstance Win32_Process -Filter "Name='yoko_rpa_mcp.exe'"
        if (-not $rpaProcesses) {
            break
        }
        Start-Sleep -Milliseconds 200
    }
    if ($rpaProcesses) {
        $rpaProcesses | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
    }
}

if (Test-Path -LiteralPath $pidFile) {
    $processId = [int](Get-Content -Raw -LiteralPath $pidFile)
    $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
    if ($process -and ($process.ProcessName -like "python*" -or $process.ProcessName -eq "dev_auth_stub")) {
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
    }
    Remove-Item -LiteralPath $pidFile -Force
}

# A PyInstaller one-file executable has a parent and extracted child process.
# Stop both, but only when they belong to this portable package.
Get-Process -Name "dev_auth_stub" -ErrorAction SilentlyContinue |
    Where-Object { $_.Path -eq $stubExe } |
    Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "Yoko RPA no-verify build stopped."
