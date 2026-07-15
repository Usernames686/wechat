param(
    [string]$Agent = "dev",
    [string]$Password = "dev",
    [int]$AuthPort = 19922
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$exe = Join-Path $root "yoko_rpa_mcp.exe"
$stub = Join-Path $root "dev_auth_stub.py"
$stubExe = Join-Path $root "dev_auth_stub.exe"
$pidFile = Join-Path $env:TEMP "yoko-dev-auth.pid"
$baseUrl = "http://127.0.0.1:$AuthPort"

if (-not (Test-Path -LiteralPath $exe)) {
    throw "Missing executable: $exe"
}

$env:YOKO_DEV_AGENT = $Agent
$env:YOKO_DEV_PASSWORD = $Password
$env:YOKO_DEV_AUTH_PORT = [string]$AuthPort
$env:YOKO_API_BASE = $baseUrl
$env:SUPABASE_URL = $baseUrl
$env:SUPABASE_KEY = "local.development.key"
$env:YOKO_RPA_TOKEN = "local-development-token"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"

$oldProcesses = Get-CimInstance Win32_Process -Filter "Name='yoko_rpa_mcp.exe'"
if ($oldProcesses) {
    $controlPort = Get-NetTCPConnection -LocalAddress "127.0.0.1" -LocalPort 9921 -State Listen -ErrorAction SilentlyContinue
    if ($controlPort) {
        try {
            Invoke-RestMethod -Uri "http://127.0.0.1:9921/shutdown" -Method Post -TimeoutSec 5 | Out-Null
        } catch {
            Write-Warning "Graceful shutdown failed; stale processes will be cleaned up."
        }
    }

    foreach ($attempt in 1..50) {
        $oldProcesses = Get-CimInstance Win32_Process -Filter "Name='yoko_rpa_mcp.exe'"
        if (-not $oldProcesses) {
            break
        }
        Start-Sleep -Milliseconds 200
    }

    if ($oldProcesses) {
        $oldProcesses | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
    }
}

foreach ($attempt in 1..50) {
    $occupiedPorts = Get-NetTCPConnection -LocalPort 9921,9922 -State Listen -ErrorAction SilentlyContinue
    if (-not $occupiedPorts) {
        break
    }
    Start-Sleep -Milliseconds 200
}
if ($occupiedPorts) {
    throw "Yoko RPA did not release its local ports."
}

$existing = Get-NetTCPConnection -LocalAddress "127.0.0.1" -LocalPort $AuthPort -State Listen -ErrorAction SilentlyContinue
if (-not $existing) {
    if (Test-Path -LiteralPath $stubExe) {
        $stubProcess = Start-Process -FilePath $stubExe -WindowStyle Hidden -PassThru
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        $stubProcess = Start-Process python -ArgumentList @("`"$stub`"") -WindowStyle Hidden -PassThru
    } else {
        throw "Missing local authentication component: $stubExe"
    }
    Set-Content -LiteralPath $pidFile -Value $stubProcess.Id -Encoding ascii

    $ready = $false
    foreach ($attempt in 1..30) {
        try {
            $health = Invoke-RestMethod -Uri "$baseUrl/health" -TimeoutSec 1
            if ($health.ok) {
                $ready = $true
                break
            }
        } catch {
            Start-Sleep -Milliseconds 200
        }
    }
    if (-not $ready) {
        throw "Local development auth fixture did not become ready on $baseUrl"
    }
}

$rpaProcess = Start-Process -FilePath $exe -ArgumentList @("--supervisor", "--no-ui") -PassThru
$serviceReady = $false
foreach ($attempt in 1..200) {
    if ($rpaProcess.HasExited) {
        throw "Yoko RPA exited during development startup with code $($rpaProcess.ExitCode)."
    }
    try {
        $serviceHealth = Invoke-RestMethod -Uri "http://127.0.0.1:9922/api/health" -TimeoutSec 1
        if ($serviceHealth.status -eq "ok") {
            $serviceReady = $true
            break
        }
    } catch {
        Start-Sleep -Milliseconds 300
    }
}
if (-not $serviceReady) {
    throw "Yoko RPA did not become healthy on port 9922."
}

$license = Invoke-RestMethod -Uri "http://127.0.0.1:9922/api/license/verify" -Headers @{ "X-API-Key" = "yoko_test" } -TimeoutSec 10
if (-not $license.valid) {
    throw "Development license verification failed: $($license.message)"
}

Write-Host "Yoko RPA no-verify build started."
Write-Host "Console: http://127.0.0.1:9922/"
Write-Host "Development account: $Agent"
$mcpTokenFile = Join-Path $HOME ".yokowebot\mcp_token.dat"
if (Test-Path -LiteralPath $mcpTokenFile) {
    $mcpToken = (Get-Content -LiteralPath $mcpTokenFile -Raw).Trim()
    Write-Host "MCP endpoint: http://127.0.0.1:9922/mcp"
    Write-Host "MCP token: $mcpToken"
}
Write-Host "Stop build: $root\stop_noverify.ps1"
Start-Process "http://127.0.0.1:9922/"
