#!/bin/sh
# Hypothesis-free Lean proof of the point-only s(21) = 5: regenerate Evan Daniel's zero-margin box tree
# for our certificate with his pinned generator, check it matches data-sha256.txt, and kernel-check it.
# Usage (from point_n21_L5/lean/zero-margin): sh build_zero_margin.sh <new work directory> [jobs] [nproc]
# Needs git, Python 3 with numpy, and elan. Each part peaks near 6 GB; `jobs` parts are built at once.
set -eu
UPSTREAM_URL=https://github.com/evand/square-packing.git
UPSTREAM_COMMIT=6aa82ba457e9eaeaaa3af0833600f27f91a2fce3
GEN_SHA256=e6e1d477fa5f2fe4eaf860f7d39a61d083e5577d1202cc2bc710a104fa080d46
ORACLE_SHA256=640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab
ZMTREE_SHA256=8c23911b9d205563d234c101478ed9c4443cb29ec10c454c4aa5743319024263
CERT_SHA256=9f631fbae420e0376ea636a232b7680e937deebe205dc035cfb9c43a3d74b456
HERE=$(cd "$(dirname "$0")" && pwd)
WORK=${1:?usage: sh build_zero_margin.sh <new work directory> [jobs] [nproc]}
JOBS=${2:-2}
NPROC=${3:-4}
PY=${PYTHON:-python3}
[ ! -e "$WORK" ] || { echo "refusing existing path: $WORK" >&2; exit 2; }
if command -v sha256sum >/dev/null; then sha() { sha256sum "$1" | cut -d' ' -f1; }; else sha() { shasum -a 256 "$1" | cut -d' ' -f1; }; fi
"$PY" -c 'import numpy' || { echo "numpy is required" >&2; exit 1; }

git clone -q "$UPSTREAM_URL" "$WORK/upstream"
git -C "$WORK/upstream" checkout -q "$UPSTREAM_COMMIT"
[ "$(git -C "$WORK/upstream" rev-parse HEAD)" = "$UPSTREAM_COMMIT" ]
U="$WORK/upstream/s12"
[ "$(sha "$U/lean/scripts/gen_zmtree.py")" = "$GEN_SHA256" ]
[ "$(sha "$U/search/zeromargin.py")" = "$ORACLE_SHA256" ]
[ "$(sha "$U/lean/Sqpack/ZMTree.lean")" = "$ZMTREE_SHA256" ]
[ ! -e "$U/lean/Sqpack/N21PtsLower.lean" ] && [ ! -e "$U/lean/Sqpack/N21PtsZ" ]
mkdir -p "$U/certificates/n21pts"
cp "$HERE/../../certificates/n21-capture-one.txt" "$U/certificates/n21pts/n21-capture-one.txt"
[ "$(sha "$U/certificates/n21pts/n21-capture-one.txt")" = "$CERT_SHA256" ]
cp "$HERE/N21PtsLower.lean" "$U/lean/Sqpack/N21PtsLower.lean"
cp "$HERE/N21PtsAxiomsZ.lean" "$U/lean/N21PtsAxiomsZ.lean"

# the generator is deterministic and untrusted; the kernel checks whatever it writes
(cd "$U" && "$PY" lean/scripts/gen_zmtree.py certificates/n21pts/n21-capture-one.txt --n 21 \
   --name N21PtsZ --outdir lean/Sqpack/N21PtsZ --nproc "$NPROC" --parts 64) > "$WORK/gen.log" 2>&1
(cd "$U/lean/Sqpack/N21PtsZ" && for f in *.lean; do echo "$(sha "$f")  $f"; done) > "$WORK/data-sha256.txt"
if diff -q "$WORK/data-sha256.txt" "$HERE/data-sha256.txt" >/dev/null; then echo "generated data matches data-sha256.txt"
else echo "note: generated data differs from data-sha256.txt (still checked by the kernel below)"; fi

cd "$U/lean"
lake exe cache get > "$WORK/cache.log" 2>&1
lake build Sqpack.N21PtsZ.Pts > "$WORK/build.log" 2>&1
ls Sqpack/N21PtsZ/Part*.lean | sed 's#\.lean$##; s#/#.#g' | xargs -P "$JOBS" -I{} lake build {} >> "$WORK/build.log" 2>&1
lake build Sqpack.N21PtsLower >> "$WORK/build.log" 2>&1
grep -q 'Build completed successfully' "$WORK/build.log"
lake env lean N21PtsAxiomsZ.lean > "$WORK/axioms.log" 2>&1
cat "$WORK/axioms.log"
grep -q "'SquarePacking.n21pts_eq_5' depends on axioms: \[propext, Classical.choice, Quot.sound\]" "$WORK/axioms.log"
echo N21_POINTS_HYPOTHESIS_FREE_VERIFIED
