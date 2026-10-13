#!/usr/bin/env bash
# Re-run the second adversarial review's programs on a checkout of the edition, in the
# order of the review's "Checks Run Here" table, and print every command before its
# output. RESULTS.txt beside this file is this script's complete output.
#
# usage: run.sh CLONE [WORK]
#   CLONE  a checkout of Kleddamag/the-seventeenth-square-candidate at
#          653b9589d0f8a152f01adc56b1d48ba53d49abc3 (tree 502e27fb); the large files of
#          the release are not needed
#   WORK   a scratch directory for audit.json (default: a new temporary directory)
#
# PYTHON names the interpreter; the default is this repository's packing/.venv. Every
# program runs with -I, from outside the clone, and reads the clone as data; -B keeps
# bytecode out of this folder. In the output, CLONE stands for the checkout's path, G for
# the review's G/ (the g20s-terminal-audit folder) and WORK for the scratch directory.
set -euo pipefail
[ $# -ge 1 ] || { echo "usage: run.sh CLONE [WORK]" >&2; exit 2; }
here="$(cd "$(dirname "$0")" && pwd)"
progs="$here/programs"
py="${PYTHON:-$here/../../../../.venv/bin/python3}"
clone="$(cd "$1" && pwd)"
if [ $# -ge 2 ]; then mkdir -p "$2"; work="$(cd "$2" && pwd)"; else work="$(mktemp -d)"; fi
g="$clone/research/finishing-threshold-goal-20261007/current-author-20261012t/g20s-terminal-audit"
c="$clone/research/finishing-threshold-goal-20261007/clean-rerun-20261011/current-build-0122/capture"
jq="$clone/local-research/claude-20261002/cloud/analysis/part3_exact/certs/JQ_v1/jQTw.n0.JQ.cert.jsonl.gz"
cont="$g/full-stopped-propagation/continuation"
receipt="$g/full-gate/producer/gate-receipt.json"

quote() { printf '%s' "$1" | sed 's/[][\.*^$|/]/\\&/g'; }
norm() {
  sed -e "s|$(quote "$g")|G|g" -e "s|$(quote "$clone")|CLONE|g" \
    -e "s|$(quote "$progs")|programs|g" -e "s|$(quote "$work")|WORK|g"
}
run() {
  printf '\n$ python3 -I -B %s\n' "$*" | norm
  "$py" -I -B "$@" 2>&1 | norm
}

{
  "$py" -I -B -c 'import sys, sympy, mpmath; print("python", sys.version.split()[0], "sympy", sympy.__version__, "mpmath", mpmath.__version__)'
  printf 'edition at %s\n' "$(git -C "$clone" rev-parse HEAD 'HEAD^{tree}' 2>/dev/null | paste -sd ' ' || echo 'CLONE is not a Git checkout')"
} | norm

run "$progs/geom.py"                                      # check 1
run "$progs/cmp_file.py" "$progs" "$clone/upper-packing-certificate.json"   # check 2
run "$progs/audit.py" "$work/audit.json"                  # check 3
run "$progs/identities.py" "$receipt" "$work/audit.json"  # check 4
run "$progs/check_rows.py" "$receipt" "$work/audit.json" \
  "$cont/prefix/round-01" "$cont/prefix/round-02" "$cont/prefix/round-03" \
  "$cont/round-04" "$cont/round-05"                       # check 5
run "$progs/replay.py" "$receipt" "$work/audit.json" \
  "$cont/inputs/accepted-six-step-prefix.json" "$cont"    # checks 6 and 7
run "$progs/stops.py"                                     # check 8, as run
run "$progs/stops_eps.py" 501 100000                      # check 8, as run (see the README)
run "$progs/stops_cuts.py"                                # check 8, corrected after review A of #577
run "$progs/audit_entry.py"                               # check 9
run "$progs/upper.py"                                     # check 10
run "$progs/coarse.py"                                    # check 11
run "$progs/profiles.py" "$clone"                         # check 12
run "$progs/admission.py" "$clone"                        # check 13
run "$progs/budgets.py" "$c/statements"                   # check 14
run "$progs/frame0917.py" "$c/statements/FRAME_0917"      # check 15
run "$progs/jq_struct.py" "$jq" \
  "$clone/research/window-extension-20261008/bigbox/join/JQ_exact_v1.json"   # check 16
