#!/bin/sh
# Independent exact-integer replay of certificate/n94_L9965.json.gz.
#   sh run.sh [DIRECTIONS]   DIRECTIONS: comma list (default: all 600, 0..599)
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
OUT="$HERE/_run"
mkdir -p "$OUT"
DIRS="${1:-$(python3 -c 'print(",".join(map(str,range(600))))')}"
gzip -dc "$HERE/../certificate/n94_L9965.json.gz" > "$OUT/cert.json"
python3 "$HERE/independent.py" "$OUT/cert.json" "$OUT/input.txt" "$DIRS" > "$OUT/premises.json"
${CXX:-c++} -std=c++17 -O3 -Wall -o "$OUT/intcheck" "$HERE/intcheck_final.cpp"
"$OUT/intcheck" "$OUT/input.txt" > "$OUT/result.jsonl"
python3 - "$OUT/result.jsonl" "$DIRS" <<'P'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1])]
want = sorted(map(int, sys.argv[2].split(',')))
got = sorted(r['r'] for r in rows)
ok = got == want and all(r['verdict'] == 'VERIFIED' for r in rows)
print(('VERIFIED' if ok else 'NOT VERIFIED'), len(rows), 'directions')
sys.exit(0 if ok else 1)
P
