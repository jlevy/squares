#!/usr/bin/env bash
# Run everything and check the results that matter.
set -euo pipefail
cd "$(dirname "$0")"

echo "== exact verification =="
out=$(python3 verify_trump11.py)
echo "$out"
grep -q "^VALID: 11 squares, 55 pairs tested" <<<"$out"
grep -q "14 separated with zero gap, 41 strictly" <<<"$out"
grep -q "20 corner coordinates exactly on the boundary" <<<"$out"
grep -q "P(s) == 0 for the published degree-8 polynomial: True" <<<"$out"
grep -q "s = 3.87708359002281417730789706010096" <<<"$out"

echo
echo "== negative control =="
out=$(python3 negative_control.py)
echo "$out"
# every perturbation must be rejected by the exact verifier
grep -q "delta = 1e-100  REJECT" <<<"$out"
! grep -qE "delta = 1e-[0-9]+ +accept" <<<"$out"
# and float64 with a tolerance must have a blind spot
grep -q "tol=1e-09 .*1e-12: accept" <<<"$out"

echo
echo "== derivation (needs sympy) =="
if python3 -c "import sympy" 2>/dev/null; then
  out=$(python3 derive_field.py)
  echo "$out"
  grep -q "matches sqpack.packings.trump11.U_MIN_POLY: True" <<<"$out"
else
  echo "sympy not installed, skipping"
fi

echo
echo "== frontier corpus =="
# Structural checks that need no network. Schema validation needs softschema:
#   for f in frontier/n-*.md; do uvx softschema@latest validate "$f"; done
python3 - <<'PY'
import pathlib, yaml, sys
files = sorted(pathlib.Path("frontier").glob("n-*.md"))
assert len(files) == 100, f"expected 100 frontier artifacts, found {len(files)}"
ns, open_n, nag = set(), 0, 0
for f in files:
    fm = yaml.safe_load(f.read_text().split("---\n")[1])
    ss, d = fm["softschema"], fm["packing"]
    assert ss["contract"] == "packing.squares:SquarePackingCase/v1", f
    assert ss["envelope"] == "packing" and ss["status"] == "enforced", f
    assert int(f.stem.split("-")[1]) == d["n"], f
    assert d["status"] in ("proved", "open"), f
    assert d["upper_bound"]["value"] >= d["lower_bound"]["value"] - 1e-9, f
    if d["status"] == "proved":
        assert abs(d["gap"]) < 1e-9, f"proved case with a gap: {f}"
    else:
        open_n += 1
        nag += d["lower_bound"]["kind"] == "nagamochi"
    ns.add(d["n"])
assert ns == set(range(1, 101)), "n = 1..100 not covered exactly once"
print(f"  100 artifacts, n = 1..100, {100-open_n} proved, {open_n} open")
print(f"  {nag} of {open_n} open cases bounded below by Nagamochi's general theorem")
assert open_n == 65 and nag == 63, "corpus counts drifted from the documented figures"
PY

echo
echo "== generated tables in sync with frontier/ =="
python3 tools/render_tables.py --check

echo
echo "== strategy catalogues =="
python3 - <<'PY'
import yaml, pathlib
for kind, field, n in (("search", "outcome", 20), ("proof", "status", 30)):
    d = yaml.safe_load(pathlib.Path(f"frontier/{kind}-strategies.yaml").read_text())
    ss = d["strategies"]
    assert d["kind"] == kind and d["count"] == len(ss) == n, f"{kind}: expected {n}"
    assert [s["id"] for s in ss] == list(range(1, n + 1)), f"{kind}: ids not 1..{n}"
    fams = set(d["families"])
    for s in ss:
        assert s["family"] in fams, f"{kind} #{s['id']}: unknown family {s['family']}"
        assert s[field] and s["name"] and s["mechanism"] and s["note"], f"{kind} #{s['id']}: empty field"
    print(f"  {kind}: {n} strategies, {len(fams)} families, all fields populated")
PY

echo
echo "ALL CHECKS PASSED"
