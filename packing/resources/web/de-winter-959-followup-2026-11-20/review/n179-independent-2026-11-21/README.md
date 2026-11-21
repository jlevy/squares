# Independent N179 Review Evidence

The
[Stage 4 review](../../../../../../docs/project/reviews/review-2026-11-21-n179-independent-algebraic-certificate.md)
accepts the 179-square construction at `S=13.88096037155557959469669157...`. Its
independent replay proves 716 wall inequalities and all 15,931 unordered pair
separations, with nine predeclared controls.
The deciding code imports only the Python standard library; no contributor program runs.

## Source and Replay

The input is the existing packet’s
[original mathematical file](../../source/n179.minpoly.json.gz), SHA-256
`28edf9561e87037b5c681e4ff0051a1bd1b8e5401c1a8376fe2e66c2c18663d1`. The
[working replay source](../../../../../campaign/issue-intake/de-winter-959-2026-11-20/review/n179_replay.py.txt)
is the separately linted copy; from `packing/`, with the project’s Python 3.14.7
interpreter and a fresh external output directory:

```bash
uv run --frozen --all-extras --group dev python -B \
  campaign/issue-intake/de-winter-959-2026-11-20/review/n179_replay.py.txt \
  --source resources/web/de-winter-959-followup-2026-11-20/source/n179.minpoly.json.gz \
  --output "$TMPDIR/n179-independent-replay"
```

Set `TMPDIR`, `CARGO_TARGET_DIR` and `UV_CACHE_DIR` to dedicated writable external
scratch directories before running.
The numerical worker enforces a 300-second wall cap, returns 124 with partial progress
if capped, and refuses an existing output path.
For a monitored run, start it with `--gate "$TMPDIR/n179-start"`, attach the local
memory guard to its PID in observe-only mode, then create that fresh gate file.
The memory guard is an observer and is not a mathematical dependency.

## Retained Runs

- [Initial plan](frozen/plan.md) and [manifest](frozen/manifest.json): frozen before
  outcomes.
- [Initial code](frozen/replay.py.txt) and
  [failure receipt](frozen/run-01/receipt.json): the reviewer’s unsupported
  `m`-as-class-index assumption failed before geometry.
- [Parser amendment](frozen/amendment-v2.md),
  [second manifest](frozen/manifest-v2.json),
  [deciding frozen code](frozen/replay-v2.py.txt), and
  [accepted receipt](frozen/run-02/receipt.json): each square’s own `u` is its
  orientation; full geometry accepted in 2.738 seconds.
- [Runnable receipt](runnable/run-03/receipt.json) and
  [comparison](runnable/comparison.json): full geometry accepted in 2.784 seconds; all
  mathematical receipt fields match.
- [Wall ledger](frozen/run-02/walls.json.gz) and
  [pair ledger](frozen/run-02/pairs.jsonl.gz): one compressed copy of each exact margin
  ledger. Decompressed bytes match the successful frozen and runnable runs; the duplicate
  ledgers are omitted.
- [SVG overlay](frozen/run-02/overlay.svg): visually inspected, approximate display
  only.
- [Ruff](runnable/ruff-check.txt), [format](runnable/ruff-format.txt), and
  [BasedPyright](runnable/basedpyright.txt): zero findings for the runnable checker.

The successful frozen checker SHA-256 is
`f5a657ad1f997f0f460d0030a5d05a48be45d80a74fd919968363e392d48cd99`; the runnable checker
SHA-256 is `8f719595eb990d2d0e1a0b53c18bf22500e269919e5f50449428bd4652ba5ccc`. Frozen
programs and documents remain exact original bytes; historical local paths in those
forensic artifacts are not the portable replay interface above.
`frozen/initial-review.md.txt` preserves the blind findings before later comparisons.
The independent implementation and the retained source are shared inputs, not shared
producer code. The later maintained side comparison is disclosed in the active review.

`env.sh` is retained solely to satisfy the original freeze manifest.
It describes the original host and is not a portable environment setup script.
The package manifest names the compressed ledger encodings and their original hashes.
No optimality, stationarity, historical priority or GeiserX starting-input identity is
proved by the finite replay.
Its result is the existence of this packing at `S`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
