$ErrorActionPreference = "Stop"

$pyinstaller = Join-Path $PSScriptRoot ".venv\Scripts\pyinstaller.exe"
if (-not (Test-Path $pyinstaller)) {
    $pyinstaller = "pyinstaller"
}

& $pyinstaller --clean --noconfirm "$PSScriptRoot\scoreboard.spec"
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller build failed with exit code $LASTEXITCODE."
}
