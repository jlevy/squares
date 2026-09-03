# Review Packets: Agenda 014 First Wave

**Date:** 2026-09-02

**Author:** Claude, for the project maintainers

**Status:** Frozen BC-128 routing decision and packet set for BC-135 independent review

These three packets carry agenda-014’s first-wave experiment decisions for n = 17, n =
68 and n = 50 to independent review, and record the routing decision for each lane.
They are review instructions, not new experiments.
Reviewers judge the retained evidence without repairing it, retrieving a target or
weakening a claim boundary.

## Routing Decision

BC-128 applies the agenda’s routing matrix to the lane exits as recorded, after the
BC-127 W5 receipt returned `no-change`. No second-wave agent is dispatched by this
document, and no candidate becomes an overnight block until BC-136 writes a separate
agenda from reviewed routes.

| Lane exit | Matrix condition | Decision | Basis |
| --- | --- | --- | --- |
| BC-123, n = 17: stopped on asymmetric host-load contamination; one serial arm, no paired sample | passes exact same-input profile at at least 2.8x | **Stop BC-129** | The 2.8x threshold was never measured; the records forbid pairing the retained control with a later candidate, and exp-053 must not resume. A future profile needs fresh pair roots and a host-wide quiet lease. The sequential resumable wall is priced at about 5.6 hours: 148 remaining directions at the observed 0.444 rows per minute. |
| BC-124, n = 68: complete; target-blind adapter admitted twice, no target opened | passes literal production adapter and independent readmission | **Candidate BC-130, conditional** | The instrument condition holds. The continuation earns candidate status only if exp-054 passes Packet B, and it cannot produce a geometry result until a separate preregistration binds the reported side token’s exact or directional semantics; until then a BC-130 run returns three typed serialization refusals. BC-136 may translate it into an overnight block only with that semantics contract named. |
| BC-125, n = 50: complete; one prospective zero-call refusal result | closure-only; does not earn a branch | **No branch** | Exp-055 goes to Packet C for review; exp-050, H-054 and every geometry claim remain unchanged. |
| BC-126, n = 54: complete; exact side, tilt and placement formulas found in one quartic field; parser and labeled correspondence absent | finds source evidence sufficient for a new source-cell contract | **Stop BC-131; retain the source refusal** | The typed blocker is `exact-source-parser-and-labeled-correspondence-absent`. The formula tool has no named negative control and its frozen-input table omits the retained 2009 HTML, so no packet can be frozen for n = 54. Both repairs are target-blind W7 work named in BC-126’s own next-evidence field. |

H-057, H-058, H-059 and H-055 move only under their own frozen criteria.
This checkpoint changes no hypothesis field, experiment decision or review flag.

## Frozen Revision and Common Contract

The evidence revision is `1e1751085fcdf0e71f563ed6b0f282feee54d07e`, the head of PR #73
at the owner’s pause.
Every experiment, result, session, hypothesis, instrument and test named below is read
from that revision. Later commits add review and state records only; any change to a
listed evidence path invalidates the packet.

Each reviewer works read-only against one packet.
No reviewer authored a first-wave lane; the lanes were written by three Codex agents and
the coordinator, and the reviewers are fresh agents assigned one packet each.
Run Python only from `packing/` with `uv run --frozen --all-extras --group dev`.
Mutations use pytest temporary paths or an operating-system temporary directory and must
not alter a retained artifact.
Reviewers do not run an n = 17 pair or assemble command, make any network request, run
the exp-055 producer command, interpret n = 19, n = 50 or n = 54 geometry, or create a
registered result.

For each experiment, report one of:

- **pass:** the exact decision, evidence boundary and limitation reproduce;
- **bounded caveat:** the outcome reproduces, but a material frozen limitation prevents
  review clearance;
- **discrepancy:** retained evidence contradicts the recorded decision or boundary; or
- **cannot-reproduce:** the named replay cannot be completed at the frozen revision.

A pass grants BC-136 permission to change only that experiment’s `needs_review` field
from `true` to `false`. It does not change the decision, hypothesis, frontier or
instrument state.
Any other determination leaves `needs_review: true`. Each response uses
the four campaign fields: **Artifact, Result, Guard, Next**.

Before a replay, confirm that `git diff --exit-code 1e175108 -- <listed evidence paths>`
is empty. Hashes below are SHA-256 values of bytes at the frozen revision, computed as
`git show 1e175108:<path> | sha256sum`.

