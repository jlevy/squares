**Verdict: accept with fixes.** The rule refutes the 99/100 mutant correctly whenever a refusal is a coverage refusal, and the trial receipt for `mixed_n96_L997` holds up when checked independently. One finding blocks: `sweep_held` accepts any verdict other than `verified` as a refusal, `audit-failed` and `non-finite` included (CC-1). Fixing it changes one function, and the trial receipt already meets the corrected rule as recorded. The other findings make the receipt checkable from its own fields, close test gaps and correct stale text.

# sqverify-fast Census `--control`: Review of the FC-1 Fix (`9f36ede38`)

**Verdict: accept with fixes.** When every refusal in the sweep is a coverage refusal, the new rule refutes the 99/100 mutant correctly. It is a sound fix for FC-1, and the trial receipt for `mixed_n96_L997` holds up under independent re-evaluation. One finding blocks a receipt from counting (CC-1). `sweep_held` takes any verdict other than `verified` as a refusal, so an `audit-failed` or `non-finite` direction would be counted as a refusal that shows the verifier works whenever its pose captures less than 1. For a 99/100 mutant, most poses do. The fix is a few lines in one function. The trial receipt meets the corrected rule as recorded, so it does not need to be run again. The other findings are non-blocking: an independent domain check, consistency checks between rows and summary, exact capture strings, test gaps, stale process text, and three corrections to the evidence text.

This review was written on 2026-10-06 by an AI agent (model `claude-opus-5-5`, tbd-strong tier), prompted separately as an adversarial reviewer. It shares no context with the lane that wrote the change. It registers nothing and moves no bound.

## Scope and Evidence

The subject is `9f36ede38` against its parent `65a8dcbce`. It changes `packing/devtools/sqverify_fast_census.py` (+171 −23: `scaled_sweep`, `sweep_held`, `control`, `scaled_control_text`, `records_mode` and the module text) and `packing/tests/test_sqverify_fast_census.py` (+83 −2). No file under `packing/sqverify_fast/` changed.

**Read:**

- the full diff;
- `control`, `direction_row` and `evidence_entry` as they now stand;
- `check_sqverify_fast.mixed_exact`, `mixed_mutant`, `mixed_refused` and the `declared_net` group;
- the crate's receipt construction (`src/lib.rs` 95–180), its witness assignment for each verdict (`src/rotated.rs` 806–1071), the axis `argmin` (`src/axis.rs` 120–200) and `src/main.rs`'s exit codes;
- `README.md` and `SOUNDNESS.md` lemma D;
- FC-1 and §4 of the 6 October re-check;
- "The controls", "The Confirmation Route", "Carrying the Route" and IR-3 of the 5 October review;
- Stage 4 of `result-import.md`.

**Run** (CPython 3.14 from `/home/user/squares-lanes/r4/packing/.venv`; the binary at `--threads 1` under `nice -n 10`; scratch under `scratchpad/r4/review-scratch/`):

1. `pytest tests/test_sqverify_fast_census.py`: 54 passed and 1 skipped. The skip is the v2 parametrization, which is empty because no v2 receipt is in the tree. `ruff check` and `ruff format --check` are clean. `basedpyright` reports only that `pytest` cannot be resolved, which comes from running it outside the worktree's own environment.
2. `spot.py`, on the trial receipt:
   - The candidate's digest is `e2e029a4…`.
   - The 201 row indices are distinct and cover 0 to 200.
   - All 187 refusal poses are inside lemma D's domain $[L/2, U_r]^2$, computed exactly.
   - `mixed_exact` at the poses for r = 0 (the axis), 3, 75, 131, 142 and 198 matches the recorded capture to 12 places, and every one is below 1.
