#!/bin/sh
# A local mutant of the s(76) cover: the D4 orbit of the heaviest piece the square at the hole's pose captures,
# removed (k2m5_review.py localmut).  Then zm_mixed.py with verify.sh's flags, depth limit 24, on the one cell that
# holds the pose (the source's record j054).  One process at a time, nice 10, a 10-minute limit.
# Usage: run_zm_local.sh WORK
. "$(dirname -- "$0")/common.sh"
zmcheck
mkdir -p mut outputs/zm_control
nice -n 10 "$PY" -I "$HERE/k2m5_review.py" localmut data/s76_cover_v5.txt 76 \
  --pose 364053/81920,11561/5120,21845/65536 --write mut/n76_local-j054.txt --out outputs/localmut-n76-j054.json > /dev/null
echo "localmut exit $?"
ZARGS="--d4 --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 24"
REG="--cx-lo 22/5 --cx-hi 89/20 --cy-lo 9/4 --cy-hi 23/10 --u-lo 5/16 --u-hi 11/32"
rm -f outputs/zm_control/n76_local-j054.jsonl
{ sha256sum zmcheck/zm_mixed.py zmcheck/mixed_cover.py zmcheck/zeromargin.py mut/n76_local-j054.txt; date -u +"start %FT%TZ"
  timeout 600 nice -n 10 "$PY" -I -u zmcheck/zm_mixed.py cert mut/n76_local-j054.txt $ZARGS --nproc 1 $REG --resume outputs/zm_control/n76_local-j054.jsonl
  echo "exit $?"; date -u +"end %FT%TZ"; } > outputs/zm_control/n76_local-j054.log 2>&1
tail -6 outputs/zm_control/n76_local-j054.log
