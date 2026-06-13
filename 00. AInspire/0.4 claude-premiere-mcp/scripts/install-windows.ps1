#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($env:OS -ne "Windows_NT") {
    Write-Host "This installer supports Windows only."
    exit 1
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot = Split-Path -Parent $ScriptDir
$CepExtensionsDir = Join-Path $env:APPDATA "Adobe\CEP\extensions"
$CepTargetDir = Join-Path $CepExtensionsDir "MCPBridgeCEP"
$ClaudeConfigPath = Join-Path $env:APPDATA "Claude\claude_desktop_config.json"
$TempDir = Join-Path $env:TEMP "premiere-mcp-bridge"
$DistEntry = Join-Path $RepoRoot "dist\index.js"

# Check Node.js — skip Windows App Installer stubs that produce no output
$NodeCmd = $null
$candidates = @((Get-Command node -All -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source))
if (-not $candidates) {
    $candidates = @()
}
# Also check common install path in case PATH is missing it
$fallback = "C:\Program Files\nodejs\node.exe"
if (($candidates -notcontains $fallback) -and (Test-Path $fallback)) {
    $candidates += $fallback
}

foreach ($c in $candidates) {
    $ver = & "$c" -v 2>$null
    if ($ver) {
        $NodeCmd = $c
        break
    }
}

if (-not $NodeCmd) {
    Write-Host "Node.js 18+ is required but a working 'node' was not found."
    Write-Host "Hint: Windows App Installer stubs may shadow the real Node.js."
    Write-Host "Install Node.js from https://nodejs.org and ensure it is in your PATH."
    exit 1
}

# Use the verified node for all subsequent calls
Set-Alias -Name node -Value $NodeCmd -Scope Script
$NpmCmd = Join-Path (Split-Path $NodeCmd) "npm.cmd"
if (Test-Path $NpmCmd) {
    Set-Alias -Name npm -Value $NpmCmd -Scope Script
}

$NodeMajor = (node -p "process.versions.node.split('.')[0]").Trim()
if ([int]$NodeMajor -lt 18) {
    $NodeVersion = node -v
    Write-Host "Node.js 18+ is required. Found: $NodeVersion"
    exit 1
}

Write-Host "Using Node.js $(node -v) at $NodeCmd"

Write-Host "Installing npm dependencies..."
npm install --prefix "$RepoRoot"

Write-Host "Building MCP server..."
npm run build --prefix "$RepoRoot"

if (-not (Test-Path $DistEntry)) {
    Write-Host "Build completed but dist\index.js was not created."
    exit 1
}

Write-Host "Enabling Adobe CEP debug mode..."
foreach ($v in 10, 11, 12) {
    $keyPath = "HKCU:\Software\Adobe\CSXS.$v"
    if (-not (Test-Path $keyPath)) {
        New-Item -Path $keyPath -Force | Out-Null
    }
    Set-ItemProperty -Path $keyPath -Name "PlayerDebugMode" -Value "1" -Type String
}

Write-Host "Installing Premiere CEP extension..."
if (-not (Test-Path $CepExtensionsDir)) {
    New-Item -ItemType Directory -Path $CepExtensionsDir -Force | Out-Null
}
if (Test-Path $CepTargetDir) {
    Remove-Item -Recurse -Force $CepTargetDir
}
Copy-Item -Recurse -Force (Join-Path $RepoRoot "cep-plugin") $CepTargetDir

Write-Host "Preparing bridge temp directory..."
if (-not (Test-Path $TempDir)) {
    New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
}

Write-Host "Updating Claude Desktop config..."
$ClaudeConfigDir = Split-Path -Parent $ClaudeConfigPath
if (-not (Test-Path $ClaudeConfigDir)) {
    New-Item -ItemType Directory -Path $ClaudeConfigDir -Force | Out-Null
}

$env:CONFIG_PATH = $ClaudeConfigPath
$env:DIST_PATH = $DistEntry
$env:TEMP_PATH = $TempDir

$TmpScript = Join-Path $env:TEMP "premiere-mcp-config-update.js"
Set-Content -Path $TmpScript -Value @'
const fs = require("fs");

const configPath = process.env.CONFIG_PATH;
const distPath = process.env.DIST_PATH;
const tempPath = process.env.TEMP_PATH;

let data = {};

if (fs.existsSync(configPath)) {
  const raw = fs.readFileSync(configPath, "utf8").trim();
  if (raw) {
    try {
      data = JSON.parse(raw);
    } catch (error) {
      console.error("Claude Desktop config is not valid JSON: " + configPath);
      process.exit(1);
    }
  }
}

if (!data || typeof data !== "object" || Array.isArray(data)) {
  data = {};
}

if (!data.mcpServers || typeof data.mcpServers !== "object" || Array.isArray(data.mcpServers)) {
  data.mcpServers = {};
}

data.mcpServers["premiere-pro"] = {
  command: "node",
  args: [distPath],
  env: {
    PREMIERE_TEMP_DIR: tempPath
  }
};

fs.writeFileSync(configPath, JSON.stringify(data, null, 2) + "\n");
'@
node $TmpScript
Remove-Item $TmpScript -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "Install complete."
Write-Host "Next:"
Write-Host "1. Restart Claude Desktop."
Write-Host "2. Restart Premiere Pro."
Write-Host "3. Open Window > Extensions > MCP Bridge (CEP)."
Write-Host "4. Set Temp Directory to $TempDir."
Write-Host "5. Click Save Configuration, then Start Bridge, then Test Connection."
