# The Review’s Programs and Receipts

The programs the [soundness review of 23 October 2026](../../../../../docs/project/reviews/review-2026-10-23-wand125-sqverify-continuous-soundness.md)
of wand125’s `sqverify_continuous` wrote and ran, and what they printed. They were
written by Claude (Anthropic), the stage 4 validation lane `c-review-sqvc-1023` of the 23
October 2026 intake pass (think-xzob), tier `tbd-strong-max`, maximum reasoning, after
reading the verifier’s source in this packet and its v3 sibling, this repository’s copies
of the modules it reuses, and the source’s published summaries and logs; they import and
copy none of the source’s code. `bounds_probe.py` transcribes the source’s box bound,
because the transcription is what it tests.

None of them decides a claim. Three are registered in
[`verifiers.yaml`](../../../../frontier/verifiers.yaml) as premise programs:
`V-sqverify-continuous-review-premises` (`premises.py`, `candidates.py`, `custody.py`),
`V-sqverify-continuous-review-probe` (`bounds_probe.py`, `probe_suite.py`) and
`V-sqverify-continuous-review-judge` (`judge_run.py`). No evidence entry cites them; the
review does. `run_timed.py` is the clock and decides nothing.

Every program runs on Python 3.14 with the standard library only, from any directory,
and reads untrusted inputs, so run it with `-I`. Paths below are relative to this
directory unless absolute; `SQ` is the repository root.

## Programs

| Program | What it does | What it read | Receipt |
| --- | --- | --- | --- |
| [`custody.py`](programs/custody.py) | Source digests of v3 and v4 by `build.rs`’s rule, every crate file’s Git blob against this repository’s `packing/sqverify_fast` at three revisions, and the top-level Rust items of `slab.rs` and `main.rs` that differ between v3 and v4 | the two packets’ crates; `git ls-tree` of this repository | [`custody.json`](receipts/custody.json) |
| [`premises.py`](programs/premises.py) | Every exact premise of the argument for T-145’s, T-157’s, a control’s and T-192’s parameters, the 86 default roots and their binary64 enclosures, and T-192’s `run_key` recomputed and compared | the parameters; the n = 28 packet’s `check1/summary.json` and `control-summary.json` | [`premises.json`](receipts/premises.json) |
| [`candidates.py`](programs/candidates.py) | Builds the n = 40 candidates and their 985/1000 controls from this repository’s copies of the two densities, in the source’s row order, and decides their facts and T-192’s certificate’s | the rect_n40_L67 and 6718 densities in their packets; T-192’s candidate and control from the release asset, fetched to scratch and held to its digests | [`candidates.json`](receipts/candidates.json) |
| [`bounds_probe.py`](programs/bounds_probe.py) | The transcribed box bound held to an exact rational oracle of its own (Sutherland–Hodgman clipping of a rationally rotated square) on adversarial boxes and on the c6715 density; `--mutate` puts one deliberate error into the transcription | the source’s `slab.rs` and `interval.rs`, as read | (run through `probe_suite.py`) |
| [`probe_suite.py`](programs/probe_suite.py) | Three clean probes and the ten mutations, one receipt | the c6715 candidate | [`probe-suite.json`](receipts/probe-suite.json) |
| [`judge_run.py`](programs/judge_run.py) | Holds one run’s output to exact arithmetic: premises, root lines, summary, and every refusal witness re-evaluated (legality decided exactly, capture by the probe’s oracle) | a run’s JSON lines and its candidate | `judge-*.json` |
| [`run_timed.py`](programs/run_timed.py) | Runs one command and records its exit status, wall and CPU seconds and output | — | `run-*.json`, `build-v4.json`, `test-v4.json` |

## How It Was Run

