#!/bin/sh
# Every k2m5_review.py output of the review, and corner_scan.py's, from the final program,
# one process at a time under nice 10.  Usage: run_all_final.sh WORK
# WORK is a scratch directory outside the checkout; the outputs go to WORK/outputs, the
# mutated covers to WORK/mut (the other run scripts read them there).  At the end each
# output is compared with the kept one in review/outputs/, ignoring wall_s and cpu_s.
. "$(dirname -- "$0")/common.sh"
O=outputs; rm -rf mut; mkdir -p mut tiling-work
R() { echo "== $* ($(date -u +%T))"; nice -n 10 "$PY" -I "$HERE/k2m5_review.py" "$@" > /dev/null; echo "exit $?"; }
R cover data/s76_cover_v5.txt 76 --out $O/cover-n76.json
R cover data/s95_cover_v2.txt 95 --out $O/cover-n95.json
R records "$K76" 76 --out $O/records-n76.json
R records "$K95" 95 --out $O/records-n95.json
PO="--count 3000 --per-root 200 --per-box 10 --fold-count 1500 --per-germ 60 --descents 10 --descent-steps 80"
R poses data/s76_cover_v5.txt 76 "$K76" $PO --out $O/poses-n76.json
R poses data/s95_cover_v2.txt 95 "$K95" $PO --out $O/poses-n95.json
# LP76 and LP95: the descent_min pose of each poses output.
LP76=$("$PY" -I -c "import json; print(','.join(json.load(open('$O/poses-n76.json'))['descent_min']['pose']))")
LP95=$("$PY" -I -c "import json; print(','.join(json.load(open('$O/poses-n95.json'))['descent_min']['pose']))")
R mutants data/s76_cover_v5.txt 76 --low-pose "$LP76" --scale 999/1000 --write-mutants mut --out $O/mutants-n76.json
R mutants data/s95_cover_v2.txt 95 --low-pose "$LP95" --scale 249/250 --write-mutants mut --out $O/mutants-n95.json
R mutants data/s76_cover_v5.txt 76 --low-pose 364053/81920,11561/5120,21845/65536 --scale 199/200 --write-mutants mut --out $O/mutants-n76-scaled-199-200.json
R cellmin data/s76_cover_v5.txt 76 --box 22/5,89/20,9/4,23/10,5/16,11/32 --threshold 1.00483 --out $O/cellmin-n76-j054.json
# tiling runs the author's tools/check_coverage.py from the retained copy, with -I.
R tiling "$K76" 76 "$K76/s76-certificate/tools/check_coverage.py" --python "$PY" --work tiling-work --out $O/tiling-n76.json
R tiling "$K95" 95 "$K95/s95-certificate/tools/check_coverage.py" --python "$PY" --work tiling-work --out $O/tiling-n95.json
echo "== corner_scan ($(date -u +%T))"
nice -n 10 "$PY" -I "$HERE/corner_scan.py" data/s76_cover_v5.txt "$K76/s76-certificate/records/zmx2/zmx2_v5.log.gz" 8010 > $O/corner_scan-n76-root8010.txt; echo "exit $?"
cmp -s $O/corner_scan-n76-root8010.txt "$REVIEW/outputs/corner_scan-n76-root8010.txt" && echo "same as kept: corner_scan-n76-root8010.txt" || echo "DIFFERS: corner_scan-n76-root8010.txt"
"$PY" -I - "$REVIEW/outputs" $O <<'PYEOF'
import json, os, sys
kept, new = sys.argv[1], sys.argv[2]
def leaves(x, path=''):
    if isinstance(x, dict):
        for k, v in x.items():
            if k not in ('wall_s', 'cpu_s'):
                yield from leaves(v, f'{path}.{k}')
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, f'{path}[{i}]')
    else:
        yield path, x
for name in sorted(os.listdir(new)):
    if not name.endswith('.json'):
        continue
    a = dict(leaves(json.load(open(os.path.join(kept, name)))))
    b = dict(leaves(json.load(open(os.path.join(new, name)))))
    diff = sorted(k for k in a.keys() | b.keys() if a.get(k) != b.get(k))
    print(f'{name}: ' + ('same as kept, apart from wall_s and cpu_s' if not diff else 'differs in ' + ', '.join(diff)))
PYEOF
date -u +"done %T"