3. The 99/100 mutant was rebuilt with `mixed_mutant` and the binary was run at directions 3, 139 and 200 with `--confirm`. Direction 3 refused (`counterexample-candidate`, exact witness below 1); 139 and 200 verified; exit 1, summary `REFUSED`. This matches the receipt.
4. `mut.py`: each of `sweep_held`'s six clauses was dropped in turn and the made-up-sweep test rerun.
5. An audit of all 39 control receipts in the tree. All are `sqverify-fast-control/v1` and `CONTROLS_REFUSED`.
6. `scaled_control_text` and `evidence_entry` were rendered on the trial receipt and census row, and `devtools.retained_data check` was run on the 3 October packet (exit 0).

## 1. Soundness of the Acceptance Rule

When `sweep_held` is true, the following hold:

- The sweep emitted as many rows as its own summary's `angle_count`.
- It exited 1 with summary `REFUSED`.
- At least one row is not `verified`.
- The verified and refused rows add up to the row count.
- Every non-verified row has a pose at which `mixed_exact` gives the mutant a capture below 1.

Each way a sweep could pass wrongly:

- **Admission, crash, timeout, fault injection.** An admission refusal, or an error inside a direction, makes `main` return `ExitCode::from(2)`. A panic exits 101, and a signal gives a negative code. All of these fail `returncode == 1`. A timeout raises `TimeoutExpired`, so no receipt is written. `--inject-fault-at-node` is not in the argument list. These cases are closed.
- **`unresolved`, `audit-failed`, `non-finite`.** These are not closed (CC-1). The verdict is recorded but never checked. In `rotated.rs`, `NonFinite` (902, 951), `AuditFailed` (924) and `Unresolved` (1007, 1056) all set `witness`, and `lib.rs` gives every witness an `exact_pose` under `--confirm`. An axis row that is `non-finite` reports its `argmin` at the vertex where the sweep stopped. A 99/100 mutant captures less than 1 across much of its domain, so a pose at one of these rows would usually pass. The claim at that pose is then false, so the refusal is right in outcome. But it is not the verifier refusing on coverage. An audit failure is a crate defect that the control should surface, not count as a refusal.
- **Wrong net angle, or wrong net.** `mixed_exact` takes the step from the file (`net_step(raw)`). The mutant is a copy of `raw`, and `control` already refuses a census row whose decided `D` differs from the file's. The mutant's own summary premises (`D`, `net_origin`, `angle_count`) are not compared with the census row (CC-3). The test compares `net_directions` with `census.net_directions(case)`, but `sweep_held` does not. For the trial, both are 201.
- **The axis `argmin` used as a centre.** This is sound. At r = 0 the crate gives `argmin` as exact rational strings for event coordinates in $[L/2, U_0]$. Any pose in the domain where the mutant captures less than 1 refutes the claim at that direction. The census itself never checks the domain (CC-2). The trial's axis pose is inside it.
- **Floats passed to `Fraction`.** This is harmless. `exact_pose` is the binary64 pair that the crate fed to `of_f64`. JSON round-trips binary64 exactly, and `Fraction(float)` is exact, so the census evaluates the same pose as the crate. The recorded `capture`, however, is a 12-decimal float string. The exact value is thrown away (CC-5).
- **A summary that does not match the rows.** Only the row count is compared with `angle_count`. Distinct indices, the summary's `refused_directions` and `fault_injected_at_box` are not checked (CC-3). For the trial, the indices are distinct and complete.
- **`returncode` and `summary_status`.** Both are required, but `summary_status` is never tested in isolation (CC-6).

**Is the bar right?** "At least one refusal, and an exact capture below 1 at every refused direction's pose" is right once each refusal is required to be a coverage refusal. One witnessed refusal is enough to show that the verifier refuses a false claim. Requiring every refusal to be witnessed fails closed on false refusals. A false refusal would only show incompleteness, but requiring it matches `check_sqverify_fast`'s declared-net group at 0.985 and costs nothing on the evidence so far. Keep it, and add CC-1's restriction on verdicts.

## 2. What a Verified Direction of the Mutant Means

