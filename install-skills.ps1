# Install HarmonyOS Skills
# Copies skills to $HOME/.agents/skills and creates symlinks at $env:APPDATA/chrys/skills

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
if (-not (Test-Path $linkDir)) {
    New-Item -ItemType Directory -Path $linkDir -Force | Out-Null
    Write-Host "Created $linkDir"
}

# Create symlink for each skill
$skills = Get-ChildItem -Path $targetDir -Directory
foreach ($skill in $skills) {
    $linkPath = Join-Path $linkDir $skill.Name

    # Remove existing item (symlink or directory) if exists
    if (Test-Path $linkPath) {
        Remove-Item $linkPath -Force
        Write-Host "Removed existing: $linkPath"
    }

    New-Item -ItemType SymbolicLink -Path $linkPath -Target $skill.FullName | Out-Null
    Write-Host "Linked: $linkPath -> $($skill.FullName)"
}

Write-Host "Installation complete."
