#!/bin/bash
# Build both pages into a scratch directory and move them out, checking that the record is untouched.
set -euo pipefail
HERE=/private/tmp/claude-502/-Users-levy-wrk-github-squares--claude-worktrees-squares-viz-explanations-4ae624/2c8216fa-fd2c-40bc-9fb8-344ac609e3c3/scratchpad/spike-v2-transitions
PY=/Users/levy/wrk/github/squares/.claude/worktrees/squares-viz-explanations-4ae624/packing/.venv/bin/python3
OUT="$HERE/build-tmp/run"
rm -rf "$OUT"
cd "$HERE"
OPENBLAS_NUM_THREADS=1 "$PY" build_candidate.py --all --out "$OUT" 2>&1 | tail -4
cmp "$OUT/transition-stats.json" "$HERE/transition-stats.json" && echo "record unchanged"
mv -f "$OUT/index.html" "$HERE/index.html"
mv -f "$OUT/index-all.html" "$HERE/index-all.html"
mv -f "$OUT/workbench.html" "$HERE/workbench.html"
rm -rf "$OUT"
ls -l "$HERE/index.html" "$HERE/index-all.html" "$HERE/workbench.html" | awk '{print $9, $5}'