At a direction where the mutant verifies, the crate has certified that the original captures at least $100/99$ throughout the domain, if the crate is sound. That says nothing for or against the control. Accepting it is right, and it is exactly the condition that made v1 fail closed on `mixed_n96_L997` at index 139: the original's centre capture there is 1.1028.

Compared with v1, nothing weakens the evidence. v1 showed one witnessed refusal at the least-bound direction. v2 shows witnessed refusals at every direction that refuses: 187 of 201 for the trial. The same-direction pairing of a verified original with a refused mutant now comes only from the near-threshold mutant at the least-bound index. Each refused direction's original is still covered by the census row, which the route requires anyway. The rule would accept a sweep that refuses at a single direction. That is still a valid negative control.

## 3. v1 Receipts

All 39 retained receipts are `sqverify-fast-control/v1` and `CONTROLS_REFUSED`. In each one, the 99/100 run at the least-bound index is `counterexample-candidate` with exit 1. The crate's `exact_below_threshold` is true, and the independent `capture_at_witness` is below 1. In 7 of the 39, the capture at the least-bound leaf's centre is also below 1.

So each v1 receipt meets the rule for one direction, as the commit says: a coverage refusal, with an exact witness below 1 evaluated apart from the crate. Each therefore meets CC-1's stricter rule as well. They do not meet "every direction ran", but that clause exists to make a v2 sweep's account complete. It adds nothing to whether a refusal is correct. Keeping them without regenerating them is right.

v1's own `held` was weaker than the claim: a capture below 1 at the centre with no witness would have passed. The data shows this never happened, but no test holds it (CC-6).

## 4. The Near-Threshold Mutant and the Original Run

