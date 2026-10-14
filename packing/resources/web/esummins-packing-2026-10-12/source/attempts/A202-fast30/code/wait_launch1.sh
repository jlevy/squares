#!/bin/bash
# wait until fewer than 2 run202.py pythons are alive, then run shard 1 of 2
cd "$(dirname "$0")/../../.." || exit 1
sleep 20
count() { powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter 'Name=\"python.exe\"' | Where-Object { \$_.CommandLine -match 'run202[.]py' } | Measure-Object | Select-Object -ExpandProperty Count" | tr -d '\r '; }
while [ "$(count)" -ge 2 ]; do sleep 30; done
exec bash attempts/A202-fast30/code/run202.sh 1 2 600