```sh
WEB=$SQ/packing/resources/web
PY=$SQ/packing/.venv/bin/python3
CRATE=$WEB/wand125-sqverify-continuous-v4-2026-10-12/square-packing/tools/sqverify_continuous/sqverify_fast
V3=$WEB/wand125-sqverify-continuous-v3-2026-10-12/square-packing/tools/sqverify_continuous/sqverify_fast

# custody, from the repository root
$PY -I programs/custody.py --v3 $V3 --v3-base $CRATE --v4 $CRATE --repo $SQ \
    --rev origin/main --rev dee22b88 --rev 910b6b12c > receipts/custody.json
# premises
$PY -I programs/premises.py --n28-summaries \
    $WEB/wand125-continuous-n28-2026-10-15/square-packing/problems/square-lower-bounds/certificates/continuous_n28_L5745/check1 \
    > receipts/premises.json
# candidates (ASSET: the unpacked n = 28 release asset's continuous_n28_L5745/)
$PY -I programs/candidates.py \
    --rect-n40-l67 $WEB/wand125-rectangle-certificates-2026-10-01/wand125-rectangles/certificates/rect_n40_L67/certified_candidate.json.gz \
    --guzhou-6718 $WEB/guzhou-n40-new-supports-2026-10-11/source/certificate/certified_candidate.json.gz \
    --n28-candidate $ASSET/candidate.json --n28-control $ASSET/control/candidate-mass0985.json \
    CAND > receipts/candidates.json
# the probe
$PY -I programs/probe_suite.py --density CAND/c6715.json > receipts/probe-suite.json
# the verifier, built from this packet, then one run and its judgement
(cd $CRATE && cargo build --release --locked)
BIN=$CRATE/target/release/sqverify-fast
$BIN --candidate CAND/c6715_mass0985.json --n 40 --continuous --core 199529/200000 \
    --tau 4999/5000 --threads 2 --max-nodes 30000000 > receipts/runs/c6715_control.jsonl
$PY -I programs/judge_run.py receipts/runs/c6715_control.jsonl CAND/c6715_mass0985.json \
    --core 199529/200000 --tau 4999/5000 --expect REFUSED > receipts/judge-c6715_control.json
```

The other runs differ only in candidate, core and threshold, as the table below gives; the
n = 28 control ran with `--n 28 --core 499/500 --tau 1 --max-nodes 200000000`, the
source’s own command. Each run went through `run_timed.py`, whose receipts keep the
absolute scratch paths the run used.

## What They Printed

**Custody** (`custody.json`): v3 `1266a8b90f9a355d74772e211a7b9a52d0236b0d33cc4113d2f897d8a1044f33`
and v4 `619b3c00bd918b329b4141c24ee30b027af7f88b86bcf2886e3c18855a61c7f5`; `axis.rs`,
`exact.rs`, `interval.rs`, `oracle.rs` and `rotated.rs` the same blobs as this
repository’s at `dee22b88`, `910b6b12c` and `origin/main`; from v3 to v4, only `Params`
and `run` of `slab.rs` changed, with `run_key` and `inherited` added.

**Premises** (`premises.json`): every premise holds for the four parameter sets, and the
`run_key` recomputed for T-192’s run and control equals the source’s, `5b9984a6…` and
`56505cf5…`.

**Candidates** (`candidates.json`): c6715, 480 orbits, mass 3999/100, 3,792 images,
SHA-256 `f4a1ae9b…`; c6718, 685 orbits (522 inherited, 163 generated), 5,424 images,
`38e0eff1…`; T-192’s, format M with `proof_net: {step: 83/40000, last: 200}`, 884
admissible rows, mass 2799999/100000, 7,068 images, its control the candidate times
985/1000 row by row.

**The probe** (`probe-suite.json`): 3,060 boxes, 17,280 poses, 3,386,054 checks, no
failure; 9 of 10 mutations detected, the midpoint rule not (the review’s §8.1 says why).
623 CPU-seconds.

**The verifier** (binary `31936c4d…`; `build-v4.json`, 34 CPU-seconds;
`test-v4.json` and `test-v4.log`, 36 tests passed, 85 CPU-seconds):

| Run | Candidate | Core, threshold | Status | Nodes | Refusals that refute | CPU-s |
| --- | --- | --- | --- | --- | --- | --- |
| `toy-uniform-tau4_5` | `runs/toy-uniform-candidate.json`, n = 12 | 9/10, 4/5 | VERIFIED | 2,132 | — | 0.0 |
| `toy-uniform-tau81_100` | the same | 9/10, 81/100 | REFUSED | 3,767 | 0 of 86 | 0.0 |
| `toy-uniform-tau41_50` | the same | 9/10, 41/50 | REFUSED | 3,767 | 86 of 86 | 0.0 |
| `c6715_control` | c6715 × 985/1000 | 199529/200000, 4999/5000 | REFUSED | 7,714 | 86 of 86 | 1.5 |
| `c6718_control` | c6718 × 985/1000 | 3350/3359, 4999/5000 | REFUSED | 5,979 | 86 of 86 | 1.9 |
| `c6718_B3348` | c6718 | 3348/3359, 4999/5000 | REFUSED | 12,364,148 | 2 of 86 | 266 |
| `n28_control` | the asset’s control | 499/500, 1 | REFUSED | 5,478 | 86 of 86 | 3.7 |

Every judge receipt holds all its checks; all 516 refusal witnesses are legal poses whose
exact capture equals the run’s. The n = 40 rows equal the source’s README rows for v3, and
the n = 28 run equals the source’s `control.jsonl` root by root.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
