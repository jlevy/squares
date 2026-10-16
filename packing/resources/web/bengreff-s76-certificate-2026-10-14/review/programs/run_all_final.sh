#!/bin/sh
# Every k2m5_review.py output of the review, from the final program, one process at a time, nice 10.
# Paths: the covers unpacked into data/, the packets in the review worktree.
cd /tmp/claude-0/-home-user/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/laneF
P=~/.local/bin/python3.14
W=/home/user/squares/.claude/worktrees/review-76-95/packing/resources/web
K76=$W/bengreff-s76-certificate-2026-10-14; K95=$W/bengreff-s95-certificate-2026-10-15
O=final; mkdir -p $O; rm -rf mutf; mkdir mutf
R() { echo "== $* ($(date -u +%T))"; nice -n 10 $P -I prog/k2m5_review.py "$@" > /dev/null; echo "exit $?"; }
R cover data/s76_cover_v5.txt 76 --out $O/cover-n76.json
R cover data/s95_cover_v2.txt 95 --out $O/cover-n95.json
R records $K76 76 --out $O/records-n76.json
R records $K95 95 --out $O/records-n95.json
PO="--count 3000 --per-root 200 --per-box 10 --fold-count 1500 --per-germ 60 --descents 10 --descent-steps 80"
R poses data/s76_cover_v5.txt 76 $K76 $PO --out $O/poses-n76.json
R poses data/s95_cover_v2.txt 95 $K95 $PO --out $O/poses-n95.json
LP76=$(python3 -c "import json; print(','.join(json.load(open('$O/poses-n76.json'))['descent_min']['pose']))")
LP95=$(python3 -c "import json; print(','.join(json.load(open('$O/poses-n95.json'))['descent_min']['pose']))")
R mutants data/s76_cover_v5.txt 76 --low-pose "$LP76" --scale 999/1000 --write-mutants mutf --out $O/mutants-n76.json
R mutants data/s95_cover_v2.txt 95 --low-pose "$LP95" --scale 249/250 --write-mutants mutf --out $O/mutants-n95.json
R mutants data/s76_cover_v5.txt 76 --low-pose 364053/81920,11561/5120,21845/65536 --scale 199/200 --write-mutants mutf --out $O/mutants-n76-scaled-199-200.json
R cellmin data/s76_cover_v5.txt 76 --box 22/5,89/20,9/4,23/10,5/16,11/32 --threshold 1.00483 --out $O/cellmin-n76-j054.json
R tiling $K76 76 $K76/s76-certificate/tools/check_coverage.py --python $P --out $O/tiling-n76.json
R tiling $K95 95 $K95/s95-certificate/tools/check_coverage.py --python $P --out $O/tiling-n95.json
echo "== corner_scan ($(date -u +%T))"
nice -n 10 $P prog/corner_scan.py data/s76_cover_v5.txt $K76/s76-certificate/records/zmx2/zmx2_v5.log.gz 8010 > $O/corner_scan-n76-root8010.txt; echo "exit $?"
for f in mut/*.txt mut2/n76_scaled-199-200.txt; do cmp -s $f mutf/$(basename $f) && echo "same bytes: $(basename $f)" || echo "DIFFERS: $f"; done
date -u +"done %T"
