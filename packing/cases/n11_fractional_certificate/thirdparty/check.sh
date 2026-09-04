#!/bin/sh
# The whole check in one command, with whatever `python3` is on PATH:
# any CPython 3.8 or later, nothing installed, no project environment.
#
#     sh check.sh
#
# Exits non-zero if the control data does not match its published constants
# or if either certificate is refused. Expect about half a minute.
set -eu
cd "$(dirname "$0")"
python3 build_n17_control.py --check control-n17-massaccesi.json
python3 verify.py certificate.json
python3 verify.py control-n17-massaccesi.json
echo "check.sh: all three steps passed"
