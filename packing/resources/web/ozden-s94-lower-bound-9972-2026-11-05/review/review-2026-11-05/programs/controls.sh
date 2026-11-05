#!/usr/bin/env bash
# The review's own controls, one after another on one core:
# the 99/100 mutant at 1198 and 3663 (each must stop as a counterexample candidate),
# threshold brackets at 1198 and 3663 (a threshold above the least capture must fail,
# one below it must verify), and the crate's least-bound box at 3663 decided exactly.
set -uo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cert="$1"; out="$2"
run() { name="$1"; shift; timeout 1750 "$here/run.sh" "$@" > "$out/$name.log" 2>&1; echo "$name exit=$? $(grep -E '^(status|nodes|boxes|least_certified_bound|least_exact_bound|least_centre_capture|lowest_centre_estimate|stop|cpu_seconds):' "$out/$name.log" | tr '\n' ' ')"; }
run mutant-r1198 bnb.py "$cert" 1198 "$out/mutant-r1198.json" --mass-factor 99/100
run mutant-r3663 bnb.py "$cert" 3663 "$out/mutant-r3663.json" --mass-factor 99/100
run thr-r1198-10012 bnb.py "$cert" 1198 "$out/thr-r1198-10012.json" --threshold 10012/10000
run thr-r1198-1001 bnb.py "$cert" 1198 "$out/thr-r1198-1001.json" --threshold 1001/1000
# The crate's least-bound box at 3663 (lab row: centre and half-widths in binary64).
read -r X0 X1 Y0 Y1 < <("$HOME/.local/bin/uv" --directory /home/user/squares/packing run --frozen --all-extras --group dev python -I -B -c "
from gmpy2 import mpq
x, y, dx, dy = 8.066693643799294, 6.673046519223423, 0.004191419923536444, 0.002095709961768222
v = [mpq(x) - mpq(dx), mpq(x) + mpq(dx), mpq(y) - mpq(dy), mpq(y) + mpq(dy)]
print(' '.join(f'{q.numerator}/{q.denominator}' for q in v))" 2>/dev/null)
run exact-box-r3663-crate-least bnb_exact.py "$cert" 3663 "$X0" "$X1" "$Y0" "$Y1" "$out/exact-box-r3663-crate-least.json"
run thr-r3663-10035 bnb.py "$cert" 3663 "$out/thr-r3663-10035.json" --threshold 10035/10000
