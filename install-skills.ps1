# Install HarmonyOS Skills
# Copies skills to $HOME/.agents/skills and creates symlinks at $env:APPDATA/chrys/skills

$ErrorActionPreference = 'Stop'
$DebugPreference = 'Continue'

$scriptDir = $PSScriptRoot
$skillsDir = Join-Path $scriptDir "skills"
$targetDir = Join-Path $HOME ".agents/skills"
$linkDir = Join-Path $env:APPDATA "chrys/skills"

Write-Debug "scriptDir: $scriptDir"
Write-Debug "skillsDir: $skillsDir"
Write-Debug "targetDir: $targetDir"
Write-Debug "linkDir: $linkDir"

# Create target directory if not exists
if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    Write-Host "Created $targetDir"
} else {
    Write-Debug "Target directory already exists"
}

# Remove existing items in target (may be old symlinks or directories)
Get-ChildItem -Path $targetDir -Directory | ForEach-Object {
    Write-Debug "Removing existing: $($_.FullName)"
    Remove-Item $_.FullName -Recurse -Force
}

# Copy skills to target directory (override existing, exclude this script)
Write-Host "Copying skills to $targetDir ..."
$scriptName = Split-Path $scriptDir -Leaf
Get-ChildItem -Path $skillsDir -Directory | ForEach-Object {
    $src = $_.FullName
    $dst = Join-Path $targetDir $_.Name
    Write-Debug "Copying: $src -> $dst"
    Copy-Item -Path $src -Destination $dst -Recurse -Force
    Write-Debug "Copied: $($_.Name)"
}
Write-Host "Done."

# Create link directory if not exists
if (-not (Test-Path $linkDir)) {
    New-Item -ItemType Directory -Path $linkDir -Force | Out-Null
    Write-Host "Created $linkDir"
} else {
    Write-Debug "Link directory already exists"
}

# Create symlink for each skill
$skills = Get-ChildItem -Path $targetDir -Directory
foreach ($skill in $skills) {
    $linkPath = Join-Path $linkDir $skill.Name

    # Remove existing item (symlink or directory) if exists
    if (Test-Path $linkPath) {
        $item = Get-Item $linkPath
        if ($item.LinkType -eq 'SymbolicLink') {
            Remove-Item $linkPath -Force
            Write-Debug "Removed existing symlink: $linkPath"
        } else {
            Remove-Item $linkPath -Recurse -Force
            Write-Debug "Removed existing directory: $linkPath"
        }
    }

    try {
        New-Item -ItemType SymbolicLink -Path $linkPath -Target $skill.FullName -ErrorAction Stop | Out-Null
        Write-Debug "Linked: $linkPath -> $($skill.FullName)"
    } catch {
        # Fallback: use cmd mklink (may still require admin)
        $cmd = "mklink /D `"$linkPath`" `"$($skill.FullName)`""
        Write-Debug "PowerShell symlink failed, trying cmd mklink: $cmd"
        $output = cmd /c $cmd 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Debug "Linked via mklink: $linkPath -> $($skill.FullName)"
        } else {
            Write-Warning "Failed to create symlink for $($skill.Name). Try running as Administrator or enable Developer Mode."
            Write-Debug "mklink output: $output"
        }
    }
}

Write-Host "Installation complete."
