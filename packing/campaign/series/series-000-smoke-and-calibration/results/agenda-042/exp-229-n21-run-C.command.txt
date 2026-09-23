#!/bin/bash
cd /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/packing
date -u +%FT%TZ > /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/attic/agenda-042-lown/n21/C-started.txt
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
time uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 21 --side 122/25 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 80 --deadline-seconds 2700 \
  --seed-windows 0 \
  --freeze /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/attic/agenda-042-lown/n21/C-covering.json --freeze-family /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/attic/agenda-042-lown/n21/C-family.json \
  --json /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/attic/agenda-042-lown/n21/C-run.json --row-log /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/attic/agenda-042-lown/n21/C-rows.jsonl --log /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/attic/agenda-042-lown/n21/C.log
date -u +%FT%TZ > /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/attic/agenda-042-lown/n21/C-ended.txt
