#!/usr/bin/env bash
# Route A at 297: T-174's retained certificate to an exact configuration, decided exactly.
# Run from packing/ with the project interpreter on PATH (uv run --frozen bash THIS SCRIPT).
# Writes the packet's receipts; the 2,600-digit values go to $SCRATCH (default /tmp), since
# they are derived again in about three CPU-minutes and are not kept in Git.
set -euo pipefail
PACKET=resources/web/hyukdongkim-s297-2026-10-25
SCRATCH=${SCRATCH:-/tmp}
TOOL="python -m devtools.build_field_configuration"
WITNESS=witnesses/known-best/n-297.yaml
mkdir -p "$PACKET/receipts"
step=${1:-all}
if [[ $step == all || $step == solve ]]; then
  $TOOL contacts "$WITNESS" --out "$PACKET/receipts/contacts.json" > /dev/null
  $TOOL solve "$WITNESS" --digits 2600 --values "$SCRATCH/n297-values-2600.json" \
    --out "$PACKET/receipts/solve.json" > /dev/null
fi
if [[ $step == all || $step == field ]]; then
  $TOOL field "$SCRATCH/n297-values-2600.json" --express 't[5]' 't[6]' 't[9]' \
    --polynomial "$PACKET/facts/s297-polynomial.json" --out "$PACKET/receipts/field.json" > /dev/null
fi
if [[ $step == all || $step == build ]]; then
  $TOOL build "$WITNESS" --values "$SCRATCH/n297-values-2600.json" \
    --field "$PACKET/receipts/field.json" --polynomial "$PACKET/facts/s297-polynomial.json" \
    --identifier W-route-a-n297 --output "$PACKET/facts/route-a-n297.json.gz" \
    --out "$PACKET/receipts/build.json" > /dev/null
fi
if [[ $step == all || $step == decide ]]; then
  for control in positive duplicate-square-overlap square-translated-outside-container; do
    $TOOL decide "$PACKET/facts/route-a-n297.json.gz" --control "$control" \
      --out "$PACKET/receipts/decide-$control.json" > /dev/null &
  done
  wait
fi
echo "route A $step: done"
