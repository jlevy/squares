#!/usr/bin/env bash
# Run everything and check the results that matter.
set -euo pipefail
cd "$(dirname "$0")"

# Some checks need PyYAML and jsonschema, which a bare system python3 usually lacks
# -- on the machine this was written on, `import yaml` failed and every frontier
# check below was silently unreachable. Prefer an interpreter that already has both;
# otherwise use a pinned zero-install runner, never a floating one (see
# `tbd guidelines supply-chain-hardening` rule 6).
if python3 -c "import yaml, jsonschema" 2>/dev/null; then
  PY=python3
elif command -v uv >/dev/null 2>&1; then
  PY="uv run --quiet --with pyyaml==6.0.3 --with jsonschema==4.26.0 python3"
else
  echo "need PyYAML + jsonschema, or uv; install one and re-run" >&2
  exit 1
fi
echo "python runner: $PY"

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
$PY - <<'PY'
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
echo "== soft-schema validation =="
uv run --quiet python tools/validate_schemas.py 2>/dev/null || $PY tools/validate_schemas.py

echo
echo "== generated tables in sync with frontier/ =="
$PY tools/render_tables.py --check

echo
echo "== strategy catalogues =="
$PY - <<'PY'
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
echo "== lint floor =="
# The floor is enforced, not aspirational. It has already earned its place: ruff's
# strict-zip rule found silent truncation in field arithmetic, its closure rule found a
# capture one edit from a bug, and clippy found an approximation of TAU written as a
# literal. Skipped, not failed, where the toolchain is absent.
if command -v uv >/dev/null 2>&1; then
  ( cd "$(dirname "$0")" && uv run --quiet ruff check . && uv run --quiet ruff format --check . \
    && uv run --quiet basedpyright ) | tail -3
else
  echo "  uv not installed, skipping Python lint"
fi
if command -v cargo >/dev/null 2>&1; then
  ( cd sqsearch && cargo clippy --release --all-targets --quiet -- -D warnings 2>&1 | tail -2 \
    && cargo fmt --check && echo "  clippy clean at pedantic; rustfmt clean" )
else
  echo "  cargo not installed, skipping Rust lint"
fi

echo
echo "== negative controls =="
# Every guard in this directory, watched failing. A check nobody has seen fail is not a
# check, and until now each of these was run once by hand and thrown away.
$PY tools/negctl.py tools/controls.yaml

echo
echo "== soundness perimeter =="
# Every component that can emit a packing, checked by sqpack through code it does not
# share. This is the check whose absence let D-014 through: the quench was validated
# only against its own constraint rows, which is no check when the rows are what the
# solver got wrong. Replaying that defect against this gate rejects it on sight.
$PY tools/perimeter_test.py

echo
echo "== defect log =="
# The logbook of what has gone wrong here, and what now stops each thing recurring.
# Checked like any other dataset: schema, contiguous ids, every open defect tracked by
# a bead, every narrative link resolving, and the generated view in sync.
$PY tools/render_defects.py --check

# A generated view must also be exempt from the Markdown auto-formatter, or the
# pre-commit hook reformats it and the drift check above fails until someone
# regenerates it. That reasoning was written down for ledger.md and not applied to
# defects.md, which sat reflowable for a day (D-027). Trusting the list is what
# failed, so the gate checks it.
$PY tools/check_generated_exempt.py

echo
echo "== search engine (sqsearch) =="
# The engine gate: geometry against a naive reference, determinism, and a positive
# control that recovers s(5) = 2 + 1/sqrt(2). A run that has not passed this may not
# be recorded. Skipped, not failed, where cargo is absent -- the rest of this repo
# is Python and prose and should stay checkable without a Rust toolchain.
if command -v cargo >/dev/null 2>&1; then
  ( cd sqsearch && cargo build --release --quiet )
  out=$(sqsearch/target/release/sqsearch --selftest)
  echo "$out" | sed 's/^/  /'
  grep -q "SELFTEST PASSED" <<<"$out"
  ! grep -q "FAIL" <<<"$out"
else
  echo "  cargo not installed, skipping"
fi

echo
echo "== differential: search energy vs validity oracle =="
# sqsearch owns move-loop energy, sqpack owns validity. They never meet in normal
# operation, so nothing would notice if they drifted -- and a search optimising
# against a different notion of overlap than the record is checked with is the
# quietest possible failure. Near-contact pairs only: that is where it could hide.
if command -v cargo >/dev/null 2>&1; then
  $PY differential_test.py 20000
else
  echo "  cargo not installed, skipping"
fi

echo
echo "== provenance: recorded commits are reachable =="
# A round records the commit that produced its numbers. If a rebase orphans that
# commit the binary can no longer be rebuilt and determinism stops being a safety
# net -- which happened once here, to exp-001, and is annotated there. Orphans are
# reported rather than fatal: history that has already been published cannot be
# fixed by failing a test, and the annotation is the honest record.
for f in campaign/series/*/experiments/*.md; do
  c=$(sed -n "s/.*engine_commit: '\(.*\)'.*/\1/p" "$f" | head -1)
  [ -n "$c" ] || continue
  if git merge-base --is-ancestor "$c" HEAD 2>/dev/null; then
    echo "  ok       $(basename "$f") -> $c"
  else
    echo "  ORPHANED $(basename "$f") -> $c (must carry an annotation)"
    grep -q "^## Annotation" "$f" || { echo "    and it has none"; exit 1; }
  fi
done

echo
echo "== campaign record =="
# Whole-set invariants no per-artifact validation can see: duplicate ids, dangling
# hypothesis references, rounds naming an unknown series, more than one open series,
# stale claims, the cross-field verdict rules, the two-way reconciliation between
# ideas.md and the registry, and whether ledger.md is stale.
$PY campaign/ledger.py --check

echo
echo "ALL CHECKS PASSED"
