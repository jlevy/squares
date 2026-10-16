#!/bin/sh
# The same cell as run_zm_control.sh, at a depth limit of 12 instead of 24, for the published s(76) cover and for
# the 199/200-scaled mutant: equal settings for both, so the pair is a control.  The published cover's own record
# for this cell (j054) reached depth 9.  One process at a time, one worker, nice 10, a 10-minute limit each.
# Usage: run_zm_control_d12.sh WORK; run run_all_final.sh with the same WORK first (it writes the mutant).
. "$(dirname -- "$0")/common.sh"
need mut/n76_scaled-199-200.txt run_all_final.sh
zmcheck
mkdir -p outputs/zm_control
ZARGS="--d4 --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 12"
REG="--cx-lo 22/5 --cx-hi 89/20 --cy-lo 9/4 --cy-hi 23/10 --u-lo 5/16 --u-hi 11/32"
for c in data/s76_cover_v5.txt mut/n76_scaled-199-200.txt; do
  t=$(basename $c .txt)
  rm -f outputs/zm_control/${t}_j054_depth12.jsonl
  { sha256sum zmcheck/zm_mixed.py zmcheck/mixed_cover.py zmcheck/zeromargin.py $c; date -u +"start %FT%TZ"
    timeout 600 nice -n 10 "$PY" -I -u zmcheck/zm_mixed.py cert $c $ZARGS --nproc 1 $REG --resume outputs/zm_control/${t}_j054_depth12.jsonl
    echo "exit $?"; date -u +"end %FT%TZ"; } > outputs/zm_control/${t}_j054_depth12.log 2>&1
  tail -4 outputs/zm_control/${t}_j054_depth12.log
done
