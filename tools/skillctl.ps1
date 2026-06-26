$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$scriptDir;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $scriptDir
}
if (-not $env:PYTHON) {
    $env:PYTHON = "python"
}
& $env:PYTHON -m skillforge.cli @args

