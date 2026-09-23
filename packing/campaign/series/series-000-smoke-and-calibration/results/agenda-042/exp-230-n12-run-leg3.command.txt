#!/bin/bash
cd /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/packing
date -u +%FT%TZ > /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/attic/agenda-042-lown/n12/leg3-started.txt
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
time uv run --frozen --all-extras --group dev python -m devtools.run_fractional_cutting \
  --n 12 --side 39609/10000 --shrink 9977/10000 \
  --angle-limit 207107/500000 --steps 180 \
  --minutes 45 --iterations 40 --cap 150 --support-cap 96 \
  --rows-rounds 2 --rows-per-direction 3 --stop-on-covering-below-n \
  --warm /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/attic/agenda-042-lown/n12/leg2-state.json \
  --log /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/attic/agenda-042-lown/n12/leg3.log --state /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/attic/agenda-042-lown/n12/leg3-state.json \
  --freeze /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/attic/agenda-042-lown/n12/leg3-family.json --json /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/attic/agenda-042-lown/n12/leg3-summary.json
date -u +%FT%TZ > /Users/levy/wrk/github/squares/.claude/worktrees/w3-review/attic/agenda-042-lown/n12/leg3-ended.txt
