# Sourced by the run scripts in this directory; not run on its own.
# It locates the packets and the project from this directory, takes the work directory
# from the script's first argument, resolves the project interpreter through uv, and
# unpacks the two covers into WORK/data with their SHA-256 checked.
# Every run script works inside WORK (create it outside the checkout) and writes its
# outputs under WORK/outputs, in the layout of the kept review/outputs/.
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REVIEW=$(dirname -- "$HERE")
K76=$(dirname -- "$REVIEW")
WEB=$(dirname -- "$K76")
K95=$WEB/bengreff-s95-certificate-2026-10-15
PACKING=$(dirname -- "$(dirname -- "$WEB")")
EVAND=$WEB/evand-square-packing-2026-09-28/square-packing/s12/search
EVAND26=$WEB/evand-square-packing-2026-09-26/square-packing/s12/search
if [ $# -lt 1 ]; then echo "usage: $0 WORK  (a scratch directory outside the checkout)" >&2; exit 2; fi
mkdir -p -- "$1" && WORK=$(CDPATH= cd -- "$1" && pwd) || exit 2
# The project interpreter (Python 3.14), never the python3 on PATH.
PY=$("${UV:-uv}" run --frozen --all-extras --group dev --project "$PACKING" python -I -c 'import sys; print(sys.executable)') || exit 2
cd -- "$WORK" || exit 2
mkdir -p data outputs
unpack() { # packet-relative gzip, output name, sha256
  [ -f "data/$2" ] || gzip -dc -- "$1" > "data/$2" || exit 2
  echo "$3  data/$2" | sha256sum -c --quiet - || { echo "cover digest differs: data/$2" >&2; exit 2; }
}
unpack "$K76/s76-certificate/cover/s76_cover_v5.txt.gz" s76_cover_v5.txt b6a1214b99f00e5dd136d74c8d87bccd178df38a1063b2c7be90517eb2b862b2
unpack "$K95/s95-certificate/cover/s95_cover_v2.txt.gz" s95_cover_v2.txt 8b2d2152867585c82920bc90c6c3ec2a2458ef2ba57311ccd7dd436d1344cb7c
# Copies of the retained zm_mixed.py (ee3e2915), mixed_cover.py (bb89de15) and
# zeromargin.py (640fe453), digests checked; zm_mixed.py imports the other two from its
# own directory.
zmcheck() {
  mkdir -p zmcheck
  cp -- "$EVAND/zm_mixed.py" "$EVAND/mixed_cover.py" "$EVAND26/zeromargin.py" zmcheck/
  sha256sum -c --quiet - <<SUMS || { echo "zm_mixed.py checker digests differ" >&2; exit 2; }
ee3e2915349b8795128417bca6414b205d526db9f01f88cd4cd32c32e8d760ac  zmcheck/zm_mixed.py
bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5  zmcheck/mixed_cover.py
640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab  zmcheck/zeromargin.py
SUMS
}
need() { # a file an earlier script writes
  [ -f "$1" ] || { echo "missing $WORK/$1: run $2 with the same WORK first" >&2; exit 2; }
}
