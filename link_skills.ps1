$repoSkillRoot = Join-Path $PSScriptRoot 'skills'
$destinationRoots = @(
    (Join-Path (Join-Path $HOME '.claude') 'skills')
    (Join-Path (Join-Path $HOME '.agents') 'skills')
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
        New-Item -ItemType SymbolicLink `
            -Path (Join-Path $destinationRoot $skillName) `
            -Target (Join-Path $repoSkillRoot $skillName)
    }
}
