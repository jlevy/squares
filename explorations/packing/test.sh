#!/usr/bin/env bash
# Run everything and check the results that matter.
#
# Usage: ./test.sh [--strict]
#
# A check this gate could not run is not a check that passed, and the difference has
# to survive a tired reader at 3am. Every skip is recorded and re-listed at the end,
# and the final line says how many there were -- so "ALL CHECKS PASSED" is printed
# only when that is literally true. `--strict` (or GATE_STRICT=1) turns any skip into
# a non-zero exit, which is what an unattended runner uses: a night that silently
# stopped checking the soundness perimeter must not read as a quiet one.
set -euo pipefail
cd "$(dirname "$0")"

STRICT="${GATE_STRICT:-0}"
[ "${1:-}" = "--strict" ] && STRICT=1
SKIPPED=()

# Record a skip and say so in the same breath. Never called for a check that ran.
skip() {
  SKIPPED+=("$1")
  echo "  SKIP: $1"
}

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

# Build the engine FIRST, before anything that reads the binary.
#
# It used to be built at its own step, two thirds of the way down -- which meant that
# on a fresh checkout the soundness perimeter ran with no binary and reported
# "sqsearch binary absent, skipping engine cells", and the gate still finished with
# "ALL CHECKS PASSED". The perimeter is the check whose absence let D-014 through, so
# the one check that most needed to run was the one a clean clone skipped. That is
# D-004's shape ("half the test suite was silently unreachable") inside the D-014
# guard. Ordering is the fix: build once, up front, and every later step that needs
# the binary finds it.
if command -v cargo >/dev/null 2>&1; then
  echo "== building sqsearch =="
  ( cd sqsearch && cargo build --release --quiet )
  echo "  built sqsearch/target/release/sqsearch"
else
  echo "== building sqsearch =="
  skip "cargo not installed: the engine, perimeter engine cells, differential test and selftest cannot run"
fi

echo
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
# sympy is a dev dependency, so `uv run` has it even where the system python3 does
# not. Asking python3 alone was why this step skipped on a clean checkout.
if python3 -c "import sympy" 2>/dev/null; then
  out=$(python3 derive_field.py)
elif command -v uv >/dev/null 2>&1 && uv run --quiet python -c "import sympy" 2>/dev/null; then
  out=$(uv run --quiet python derive_field.py)
else
  out=""
fi
if [ -n "$out" ]; then
  echo "$out"
  grep -q "matches sqpack.packings.trump11.U_MIN_POLY: True" <<<"$out"
else
  skip "sympy not available to python3 or uv: the degree-8 field derivation is unchecked"
fi

echo
echo "== fixed-angle cell is an LP, rebuilt independently =="
# The claim the quench rests on: fix the angles and each pair's separating axis and
# what remains is a linear program. This is the SECOND implementation of it, and that
# is the point -- sqpack.quench writes one row per pair from half-extents, this writes
# sixteen from corner pairs, and neither shares constraint-assembly code with the
# other. D-014 is what happens when a solver is checked only against its own rows.
# It also reproduces H-019's one-sided slopes through those unrelated rows.
out=$(uv run --quiet python lp_cell.py 2>/dev/null || python3 lp_cell.py)
echo "$out" | sed 's/^/  /'
grep -q "23 variables, 1056 constraints" <<<"$out"
grep -q "ALL CHECKS PASSED" <<<"$out"

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
  skip "uv not installed: ruff, ruff-format and basedpyright did not run"
fi
if command -v cargo >/dev/null 2>&1; then
  ( cd sqsearch && cargo clippy --release --all-targets --quiet -- -D warnings 2>&1 | tail -2 \
    && cargo fmt --check && echo "  clippy clean at pedantic; rustfmt clean" )
