#!/bin/sh
# The review's cross-check of F2: zmx2.rs 6b7f0f79, the version the 28 September and
# 2 October reviews derived, run over the D4 region of the s(44) cover, to compare root for
# root with the e2bb84e9 replay in receipts/. It decides nothing the replay does not.
#
# Usage, from packing/: sh resources/web/moh63-dev-s44-equals-7-2026-10-29/review/programs/run_zmx2_6b7f0f79.sh WORK
# WORK must hold the build of `python -m devtools.replay_evand_zmx2 build --checker 6b7f0f79
# --work WORK` and the cover staged by `... run --case 44` (WORK/s12/certificates/).
set -eu
WORK=$1
OUT=resources/web/moh63-dev-s44-equals-7-2026-10-29/review/outputs/zmx2
mkdir -p "$OUT"
BIN="$WORK/6b7f0f79/verify2/target/release/zmx2"
COVER="$WORK/s12/certificates/s44_cover_7.txt"
echo "# binary sha256: $(sha256sum "$BIN" | cut -d' ' -f1)" > "$OUT/n44_zmx2_6b7f0f79_d4.log"
echo "# cover sha256: $(sha256sum "$COVER" | cut -d' ' -f1)" >> "$OUT/n44_zmx2_6b7f0f79_d4.log"
echo "# started $(date -u +%FT%TZ)" >> "$OUT/n44_zmx2_6b7f0f79_d4.log"
rm -f "$OUT/n44_zmx2_6b7f0f79_d4_roots.log"
"$BIN" cert "$COVER" --d4 --threads 2 --log "$OUT/n44_zmx2_6b7f0f79_d4_roots.log" \
    | grep -v '^progress' >> "$OUT/n44_zmx2_6b7f0f79_d4.log"
echo "# finished $(date -u +%FT%TZ)" >> "$OUT/n44_zmx2_6b7f0f79_d4.log"
