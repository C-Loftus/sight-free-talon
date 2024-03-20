# Used for testing the addon in NVDA and quickly updating the addon

Set-Location $PSScriptRoot

Copy-Item ".\addon\globalPlugins\nvda-addon.py" -Destination "$env:APPDATA\nvda\scratchpad\globalPlugins\sight-free-talon-server-tmp.py"

Write-Host "Copied addon to $env:APPDATA\nvda\scratchpad\globalPlugins\sight-free-talon-server-tmp.py"