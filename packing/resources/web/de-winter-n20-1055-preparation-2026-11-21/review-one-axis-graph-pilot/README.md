# Independent Sixteen-Case Separation-Graph Pilot

The first frozen run completely enumerates the Boolean separation choices for sixteen
predeclared canonical cases.
It retains 1,280 models and passes all seventeen controls.
Fourteen cases reduce by unit propagation to a fully satisfied formula with free bits;
cases 244 and 3670 instead produce contradictions and have no models.
None of these selected cases needs a recursive split.
The truth-table controls also exercise branching.

| Case index | Edges | Clauses | Models | Forced variables | Remaining free bits |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 22 | 92 | 128 | 15 | 7 |
| 244 | 21 | 93 | 0 | 7 | contradiction |
| 489 | 21 | 97 | 128 | 14 | 7 |
| 734 | 19 | 77 | 64 | 13 | 6 |
| 978 | 19 | 78 | 64 | 13 | 6 |
| 1223 | 19 | 83 | 4 | 17 | 2 |
| 1468 | 20 | 83 | 8 | 17 | 3 |
| 1712 | 20 | 85 | 4 | 18 | 2 |
| 1957 | 21 | 99 | 16 | 17 | 4 |
| 2202 | 22 | 103 | 128 | 15 | 7 |
| 2446 | 22 | 103 | 32 | 17 | 5 |
| 2691 | 21 | 92 | 64 | 15 | 6 |
| 2936 | 21 | 90 | 64 | 15 | 6 |
| 3180 | 21 | 93 | 64 | 15 | 6 |
| 3425 | 21 | 82 | 512 | 12 | 9 |
| 3670 | 20 | 92 | 0 | 10 | contradiction |

The [full receipt](results/graph-pilot.json.gz) retains every model, exact case IDs,
input row and clause identities, control model sets, search counters and timings.
Every model passes a separate literal-by-literal check of all original clauses.
The sixteen indices were fixed by `floor(i*3670/15)` before execution; no graph outcome
was used to select them.

This proves only the sixteen finite model sets.
A Boolean model is a separation choice not excluded by these necessary clauses, not a
feasible placement. The full 3,671-case graph census and the source’s 273,584 total
remain unverified. Geometric-rule extraction and graph-to-bank applicability are also
open. The one-axis theorem has not cleared Stage 4.

## Input, Exposure and Reproduction

The input is the accepted
[complete case-to-clause receipt](../review-one-axis-case-clauses/README.md).
It is not copied into this directory.
The checker hashes all 24,888,016 expanded bytes using 64 KiB blocks, then parses all
3,671 case rows with a bounded incremental decoder.
Only the sixteen selected cases are retained.
The observed maximum decoder buffer was 81,295 bytes, below the 1 MiB ceiling.

The source receipt’s near-grid and local-path premises remain prerequisites.
The domain is `0 < tan(theta/2) <= 1/24`, one aligned tile and nineteen independently
signed common-magnitude tilts in a hypothetical board `S < 5`.

The reviewer had previously read the producer’s solver.
This is separately written first-party search and literal-level checking, not a blind
review. No contributor code, solver or certificate bank was imported or executed.

The [checker](checker.py.txt) is byte-identical to `check_graph_pilot.py`. The
[selection plan](graph-pilot-plan.md), [plan freeze](graph-pilot-plan-freeze.json),
[implementation and proof](implementation-freeze.md), [execution freeze](freeze.json)
and [original checksums](original-input-sha256sums.txt) retain the pre-execution record.
The [retention map](retention.json) resolves their historical local filenames to the
maintained files.

From this directory, use isolated project Python 3.14 and the
[replay supervisor](../review-one-axis-case-clauses/replay-with-memory-guard.py.txt).

```bash
"$PYTHON" -I -B checker.py.txt \
  --input ../review-one-axis-case-clauses/results/case-clauses.json.gz \
  --output "$OUT/graph-pilot.json.gz"
```

Use fresh output paths, one worker and external scratch/cache directories.
The frozen limits are 60 supervised seconds, 55 internal seconds, 0.25 GiB owned process
tree, 0.23 GiB worker peak RSS, pressure-1 admission and stop at pressure 2. The
ceilings are one million search nodes, 100,000 models overall and 50,000 per case.
The retained [supervisor](strict-supervisor.py.txt) records the actual launcher and its
host memory-guard dependency.

## Observed Execution

Admission was recorded at `2026-11-23T01:26:26+00:00`. The supervisor and worker/guard
results are retained verbatim, including timestamps.
Worker and guard exited zero, with no cap or recorded intervention.

The run took 0.767 supervised seconds, 0.486 worker seconds and 0.463 CPU seconds.
Worker peak RSS was 31,211,520 bytes (29.77 MiB). The complete sixteen case searches and
direct model audits took 0.217 seconds in total.

The guard required pressure 1 before releasing the worker.
The subsecond job has only the initial periodic sample, taken before release; it does
not measure the worker’s peak footprint.
Peak worker memory above is from process accounting, not the guard’s startup sample.
No claim of continuous sampled pressure or a sampled peak is made.

[Supervisor](results/pilot-execution-01.run.json),
[admission](results/pilot-execution-01.preflight.json),
[journal](results/pilot-execution-01.jsonl),
[observer log](results/pilot-execution-01.guard.stderr),
[worker log](results/pilot-execution-01.worker.log).
The [identity record](results/graph-pilot.json.gz.identity.json) binds the 22,344-byte
original receipt to its unchanged 6,818-byte deterministic gzip; the worker verified a
streamed decompression roundtrip.

A full-roster run requires a separate implementation and freeze with complete case
coverage and appropriate limits.
The pilot freeze does not authorize broadening its selection.

## Compressed Files

| Stored path | Origin | Git blob of original bytes | SHA-256 of original bytes |
| --- | --- | --- | --- |
| `results/graph-pilot.json.gz` | receipt | `77ef180183fb3c82c1613db7b0197414c284a386` | `d72757517d73ea27d483b5c10efe65de9b5072753a8b2c879f43ec7ecfe08352` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
