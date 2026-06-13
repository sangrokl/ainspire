#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

if ($env:OS -ne "Windows_NT") {
    Write-Host "This doctor command supports Windows only."
    exit 1
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot = Split-Path -Parent $ScriptDir
$DistEntry = Join-Path $RepoRoot "dist\index.js"
$CepTargetDir = Join-Path $env:APPDATA "Adobe\CEP\extensions\MCPBridgeCEP"
$ClaudeConfigPath = Join-Path $env:APPDATA "Claude\claude_desktop_config.json"
$TempDir = Join-Path $env:TEMP "premiere-mcp-bridge"
$Failures = 0

function Pass($msg) { Write-Host "[ok] $msg" }
function Fail($msg) { Write-Host "[missing] $msg"; $script:Failures++ }
function Info($msg) { Write-Host "[info] $msg" }

# Node.js check — skip Windows App Installer stubs
$NodeCmd = $null
$candidates = @((Get-Command node -All -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source))
if (-not $candidates) { $candidates = @() }
$fallback = "C:\Program Files\nodejs\node.exe"
if (($candidates -notcontains $fallback) -and (Test-Path $fallback)) {
    $candidates += $fallback
}
foreach ($c in $candidates) {
    $ver = & "$c" -v 2>$null
    if ($ver) { $NodeCmd = $c; break }
}

if ($NodeCmd) {
    Set-Alias -Name node -Value $NodeCmd -Scope Script
    $NodeVersion = node -v
    $NodeMajor = (node -p "process.versions.node.split('.')[0]").Trim()
    if ([int]$NodeMajor -ge 18) {
        Pass "Node.js available ($NodeVersion) at $NodeCmd"
    } else {
        Fail "Node.js 18+ required (found $NodeVersion)"
    }
} else {
    Fail "Node.js not found (Windows App Installer stubs may shadow real Node.js)"
}

# Build output
if (Test-Path $DistEntry) {
    Pass "Built MCP server found at $DistEntry"
} else {
    Fail "Build output missing at $DistEntry (run npm run build)"
}

# CEP extension
if (Test-Path $CepTargetDir) {
    $manifest = Join-Path $CepTargetDir "CSXS\manifest.xml"
    $index = Join-Path $CepTargetDir "index.html"
    if ((Test-Path $manifest) -and (Test-Path $index)) {
        Pass "Premiere CEP extension installed at $CepTargetDir"
    } else {
        Fail "CEP extension folder exists but is incomplete at $CepTargetDir"
    }
} else {
    Fail "Premiere CEP extension not installed at $CepTargetDir"
}

# Temp directory
if (Test-Path $TempDir) {
    Pass "Bridge temp directory exists at $TempDir"
} else {
    Fail "Bridge temp directory missing at $TempDir"
}

# CEP debug mode registry
foreach ($v in 12, 11, 10) {
    $keyPath = "HKCU:\Software\Adobe\CSXS.$v"
    try {
        $value = Get-ItemPropertyValue -Path $keyPath -Name "PlayerDebugMode" -ErrorAction Stop
        if ($value -eq 1) {
            Pass "Adobe CEP debug mode enabled for CSXS.$v"
        } else {
            Fail "Adobe CEP debug mode not enabled for CSXS.$v"
        }
    } catch {
        Fail "Adobe CEP debug mode not enabled for CSXS.$v"
    }
}

# Claude Desktop config
if (Test-Path $ClaudeConfigPath) {
    $env:CONFIG_PATH = $ClaudeConfigPath
    $env:DIST_PATH = $DistEntry
    $env:TEMP_PATH = $TempDir
    $TmpScript = Join-Path $env:TEMP "premiere-mcp-config-check.js"
    Set-Content -Path $TmpScript -Value @'
const fs = require("fs");

const configPath = process.env.CONFIG_PATH;
const distPath = process.env.DIST_PATH;
const tempPath = process.env.TEMP_PATH;

try {
  const raw = fs.readFileSync(configPath, "utf8");
  const data = JSON.parse(raw);
  const server = data && data.mcpServers && data.mcpServers["premiere-pro"];

  if (!server) {
    console.log("missing-server");
    process.exit(0);
  }

  const arg0 = Array.isArray(server.args) ? server.args[0] : "";
  const temp = server.env && server.env.PREMIERE_TEMP_DIR;

  if (server.command !== "node") {
    console.log("bad-command:" + (server.command || ""));
  } else if (arg0 !== distPath) {
    console.log("bad-path:" + arg0);
  } else if (temp !== tempPath) {
    console.log("bad-temp:" + (temp || ""));
  } else {
    console.log("ok");
  }
} catch (error) {
  console.log("invalid-json:" + error.message);
}
'@
    $ConfigCheck = (node $TmpScript 2>$null) | Select-Object -First 1
    Remove-Item $TmpScript -ErrorAction SilentlyContinue

    switch -Wildcard ($ConfigCheck) {
        "ok" { Pass "Claude Desktop config contains a valid premiere-pro entry" }
        "missing-server" { Fail "Claude Desktop config is present but missing the premiere-pro entry" }
        "bad-command:*" { Fail "Claude Desktop config has a premiere-pro entry with the wrong command ($($ConfigCheck -replace '^bad-command:',''))" }
        "bad-path:*" { Fail "Claude Desktop config points to the wrong dist path ($($ConfigCheck -replace '^bad-path:',''))" }
        "bad-temp:*" { Fail "Claude Desktop config points to the wrong temp dir ($($ConfigCheck -replace '^bad-temp:',''))" }
        "invalid-json:*" { Fail "Claude Desktop config is not valid JSON" }
        default { Fail "Claude Desktop config check returned an unexpected result: $ConfigCheck" }
    }
} else {
    Fail "Claude Desktop config not found at $ClaudeConfigPath"
}

Info "Premiere panel check must still be done manually inside Premiere Pro."
Info "Open Window > Extensions > MCP Bridge (CEP), then click Test Connection."

if ($Failures -gt 0) {
    Write-Host ""
    Write-Host "Doctor found $Failures issue(s)."
    exit 1
}

Write-Host ""
Write-Host "Doctor check passed."
