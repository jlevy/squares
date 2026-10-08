**Verdict: accept with one fix.** `f1ddc2379` fixes CC-1 and makes the control sound. The `mixed_n96_L997` v2 receipt holds up when every refusal is evaluated again independently. One finding blocks the merge but not the receipt: the commit edits `frontier/verifiers.yaml` without regenerating `frontier/VERIFIERS.md`, so `tests/test_verifier_registry.py` and the validation gate now fail (CR-1). CR-2 to CR-7 are non-blocking. They cover stale text, the near-threshold rule, tests that miss mutations, an `captures_agree` field at the axis that compares nothing, the domain's width, and formats where the control always fails.

# sqverify-fast Census `--control`: Re-check of the FC-1 Fix Response (`f1ddc2379`)

## Scope

This re-check was written on 2026-10-06 by an AI agent (model `claude-opus-5-5`, tbd-strong tier). It was prompted separately as an adversarial reviewer and shares no context with the lane that wrote the change. It covers `f1ddc2379` against `9f36ede38` and the review of 6 October (CC-1 to CC-8). It also covers the v2 receipt `mixed_n96_L997.control.json` and its row in `census.json`. It registers nothing and moves no bound. All runs used CPython 3.14 from `/home/user/squares-lanes/r4/packing/.venv`, from `packing/`. The binary ran at `--threads 1` under `nice -n 10`. Scratch files are under `scratchpad/r4/review-scratch/`.

**Runs:**

