#!/usr/bin/env bash
# Run everything and check the results that matter.
#
# Usage: ./test.sh [--strict] [--deep] [--jobs N] [--only PATTERN] [--list]
#
# A check this gate could not run is not a check that passed, and the difference has
# to survive a tired reader at 3am. Every skip is recorded and re-listed at the end,
# and the final line says how many there were -- so "ALL CHECKS PASSED" is printed
# only when that is literally true. `--strict` (or GATE_STRICT=1) turns any skip into
# a non-zero exit, which is what an unattended runner uses: a night that silently
# stopped checking the soundness perimeter must not read as a quiet one.
#
# The steps run CONCURRENTLY. Every one of them is read-only -- the renderers and the
# ledger only write under `--update`, and the negative controls now mutate a private
# snapshot rather than this directory -- so there is nothing for them to race over, and
# running them one at a time was leaving nine of ten cores idle for three minutes. The
# machine's core count is the default width; `--jobs 1` restores serial execution at
# both the step and process-pool layers, which is what to use when a failure needs a
# clean transcript.
#
# Output is replayed in the declared order regardless of which step finished first, so
# two runs of the same tree produce the same transcript and a diff of two runs means
# something.
#
# `--only PATTERN` runs just the steps whose name matches, for the inner loop; it is
# refused under `--strict`, because a handover gate that ran four of twenty-five checks
# and printed a pass is the exact failure this file's skip accounting exists to stop.
set -euo pipefail
cd "$(dirname "$0")"

STRICT="${GATE_STRICT:-0}"
DEEP="${GATE_DEEP:-0}"
JOBS="${GATE_JOBS:-0}"
ONLY=""
LIST=0
while [ $# -gt 0 ]; do
  case "$1" in
    --strict) STRICT=1 ;;
    --deep) DEEP=1 ;;
    --jobs)
      [ $# -ge 2 ] || { echo "--jobs requires a value" >&2; exit 2; }
      JOBS="$2"; shift
      ;;
    --jobs=*) JOBS="${1#*=}" ;;
    --only)
      [ $# -ge 2 ] || { echo "--only requires a value" >&2; exit 2; }
      ONLY="$2"; shift
      ;;
    --only=*) ONLY="${1#*=}" ;;
    --list) LIST=1 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
  shift
done
# The handover gate is `--strict`; it must exercise the producer, not only audit the
# committed fixture. A caller can still request `--deep` without making skips fatal.
[ "$STRICT" = "1" ] && DEEP=1
if [ "$STRICT" = "1" ] && [ "$DEEP" != "1" ]; then
  echo "strict mode did not enable deep regeneration" >&2
  exit 1
fi
if [ "$STRICT" = "1" ] && [ -n "$ONLY" ]; then
  echo "strict mode cannot be combined with --only: a partial gate is not a gate" >&2
  exit 1
fi
if [ "$JOBS" = "0" ]; then
  JOBS=$( { command -v sysctl >/dev/null 2>&1 && sysctl -n hw.ncpu; } \
    || { command -v nproc >/dev/null 2>&1 && nproc; } || echo 4 )
fi

require_positive_integer() {
  local name="$1" value="$2"
  case "$value" in
    ''|*[!0-9]*|0)
      echo "$name must be a positive integer, got '$value'" >&2
      exit 2
      ;;
  esac
}

require_positive_integer "--jobs/GATE_JOBS" "$JOBS"

# Several steps are themselves lists of independent multi-second quenches and open
# their own process pool. If both layers use every core, ten concurrent steps can each
# ask for ten workers. `PACK_JOBS` is therefore a PER-STEP CAP, not a shared global
# budget. The default below was measured on the ten-core development host; concurrent
# pool-backed steps can still exceed JOBS in aggregate. `--jobs 1` is the exact serial
# mode. A tool run directly from a shell sees no cap and uses the whole machine.
INNER="${GATE_INNER_JOBS:-0}"
if [ "$INNER" = "0" ]; then
  INNER=$(( JOBS / 3 ))
  [ "$INNER" -lt 1 ] && INNER=1
fi
require_positive_integer "GATE_INNER_JOBS" "$INNER"
export PACK_JOBS="$INNER"

