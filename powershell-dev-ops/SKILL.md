---
name: powershell-dev-ops
description: Conventions and defensive practices for PowerShell and Windows 11 DevOps automation, path handling, and CLI command execution
---

# PowerShell & Windows 11 Automation

## Environment Profile
- **Shell**: PowerShell 5.1 / PowerShell 7+ on Windows 11 Professional.
- **Username / Path**: User profile contains spaces (`C:\Users\Preferred Customer`). Always quote paths defensively.

## Core Rules

1. **Path Quoting & Splitting**:
   - Always quote paths containing variables or spaces: `"$HOME\Downloads\setup.exe"`.
   - Use `Join-Path` or forward slashes in cross-platform tools: `Join-Path $env:USERPROFILE "Downloads"`.

2. **No Bash Constructs**:
   - Never use Bash syntax: `export VAR=val`, `source .env`, `VAR=val command`, or `${VAR}` variable expansion inside nested commands.
   - In PowerShell, set environment variables via `$env:VAR = "value"`.

3. **PowerShell-Native Cmdlets**:
   - Directory navigation / inspection: `Get-ChildItem -Path ... -Recurse -Depth 2`
   - File tests: `Test-Path $Path`
   - Reading files: `Get-Content -Path $Path -Raw`
   - Writing files: `Set-Content -Path $Path -Value $Data` / `Out-File` with UTF8 encoding.
   - Spawning processes: `Start-Process -FilePath ... -ArgumentList ... -Wait`

4. **Error Handling**:
   - In automated scripts, set `$ErrorActionPreference = "Stop"` so failures do not silently continue.
   - Check `$LASTEXITCODE` immediately after running native executables.