## Packet A: n = 17 / H-057

### Decision under review

| Experiment | Frozen decision | Evidence status | Proposed BC-136 transition |
| --- | --- | --- | --- |
| exp-053 | `unresolved`, `needs_review: true` | One exact serial arm retained at 524.743164166 s for ordinals 33, 107 and 180; the candidate arm was stopped by the contamination guard and deleted; no paired sample, later pair or canonical result exists | Clear review only if the typed contamination stop, the retained arm bytes and the absence boundary pass |

H-057 remains instrument-ready and undecided under a pass.
The serial arm prices the workload; it is not a speedup sample, a serial-versus-parallel
equivalence result or an H-052 decision.
No frontier transition is proposed.

### Frozen bytes

| Artifact | SHA-256 |
| --- | --- |
| exp-053 record | `e6529af9d3e97d8e3ba2bb96d3b876efd8279aa2cd7f407b71adcc13fdb13cc8` |
| session-073 | `7f40fc5b43d666b6af567999859b88347c9e3c3ba6ff5888155362d52cf4925b` |
| H-057 | `77c82bd2c82886933a82cbe9c175183dcdac3d037ea8d5b8e648cd66a7f7bbbd` |
| profiler `runner.py` | `e31abda6ce13df471be8d8e4573ed614005c2e1bfe067902ac8312b2a29da618` |
| benchmark adapter | `1ec0e7cad3b69e167cd236dea88374cdfa349cc0d0be49ed73a87a413548a8e5` |
| focused test | `248a9ea0e366f6e8de616daf4c97d473dc548fcbd9697be6658571c9a787ab28` |
| pair-01-ab `pair-binding.json` | `61b8de0c1a62b409295913ebc88c124c86261140403f34321f64de5e2247ad00` |
| arm-A `receipt.json` | `30c40271a8e8fc71dac8c3f8ee9750b09338ca1d3e8375cfb79cf0daba0f6b93` |
| arm-A `merged.json` | `bd383747cfcfaf2c13c800c1b09fa4e430ef3d2f5f04106d7d9f37482dce33ba` |
| arm-A `fragment-033.json` | `a5ab6bb69daaed3bb1357db76d44706d4785d24a27fafbffbe183e3637adfc2b` |
| arm-A `fragment-107.json` | `a69cf3197c384e571dd6d42ababc5efc43d7877c1d0f8b9fb31649cc5c6c434e` |
| arm-A `fragment-180.json` | `c7a4b6674a17898ab2a7cdf63c3e2cd9f09361627666079149f61f77c5147933` |

The paths are `packing/cases/n17_weighted_certificate_parallel/runner.py`,
`packing/benchmarks/n17_weighted_certificate_parallel.py`,
`packing/tests/test_n17_weighted_certificate_parallel.py`, and the raw directory
`packing/campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.raw/pair-01-ab/`.
The frozen scientific-package manifest is
`309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54` and the parent row
hash is `9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6`, both
unchanged from exp-052. The 30-guard self-test receipt recorded under normal and
optimized Python is `0c256e5a164078119ffb3a98e9de2825c733a02cfbcff1c1b0aa8a6d28da0958`.

### Declared absences

The canonical result
`packing/campaign/series/series-000-smoke-and-calibration/results/exp-053-h-057-n17-parent-bound-parallel-speedup.json`,
the `arm-B` directory, `pair-02-ba`, `pair-03-ab` and any `.arm-*.partial-*` path must
be absent before and after review.
Session-073’s `outputs` list names the canonical result path as a declared-absent
placeholder; that is a packet fact, not a discrepancy.

### Required replay and guard

1. Confirm every declared absence with `git ls-files` and on disk, and recompute the
   twelve hashes above.

2. Inspect `receipt.json`: `mode` is `serial`, `elapsed_ns` is `524743164166`, and its
   three `fragment_sha256` entries equal the three fragment hashes above.
   Confirm `merged.json` hashes to the merged value.

3. Run:

   ```text
   uv run --frozen --all-extras --group dev pytest -q tests/test_n17_weighted_certificate_parallel.py
   uv run --frozen --all-extras --group dev python -m benchmarks.n17_weighted_certificate_parallel selftest
   uv run --frozen --all-extras --group dev python -O -m benchmarks.n17_weighted_certificate_parallel selftest
   ```

   Seven tests pass; both self-tests report 30 guards, zero skips and the same receipt
   hash, expected `0c256e5a…0958`.

