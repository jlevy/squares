#!/usr/bin/env bash
# The synthetic trials of the review of jlevy/squares#1031, rerun with the frozen programs.
# Run from the packet directory: bash programs/rv1031_synthetic.sh PYTHON
# Writes out/synthetic/: two synthetic certificates in the source's byte layouts, the
# check and the controls on each, the controls on the first under each broken copy, and
# the contraction program on the second. Decides nothing about the certificate.
set -euo pipefail
PY=${1:-python3}
S=out/synthetic
mkdir -p $S
run() { nice -n 19 "$PY" -I -B "$@"; }
run programs/rv1031_synth.py $S/contact contact
run programs/rv1031_synth.py $S/dilated dilated
for k in contact dilated; do
  run programs/rv1031_check.py --json $S/$k.json --witness $S/$k.yaml --claim 8.000000000001 --out $S/check-$k.json || true
  run programs/rv1031_controls.py --json $S/$k.json --witness $S/$k.yaml --claim 8.000000000001 \
    --plan programs/controls-plan.json --out $S/controls-$k.json > /dev/null || true
done
for m in "always-accept" "always-refuse" "method A with one square's normals only" "method A with sin D signed in H" \
         "method A counting a zero margin as overlap" "method B with open half-planes" \
         "method B taking every listing as counterclockwise" "a reader that takes a leading plus" "form P read clockwise"; do
  f=$S/controls-mutant-$(echo "$m" | tr ' ' '-' | tr -d "'").json
  run programs/rv1031_controls.py --json $S/contact.json --witness $S/contact.yaml --claim 8.000000000001 \
    --plan programs/controls-plan.json --mutant "$m" --out "$f" > /dev/null || true
done
run programs/rv1031_contract.py --kind json --file $S/dilated.json --twin-kind witness --twin $S/dilated.yaml \
  --out $S/contraction-dilated.json
