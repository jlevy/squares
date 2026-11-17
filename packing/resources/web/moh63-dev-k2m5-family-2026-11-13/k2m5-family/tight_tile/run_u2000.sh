#!/bin/bash
# Larger tilt range u0 = 1/2000 (t0 = dmax = 1/500) for the five tile neighbourhoods where zmx2 leaves boxes with
# u up to 3.36e-4 (> 1/4000): coverage needs them.  Output: out_u2000/.  Usage:
#   cd ~/PycharmProjects/square-packing/sq/ttbox && nohup bash run_u2000.sh > u2000.out 2>&1 &
cd "$(dirname "$0")"
PY="$HOME/miniforge3/bin/python3"; [ -x "$PY" ] || PY=$(command -v python3)
NP=${NP:-6}; COV=../certificate/sol_exact_box11.txt
mkdir -p out_u2000
echo "start $(date)"
cat <<J | tr ' ' ',' | U0=1/2000 xargs -P "$NP" -n 1 sh -c 'IFS=, read -r d s k a b <<EOF
$0
EOF
f="out_u2000/d${d}_s${s}_${k}_${a}${b:+_$b}.out"; [ -f "$f" ] && grep -q "^ALL-OK\|^NOT-OK" "$f" && exit 0
U0=1/2000 '"$PY"' run_tt.py '"$COV"' $d $s $k $a $b > "$f" 2>&1; echo "$(date +%T) $(tail -1 "$f") $f"'
1.5 1 line 4.2
1.5 1 strip 4.2+ 4.3-
1.5 1 line 4.3
1.5 1 line 4.5
1.5 1 strip 4.5+ 4.6-
1.5 1 line 4.6
1.5 -1 line 5.4
1.5 -1 strip 5.4+ 5.5-
1.5 -1 line 5.5
1.5 -1 line 3.8
1.5 -1 strip 3.8+ 3.9-
1.5 -1 line 3.9
2.5 -1 line 4.4
2.5 -1 strip 4.4+ 4.5-
2.5 -1 line 4.5
J
echo "u2000 done $(date)"