4. The required mutation is `test_pair_contract_refuses_ordinal_or_output_substitution`;
   it must reject a changed ordinal and a wrong output root.
   Also confirm
   `test_parallel_failure_stops_children_cleans_partial_and_preserves_complete_arm`
   removes a partial candidate arm while leaving the complete arm’s receipt bytes
   unchanged.

5. Do not invoke the `pair` or `assemble` subcommands with any real root.
   The four frozen commands in exp-053 are the scientific run and are excluded.

### Required boundary determination

Pass exp-053 only if the reviewer reproduces the retained arm, the absences and the
self-test receipt, and agrees that no paired sample exists, the 2.8x threshold was never
measured, and the arm is a process cost rather than an H-057 sample.
A hash, absence, guard-count or receipt mismatch is a discrepancy.
Inability to run the self-test or the focused suite at the frozen revision is
cannot-reproduce.

## Packet B: n = 68 / H-058

### Decision under review

| Experiment | Frozen decision | Evidence status | Proposed BC-136 transition |
| --- | --- | --- | --- |
| exp-054 | `unresolved`, `needs_review: true` | Target-blind production adapter admitted by a fresh different-lane W2 after a prepublication depth-guard correction: 35 focused tests, 20 named mutations, byte-identical normal and optimized receipts; no network, source or target access; result absent | Clear review only if the target-blind admission, the corrected guard and the no-sample boundary pass |

H-058 remains instrument-ready and unmeasured under a pass.
The reported side token is intentionally unbound, so the production path yields three
typed `serialization-refusal` outcomes; that is premeasurement behavior, not a sample,
an instrument defect or an H-058 decision.
H-053 and the frontier are untouched.

### Frozen bytes

| Artifact | SHA-256 |
| --- | --- |
| exp-054 record | `3b998c0466cb568d26a21bf572d6777657121b4abdba752ee9ed9fec69aedc4e` |
| session-074 | `c983e77e9744b90bdfdf1fe1fdfb46a685fe282e2fb6f9f23c53beced7caf8ec` |
| H-058 | `5689e654e8828877144ef066772b00e491a1df5bb3f2b6997301ff4364a11de8` |
| production `adapter.py` | `9b503050115a5a48b01ec9f4d348b869495fbe4ee4847dc83188b05a3352f539` |
| production `run.py` | `8cef0f9cd4f473e594ed55e650be2fe7b286a798d2a94e5edb0a35efb7b12d54` |
| production `verify.py` | `e39a6a725e7af01a2e1796e1a218576f76b8a2ec2cecf7fbde3f38aeb9630a7a` |
| focused test | `17f4be0611fb02419d9007222f07b3f585b290c03866403a1d2bd5da954f01df` |
| refusal `verify.py` (shared proof kernel) | `1533210f9d8e17cbdfa822da59187d280fc4ab063816644825c50d7b8b24552f` |
| refusal `run.py` | `3d91046ad9d4ea7b3a7e2f3e7f1ca02aec7cd7118d2291a50f622e8541020029` |

The paths are `packing/cases/unitsquare_precision/production/{adapter,run,verify}.py`,
`packing/tests/test_unitsquare_precision_production.py` and
`packing/cases/unitsquare_precision/refusal/{run,verify}.py`. Two packet facts follow
from the correction.
Session-074’s phases 3 and 5 declare pre-correction hashes for `adapter.py`, `run.py`
and the test (`525c485c…`, `ededfb79…`, `a8ef4fe3…`); they are historical, and only the
values above bind the frozen bytes, as session-074’s `checks`, exp-054 and H-058 state.
The production package is new at the freeze commit, so the depth-guard fix is not
visible as a diff hunk; it is attested by the corrected bytes and the regression test.
The 1,112-byte literal self-test receipt,
`becb4c7f865f2f4b3a9d6bd22b11bb736efe73ba2d7dc97e025cd4becbd55906`, is a runtime
artifact, not a repository file; the replay reproduces it.

### Declared absences

`packing/campaign/series/series-000-smoke-and-calibration/results/exp-054-h-058-n68-one-parent-production-serialization.json`
and the exp-051 result path must be absent before and after review.
No `square-68.svg` or other n = 68 source byte is tracked, and none may be fetched.
The expected parent digest
`558fbdddfeb0b2f8752b88e172d2776544beb4d2a7122189ef77c1e1c5ebdc6d` is a declaration
only.

