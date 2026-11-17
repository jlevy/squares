#!/bin/bash
# Tight-Tile Lemma: run every job of make_jobs.py that has no finished output yet (fixed launcher: one job per line).
# Usage:  cd ~/PycharmProjects/square-packing/sq/ttbox && NP=8 nohup bash run_all2.sh > run2.out 2>&1 &
cd "$(dirname "$0")"
PY="$HOME/miniforge3/bin/python3"; [ -x "$PY" ] || PY=$(command -v python3)
NP=${NP:-8}; COV=../certificate/sol_exact_box11.txt
mkdir -p out
echo "start $(date)"
"$PY" make_jobs.py | tr ' ' ',' | xargs -P "$NP" -n 1 sh -c 'IFS=, read -r d s k a b <<EOF
$0
EOF
n="d${d}_s${s}_${k}_${a}${b:+_$b}"
for g in out/$n.out out/${n}_*.out; do [ -f "$g" ] && grep -q "^ALL-OK\|^NOT-OK" "$g" && exit 0; done
f=out/$n.out; '"$PY"' run_tt.py '"$COV"' $d $s $k $a $b > "$f" 2>&1; echo "$(date +%T) $(tail -1 "$f") $f"'
echo "all done $(date)"
