#!/bin/sh
# The #610 triage's comparisons and premise checks, re-run from this packet's retained bytes
# and receipts. None of them decides coverage: that is zmx2's and zm_mixed.py's, whose
# receipts sit beside this directory. These are triage diagnostics, not repository tools;
# registering cases 76 and 95 in devtools.replay_evand_zmx2 and
# devtools.audit_evand_mixed_covers is the tooling slice the two imports owe. The author's
# two scripts are copied to a scratch directory and run there with -I.
#
#   sh triage_checks.sh PACKING_DIR        (PACKING_DIR: the repository's packing/)
set -eu
PK=$1
P=$PK/resources/web/bengreff-s95-certificate-2026-10-15
S=$P/s95-certificate
R=$P/receipts
PG=$R/programs
PY=$PK/.venv/bin/python3
SHA=8b2d2152867585c82920bc90c6c3ec2a2458ef2ba57311ccd7dd436d1344cb7c
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
gunzip -c "$S/cover/s95_cover_v2.txt.gz" > "$T/s95_cover_v2.txt"
gunzip -c "$PK/resources/web/wand125-point-and-mixed-2026-10-01/square-packing-bounds/certificates/k2m5_n59_L8/n59_mixed_cover_8.txt.gz" > "$T/n59_mixed_cover_8.txt"
gunzip -c "$R/n95_zmx2_d4_roots.log.gz" > "$T/n95_zmx2_d4_roots.log"
cp "$S/tools/check_total.py" "$S/tools/check_coverage.py" "$T/"
cd "$T"
echo "== interpreter"; "$PY" --version
echo "== cover digests (s(95) cover; wand125's s(59) cover)"
sha256sum s95_cover_v2.txt n59_mixed_cover_8.txt
echo "== the source's SHA256SUMS over the retained tree"
(cd "$S" && sha256sum -c --quiet SHA256SUMS && echo "all $(wc -l < SHA256SUMS) listed files match")
echo "== the source's tools/check_total.py, run with -I from scratch"
"$PY" -I "$T/check_total.py" "$T/s95_cover_v2.txt" 95
echo "== devtools.audit_evand_mixed_covers.audit_cover, compared with receipts/n95_cover_audit.json"
"$PY" -I "$PG/audit_stated.py" "$PK" "$T/s95_cover_v2.txt" 95 10 3791753447/40000000 48352 11438 > "$T/audit.json"
cmp "$T/audit.json" "$R/n95_cover_audit.json" && echo "audit equals the retained receipt"
echo "== the Lean data against the cover"
"$PY" -I "$PG/lean_data_binding.py" "$S/lean/S95T_Pts.lean.gz" "$T/s95_cover_v2.txt" "$S/lean/S95Lower.lean" 95 10
echo "== the corner [0, 5/2)^2 against wand125's s(59) cover"
"$PY" -I "$PG/corner_compare.py" "$T/n59_mixed_cover_8.txt" "$T/s95_cover_v2.txt"
echo "== wall segments, and the stripped cover the wall control ran"
"$PY" -I "$PG/wall_mass.py" "$T/s95_cover_v2.txt" "$T/s95_nowall.txt"
sha256sum s95_nowall.txt
echo "== the two mutations the zmx2 controls ran"
"$PY" -I "$PG/make_mutants.py" "$PK" "$T/s95_cover_v2.txt" "$T" s95
echo "== zmx2: the replay against the source's records"
"$PY" -I "$PG/zmx2_compare.py" "$S/records/zmx2/zmx2_s95_v2.log.gz" "$T/n95_zmx2_d4_roots.log" "$S/records/zmx2/failing_roots.txt"
echo "== zm_mixed.py records read with exact fractions: the source's, then the replay's sample"
"$PY" -I "$PG/zm_records.py" "$S/records/zm_mixed" "$S/records/zmx2/failing_roots.txt" "$S/records/zm_mixed/jobs.txt" "$SHA"
"$PY" -I "$PG/zm_records.py" "$R/n95_zm_mixed_sample" "$S/records/zmx2/failing_roots.txt" "$S/records/zm_mixed/jobs.txt" "$SHA" --partial
echo "== zm_mixed.py: the replay's sample against the source's records"
"$PY" -I "$PG/zm_compare.py" "$S/records/zm_mixed" "$R/n95_zm_mixed_sample"
echo "== the sample is the one zm_sample.py chooses"
"$PY" -I "$PG/zm_sample.py" "$S/records/zm_mixed" "$S/records/zm_mixed/jobs.txt" "$T/jobs_sample.txt" 4 38 271,287 | tail -1
cmp "$T/jobs_sample.txt" "$R/n95_zm_mixed_sample/jobs_sample.txt" && echo "sample equals the retained jobs_sample.txt"
echo "== the source's tools/check_coverage.py, run with -I from scratch, on the replay's zmx2 log and the source's zm_mixed.py records"
"$PY" -I "$T/check_coverage.py" "$T/n95_zmx2_d4_roots.log" "$S/records/zm_mixed" "$SHA" 10
echo "== the wall control's census against the replay's, root for root (headers differ in the cover hash)"
gunzip -c "$R/controls/n95_control_nowall_zmx2_d4_roots.log.gz" > "$T/nowall_roots.log"
"$PY" -I "$PG/zmx2_compare.py" "$T/n95_zmx2_d4_roots.log" "$T/nowall_roots.log" "$S/records/zmx2/failing_roots.txt" | grep -v '^   '
echo "== done"
