# A214 -- build the C kernel DLL (one command).  Usage:  powershell -File code\build214.ps1
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$out  = Join-Path $here "..\build\ckernel214.dll"
$clang = "C:\Program Files\LLVM\bin\clang.exe"
New-Item -ItemType Directory -Force (Join-Path $here "..\build") | Out-Null
& $clang -O2 -shared -nostdlib -Wl,-noentry -ffp-contract=off -fno-fast-math -Wall -Wextra -std=c11 -o $out (Join-Path $here "ckernel214.c")
if ($LASTEXITCODE -ne 0) { throw "clang failed" }
Remove-Item -Force -ErrorAction SilentlyContinue (Join-Path $here "..uild\ckernel214.lib"), (Join-Path $here "..uild\ckernel214.exp")
$h = (Get-FileHash -Algorithm SHA256 $out).Hash.ToLower()
"$h  ckernel214.dll" | Out-File -Encoding ascii (Join-Path $here "..\build\ckernel214.dll.sha256")
Write-Output "built $out  sha256 $h"
