# The Mathematical Review’s Programs, 23 October 2026

These are the programs the
[mathematical review of 23 October 2026](../../../../../../docs/project/reviews/review-2026-10-23-wand125-n31-fine-net.md)
of wand125’s `mixed_n31_L59775` ($s(31) \ge 2391/400$) wrote and ran, kept as they ran,
with what each wrote in [`outputs/`](outputs/). The review was the stage 4 mathematical
review lane of the import think-wop1 (bead think-oc25): Claude (Anthropic), at the
`tbd-strong-max` tier and maximum reasoning, prompted separately from the records lane
that registered the entry.

Each program ran under the project interpreter (CPython 3.14.7, `python3 -I`), at
`nice -n 19` and one process at a time, reading the packet’s retained candidate
(`../../release/certificates/mixed_n31_L59775/candidate.json.gz`) and, for two of them,
the source’s run and control logs beside it, as data.
No program imports or runs anything of the source, of this repository’s `sqverify_fast`
crate or of `devtools`; the standard library does all of the deciding arithmetic, and
numpy appears only in the float pass of `capture.py`, which chooses cells and decides
nothing.

## What Its Authors Read

Before writing these programs the lane read the mathematics (the certificate semantics
in the source’s README and the proof in its `SPEC.md`, sections 2 to 4, retained by the
2026-10-06 check2 packet), the certificate format (the same `SPEC.md`, section 2, and
the candidate itself), the source’s receipts and logs (to compare, not to decide), the
declared-net soundness review of the maintained crate and its fix check (6 October),
and, of other results on this route, the n68 and n84/n85 reviews of 19 October and the
opening of the review of ten check2 certificates of 6 October.
Those reviews describe the maintained crate’s admission conditions, its per-bin domain
and its quadrant reduction in words; none of them reproduces its code.
The lane did not read the source’s adapted crate (pinned, unopened), this repository’s
`packing/sqverify_fast/` source or `SOUNDNESS.md`, or any program of `devtools`, before
these programs had run, and it did not read the programs of the 14 October fine-net
review. So the capture checker is clean-room with respect to the producer’s checker,
which is this repository’s crate adapted: written from the mathematics and the format
alone. The source’s commit names Claude as co-author, and these programs were written by
a Claude agent: the authorship overlaps the producer’s at the system family.

## The Programs

| Program | What it does | Reads | Output |
| --- | --- | --- | --- |
| [`n31_exact.py`](programs/n31_exact.py) | The module the others import: the candidate read exactly (duplicate keys, floating-point tokens and non-string rationals refused), the eight D4 images and the merged expansion, the net direction as integers $(C, S, E)$, and $r(t)$ | (a module) | — |
| [`premises.py`](programs/premises.py) | Every exact premise of the file and the measure: identity, claim, rows, positivity, mass sum and its gap, the merged expansion’s integral and its D4 invariance, the net’s premises, nonempty per-bin domains | the candidate | `premises.json` |
| [`net.py`](programs/net.py) | The reduction from a packing to the capture condition, node by node: the bins abut and reach past $\tan(\pi/8)$, the core fits strictly inside at both ends of all 2,073 bins (exact $z$), every $a_j$ lies where $r$ increases, and the quadrant’s four quarter-turn images tile every node’s domain | the candidate | `net.json` |
| [`n31_geometry.py`](programs/n31_geometry.py) | Integer formulas, with no division, for the area of a rotated box intersected with a rectangle (sixteen corner terms) and for chords of lines in the rotated frame | (a module) | — |
| [`n31_brute.py`](programs/n31_brute.py) | A second exact method for one core’s capture: Sutherland–Hodgman clipping and the shoelace formula in Fractions | (a module) | — |
| [`geometry_selftest.py`](programs/geometry_selftest.py) | Holds `n31_geometry` to brute-force clipping on random and adversarial cases at nine directions | — | `geometry-selftest.json` |
| [`sample_plan.py`](programs/sample_plan.py) | The stratified sample of directions, fixed before any ran: one direction drawn per stratum by a generator seeded from the candidate’s SHA-256, plus named directions | the candidate; the run log, to name the source’s tightest and heaviest directions | `sample-plan.json` |
| [`capture.py`](programs/capture.py) | Decides the capture condition at each direction it is given, over the whole quadrant domain, by a float-guided branch and bound whose every leaf is decided in exact integers; also the mutants (`--mass-scale`, `--drop-row`) | the candidate | `capture-<tag>-<j>.json` |
| [`bound_selftest.py`](programs/bound_selftest.py) | Holds `capture.py`’s exact cell bound to the second method: for random cells at four directions, the bound must not exceed the exact capture at any of seven points of the cell | the candidate | `bound-selftest.json` |
| [`run_after_sample.sh`](programs/run_after_sample.sh) | Runs the controls, the sharp control, `source_log_points.py`, `bound_selftest.py` and `summarize.py` in order | — | `controls.stdout.txt` and the files of those programs |
| [`source_log_points.py`](programs/source_log_points.py) | Single poses the source’s logs name, evaluated by `n31_brute`: the axis row’s argmin, the tightest rows’ least-bound boxes, and every control witness against its logged exact rational | the candidate; `check2/run.jsonl.gz`; `check2/control-197_200.jsonl.gz` | `source-log-points.json` |
| [`summarize.py`](programs/summarize.py) | Tabulates the receipts beside the source’s log; decides nothing | the receipts; the run log; the plan | `summary.json` |

