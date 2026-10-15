#!/bin/sh
# The #594 triage's comparisons and premise checks, re-run from this packet's retained bytes
# and receipts. None of them decides coverage: that is zmx2's and zm_mixed.py's, whose
# receipts sit beside this directory. These are triage diagnostics, not repository tools;
# registering case 76 in devtools.replay_evand_zmx2 and devtools.audit_evand_mixed_covers is
# the tooling slice the import owes.
#
#   sh triage_checks.sh PACKING_DIR        (PACKING_DIR: the repository's packing/)
set -eu
PK=$1
P=$PK/resources/web/bengreff-s76-certificate-2026-10-14
S=$P/s76-certificate
R=$P/receipts
PG=$R/programs
PY=$PK/.venv/bin/python3
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
gunzip -c "$S/cover/s76_cover_v5.txt.gz" > "$T/s76_cover_v5.txt"
gunzip -c "$PK/resources/web/wand125-point-and-mixed-2026-10-01/square-packing-bounds/certificates/k2m5_n59_L8/n59_mixed_cover_8.txt.gz" > "$T/n59_mixed_cover_8.txt"
gunzip -c "$R/n76_zmx2_d4_roots.log.gz" > "$T/n76_zmx2_d4_roots.log"
echo "== interpreter"; "$PY" --version
echo "== cover digests (s(76) cover; wand125's s(59) cover)"
(cd "$T" && sha256sum s76_cover_v5.txt n59_mixed_cover_8.txt)
echo "== the source's tools/check_total.py"
"$PY" -I "$S/tools/check_total.py" "$T/s76_cover_v5.txt" 76
echo "== devtools.audit_evand_mixed_covers.audit_cover, compared with receipts/n76_cover_audit.json"
"$PY" -I "$PG/audit76.py" "$PK" "$T/s76_cover_v5.txt" > "$T/audit.json"
cmp "$T/audit.json" "$R/n76_cover_audit.json" && echo "audit equals the retained receipt"
echo "== the Lean data against the cover"
"$PY" -I "$PG/lean_data_binding.py" "$S/lean/S76T_Pts.lean.gz" "$T/s76_cover_v5.txt" "$S/lean/S76Lower.lean"
echo "== the corner [0, 5/2)^2 against wand125's s(59) cover"
"$PY" -I "$PG/corner_compare.py" "$T/n59_mixed_cover_8.txt" "$T/s76_cover_v5.txt"
echo "== wall segments, and the stripped cover the wall control ran"
"$PY" -I "$PG/wall_mass.py" "$T/s76_cover_v5.txt" "$T/s76_nowall.txt"
(cd "$T" && sha256sum s76_nowall.txt)
echo "== the two mutations the zmx2 controls ran"
"$PY" -I "$PG/make_mutants.py" "$PK" "$T/s76_cover_v5.txt" "$T"
echo "== zmx2: the replay against the source's records"
"$PY" -I "$PG/zmx2_compare.py" "$S/records/zmx2/zmx2_v5.log.gz" "$T/n76_zmx2_d4_roots.log" "$S/records/zmx2/failing_roots.txt"
echo "== zm_mixed.py: the replay against the source's records"
"$PY" -I "$PG/zm_compare.py" "$S/records/zm_mixed" "$R/n76_zm_mixed"
echo "== zm_mixed.py records read with exact fractions: the source's, then the replay's"
"$PY" -I "$PG/zm_records.py" "$S/records/zm_mixed" "$S/records/zmx2/failing_roots.txt" "$S/records/zm_mixed/jobs.txt"
"$PY" -I "$PG/zm_records.py" "$R/n76_zm_mixed" "$S/records/zmx2/failing_roots.txt" "$S/records/zm_mixed/jobs.txt"
echo "== the source's tools/check_coverage.py on the replay's own logs"
"$PY" -I "$S/tools/check_coverage.py" "$T/n76_zmx2_d4_roots.log" "$R/n76_zm_mixed" b6a1214b99f00e5dd136d74c8d87bccd178df38a1063b2c7be90517eb2b862b2
if [ -f "$R/controls/n76_control_nowall_zmx2_d4_roots.log.gz" ]; then
  echo "== the wall control's census against the replay's, root for root"
  gunzip -c "$R/controls/n76_control_nowall_zmx2_d4_roots.log.gz" > "$T/nowall_roots.log"
  "$PY" -I "$PG/zmx2_compare.py" "$T/n76_zmx2_d4_roots.log" "$T/nowall_roots.log" "$S/records/zmx2/failing_roots.txt" || true
fi
echo "== done"
