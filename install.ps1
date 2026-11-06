# Install the Claude Code status line into ~/.claude (Windows).
# Run: powershell -NoProfile -ExecutionPolicy Bypass -File install.ps1

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$dest = Join-Path $HOME '.claude'

# Find a real Python 3.8+ (skip the Microsoft Store stub in WindowsApps)
$py = $null
foreach ($name in 'python', 'python3', 'py') {
    foreach ($cmd in @(Get-Command $name -All -CommandType Application -ErrorAction SilentlyContinue)) {
        if ($cmd.Source -like '*\WindowsApps\*') { continue }
        & $cmd.Source -c 'import sys; sys.exit(sys.version_info < (3, 8))' 2>$null
        if ($LASTEXITCODE -eq 0) { $py = $cmd.Source; break }
    }
    if ($py) { break }
}
if (-not $py) {
    Write-Error 'Python 3.8+ not found - install it from python.org (or winget install Python.Python.3.13), then rerun'
    exit 1
}

New-Item -ItemType Directory -Force $dest | Out-Null
Copy-Item (Join-Path $here 'statusline.py') $dest -Force

# Forward slashes: Claude Code runs the command through Git Bash when installed,
# which would eat backslashes (see the Windows section of the statusline docs)
$script = (Join-Path $dest 'statusline.py') -replace '\\', '/'
$command = ($py -replace '\\', '/') + ' ' + $script
if ($command.Split(' ').Count -gt 2) {
    Write-Warning "Path contains spaces - check the statusLine command in $dest\settings.json"
}

& $py (Join-Path $here 'merge_settings.py') (Join-Path $dest 'settings.json') $command
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'done - the status line appears on the next Claude Code refresh'