## How to Run Them

From this directory, with `$PY` the project interpreter and `$C` the retained candidate
`../../release/certificates/mixed_n31_L59775/candidate.json.gz`:

```sh
$PY -I programs/premises.py $C 4a7df269037a6449ba2d4bee2b6a76962df097c1515025545d4ca4cfcc39be3b outputs/premises.json
$PY -I programs/net.py $C outputs/net.json
$PY -I programs/geometry_selftest.py outputs/geometry-selftest.json 2000
$PY -I programs/sample_plan.py $C ../../release/certificates/mixed_n31_L59775/check2/run.jsonl.gz 96 outputs/sample-plan.json > outputs/sample-directions.txt
$PY -I programs/capture.py $C outputs $(cat outputs/sample-directions.txt) --cpu-limit 900 --max-nodes 3000000
bash programs/run_after_sample.sh $PY ../../release/certificates/mixed_n31_L59775
```

`run_after_sample.sh` runs, in order and one at a time, the mutants (every mass scaled
by $99/100$ at five directions; the heaviest row removed at three; the sharp control),
`source_log_points.py`, `bound_selftest.py` and `summarize.py`, and writes
`outputs/program-digests.sha256`.

The sample ran in two invocations of the same `capture.py` (SHA-256 `78342918…8ce9`).
The first was stopped by the session’s time limit on background commands after its 18th
direction (0 to 296; `capture-original.stderr.txt` is empty and its `time` line was lost
with it), and direction 319, which it had begun, left no receipt.
The second ran the 104 directions without a receipt (`sample-directions-resumed.txt`),
appending to the same stdout.
A receipt is written only when its direction is decided, and the trees are deterministic
(direction 0’s run here repeated a trial’s node and leaf counts exactly), so the split
changes nothing in the results.

## What They Printed

| Program | Printed (the full record is the output file) | CPU-seconds |
| --- | --- | ---: |
| `premises.py` | `PREMISES_HOLD all checks true` | 0.18 |
| `net.py` | `NET_COVERS all checks true` | 0.31 |
| `geometry_selftest.py` | `PASS {'area': 18000, 'chord_sigma': 18000, 'chord_omega': 18000, 'nonzero_area': 4346, 'partial_area': 3570}` | 2.65 |
| `sample_plan.py` | the 122 directions, in `sample-directions.txt` (seed 5367712863739339849) | 0.2 |
| `capture.py`, the sample | one line per direction in `capture-original.stdout.txt`: all 122 `VERIFIED` | 1,909.7 |
| `capture.py`, $99/100$ | `REFUTED` at 0, 1, 676, 1036 and 2072 (`controls.stdout.txt`) | 1.9 |
| `capture.py`, row 33 removed | `REFUTED` at 1, 1036 and 2072 | 1.2 |
| `capture.py`, the sharp control | `sharp control at direction 1841, scale 499891977421/500000000000`, then `REFUTED` | 7.5 |
| `source_log_points.py` | `CONSISTENT axis 1.001298750503704 tightest 12 control witnesses 31` | 3.2 |
| `bound_selftest.py` | `PASS 24 cells least gap 6.796443483983797e-22` | 10.6 |
| `summarize.py` | `planned 122 decided 122 verified 122 not verified [] missing []` and the controls’ verdicts (`summary.stdout.txt`) | 0.1 |

The CPU of each `capture.py` direction is its receipt’s `cpu_total`; the others are the
programs’ own counts or the shell’s `time` (user plus system).
The sample’s second invocation took 1,487.7 CPU-seconds by `time` for its 104 directions
(`capture-original-resumed.time.txt`), equal to its receipts’ sum to within its
start-up. Every stderr file is empty.

The last line of `run_after_sample.sh`, `sha256sum programs/*`, failed because Python
had written `programs/__pycache__/` when the programs imported each other; the cache was
deleted and `program-digests.sha256` was written with `sha256sum programs/*.py
programs/*.sh`. The script is kept as it ran.

**Runs that decided nothing.** Before `capture.py` was frozen, eleven development trials
of earlier drafts ran at directions 0, 1, 5, 20, 60, 296, 676 and 2072 and on one
$99/100$ mutant, about 330 CPU-seconds in all.
They chose the method and its price; their code is not kept, and no record cites them.
Where the final program repeated a trial’s direction, the node and leaf counts were
equal.
Five one-off summaries of the candidate and the logs (row densities and positions,
log statistics), a few seconds in all, were run in scratch space; they decide nothing
and are not kept.

**Registration.** `summarize.py` decides nothing and is registered nowhere.
The premise programs, the capture checker and the pose evaluator are registered in
`packing/frontier/verifiers.yaml` with their `independence` records, and the sample’s
evidence entry is cited by the case record `n-031.md`, not by the result, because a
sample sets no rung.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