1. `pytest tests/test_sqverify_fast_census.py`: 65 passed, 1 skipped. The skip is the v2 receipt parametrization, which is still empty because no v2 receipt is in the tree. `ruff check` and `ruff format --check` are clean on both files.
2. `pytest tests/test_verifier_registry.py`: `test_the_committed_views_agree_with_the_records` fails. `python -m devtools.render_verifiers --check` exits 1 with "packing/frontier/VERIFIERS.md is stale".
3. `recheck.py` and `allrefusals.py` evaluate the receipt again with `check_sqverify_fast.mixed_exact` from the retained candidate (digest `e2e029a4…`, the same as the receipt's). Three things were checked against my own copy of `certificate::domain_upper`:
   - all 187 refusals;
   - the near-threshold witness and centre;
   - the domain of every pose.
4. The 99/100 mutant was rebuilt with `mixed_mutant`; its SHA-256 `bdb3f936…` equals the receipt's `mutant_input_sha256`. I ran the binary on it at directions 0 and 64 with `--confirm`. Both refused with exit 1, and both poses and captures equal the receipt's.
5. Mutation testing (`mutplug.py`, a pytest plugin that loads the module with one textual change and does not edit the tree): nine mutants of the new rule, with the census tests rerun on each.

## 1. Does `f1ddc2379` Fix CC-1 to CC-8?

**CC-1 — fixed for the sweep; the near-threshold run is partly fixed.** `refusal_record` counts a refusal as a coverage refusal only in two cases:

- at r > 0, a `counterexample-candidate` whose `exact_below_threshold` is `True`;
- at r = 0, `refused` with `method: axis-vertex-sweep`.

Every other verdict sets `coverage_refusal` to false. That includes `audit-failed`, `non-finite`, `unresolved`, `fault-injected`, a missing verdict, and the axis's `non-finite`. `refusal_held` then fails the record, and so `sweep_held` fails. This matches the crate. `src/lib.rs` lines 111–117 give the axis `refused` only when the sweep's minimum is finite and below `threshold_hi`, and `non-finite` otherwise.

The near-threshold `held` now requires `counterexample-candidate`. It does not require `exact_below_threshold`, and it does not compare the crate's exact capture at the witness with the independent one (CR-3). The review asked for "the same restriction".

**CC-2 — fixed. The domain is wider than the review stated, and that is sound.** `domain_bounds` returns $[\rho(a_r), L - \rho(a_r)]$ on each axis. Its upper end equals `certificate::domain_upper`'s $U_r$ for the per-bin domain. Its lower end is $\rho(a_r)$, not the $L/2$ of the review and of lemma D's statement. That is the full proof domain $[a_r, L - a_r]^2$ that lemma C1 reduces to a quadrant by a quarter turn, and $F_r$ is invariant under that turn. A capture below 1 anywhere in the wider set therefore refutes the claim at node $r$. CR-6 asks for this to be written down.

The trial's poses all lie in the narrower quadrant anyway:

- all 187 are in $[L/2, U_r]^2$;
- the least margin above $L/2$ is 0.112;
- the least margin below $U_r$ is 0.572.

**CC-3 — fixed.** The sweep now requires each of the following:

- `indices_complete` (row indices equal `range(angle_count)`, in order);
- `summary_refused_directions` equal to the refused rows' indices;
- `fault_injected_at_box is None`;
- `premises_agree` over `D`, `B`, `L`, `n`, `net_origin`, `angle_count` and `format`.

`mutant_input_sha256` is kept. All seven keys are present in the census row's premises, so the comparison is not vacuous on the trial.

Two minor points:

- A summary that omits `fault_injected_at_box` reads as `None`. The crate always writes the key.
- `centre_domain` is not among the compared keys (CR-7).

**CC-4 — fixed.** `original_at_least_1` is `capture / factor >= 1`, which is `mixed_exact` of the original. On the trial the least value is 1.00587 over all 187 poses.

**CC-5 — fixed at oblique directions. At the axis, nothing is compared.** `capture` is `str(Fraction)`, and at r > 0 `captures_agree` requires `Fraction(exact_coverage) == capture` exactly. At the axis, `captures_agree` is `crate is None`, which is true whenever the crate sends no witness. Nothing is compared, yet the field reads `true`. The crate does report a comparable number there (CR-5).

**CC-6 — partly fixed.** The new tests cover:

- every clause of `sweep_held` and `refusal_held`, by override;
- the verdict table;
- a domain and agreement case;
- `domain_bounds` at r = 0 and r = 5;
- `scaled_sweep` against a stub binary, covering the axis `argmin`, an audit failure and a missing row;
- the v2 sentence and `near_factor`;
- for v1 receipts, that the 99/100 refusal is `counterexample-candidate` with a witness capture below 1. All 39 pass.

Gaps remain, set out under question 2 (CR-4).

**CC-7 — partly fixed.** Four places are updated:

- `result-import.md` Stage 4;
- `control`'s docstring;
- `render_mixed_report`'s *Control* text;
- the `verifiers.yaml` note.

Four things are not done:

- `VERIFIERS.md` was not regenerated, which turns a gate red (CR-1).
- The committed `benchmarks/measure-verifier/census-mixed/README.md` was not regenerated and still says "two mutants refused there".
- The module docstring's first `--control` sentence still says "two mutants must be refused" at the least-bound direction, and the text after it now contradicts that.
- Stage 4 links to `review-2026-10-06-sqverify-fast-census-control-fc1.md`, which is not yet in the tree (CR-2).

**CC-8 — fixed.** Rendered on the trial receipt, the v2 text reads: "…refused at 187 of the 201 net directions, each a coverage refusal at a centre in the per-bin domain where the mutant's exact capture is below 1 (the crate's confirmed witness, or at the axis the vertex sweep's least vertex); the mutant verified at the other 14, where by the verifier's own decision the original captures at least 100/99; and every mass scaled by 0.9068 so that…". All three corrections are in, and each is accurate for this receipt.

### On `refusal_record`

In the code as it stands, the r = 0 case reaches the axis branch only when the method is `axis-vertex-sweep`. The `index > 0` guard means an r = 0 `counterexample-candidate` never counts. The crate produces such a row only for a file with points or segments: `src/lib.rs` line 103 runs the vertex sweep only for rectangles alone. For those files, a correct refusal at r = 0 would therefore fail the receipt. This fails closed, not open (CR-7).

The pose is taken as given, from `argmin` (exact rational strings) or `exact_pose` (binary64, which `Fraction` reads exactly). Its length is never checked; a pose with one element would raise an error and write no receipt, which also fails closed.

## 2. Do the New Tests Hold What They Claim?

The tests hold the rule's structure: each boolean clause, each verdict, rows against the summary, and the parser. They do not hold the computations that produce those booleans with the real evaluator.

All three new unit tests that build a refusal record monkeypatch `census.mixed_exact` to return 1:

- `test_only_a_coverage_refusal_counts`;
- `test_a_refusal_outside_the_domain_or_disagreeing_with_the_crate_does_not_count`;
- `test_a_sweep_reads_the_binarys_rows_and_summary`.

That is legitimate for testing the verdict logic and the parser, and none of them passes because of the patch in a way that hides a wrong result. But the only test that runs `refusal_record`'s arithmetic against the real `mixed_exact` is `test_each_scaled_sweep_refuses_its_mutant_somewhere_with_an_exact_witness`. That test is parametrized over v2 receipts in the tree, and there are none, so it is skipped. Until a v2 receipt lands, nothing in the tree runs the real evaluator through this code: which index is passed, the factor, the `capture / factor` step, or exact parsing of float poses.

Mutation results. Each mutant was applied to `sqverify_fast_census.py` alone, and the census tests were rerun:

| Mutant | Result |
| --- | --- |
| M1: drop `exact_below_threshold is True` from a candidate's coverage | survives |
| M2: `captures_agree` at the axis always true | survives (it already is; CR-5) |
| M3: near-threshold `held` accepts any verdict but `verified` (the old rule) | survives |
| M4: near-threshold `held` ignores `centre_in_domain` | survives |
| M5: domain lower end 0 | killed |
| M6: drop `index > 0` | survives |
| M7: axis detected by `r == 0` alone, method ignored | survives |
| M8: `premises_agree` compares only `n` | survives |
| M9: `original_at_least_1` always true | survives |

How much each survivor matters:

- **M1** is harmless. Whenever `captures_agree` and `capture_below_1` hold, the crate's exact capture equals the independent one and is below 1, so the `exact_below_threshold` clause adds nothing.
- **M6 and M7** would only change rows the crate does not emit at r = 0 for a rectangles-only file.
- **M3, M4, M8 and M9** are real gaps. `held` is a closure inside `control`, so no test reaches it without the binary. The per-receipt test checks the stored near-threshold verdict and domain flags, not the rule. M8 and M9 survive because the made-up records set the fields directly.

## 3. Does the Receipt Meet the Review's Conditions?

**The receipt as recorded:**

- kind `sqverify-fast-control/v2`, status `CONTROLS_REFUSED`;
- binary `567a0fd5…`, the census row's binary (source `d97758bb…`);
- the original verified again at index 139, exit 0.

**The 99/100 sweep:**

- It covers 201 of 201 rows, with indices complete. It exited 1 with summary `REFUSED`, its premises agree with the census row, and no fault was injected.
- Its summary's refused directions equal the rows': 187 of them.
- 186 are `counterexample-candidate` with `exact_below_threshold: true` and the crate's capture equal to the independent one. The axis row is `refused` by `axis-vertex-sweep`.
- No row is `audit-failed`, `non-finite` or `unresolved`.
- It verified at 14 directions: 1, 2, 132–141, 199 and 200.

**Independent evaluation.** I evaluated all 187 refusals again from the candidate with `mixed_exact`, not only three:

- Every mutant capture equals the recorded rational exactly and lies in [0.9958144, 0.99999999999749].
- Every original capture at those poses is at least 1.00587.
- Every pose lies in $[L/2, U_r]^2$ with $U_r$ computed apart from the crate. That is the narrower set, so the poses are also in the code's $[\rho(a_r), L - \rho(a_r)]^2$.

Values at the indices I printed:

| r | Verdict | Mutant capture | Original capture |
| --- | --- | --- | --- |
| 0 (axis) | `refused` | 0.998465863048 | 1.008551376816 |
| 3 | candidate | 0.999999998155 | 1.010101008238 |
| 64 | candidate | 0.999845598710 | 1.009945049202 |
| 131 | candidate | 0.999923025316 | 1.010023257895 |
| 142 | candidate | 0.999941741137 | 1.010042162765 |
| 175 | candidate | 0.999515698179 | 1.009611816342 |
| 198 | candidate | 0.999999998491 | 1.010101008577 |

My rerun of the binary at r = 0 reproduced the axis `argmin` and reported `min_certified_lower_bound` 0.9984658629684, which lies just below the exact 0.9984658630477, as a lower bound should.

**The near-threshold run.** The factor is $453393222524583/500000000000000 \approx 0.9068$. The verdict is `counterexample-candidate`, exit 1, with `exact_below_threshold: true`. The independent capture at the witness is 0.99255309576, equal to the recorded value and to the crate's `exact_coverage`. The capture at the centre is $\le 1 - 10^{-6}$. Both the witness and the centre lie in the quadrant at index 139.

**Against the review's four conditions:**

1. *CC-1's rule is in the code and the test.* Met.
2. *Every refusal is a confirmed candidate or the axis's `refused`.* Met.
3. *No row is `audit-failed`, `non-finite` or `unresolved`.* Met.
4. *`tests/test_sqverify_fast_census.py` recomputes the receipt's refusals from the candidate in the tree.* **Not yet met.** The receipt is not in the tree, so the v2 parametrization is empty. With the commit's test, landing the receipt meets this condition: it asserts the domain, the exact capture equal to the receipt's and below 1, and the original at least 1.

The review's further checks, CC-2's domain and CC-4's original at least 1, are met for all 187 poses.

## 4. Does Anything New Weaken a Control or an Evidence Sentence?

No change weakens a control. Every clause added to `sweep_held` and the near-threshold `held` is a further condition, and each failure fails closed. Two changes in scope are worth naming:

- **The domain.** The domain check uses $[\rho(a_r), L - \rho(a_r)]^2$, not the review's $[L/2, U_r]^2$. It is sound for the reason in CC-2 above, but it is the one place where the code accepts more than the review wrote (CR-6).
- **The axis field.** `captures_agree: true` at the axis claims an agreement nobody checked. It is not used in any evidence sentence, but a reader of the receipt would take it at face value (CR-5).

The evidence sentence is now more exact than in `9f36ede38`. It still ends "tests/test_sqverify_fast_census.py holds the receipts", which is true for a v2 receipt only once that receipt is in the tree.

## Findings

### CR-1 — Blocking (merge, not the receipt): `VERIFIERS.md` is stale

**What is wrong.** The commit edits the `V-…` note in `frontier/verifiers.yaml` but does not regenerate `frontier/VERIFIERS.md`. `render_verifiers --check` exits 1, `test_verifier_registry.py::test_the_committed_views_agree_with_the_records` fails, and `packing-validate` runs the same check (`src/sqpack/cli/validate.py` line 3495).

**Fix.** Run `python -m devtools.render_verifiers --update` and commit the result.

### CR-2 — Non-blocking: CC-7 is incomplete

**What is wrong.** Three pieces of text are left over:

- The module docstring of `sqverify_fast_census.py` (lines 34–35) still says the original "must verify again at its least-bound direction, and two mutants must be refused".
- The committed `benchmarks/measure-verifier/census-mixed/README.md` was not regenerated from the new `render_mixed_report` text.
- Stage 4's link to `review-2026-10-06-sqverify-fast-census-control-fc1.md#for-the-records-lane` points at a file not yet in the tree.

**Fix.** Rewrite the docstring sentence, regenerate the README, and land the review in the same branch.

### CR-3 — Non-blocking: the near-threshold rule is not CC-1's rule

**What is wrong.** `held` requires `counterexample-candidate` but not `exact_below_threshold`, and it never checks the crate's exact capture at the witness against `capture_at_witness`. The crate can emit a candidate whose exact check fails: the float test at `src/rotated.rs` line 973 decides the verdict before `--confirm`. The outcome stays correct, because `at_centre` is an exact capture below 1 at a centre the tool checks is in the domain, so the mutant's claim is false either way. Mutants M3 and M4 survive.

**Fix.** Require `exact_below_threshold is True`, and record and require agreement between the crate's capture and the independent one at the witness. Expose `held` at module level so a made-up run can test it.

### CR-4 — Non-blocking: the tests never run the real evaluator through `refusal_record`

**What is wrong.** Every new unit test that builds a refusal monkeypatches `mixed_exact`. The only real-evaluator test of the sweep is parametrized over v2 receipts in the tree, of which there are none. Mutants M8 and M9 survive.

**Fix.**

- Land the `mixed_n96_L997` receipt, which is also the review's fourth condition.
- Add one unpatched `refusal_record` case on `RECOMPUTED` at a known pose, checking `capture`, `original_at_least_1` and `in_domain` against values computed in the test.
- Add a made-up case where one premise differs from the census row's.

### CR-5 — Non-blocking: `captures_agree` at the axis compares nothing

**What is wrong.** At r = 0 the field is `crate is None`, so it reads `true` with nothing compared. The axis row carries `min_certified_lower_bound`, a certified lower bound on the capture at the sweep's least vertex: 0.9984658629684 against the exact 0.9984658630477 on the trial.

**Fix.** At the axis, record that bound. Require the exact capture to be at least the bound, and above it by no more than a stated tolerance. Alternatively, record `captures_agree: null` with a field that says no comparison was made.

### CR-6 — Non-blocking: the per-bin domain is wider than the review stated, without saying why

**What is wrong.** `domain_bounds` uses $[\rho(a_r), L - \rho(a_r)]$, where the review and lemma D's statement use $[L/2, U_r]$. It is sound: lemma C1's quarter turn gives $F_r$ the same values on $[a_r, L - a_r]^2$ as on the quadrant, and N4 needs the whole of that set. The docstring cites lemma D alone.

**Fix.** Cite lemma C1 in the docstring as well, or check the quadrant the crate searches. The crate's search box is rounded outward (lemma C1's note), so a witness that lies a few ulps outside the exact domain would fail closed; say so.

