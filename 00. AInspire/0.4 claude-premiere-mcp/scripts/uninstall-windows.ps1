#Requires -Version 5.1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($env:OS -ne "Windows_NT") {
    Write-Host "This uninstaller supports Windows only."
    exit 1
}

$CepTargetDir = Join-Path $env:APPDATA "Adobe\CEP\extensions\MCPBridgeCEP"
$ClaudeConfigPath = Join-Path $env:APPDATA "Claude\claude_desktop_config.json"
$TempDir = Join-Path $env:TEMP "premiere-mcp-bridge"

# Find a working node — skip Windows App Installer stubs
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
}

Write-Host "Removing Premiere CEP extension..."
if (Test-Path $CepTargetDir) {
    Remove-Item -Recurse -Force $CepTargetDir
}

Write-Host "Removing bridge temp directory..."
if (Test-Path $TempDir) {
    Remove-Item -Recurse -Force $TempDir
}

if (Test-Path $ClaudeConfigPath) {
    Write-Host "Removing Claude Desktop config entry..."
    $env:CONFIG_PATH = $ClaudeConfigPath
    $TmpScript = Join-Path $env:TEMP "premiere-mcp-config-remove.js"
    Set-Content -Path $TmpScript -Value @'
const fs = require("fs");

const configPath = process.env.CONFIG_PATH;
let data = {};

const raw = fs.readFileSync(configPath, "utf8").trim();
if (raw) {
  try {
    data = JSON.parse(raw);
  } catch (error) {
    console.error("Claude Desktop config is not valid JSON: " + configPath);
    process.exit(1);
  }
}

if (data && typeof data === "object" && !Array.isArray(data) && data.mcpServers && typeof data.mcpServers === "object" && !Array.isArray(data.mcpServers)) {
  delete data.mcpServers["premiere-pro"];
}

fs.writeFileSync(configPath, JSON.stringify(data, null, 2) + "\n");
'@
    node $TmpScript
    Remove-Item $TmpScript -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "Uninstall complete."
Write-Host "Note: Adobe CEP debug mode remains enabled so other CEP plugins keep working."
