# The Stage 4 Review of T-046: Programs and Receipts

These are the programs and receipts of the stage 4 review of `T-046`’s 46 standing
rectangle-density certificates and of the census route’s mass condition at
$n - 1/1000$
([the review](../../../../../../docs/project/reviews/review-2026-10-26-wand125-rectangle-certificates-t046.md)).
They were written on 26 October 2026 by the review lane `w-t046-review-1026` (bead
`think-buaj`), Claude Opus 5.5 (`claude-opus-5-5`) at the strong sub-agent tier.

The certificates are the ones this packet retains, at
[`39d8ecc`](https://github.com/wand125/square-packing-bounds/tree/39d8ecc74d651b54ec977c331c8f2015b442a6c4),
and the ten of the
[27 September packet](../../../wand125-rectangle-certificates-2026-09-27/README.md)
that `T-046` still cites. The census rows, receipts and control receipts are
`packing/benchmarks/measure-verifier/census/`.

All programs ran with CPython 3.14.7 (`packing/.venv/bin/python3 -I`) from `packing/`
of a checkout at `main` `91831e174`, at most two processes at a time. None writes
anywhere but its `--out` file.

## What Each Program Does

| Program | Role | What it read | Receipt |
| --- | --- | --- | --- |
| `certificates_t046.py` | premise check: every premise but coverage in exact rationals, and the source’s accepting-run records against the preflight | the 48 retained candidates, their metadata, summaries and per-angle rows; both packet READMEs and tree manifests; the preflight receipt | `outputs/certificates.json` |
| `route_t046.py` | checks 1 to 6 and 8 of the format T route review’s section 5, with the mass condition as widened | the 46 census rows, receipts and control receipts; the candidates; the case records | `outputs/route.json` |
| `exact_capture_t046.py` | the review’s exact capture evaluator, a module | a candidate | (run by `probes_t046.py`) |
| `probes_t046.py` | samples coverage, decides nothing: the receipts’ captures recomputed, FT-11 over all 200 centres, corners, uniform poses and a local search | the candidates; the census rows, receipts and control receipts | `outputs/probes.json` |
| `rerun_t046.py` | six census directions re-run with a binary built here, compared field for field | the binary; the candidates; the census receipts | `outputs/reruns.json` |

`exact_capture_t046.py` was written from `packing/sqverify_fast/SOUNDNESS.md`’s
statement of the density and the theorem’s square alone. Its author had not opened
`sqpack.rectangle_density`, the crate’s `oracle.rs` or `exact.rs`, or Tokoharu’s
`verify.cpp` when it first agreed with the receipts, and it imports nothing from this
repository.

## How to Run Them

From `packing/`, with `P` this folder’s `programs/` and `O` its `outputs/`:

```sh
.venv/bin/python3 -I $P/certificates_t046.py --packing . --out $O/certificates.json
.venv/bin/python3 -I $P/route_t046.py --packing . --out $O/route.json
.venv/bin/python3 -I $P/probes_t046.py --packing . --out $O/probes.json --workers 2
cargo +1.98.0 build --release -j 2 --manifest-path sqverify_fast/Cargo.toml
.venv/bin/python3 -I $P/rerun_t046.py --packing . \
  --binary sqverify_fast/target/release/sqverify-fast --out $O/reruns.json
```

Each exits 0 and writes `"status": "PASS"` when every check holds.
`probes_t046.py` is seeded (`20261026`), so a re-run evaluates the same poses.
The binary built at `main` `91831e174` had SHA-256 `567a0fd5…`, the build that ran the
22 rows of 25 October and all 46 controls.

## What They Found

- `certificates.json`: all 48 candidates pass, with no problem. Masses are $n - 1/100$
  but for `rect_n27_L56` and `rect_n21_L49875`, at $n - 1/1000$.
- `route.json`: all 46 rows pass every condition. Only `rect_n27_L56` needs the widened
  mass condition, and no case record’s verified lower bound moves.
- `probes.json`: 184 receipt captures equal as rationals, FT-11 holds for all
  46, and no sampled pose captures less than $10001/10000$; the least found is
  $1.000512$ (`rect_n30_L5865`, found by the local search from its control centre at direction 133, whose own capture is $1.000592$).
- `reruns.json`: all six directions reproduced in every field but the timings.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
