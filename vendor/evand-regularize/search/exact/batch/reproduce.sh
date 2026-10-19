#!/usr/bin/env bash
# Re-solve every input with exactsolve.py and check that the regenerated certificate equals the shipped one.
#   ./reproduce.sh [-j JOBS] [n ...]      (default: all inputs, JOBS = 8; ~1-2 CPU-hours for all 321)
# Needs python3 with numpy, scipy, mpmath.  Outputs go to a temporary directory.
set -u
cd "$(dirname "$0")"
J=8
if [ "${1:-}" = "-j" ]; then J=$2; shift 2; fi
if [ $# -gt 0 ]; then L=$(printf 'inputs/n-%s.txt\n' "$@"); else L=$(ls inputs/n-*.txt); fi
OUT=$(mktemp -d)
echo "$L" | xargs -P "$J" -I{} sh -c 'f={}; b=$(basename "$f" .txt); python3 ../exactsolve.py "$f" --out "'"$OUT"'" -q > /dev/null 2>&1;
  if cmp -s "'"$OUT"'/$b.cert" "certs/$b.cert"; then echo "$b same"; else echo "$b DIFFERENT"; fi'
echo "outputs in $OUT"
