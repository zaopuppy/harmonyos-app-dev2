# HarmonyOS Dev Environment Setup
# Source this script before using hdc, hvigorw, or ohpm
# Usage: . ./setup_env.ps1  (note the leading dot)

# Derive DEVECO_SDK_HOME from hdc if not set
if (-not $env:DEVECO_SDK_HOME) {
    $hdcCmd = Get-Command hdc -ErrorAction SilentlyContinue
    if ($hdcCmd) {
        $hdcPath = $hdcCmd.Source
        # hdc is at $DEVECO_SDK_HOME/default/openharmony/toolchains/hdc.exe
        $env:DEVECO_SDK_HOME = Split-Path (Split-Path (Split-Path (Split-Path (Split-Path $hdcPath -Parent) -Parent) -Parent) -Parent) -Parent
        Write-Host "DEVECO_SDK_HOME derived from hdc: $env:DEVECO_SDK_HOME"
    } else {
        Write-Host "DEVECO_SDK_HOME not set and hdc not found in PATH"
        return 1
    }
}

# Set DEVECO_HOME (parent of SDK root)
$env:DEVECO_HOME = Split-Path $env:DEVECO_SDK_HOME -Parent
$env:PATH = "$env:DEVECO_SDK_HOME\default\openharmony\toolchains;$env:DEVECO_HOME\tools\node;$env:DEVECO_HOME\tools\ohpm\bin;$env:DEVECO_HOME\tools\hvigor\bin;$env:PATH"

Write-Host "Environment configured:"
Write-Host "  DEVECO_SDK_HOME=$env:DEVECO_SDK_HOME"
Write-Host "  DEVECO_HOME=$env:DEVECO_HOME"
Write-Host "  PATH updated"