### Required replay and guard

1. Confirm the absences and recompute the nine hashes above.

2. Read `run.py` and confirm that its entry point runs only the literal self-test: it
   requires the registered result path, uses the in-memory synthetic SVG and a temporary
   output root, and opens no network channel.
   Confirm in `adapter.py` that `mark_selected_path` checks the element and depth bounds
   before descending.

3. Run:

   ```text
   uv run --frozen --all-extras --group dev pytest -q tests/test_unitsquare_precision_production.py
   uv run --frozen --all-extras --group dev ruff check cases/unitsquare_precision/production tests/test_unitsquare_precision_production.py
   uv run --frozen --all-extras --group dev basedpyright cases/unitsquare_precision/production tests/test_unitsquare_precision_production.py
   ```

   Thirty-five tests pass.
   `test_literal_production_argv_is_target_blind_and_optimized` runs the registered argv
   under normal and optimized Python inside the suite, asserts identical output and
   confirms the result path stays absent; report the receipt hash it observes and
   whether it equals `becb4c7f…5906`. Do not invoke the registered command by hand.

4. The required mutation is
   `test_selected_path_scan_enforces_depth_before_python_recursion`; it must refuse
   nesting deeper than the recursion limit with the bounded-parser error.
   Also confirm all twenty names in the mutation receipt fired, and that
   `test_whole_result_verifier_rejects_model_binding_and_proof_mutations` rejects.

5. Confirm the result path is still absent and that no network request was made.

### Required boundary determination

Pass exp-054 only if the target-blind admission reproduces as stated, the corrected
guard runs before descent, and the reviewer agrees that the round supplies no H-058
sample and that the three typed serialization refusals are premeasurement behavior.
A network access, result creation, a guard that fails to fire, or a claim about n = 68
geometry is a discrepancy.
The historical hash split is a packet fact; treat it as a discrepancy only if the frozen
bytes differ from the values above.
Do not write side semantics during review.

## Packet C: n = 50 / H-059

### Decision under review

| Experiment | Frozen decision | Evidence status | Proposed BC-136 transition |
| --- | --- | --- | --- |
| exp-055 | `accepted`, `needs_review: true` | One registered command published a 5,211-byte prospective zero-call refusal result in 0.72 s; four stage sentinels calibrated, every named mutation rejected, independent verification byte-identical under normal and optimized Python; exp-050 unchanged | Clear review only if the immutable result verifies independently, the mutation rejects, exp-050 is unchanged and the protocol-only claim boundary passes |

The result accepts H-059’s prospective protocol claim only.
It does not repair exp-050, clear its review history, change H-054, establish n = 50
feasibility or authorize source or geometry work.
No frontier transition is proposed.

### Frozen bytes

| Artifact | SHA-256 |
| --- | --- |
| exp-055 result (5,211 bytes) | `9c90a04e5691f168f042a455780cbdd5a66eac248e617930b79d084496a8654c` |
| exp-055 record | `8aff96fb56f72750f6768bac9e487727abf71bdff1300f14202270f13e4e8e70` |
| session-075 | `2b747e2d8b5ce9a394c80af4b8e45858c1942346803f619b5682eef2c35058c3` |
| H-059 | `3ffd27df1cd7b387ac7b17fbce782f0ca0d39019c2bd01f6facb8f2ef41cccd9` |
| `__init__.py` | `55ea8c0d142f15f1ed2c6e7201dbb4abf31b56f6ab2eee4453eca00e6c6b2ab5` |
| `harness.py` | `0ea3a32714152ed5ed2ac2011dd64e27bfe9cb70af5b2c6cb1768a6870bfa6d1` |
| producer-refusal `run.py` | `31990dfe1fee0a653e73d68bcf07c0c3788027823f43095bb4c02810c28de894` |
| independent `verify.py` | `950fd4a4c41224792742d11e5e6b3f2caeeb4937204d680671892ba28820a0df` |
| focused test | `559508b435708621c19e174541207b90008190f48c0792fa2098889ab0800574` |
| independent test | `cdc16b6cf40c7a2ee3df8b5267514a1af490357ee2dde1ff7b353e54ee63d757` |
| frozen producer `source_semantics_runner.py` | `52baeb1b6ad52aa504498ba21aeb6b3d361aaaec2461c76904a357d8d95cf29d` |
| exp-050 result (1,574 bytes, must not change) | `ab00e50debe0bc60279ce3472ed0c09eb062e8271a481a38c6ac65036aff4a02` |
| `tests/conftest.py` | `49b96a7f7216906106717fdff73d29e5f64bfb2d74ee0388375fa40b55da1cad` |