# Record a skip. Called from inside a step, so it reports through the step's file;
# never called for a check that ran.
skip() {
  echo "$1" >> "$RESULTS/$STEP_ID.skip"
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
  PY="uv run --frozen --quiet --with pyyaml==6.0.3 --with jsonschema==4.26.0 python3"
else
  echo "need PyYAML + jsonschema, or uv; install one and re-run" >&2
  exit 1
fi

# ---------------------------------------------------------------------------------
# Steps. Each is a function; the table at the bottom is the only place a step is
# named, so a step cannot be defined and then forgotten out of the run.
# ---------------------------------------------------------------------------------

step_exact_verification() {
  out=$(python3 verify_trump11.py)
  echo "$out"
  grep -q "^VALID: 11 squares, 55 pairs tested" <<<"$out"
  grep -q "14 separated with zero gap, 41 strictly" <<<"$out"
  grep -q "20 corner coordinates exactly on the boundary" <<<"$out"
  grep -q "P(s) == 0 for the published degree-8 polynomial: True" <<<"$out"
  grep -q "s = 3.87708359002281417730789706010096" <<<"$out"
}

step_negative_control() {
  out=$(python3 negative_control.py)
  echo "$out"
  # every perturbation must be rejected by the exact verifier
  grep -q "delta = 1e-100  REJECT" <<<"$out"
  ! grep -qE "delta = 1e-[0-9]+ +accept" <<<"$out"
  # and float64 with a tolerance must have a blind spot
  grep -q "tol=1e-09 .*1e-12: accept" <<<"$out"
}

step_derivation() {
  # sympy is a dev dependency, so `uv run` has it even where the system python3 does
  # not. Asking python3 alone was why this step skipped on a clean checkout.
  if python3 -c "import sympy" 2>/dev/null; then
    out=$(python3 derive_field.py)
  elif command -v uv >/dev/null 2>&1 && uv run --frozen --quiet python -c "import sympy" 2>/dev/null; then
    out=$(uv run --frozen --quiet python derive_field.py)
  else
    out=""
  fi
  if [ -n "$out" ]; then
    echo "$out"
    grep -q "matches sqpack.packings.trump11.U_MIN_POLY: True" <<<"$out"
  else
    skip "sympy not available to python3 or uv: the degree-8 field derivation is unchecked"
  fi
}

step_lp_cell() {
  # The claim the quench rests on: fix the angles and each pair's separating axis and
  # what remains is a linear program. This is the SECOND implementation of it, and that
  # is the point -- sqpack.quench writes one row per pair from half-extents, this writes
  # sixteen from corner pairs, and neither shares constraint-assembly code with the
  # other. D-014 is what happens when a solver is checked only against its own rows.
  # It also reproduces H-019's one-sided slopes through those unrelated rows.
  out=$(uv run --frozen --quiet python lp_cell.py 2>/dev/null || python3 lp_cell.py)
  echo "$out" | sed 's/^/  /'
  grep -q "23 variables, 1056 constraints" <<<"$out"
  grep -q "ALL CHECKS PASSED" <<<"$out"
}

step_frontier_corpus() {
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
}

step_soft_schema_validation() {
  uv run --frozen --quiet python tools/validate_schemas.py 2>/dev/null || $PY tools/validate_schemas.py
}

step_generated_tables_in_sync() {
  $PY tools/render_tables.py --check
}

step_strategy_catalogues() {
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
}

step_lint_floor_python() {
  # The floor is enforced, not aspirational. It has already earned its place: ruff's
  # strict-zip rule found silent truncation in field arithmetic, its closure rule found a
  # capture one edit from a bug, and clippy found an approximation of TAU written as a
  # literal. Skipped, not failed, where the toolchain is absent.
  if command -v uv >/dev/null 2>&1; then
    ( uv run --frozen --quiet ruff check . \
      && uv run --frozen --quiet ruff format --check . \
      && uv run --frozen --quiet basedpyright ) | tail -3
  else
    skip "uv not installed: ruff, ruff-format and basedpyright did not run"
  fi
}

step_lint_floor_rust() {
  if command -v cargo >/dev/null 2>&1; then
    ( cd sqsearch && cargo clippy --release --all-targets --quiet -- -D warnings 2>&1 | tail -2 \
      && cargo fmt --check && echo "  clippy clean at pedantic; rustfmt clean" )
  else
    skip "cargo not installed: clippy and rustfmt did not run"
  fi
}

step_basin_identity() {
  # The piece that makes "basin" a noun. Until a float configuration can be turned into a
  # name, every basin count is a count of floating-point strings and every discovery curve
  # is an artifact of the tolerance used to compare them (D-020). Checked against Trump's
  # packing and against the wrong-basin n=11 configuration the annealer actually produced,
  # not against fixtures invented to pass.
  $PY tools/canonical_check.py
}

step_golden_basin_maps() {
  # The end-to-end pipeline on answers that existed before this code: anneal near a proved
  # optimum, quench onto it, recognise the closed form, and have sqpack accept the packing
  # through code the quench does not share. A golden captured from a previous RUN would
  # only freeze whatever the code did that morning -- D-030 is what that would have frozen.
  # Fast by default: the committed map already holds the sides, so re-deriving every
  # closed form and re-checking it against the proved s(n) costs milliseconds and still
  # refuses a golden edited to make a test pass -- the oracles are mathematics, so the
  # file cannot be adjusted into agreement with them. Regenerating by re-quenching is
  # costly and is what `--deep` is for. `--strict` implies `--deep`, because the runbook's
  # handover gate must exercise the producer before an unattended night. Verified against
  # three tampering modes: a ladder value that does not match the proved one, a gap below
  # it, and a stored basin below it.
  if [ "$DEEP" = "1" ]; then
    $PY tools/golden_basins.py --deep
  else
    $PY tools/golden_basins.py
    echo "  (fast path; ./test.sh --deep re-quenches and diffs the whole map)"
  fi
}

step_basin_atlas() {
  # One real pipeline smoke test plus synthetic store invariants. The synthetic
  # non-converged offer proves the store preserves that status; the strict/deep golden run
  # is the instrument-level regression for D-030's budget-censored census.
  $PY tools/atlas_check.py
}

step_negative_controls() {
  # Every guard in this directory, watched failing. A check nobody has seen fail is not a
  # check, and until now each of these was run once by hand and thrown away. Each control
  # corrupts a private clone of the repository, so this step neither touches the working
  # tree nor cares what else is running beside it.
  $PY tools/negctl.py tools/controls.yaml
}

step_historical_regressions() {
  # Named reproductions for defects that span components or need a focused fixture.
  # Keeping this in the main gate prevents a passing standalone check from becoming a
  # forgotten optional command.
  $PY tools/regression_test.py

  # Command-line boundary checks for the gate itself. `--list` exits before acquiring
  # the activity marker, so these nested probes cannot clear the parent gate's marker.
  local out trace
  if out=$(bash test.sh --jobs -1 --list 2>&1); then
    echo "test.sh accepted --jobs -1" >&2
    return 1
  fi
  grep -q -- "--jobs/GATE_JOBS must be a positive integer" <<<"$out"
  if out=$(bash test.sh --jobs nope --list 2>&1); then
    echo "test.sh accepted --jobs nope" >&2
    return 1
  fi
  grep -q -- "--jobs/GATE_JOBS must be a positive integer" <<<"$out"
  if out=$(GATE_INNER_JOBS=nope bash test.sh --list 2>&1); then
    echo "test.sh accepted GATE_INNER_JOBS=nope" >&2
    return 1
  fi
  grep -q "GATE_INNER_JOBS must be a positive integer" <<<"$out"
  trace=$(bash -x test.sh --jobs 1 --list 2>&1 >/dev/null)
  grep -q "export PACK_JOBS=1" <<<"$trace"
}

step_soundness_perimeter() {
  # Every component that can emit a packing, checked by sqpack through code it does not
  # share. This is the check whose absence let D-014 through: the quench was validated
  # only against its own constraint rows, which is no check when the rows are what the
  # solver got wrong. Replaying that defect against this gate rejects it on sight.
  out=$($PY tools/perimeter_test.py 2>&1); echo "$out"
  grep -q "skipping engine cells" <<<"$out" \
    && skip "soundness perimeter ran without the engine: its sqsearch cells did not run"
  return 0
}

step_defect_log() {
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
}

step_bead_tree() {
  # The work list lives on the tbd-sync branch, outside this directory, so nothing here
  # could see it -- and the one time it went inconsistent (D-025) a person found it by
  # reading `tbd list --spec` and noticing two epics with the same title. Two invariants
  # catch that class: no open bead under a closed parent, no two open siblings with one
  # title. Reads the beads out of git, so it needs no tbd binary, and skips loudly in a
  # checkout that has no tbd-sync branch.
  out=$($PY tools/check_beads.py 2>&1); echo "$out"
  grep -q "^SKIP" <<<"$out" \
    && skip "no bead store reachable: the bead-tree invariants did not run"
  return 0
}

step_skills_mirrored() {
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
}

step_synopsis() {
  # SYNOPSIS.md is the root document and a living one: it restates numbers that live
  # authoritatively elsewhere, which is the exact shape of thing that drifted in D-010,
  # D-017 and D-022. It cannot be generated -- most of it is judgement -- so it is
  # reconciled instead, the way ideas.md is.
  $PY tools/check_synopsis.py
}

step_readme() {
  # The other high-level document, and the one that was NOT reconciled -- which is why it
  # restated defect counts and went stale behind them twice in a day (D-028). The counts
  # now live only in the generated view. What is left is checkable: the layout tree
  # against the directory, the report index against docs/project/research/, and every
  # link and anchor, including the ones into SYNOPSIS.md.
  $PY tools/check_readme.py
}

step_search_engine() {
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
}

step_differential() {
  # sqsearch owns move-loop energy, sqpack owns validity. They never meet in normal
  # operation, so nothing would notice if they drifted -- and a search optimising
  # against a different notion of overlap than the record is checked with is the
  # quietest possible failure. Near-contact pairs only: that is where it could hide.
  if [ -x sqsearch/target/release/sqsearch ]; then
    $PY differential_test.py 20000
  else
    skip "sqsearch binary absent: search energy was not checked against the validity oracle"
  fi
}

step_provenance() {
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
}

step_campaign_record() {
  # Whole-set invariants no per-artifact validation can see: duplicate ids, dangling
  # hypothesis references, rounds naming an unknown series, more than one open series,
  # stale claims, the cross-field verdict rules, the two-way reconciliation between
  # ideas.md and the registry, and whether ledger.md is stale.
  $PY campaign/ledger.py --check
}

# The run order. Slowest first, so the long poles start immediately and the short
# steps fill in behind them rather than the other way round; the transcript is
# replayed in this order too. Measured on a ten-core machine -- re-sort it when the
# "where the time went" table says the order has stopped matching reality.
STEPS=(
  "soundness perimeter|step_soundness_perimeter"
  "lint floor (python)|step_lint_floor_python"
  "basin atlas|step_basin_atlas"
  "historical regressions|step_historical_regressions"
  "negative controls|step_negative_controls"
  "fixed-angle cell is an LP, rebuilt independently|step_lp_cell"
  "bead tree|step_bead_tree"
  "golden basin maps (proved cases, checked against mathematics)|step_golden_basin_maps"
  "basin identity|step_basin_identity"
  "soft-schema validation|step_soft_schema_validation"
  "derivation (needs sympy)|step_derivation"
  "search engine (sqsearch)|step_search_engine"
  "lint floor (rust)|step_lint_floor_rust"
  "exact verification|step_exact_verification"
  "negative control|step_negative_control"
  "frontier corpus|step_frontier_corpus"
  "generated tables in sync with frontier/|step_generated_tables_in_sync"
  "strategy catalogues|step_strategy_catalogues"
  "defect log|step_defect_log"
  "skills mirrored between .agents and .claude|step_skills_mirrored"
  "synopsis agrees with the artifacts|step_synopsis"
  "README agrees with the directory|step_readme"
  "differential: search energy vs validity oracle|step_differential"
  "provenance: recorded commits are reachable|step_provenance"
  "campaign record|step_campaign_record"
)

if [ "$LIST" = "1" ]; then
  for entry in "${STEPS[@]}"; do echo "${entry%%|*}"; done
  exit 0
fi

SELECTED=()
for entry in "${STEPS[@]}"; do
  [ -n "$ONLY" ] && [[ "${entry%%|*}" != *"$ONLY"* ]] && continue
  SELECTED+=("$entry")
done
if [ ${#SELECTED[@]} -eq 0 ]; then
  echo "--only '$ONLY' matched no step; ./test.sh --list shows the names" >&2
  exit 2
fi

# A private directory per run for each step's captured output, exit code, timing and
# skips. Steps run in subshells and cannot append to a parent array, so they report
# through files and the parent does the accounting after the wait. This starts after
# `--list`, so nested CLI regressions never acquire or clear the activity marker.
RESULTS=$(mktemp -d "${TMPDIR:-/tmp}/gate-XXXXXX")

# The gate itself no longer writes anything into this directory: tools/negctl.py used
# to corrupt tracked files in place and now works in a snapshot, and every other step
# is read-only unless asked for --update. The marker stays because campaign/runner.py
# refuses to start a round while a gate is running.
touch .gate-running
trap 'rm -f .gate-running; rm -rf "$RESULTS"' EXIT

echo "python runner: $PY"
echo "running ${#SELECTED[@]} steps, $JOBS at a time; pool cap $INNER per step"

NEEDS_ENGINE=0
for entry in "${SELECTED[@]}"; do
  case "${entry##*|}" in
    step_soundness_perimeter|step_search_engine|step_differential)
      NEEDS_ENGINE=1
      ;;
  esac
done

# Build the engine FIRST, before anything that reads the binary.
#
# It used to be built at its own step, two thirds of the way down -- which meant that
# on a fresh checkout the soundness perimeter ran with no binary and reported
# "sqsearch binary absent, skipping engine cells", and the gate still finished with
# "ALL CHECKS PASSED". The perimeter is the check whose absence let D-014 through, so
# the one check that most needed to run was the one a clean clone skipped. That is
# D-004's shape ("half the test suite was silently unreachable") inside the D-014
# guard. Ordering is the fix: build once, up front, and every later step that needs
# the binary finds it. It is also why this is not one of the concurrent steps: three
# of them read the binary, and a build racing its readers is the same bug again.
if [ "$NEEDS_ENGINE" = "1" ]; then
  echo
  echo "== building sqsearch =="
  STEP_ID="build"
  if command -v cargo >/dev/null 2>&1; then
    ( cd sqsearch && cargo build --locked --release --quiet )
    echo "  built sqsearch/target/release/sqsearch"
  else
    skip "cargo not installed: the engine, perimeter engine cells, differential test and selftest cannot run"
  fi
fi

# --- the concurrent run ------------------------------------------------------------
#
# Every step is read-only, so the only shared state is the terminal, and that is what
# the per-step capture files are for. A step's exit status is its verdict: the bodies
# above assert with `grep -q` under `set -e`, and that is preserved inside a subshell.
run_step() {
  local id="$1" name="$2" fn="$3" started
  started=$(date +%s)
  STEP_ID="$id"
  if ( set -euo pipefail; "$fn" ) > "$RESULTS/$id.out" 2>&1; then
    echo 0 > "$RESULTS/$id.rc"
  else
    echo $? > "$RESULTS/$id.rc"
  fi
  echo "$(( $(date +%s) - started ))" > "$RESULTS/$id.t"
}

index=0
for entry in "${SELECTED[@]}"; do
  # Throttle to $JOBS concurrent children. `wait -n` returns as soon as any one
  # finishes, so a fast step frees its slot immediately instead of waiting for a
  # batch boundary.
  while [ "$(jobs -rp | wc -l)" -ge "$JOBS" ]; do wait -n || true; done
  run_step "$index" "${entry%%|*}" "${entry##*|}" &
  index=$((index + 1))
done
wait

# --- the transcript, replayed in declared order ------------------------------------
FAILED=()
SKIPPED=()
TIMINGS=()
index=0
for entry in "${SELECTED[@]}"; do
  name="${entry%%|*}"
  echo
  echo "== $name =="
  cat "$RESULTS/$index.out"
  rc=$(cat "$RESULTS/$index.rc")
  secs=$(cat "$RESULTS/$index.t")
  TIMINGS+=("$secs|$name")
  [ "$rc" != "0" ] && FAILED+=("$name (exit $rc)")
  if [ -f "$RESULTS/$index.skip" ]; then
    while IFS= read -r line; do SKIPPED+=("$line"); done < "$RESULTS/$index.skip"
  fi
  index=$((index + 1))
done
if [ -f "$RESULTS/build.skip" ]; then
  while IFS= read -r line; do SKIPPED+=("$line"); done < "$RESULTS/build.skip"
fi

echo
echo "== where the time went =="
printf '%s\n' "${TIMINGS[@]}" | sort -rn | head -8 | while IFS='|' read -r secs name; do
  printf '  %5ss  %s\n' "$secs" "$name"
done
printf '  %5ss  TOTAL (wall)\n' "$SECONDS"

echo
if [ ${#FAILED[@]} -ne 0 ]; then
  echo "${#FAILED[@]} STEPS FAILED:"
  for f in "${FAILED[@]}"; do echo "  - $f"; done
  exit 1
fi
if [ ${#SKIPPED[@]} -ne 0 ]; then
  echo "GATE COMPLETED, BUT ${#SKIPPED[@]} CHECKS WERE SKIPPED:"
  for s in "${SKIPPED[@]}"; do echo "  - $s"; done
  if [ "$STRICT" = "1" ]; then
    echo "strict mode: a skipped check is not a passed check" >&2
    exit 1
  fi
  if [ -n "$ONLY" ]; then
    echo "${#SELECTED[@]} of ${#STEPS[@]} STEPS COMPLETED (--only '$ONLY'; skipped checks make this incomplete)"
    exit 0
  fi
  echo "(re-run with --strict to make this an error; the unattended runner does)"
elif [ -n "$ONLY" ]; then
  echo "${#SELECTED[@]} of ${#STEPS[@]} STEPS PASSED (--only '$ONLY'; this is not a full gate)"
else
  echo "ALL CHECKS PASSED"
fi
