#!/bin/sh
# Re-check s(76) = 9 from scratch.
#
#   sh verify.sh <new work directory> [threads] [--full-zm]
#
#   always    : cover sha256 and exact total/format check (tools/check_total.py);
#               fetch Evan Daniel's checkers at a pinned commit (not bundled) and verify their sha256;
#               zmx2 d4      (exact D4 invariance of the cover)
#               zmx2 cert --d4 over all 8,100 roots; the roots it leaves uncertified must be exactly
#                            records/zmx2/failing_roots.txt (about 5 CPU-minutes);
#               zm_mixed cert on the 64 sub-roots of those roots (records/zm_mixed/jobs.txt), exact
#                            rational arithmetic (about 30 CPU-minutes); each job prints
#                            "VERIFIED-D4 (PARTIAL)" because it covers only its own sub-root;
#               tools/check_coverage.py on the fresh zmx2 log and the fresh zm_mixed records.
#   --full-zm : also zm_mixed over the whole D4 region (all 129,600 roots; several hundred CPU-hours).
#
# Needs git, Python 3 with numpy, and Rust >= 1.86 (cargo; set CARGO to choose a toolchain).
set -eu
UPSTREAM_URL=https://github.com/evand/square-packing.git
UPSTREAM_COMMIT=b91d70b6ed314624c1434b628a9c7bf9a132c743
ZMX2_RS=6b7f0f79466bf25c9a85f8fe2f3866de734935f0521ea188136818c2fb5b3fed
ZM_MIXED=ee3e2915349b8795128417bca6414b205d526db9f01f88cd4cd32c32e8d760ac
ZEROMARGIN=640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab
MIXED_COVER=bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5
COVER_SHA=b6a1214b99f00e5dd136d74c8d87bccd178df38a1063b2c7be90517eb2b862b2
ZARGS="--d4 --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 24"

HERE=$(cd "$(dirname "$0")" && pwd)
WORK=${1:?usage: sh verify.sh <new work directory> [threads] [--full-zm]}
shift
THREADS=8; FULL=0
for arg in "$@"; do case "$arg" in --full-zm) FULL=1 ;; *) THREADS=$arg ;; esac; done
CARGO=${CARGO:-cargo}
[ ! -e "$WORK" ] || { echo "refusing existing path: $WORK" >&2; exit 2; }
if command -v sha256sum >/dev/null; then sha() { sha256sum "$1" | cut -d' ' -f1; }; else sha() { shasum -a 256 "$1" | cut -d' ' -f1; }; fi
mkdir -p "$WORK"; WORK=$(cd "$WORK" && pwd)

echo "== cover"
gunzip -c "$HERE/cover/s76_cover_v5.txt.gz" > "$WORK/s76_cover_v5.txt"
COVER="$WORK/s76_cover_v5.txt"
[ "$(sha "$COVER")" = "$COVER_SHA" ] || { echo "cover sha256 mismatch" >&2; exit 1; }
python3 "$HERE/tools/check_total.py" "$COVER" 76

echo "== checkers (evand/square-packing@$UPSTREAM_COMMIT)"
git clone -q "$UPSTREAM_URL" "$WORK/upstream"
(cd "$WORK/upstream" && git checkout -q "$UPSTREAM_COMMIT")
U="$WORK/upstream/s12"
[ "$(sha "$U/verify2/src/bin/zmx2.rs")" = "$ZMX2_RS" ]
[ "$(sha "$U/search/zm_mixed.py")" = "$ZM_MIXED" ]
[ "$(sha "$U/search/zeromargin.py")" = "$ZEROMARGIN" ]
[ "$(sha "$U/search/mixed_cover.py")" = "$MIXED_COVER" ]
echo "checker hashes OK"
(cd "$U/verify2" && "$CARGO" build --release --bin zmx2 >/dev/null 2>&1)
ZMX2="$U/verify2/target/release/zmx2"

echo "== zmx2 d4"
"$ZMX2" d4 "$COVER"

echo "== zmx2 cert --d4 (all roots)"
"$ZMX2" cert "$COVER" --d4 --threads "$THREADS" --uncert-cap 200000 --log "$WORK/zmx2.log" > "$WORK/zmx2.out" 2>&1 || true
grep -E "^done" "$WORK/zmx2.out"
python3 - "$WORK/zmx2.log" "$HERE/records/zmx2/failing_roots.txt" <<'PY'
import re, sys
bad = sorted(set(m.group(1) for ln in open(sys.argv[1]) if ln.startswith("ROOT")
                 for m in [re.search(r"root (\S+) .*uncert (\d+)", ln)] if m and int(m.group(2)) > 0))
want = sorted(l.strip() for l in open(sys.argv[2]) if l.strip())
assert bad == want, "zmx2 leaves different roots uncertified: %s" % bad
print("zmx2 leaves exactly the %d listed roots uncertified" % len(bad))
PY

echo "== zm_mixed on the 64 sub-roots ($THREADS in parallel)"
mkdir -p "$WORK/zm_mixed"
export COVER WORK U ZARGS
cut -d' ' -f1- "$HERE/records/zm_mixed/jobs.txt" | xargs -P "$THREADS" -L 1 sh -c \
  'i=$0; cd "$U/search" && python3 -u zm_mixed.py cert "$COVER" $ZARGS --nproc 1 --cx-lo $1 --cx-hi $2 --cy-lo $3 --cy-hi $4 --u-lo $5 --u-hi $6 --resume "$WORK/zm_mixed/j$i.jsonl" > "$WORK/zm_mixed/j$i.log" 2>&1'
if grep -l "NOT VERIFIED" "$WORK"/zm_mixed/j*.log >/dev/null 2>&1; then echo "zm_mixed: some root NOT VERIFIED" >&2; exit 1; fi
echo "zm_mixed: all sub-roots VERIFIED"

echo "== coverage"
python3 "$HERE/tools/check_coverage.py" "$WORK/zmx2.log" "$WORK/zm_mixed" "$COVER_SHA"

if [ "$FULL" = 1 ]; then
  echo "== zm_mixed over the whole D4 region (long)"
  (cd "$U/search" && python3 -u zm_mixed.py cert "$COVER" $ZARGS --nproc "$THREADS" --resume "$WORK/zm_full.jsonl" --manifest "$WORK/zm_full_manifest.json") > "$WORK/zm_full.log" 2>&1
  tail -3 "$WORK/zm_full.log"
  if grep -q "NOT VERIFIED" "$WORK/zm_full.log" || ! grep -q "VERIFIED" "$WORK/zm_full.log"; then echo "zm_mixed full pass: NOT VERIFIED" >&2; exit 1; fi
fi
echo "== s(76) >= 9 certified; with the 9x9 grid, s(76) = 9"
