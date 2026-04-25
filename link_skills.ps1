$repoSkillRoot = Join-Path $PSScriptRoot 'skills'
$destinationRoots = @(
    (Join-Path (Join-Path $HOME '.claude') 'skills')
    (Join-Path (Join-Path $HOME '.agents') 'skills')
    (Join-Path (Join-Path $env:APPDATA 'chrys') 'skills')
)
$skillNames = @(
    'harmony-api'
    'harmony-arkts'
    'harmony-arkui'
    'harmony-cli'
    'harmony-template'
    'harmony-ut'
)

foreach ($destinationRoot in $destinationRoots) {
    foreach ($skillName in $skillNames) {
        $linkPath = Join-Path $destinationRoot $skillName
        if (Test-Path $linkPath) {
            Remove-Item $linkPath -Force
        }
        New-Item -ItemType SymbolicLink `
            -Path $linkPath `
            -Target (Join-Path $repoSkillRoot $skillName)
    }
}