The paths are `packing/cases/n050_producer_refusal/`,
`packing/tests/test_n050_producer_refusal.py`,
`packing/tests/test_n050_producer_refusal_independent.py`,
`packing/cases/n050_exact/source_semantics_runner.py`, and the two results under
`packing/campaign/series/series-000-smoke-and-calibration/results/`. The result’s six
`instrument_bindings` are the six instrument and test hashes above.
The 390-byte verification receipt recorded as
`64d37a00c43384033adedc94e1c4ba42ad1010a6f419d5b17f07c14265b73ccc` is verifier stdout,
not a repository file; the replay reproduces it.

### Declared absences and invariants

The exp-050 result is byte-identical before and after review.
`packing/cases/n050_producer_refusal/` holds exactly four tracked files and no fixture,
source or geometry data.
No n = 19 or n = 50 geometry artifact was added.

### Required replay and guard

1. Recompute the thirteen hashes above and confirm the result’s six instrument bindings
   equal the computed instrument and test hashes.

2. Run the independent verifier under normal and optimized Python:

   ```text
   uv run --frozen --all-extras --group dev python -m cases.n050_producer_refusal.verify campaign/series/series-000-smoke-and-calibration/results/exp-055-h-059-n50-producer-refusal-ordering.json
   uv run --frozen --all-extras --group dev python -O -m cases.n050_producer_refusal.verify campaign/series/series-000-smoke-and-calibration/results/exp-055-h-059-n50-producer-refusal-ordering.json
   ```

   Both exit 0 with identical output; report its SHA-256 and whether it equals
   `64d37a00…3ccc`. The verifier must not import the harness or producer.

3. Run the focused suites:

   ```text
   uv run --frozen --all-extras --group dev pytest -q tests/test_n050_producer_refusal.py tests/test_n050_producer_refusal_independent.py
   ```

   Twenty-one tests pass.
   Confirm the `conftest.py` fixture gives the frozen-import tests clean module state.

4. The required mutation is
   `test_independent_verifier_rejects_named_mutations[review-cleared]`; the verifier
   must reject a result whose `needs_review` was set to `false`. Also confirm the four
   stage sentinels (`binding_observation`, `fixture_loading`, `receipt_evaluation`,
   `publication`) each calibrate once and that every producer-side mutation in the
   result is recorded `rejected: true`.

5. Do not run `python -m cases.n050_producer_refusal.run --record …`; it is the one-shot
   producer command and is excluded.
   `--selftest` is safe if needed.
   Confirm the exp-050 result hash is unchanged after every step.

### Required boundary determination

Pass exp-055 only if the immutable result verifies independently under both
interpreters, the mutation rejects, exp-050 is unchanged and the reviewer agrees the
acceptance covers the prospective protocol claim only.
The recorded uncertainty that the result cannot itself prove no failed pre-publication
process was attempted rests on the contemporaneous session record; a bounded caveat on
that ground must name a frozen limitation that a later round could repair, not restate
the uncertainty. A verifier failure, a binding mismatch, a changed exp-050 hash or a
claim that the result decides H-054 or n = 50 feasibility is a discrepancy.

## n = 54: No Packet

BC-126 produced no experiment decision.
Its source and formula audit is retained in
[`packing/resources/web/n54-source-formula-audit-2026/`](../../../packing/resources/web/n54-source-formula-audit-2026/README.md)
with the tool `devtools.audit_n54_source_formula` and two positive tests.
The different-lane preflight found no named negative control and a frozen-input table
that omits the retained 2009 HTML, so the packet cannot be frozen.
H-055 remains `instrument_ready: false`, and both repairs are target-blind W7 work.

## Coordinator Reconciliation Rule

BC-135 records the three determinations separately; a lane-level pass cannot hide a
caveat on an experiment.
BC-136 applies only explicitly cleared `needs_review` transitions and otherwise
preserves each frozen decision verbatim.
Source, instrument or result repairs become newly registered future work.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