### CR-7 — Non-blocking: v2 cannot pass on format L or on files with points or segments

**What is wrong.** `in_domain` is false for any file that is not format M, and the near-threshold domain flags are too. Every v2 control on the census's four format L rows therefore fails, and those rows use Tokoharu's domain. Three of them also carry points or segments, so their r = 0 direction runs branch and bound, and the `index > 0` guard would discard a correct candidate there. `premises_agree` does not compare `centre_domain`. Nothing in the text says the control is for format M only.

**Fix.** Either compute Tokoharu's domain with the `index > 0` guard lifted for branch-and-bound rows at r = 0, or state that `--control` v2 serves format M with the per-bin domain only and refuse other rows before running.

## For the Records Lane

**The `mixed_n96_L997` receipt.** It may stand where the census route requires `CONTROLS_REFUSED`, on one condition still open: it must be committed under `benchmarks/measure-verifier/census-mixed/wand125-mixed-bounds-2026-10-03/`, so that `test_each_scaled_sweep_refuses_its_mutant_somewhere_with_an_exact_witness` recomputes it from the candidate in the tree and passes. It does not need to be regenerated.

It meets every other condition of the review as recorded, and I confirmed that independently:

- all 187 refusals are coverage refusals, with no `audit-failed`, `non-finite` or `unresolved` row;
- each pose is in the domain;
- each mutant capture is below 1 and equals the crate's;
- the original captures at least 1.00587 at every pose;
- the near-threshold refusal is confirmed at its witness.

Fix CR-1 on the same branch, since that branch's gate is red without it.

**Future v2 receipts.** Receipts made with `f1ddc2379`'s code may stand in the same way for format M certificates on the per-bin domain, each once it is in the tree and held by that test. They need no further re-judging against CC-1, CC-2 or CC-4: the code now enforces those for the sweep. Until CR-3 is fixed, also check by hand that the near-threshold run has `exact_below_threshold: true`. A v2 control on a format L certificate will report `CONTROL_FAILED` whatever the verifier does (CR-7), and that moves nothing. Existing v1 `CONTROLS_REFUSED` receipts stand as the review said, and the new v1 assertion holds all 39.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