else
  skip "cargo not installed: clippy and rustfmt did not run"
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
out=$($PY tools/perimeter_test.py 2>&1); echo "$out"
grep -q "skipping engine cells" <<<"$out" \
  && skip "soundness perimeter ran without the engine: its sqsearch cells did not run"

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
echo "== bead tree =="
# The work list lives on the tbd-sync branch, outside this directory, so nothing here
# could see it -- and the one time it went inconsistent (D-025) a person found it by
# reading `tbd list --spec` and noticing two epics with the same title. Two invariants
# catch that class: no open bead under a closed parent, no two open siblings with one
# title. Reads the beads out of git, so it needs no tbd binary, and skips loudly in a
# checkout that has no tbd-sync branch.
out=$($PY tools/check_beads.py 2>&1); echo "$out"
grep -q "^SKIP" <<<"$out" \
  && skip "no bead store reachable: the bead-tree invariants did not run"

echo
echo "== hand-written skills mirrored between .agents and .claude =="
# Codex reads .agents/skills/, Claude Code reads .claude/skills/, and experiment-loop is
# hand-written into both. The runbook links into the .agents copy while an agent working
# here loads the .claude one, so a drift makes the contract this campaign runs under
# depend on which tool opened it. `make skills-check` has existed for this and nothing
# ran it -- a check outside the gate is a check that gets remembered, which is D-027
# exactly. Skipped, not failed, where make is absent.
if command -v make >/dev/null 2>&1; then
  ( cd ../.. && make --no-print-directory skills-check ) | sed 's/^/  /'
else
  skip "make not installed: the .agents/.claude skill mirrors were not compared"
fi

echo
echo "== synopsis agrees with the artifacts =="
# SYNOPSIS.md is the root document and a living one: it restates numbers that live
# authoritatively elsewhere, which is the exact shape of thing that drifted in D-010,
# D-017 and D-022. It cannot be generated -- most of it is judgement -- so it is
# reconciled instead, the way ideas.md is.
$PY tools/check_synopsis.py

echo
echo "== README agrees with the directory =="
# The other high-level document, and the one that was NOT reconciled -- which is why it
# restated defect counts and went stale behind them twice in a day (D-028). The counts
# now live only in the generated view. What is left is checkable: the layout tree
# against the directory, the report index against docs/project/research/, and every
# link and anchor, including the ones into SYNOPSIS.md.
$PY tools/check_readme.py

echo
echo "== search engine (sqsearch) =="
# The engine gate: geometry against a naive reference, determinism, and a positive
# control that recovers s(5) = 2 + 1/sqrt(2). A run that has not passed this may not
# be recorded. Skipped, not failed, where cargo is absent -- the rest of this repo
# is Python and prose and should stay checkable without a Rust toolchain.
if [ -x sqsearch/target/release/sqsearch ]; then
  out=$(sqsearch/target/release/sqsearch --selftest)
  echo "$out" | sed 's/^/  /'
  grep -q "SELFTEST PASSED" <<<"$out"
  ! grep -q "FAIL" <<<"$out"
else
  skip "sqsearch binary absent: the engine selftest did not run"
fi

echo
echo "== differential: search energy vs validity oracle =="
# sqsearch owns move-loop energy, sqpack owns validity. They never meet in normal
# operation, so nothing would notice if they drifted -- and a search optimising
# against a different notion of overlap than the record is checked with is the
# quietest possible failure. Near-contact pairs only: that is where it could hide.
if [ -x sqsearch/target/release/sqsearch ]; then
  $PY differential_test.py 20000
else
  skip "sqsearch binary absent: search energy was not checked against the validity oracle"
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
if [ ${#SKIPPED[@]} -eq 0 ]; then
  echo "ALL CHECKS PASSED"
else
  echo "CHECKS PASSED, BUT ${#SKIPPED[@]} WERE SKIPPED:"
  for s in "${SKIPPED[@]}"; do echo "  - $s"; done
  if [ "$STRICT" = "1" ]; then
    echo "strict mode: a skipped check is not a passed check" >&2
    exit 1
  fi
  echo "(re-run with --strict to make this an error; the unattended runner does)"
fi
