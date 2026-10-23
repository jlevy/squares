#!/bin/sh
# Reproduce the n = 40 examples: two claims (VERIFIED) and their controls (REFUSED).
#   sh run.sh OUT_DIR [THREADS]
# Needs the release build of ../../sqverify_fast and network access for prepare.py.
set -u
out=${1:?usage: run.sh OUT_DIR [THREADS]}
threads=${2:-4}
here=$(cd "$(dirname "$0")" && pwd)
bin="$here/../../sqverify_fast/target/release/sqverify-fast"
mkdir -p "$out"
python3 "$here/prepare.py" "$out" || exit 2
status=0
check() {  # label candidate core expected
  "$bin" --candidate "$out/$2.json" --n 40 --continuous --core "$3" --tau 4999/5000 \
    --threads "$threads" --max-nodes 30000000 > "$out/$1.jsonl" 2> "$out/$1.log"
  got=$(tail -n 1 "$out/$1.jsonl" | python3 -c 'import json,sys; print(json.loads(sys.stdin.read())["status"])')
  echo "$1: $got (expected $4)"
  [ "$got" = "$4" ] || status=1
}
check c6715         c6715          199529/200000 VERIFIED
check c6715_control c6715_mass0985 199529/200000 REFUSED
check c6718         c6718          3350/3359     VERIFIED
check c6718_control c6718_mass0985 3350/3359     REFUSED
check c6718_B3348   c6718          3348/3359     REFUSED
exit $status
