# cfcheck

## What it checks

An independent exact checker for the closed-form square-packing certificates in
`problems/closed-form/` of this repository: [SPEC.md](../SPEC.md),
[intervals.json](../intervals.json), and the per-interval release assets.
It checks family structure, wall periods, savings, global/local agreement,
region coverage, root lattices, midpoint tilings, and every leaf's named test.
The `coverage` command separately checks all 34 parameter intervals and sample
closed-form values; run it as well as all required `interval` commands.

ACCEPT means that the named sufficient test proves the whole leaf box safe:
either no admissible unit square exists there (EMPTY), or its measure is at
least 1 throughout, under the test's hypotheses. REFUSE means that a required
check failed or could not be established; it need not exhibit a counterexample.
There is no fallback to another leaf test and no silent repair of malformed data.
Only complete structural checks plus acceptance of every leaf establish the
certificate for an interval; all 34 intervals are needed for the full claim.

## Independence

Written from SPEC.md and the published bundles only; shares no code with the
original checkers (`replay4d`, `seam4d_core`, `validate_family.py`), which were
not read. Written with AI assistance (OpenAI Codex), reviewed by the author,
and not peer reviewed.

## Results so far

Only intervals 1 and 34 of 34 have been fully replayed with this checker.
All leaves were accepted, with zero refusals:

| Index | Interval | Roots | Leaves | Refusals |
| --- | --- | ---: | ---: | ---: |
| 1 | (0, 0.02] | 40,257 | 1,653,457 | 0 |
| 34 | (0.99, 1] | 50,787 | 1,485,224 | 0 |

The production build used `rustc 1.99.0`. Unchanged JSON reports and checkpoint
hashes are in [receipts/](receipts/README.md). Interval 1 includes 24,226 roots
resumed from checkpoints written by earlier runs of this same checker on the same inputs.

## How to run

Build and test from this directory (tests require no large bundles):

```sh
cargo build --release --locked
cargo test --release --locked
```

With dependencies cached, add `--offline` to both commands. Run the binary from
`problems/closed-form/`, with release assets unpacked beneath `assets/`:

```sh
indep-checker/target/release/cfcheck coverage intervals.json
mkdir -p work
indep-checker/target/release/cfcheck interval assets/interval_0.99_1 \
  --intervals intervals.json --index 34 --threads 2 --chunk-leaves 1 \
  --progress --progress-file work/interval34 --json work/interval34.json
```

General form: `cfcheck interval <assets-dir> --intervals intervals.json --index N
--threads T --progress --progress-file <prefix> --json <report>`.
Paths must be relative to, and remain within, the current working directory.
To continue an interrupted run, repeat the command with `--resume` and the same
progress prefix; interval checkpoints have one suffix per region. Input and root
hashes are checked, and domain and tiling checks always rerun. Checkpoints are
trusted prior computations, so retain them only from trusted runs of this checker.
`--chunk-leaves N` defaults to 64; use 1 for intervals with heavy leaves to spread
them across workers. Completed roots are committed in record order.

The JSON has input SHA-256 values, full `roots`, `leaves`, and `leaf_kinds`,
`checked_leaf_kinds` (including resumed roots), `resumed_roots`, and `refusals`.
`details.regions` gives per-region accepted roots and timings for newly computed
leaves. Full success requires `ok: true`, `partial: false`, `incomplete: false`,
and empty `refusals` and `interruptions`, with final `CFCHECK OK` (exit 0).
`--max-roots` and kind filters produce `CFCHECK PARTIAL`, also exit 0: this is
not full acceptance. `--deadline SECONDS` can stop a run as incomplete (exit 1).
Verification refusals exit 1; input, parsing, and argument errors exit 2.

## Cost

Seconds per newly computed leaf, weighted across regions from the two receipts:

| Kind | Interval 1 | Interval 34 |
| --- | ---: | ---: |
| B3D | 0.756994 | 0.939796 |
| B3T:x | 0.550303 | 1.08119 |
| B3T:y | 0.442553 | 1.22559 |
| B3U:x | 0.0780705 | 0.208899 |
| B3U:xy | unmeasured | 0.427081 |
| B3U:xyh | unmeasured | 8.20827 |
| B3U:y | 0.0560889 | 0.142029 |
| B4U | 1981.35 | unmeasured |
| CORE | 0.00205324 | 0.00627767 |
| CORE1:P | 0.114041 | 0.184269 |
| CORE1:Tx | 0.0833447 | 0.638032 |
| CORE1:TxHy | unmeasured | 0.469487 |
| CORE1:Ty | 0.122898 | 0.689004 |
| CORE1:x | 0.0257847 | 0.146039 |
| CORE1:xy | unmeasured | 0.140538 |
| CORE1:xyh | unmeasured | 0.401492 |
| CORE1:y | 0.0202855 | 0.13178 |
| EDGE | 1.13431e-05 | 0.000735017 |
| EMPTY | 4.49253e-06 | 0.00063293 |
| EX:CORE | unmeasured | unmeasured |
| EY:CORE | unmeasured | unmeasured |

These are summed per-leaf elapsed seconds on worker threads, an approximation
to CPU cost, not operating-system CPU measurements. Resumed leaves have no timing
in the final report. Measured work totals 85.80 worker-hours for interval 1
(900,992 timed leaves) and 156.21 for interval 34 (1,485,224 leaves),
or 242.02 hours recorded. The timings of the 24,226 resumed roots of interval 1
are not in the report, so the total for the two intervals is larger. The cost of
other intervals depends on their mix of leaf kinds and has not been measured.

Memory is approximately 50-250 MB per worker thread with per-leaf cache clearing.
B4U leaves take minutes to over an hour each; spread them across workers with
`--chunk-leaves 1`. Wall time also depends on worker count and load balance.

## Limitations

Only 2 of 34 intervals have been replayed independently. This is not a formal
proof checked by a proof assistant. Correctness still depends on the specification,
implementation, compiler, and trusted resumed computations.
Arithmetic decisions use exact integers and rationals: checked i128 operations
fall back to arbitrary-precision integers/rationals on overflow, with exact
polynomials, Sturm sequences, and algebraic-root isolation. No floating point is
used in mathematical accept/refuse decisions; floating point is used for timing
and progress statistics. Metadata such as `eps` does not alter the measure.