Both are unchanged in substance. `direction_row` is untouched. The near-threshold loop body, its factor (rounded down so that the centre's capture is at most $1 - 10^{-6}$) and its branch of `held` are byte-for-byte as before. The one-element tuple loop is left over from the old two-element loop and is only cosmetic.

The commit did not introduce the following, but the trial makes it visible. For `mixed_n96_L997` the near-threshold factor is $453393222524583/500000000000000 \approx 0.9068$. That cuts deeper than the 99/100 mutant, and it is refused at the third box with a capture of 0.9926. Across the 39 v1 receipts the factor ranges from 0.854 to 0.995, and it is refused within 1 to 9 boxes in 14 of them. IR-3 already says the name describes the centre, not the refusal. The evidence text should state the factor (CC-8).

The near-threshold `held` has the same unchecked verdict as CC-1 (`verdict not in (None, "verified")`); fold the same restriction in.

## 5. The Evidence Text

The v1 branch reproduces the old sentence; rendered on `mixed_n67_L848`, it is unchanged.

The v2 branch, rendered on the trial: "Controls: the original verified again at index 139, every mass scaled by 99/100 refused at 187 of the 201 net directions, each with an exact capture below 1 at its witness (the mutant verified at the other 14, where the certificate has more than 1% slack), …". The counts are true to the receipt. Three phrases are not quite exact (CC-8):

- "where the certificate has more than 1% slack" is the crate's own certification, not a fact established by an independent check;
- at the axis the pose is the vertex sweep's `argmin`, not a witness;
- the crate never evaluated the axis capture exactly, so "evaluated again" does not apply to it.

`evidence_entry` trusts the receipt's `status` without re-deriving it, which is unchanged from v1 (FC-6).

## 6. Tests

What is held:

- the rule on made-up sweeps;
- for each v2 receipt in the tree: `sweep_held`, `net_directions` against the case, and every refusal's capture recomputed from the candidate.

The second item is empty until a v2 receipt lands.

What is not held (CC-6):

- Dropping the `summary_status`, non-empty-refusals or counts-add-up clause from `sweep_held` leaves the made-up-sweep test passing (`mut.py`).
- `scaled_sweep`'s parsing is not tested at all: the choice between `exact_pose` and `argmin`, the axis path, and rows against summary.
- The v2 branch of `scaled_control_text` and the new `records_mode` line are not tested.
- No condition on a refusal's verdict, its domain, or the crate and independent evaluator agreeing.
- Nothing holds the commit's claim that each v1 receipt has a witnessed coverage refusal. The v1 assertion still accepts a capture below 1 at the centre alone.

## 7. The Trial Receipt

**The census row** meets items 1 to 4 of the 5 October checklist:

- **Case.** `VERIFIED`, exit 0, 201 directions verified, `refused_directions` empty, threshold `1`, `clears_threshold` true.
- **Premises.** Format M, `per-bin`, `angle_count` 201, `D` `83/40000`, `B` `9977/10000`, `mass_exact` `9599999/100000` = $96 - 10^{-5}$, no point or segment, `fault_injected_at_box` null.
- **Candidate.** The digest `e2e029a4…` equals the retained file's, and `retained_data check` exits 0 against the pin `c4bdda46…`.
- **Build.** `d97758bb…`, which `REVIEWED_SOURCES` admits. `--evidence` rendered the entry without refusing it.

The certificate is in the 3 October review of these certificates (its table at lines 59 and 411).

**The control** is v2 with status `CONTROLS_REFUSED`. `captures_agree` is true, with both evaluators giving 1.10279… at index 139.

| Run | Result |
| --- | --- |
| Original | verified, exit 0 |
| 99/100 sweep | 201 of 201 rows, exit 1, `REFUSED`; refused at 187 (186 `counterexample-candidate` with the crate's `exact_below_threshold` true; the axis `refused`) |
| 99/100 sweep, verified | 14 directions: 1, 2, 132–141, 199, 200 |
| Near-threshold | refused (`counterexample-candidate`, exit 1) |

Every recorded mutant capture lies in [0.995814, 0.999999999997].

**Spot checks.** My `mixed_exact` at r = 0, 3, 75, 131, 142 and 198 agrees with the recorded captures and is below 1. The original's capture at those poses is between 1.00855 and 1.01010, so it is above 1 at every pose checked. All 187 poses are inside $[L/2, U_r]^2$. The rerun of the binary at 3, 139 and 200 reproduced the receipt.

The receipt passes the committed rule, and it passes CC-1's stricter rule as recorded. Together with the 3 October review of the mathematics, it supports counting `mixed_n96_L997`'s row as a complete replay on the route, once CC-1 is in the code and the receipt is held by the test in the tree.

## Findings

### CC-1 — Blocking: `sweep_held` does not require a refusal to be a coverage refusal

**What is wrong.** `scaled_sweep` treats every row that is not `verified` as a refusal. `sweep_held` asks only that its pose captures less than 1. `audit-failed`, `non-finite` (oblique or axis) and `unresolved` rows all carry a pose, and a 99/100 mutant's pose almost always captures less than 1. A crate audit failure on the mutant would therefore be counted as a correct refusal and contribute to a `CONTROLS_REFUSED` receipt.

**Fix.**

- Accept a refusal only as `counterexample-candidate` at an oblique direction, with the crate's `exact_below_threshold` true and agreeing with `mixed_exact`, or as `refused` with `method: axis-vertex-sweep` at r = 0.
- Make any `audit-failed`, `non-finite` or `fault-injected` row fail the receipt.
- Fail closed on `unresolved` unless a reviewer decides otherwise.
- Apply the same restriction to the near-threshold `held`.
- Add made-up-sweep cases for each.

The trial receipt satisfies the fixed rule from its own recorded fields.

### CC-2 — Non-blocking: no independent domain check on refusal poses

**What is wrong.** A capture below 1 refutes the claim only at a centre in $[L/2, U_r]^2$, but `mixed_exact` evaluates anywhere. The crate's poses lie in the domain by construction: box centres and corners, and axis events. The census relies on that and does not check it.

**Fix.** Compute $U_r = L - \rho(\max(0, rD - D/2))$ exactly, apart from the crate. Record `in_domain` for each refusal and for the near-threshold witness, and require it. I checked all 187 trial poses, and every one is in the domain.

### CC-3 — Non-blocking: rows are not reconciled with the summary or with the census row

**What is wrong.** Row count equal to `angle_count` is the only check that rows and summary agree.

**Fix.** Require:

- distinct row indices equal to `range(angle_count)`;
- the summary's `refused_directions` equal to the refused indices;
- `fault_injected_at_box` null;
- the mutant summary's `D`, `net_origin` and `angle_count` equal to the census row's.

Also record the mutant's `input_sha256`.

### CC-4 — Non-blocking: the sweep's poses are a free check of the original that is thrown away

**What is wrong.** At each refusal pose, capture ÷ 99/100 is the original's exact capture. A value below 1 there would be a counterexample to the census row.

**Fix.** Record it and require it to be at least 1. On the trial it is at least 1.0059 at every pose, giving 187 independent point checks of the original.

### CC-5 — Non-blocking: the receipt keeps a rounded float, not the exact capture

**What is wrong.** `capture` is stored as `f"{float(capture):.12f}"`. A capture of $1 - 10^{-13}$ would display as `1.000000000000` beside `capture_below_1: true`. The receipt cannot be re-judged from its own fields, whereas v1 kept exact strings.

**Fix.** Store `str(capture)`, keeping the float only as a convenience field.

### CC-6 — Non-blocking: the tests leave parts of the rule and the parser unheld

**Fix.**

- Add made-up-sweep cases that isolate `summary_status`, empty refusals with exit 1, and counts that do not add up, plus CC-1's verdict cases.
- Test `scaled_sweep` against a stub binary that prints fixed JSON lines, covering the axis `argmin` path and an `audit-failed` row.
- Test the v2 branch of `scaled_control_text`.
- For v1 receipts, assert that the 99/100 run is `counterexample-candidate` with `capture_at_witness` present and below 1. All 39 pass this.
- Land the trial receipt, or a small fixture, so the v2 parametrization is not empty.

### CC-7 — Non-blocking: process and generated text still describe the one-direction control

**What is wrong.** Several places still describe the old behaviour:

- `result-import.md` Stage 4 (line 295: "it tests the 99/100 mutant at one direction … and then fails closed");
- the census-mixed README's *Control* column text, generated from `sqverify_fast_census.py` line 1110 ("two mutants refused there");
- `control`'s docstring;
- the census sentence in `VERIFIERS.md`.

**Fix.** Update them in the same change, regenerate the README, and point Stage 4 at this review.

### CC-8 — Non-blocking: three corrections to the evidence text

**Fix.**

- Say "where the mutant verified, so by the verifier's own decision the original captures at least 100/99 there", not that the certificate *has* more than 1% slack.
- Say "at its witness (at the axis, the vertex sweep's least vertex)".
- State the near-threshold factor. For `mixed_n96_L997` it is 0.9068, a deeper cut than the 99/100 mutant.

## For the Records Lane

A `sqverify-fast-control/v2` receipt made with `9f36ede38` may stand where the route requires `CONTROLS_REFUSED` (checklist item 5 of the 5 October review) only if all of the following hold:

- CC-1's rule is in the code and the test.
- Each refusal recorded in the receipt is `counterexample-candidate` with the crate's `exact_below_threshold` true, or the axis's `refused`.
- No row is `audit-failed`, `non-finite` or `unresolved`.
- `tests/test_sqverify_fast_census.py` recomputes the receipt's refusals from the candidate in the tree.

The `mixed_n96_L997` trial receipt meets all of these as recorded and need not be regenerated.

Further receipts should be made after CC-1 lands, or re-judged against it before they count. Do the following before relying on any receipt:

- Check CC-2's domain condition.
- Check CC-4's condition that the original captures at least 1 at every pose.

Existing v1 `CONTROLS_REFUSED` receipts stand as they are. A `CONTROL_FAILED` receipt of either kind moves nothing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
