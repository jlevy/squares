#!/bin/sh
# Upper bounds on c*(k) in Lean (certificates/k2-minus-c/README.md): rebuild the modules and print their axioms.
# Run from anywhere.  About 5 minutes from a cold Mathlib cache on 16 cores (the RyuStair* modules take ~1 min).
#
#   certificates/k2-minus-c/verify.sh          the Ryu-line theorems (in the default Lean target)
#   certificates/k2-minus-c/verify.sh --fang   also Fang's theorems: regenerates and builds the 18 piece
#                                              certificates (~19 min wall at 8 jobs, <= ~8 GB per job), then FangFinal
#
# Passes iff every listed theorem depends on exactly propext, Classical.choice, Quot.sound.
set -e
cd "$(dirname "$0")/../.."          # repo root
FANG=0
case "${1:-}" in --fang) FANG=1 ;; "") ;; *) echo "usage: $0 [--fang]"; exit 2 ;; esac
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT

THMS="UnitSquarePacking.Ryu.packs_sub_8sqrt UnitSquarePacking.Ryu.packs_sub_4sqrt2
UnitSquarePacking.Ryu.packs_sub_4sqrt2_layers UnitSquarePacking.Ryu.packs_stair
UnitSquarePacking.Ryu.packs_stair_k25 UnitSquarePacking.Ryu.packs_ryu_thm12"
MODS="Sqpack.RyuBound Sqpack.RyuFill Sqpack.RyuLayers Sqpack.RyuStairBound"
if [ "$FANG" = 1 ]; then
  echo "--- Fang's pieces (search/exact/fang_pieces.py, lean/scripts/build_chunks.sh)"
  python3 search/exact/fang_pieces.py
  for m in P110 P132 P156 P182 P211 P241 P273 P308 P343 P381 P421 P463 P507 P553 P601 P651 R257 R443; do
    lean/scripts/build_chunks.sh Sqpack.Exact.Fang.$m 8
  done
  MODS="$MODS Sqpack.FangFinal"
  THMS="$THMS UnitSquarePacking.FangGlue.theorem1 UnitSquarePacking.FangGlue.theorem2"
fi

echo "--- lake build $MODS"
( cd lean && lake build $MODS )

echo "--- axioms"
{ for m in $MODS; do echo "import $m"; done
  for t in $THMS; do echo "#print axioms $t"; done; } > "$TMP/Ax.lean"
cp "$TMP/Ax.lean" lean/.k2c_axioms_tmp.lean
( cd lean && lake env lean .k2c_axioms_tmp.lean ) > "$TMP/out" 2>&1 || { cat "$TMP/out"; rm -f lean/.k2c_axioms_tmp.lean; exit 1; }
rm -f lean/.k2c_axioms_tmp.lean
cat "$TMP/out"
n=$(echo "$THMS" | wc -w)
ok=$(grep -c "depends on axioms: \[propext, Classical.choice, Quot.sound\]$" "$TMP/out" || true)
if [ "$ok" = "$n" ] && ! grep -q sorryAx "$TMP/out"; then
  echo "VERIFIED: $n theorems, standard axioms only"
else
  echo "NOT VERIFIED: $ok of $n theorems with exactly the standard axioms"; exit 1
fi
