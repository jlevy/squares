#!/bin/sh
# zm_mixed.py (ee3e2915, with mixed_cover.py bb89de15 and zeromargin.py 640fe453 copied from the retained evand
# packets, digests checked) on ONE cell, with verify.sh's flags: the published s(76) cover's record j054 is the
# source's; here the 199/200-scaled mutant, whose exact mu is 0.99978 at an admissible pose of that cell.
# One process, one worker, nice 10, a 15-minute limit.
cd /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneF
P=/home/user/squares/.claude/worktrees/review-76-95/packing/.venv/bin/python3
sha256sum zmcheck/zm_mixed.py zmcheck/mixed_cover.py zmcheck/zeromargin.py mut2/n76_scaled-199-200.txt
ZARGS="--d4 --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 24"
rm -f out/zm_control/n76_scaled-199-200_j054.jsonl
date -u +"start %FT%TZ"
timeout 900 nice -n 10 $P -I -u zmcheck/zm_mixed.py cert mut2/n76_scaled-199-200.txt $ZARGS --nproc 1 \
  --cx-lo 22/5 --cx-hi 89/20 --cy-lo 9/4 --cy-hi 23/10 --u-lo 5/16 --u-hi 11/32 \
  --resume out/zm_control/n76_scaled-199-200_j054.jsonl
echo "exit $?"
date -u +"end %FT%TZ"
