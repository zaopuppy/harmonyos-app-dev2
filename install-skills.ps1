# Install HarmonyOS Skills
# Copies skills to $HOME/.agents/skills and creates symlink at $APPDATA/chrys/skills

$ErrorActionPreference = 'Stop'

$scriptDir = $PSScriptRoot
$skillsDir = Join-Path $scriptDir "skills"
$targetDir = Join-Path $HOME ".agents/skills"
$linkDir = Join-Path $env:APPDATA "chrys/skills"

# Create target directory if not exists
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    Write-Host "Created $targetDir"
}

# Copy skills to target directory (override existing)
Write-Host "Copying skills to $targetDir ..."
Copy-Item -Path "$skillsDir/*" -Destination $targetDir -Recurse -Force
Write-Host "Done."

# Create link directory if not exists
$linkParent = Split-Path $linkDir -Parent
if (-not (Test-Path $linkParent)) {
    New-Item -ItemType Directory -Path $linkParent -Force | Out-Null
    Write-Host "Created $linkParent"
}

# Remove existing link if exists
if (Test-Path $linkDir) {
    $item = Get-Item $linkDir
    if ($item.LinkType -eq 'SymbolicLink') {
        Remove-Item $linkDir -Force
        Write-Host "Removed existing symlink at $linkDir"
    } else {
        Remove-Item $linkDir -Recurse -Force
        Write-Host "Removed existing directory at $linkDir"
    }
}

# Create symlink
New-Item -ItemType SymbolicLink -Path $linkDir -Target $targetDir | Out-Null
Write-Host "Created symlink: $linkDir -> $targetDir"
Write-Host "Installation complete."
