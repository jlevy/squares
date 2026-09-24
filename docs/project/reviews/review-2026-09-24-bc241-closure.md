# Closing BC-241: The Trump Local Theorem After a Full Generator Replay

A closure review (Fable, extra-high thinking, 24 September 2026) of what the
source-distinct BC-241 review of
[BC-240](../../../packing/cases/trump11/isolation-theorem.md) left open, with the full
radius-generator replay that BC-241 was forbidden to run.
Every rung of the n11 settlement ladder closes its Trump-degenerate leaves with BC-240’s
first clause, so
[exp-232](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-232-h236-rung-zero-closed.md)
and
[H-236](../../../packing/campaign/hypotheses/H-236-n11-fixed-angle-global-optimality-at-trump.md)
currently carry “pending BC-241”. This review says what that qualifier can now become.

## Verdict

**BC-241 can close.** The radius generator, run in full on a different host and by a
different operator than BC-199, reproduces every retained value of the BC-199 record:
4,954 leaf values including all 128 branch moduli, argmin faces, stress constants and
caps, with the only difference the declared `tangent_cones.py` source drift.
The method-distinct `capture_radius` control reproduces the per-row weighted modulus on
all 8,448 faces to 32 digits and matches its own exp-227 record on every value.
The BC-241 checker still accepts at this head with all three falsifying mutations
refused.

The first clause of BC-240, the only clause the rung leaves use, is therefore supported
by a source-distinct review of its rows, curvatures, stresses and aggregate arithmetic,
by two executions of the generator that agree exactly, and by a second implementation of
the face linear programs that agrees on every face.
What remains is a packaging obligation and one unshared-source producer, both listed
below; neither is a mathematical gap.

## What BC-241 Left Open

The closure manager’s terminal disposition
([gate-hour-04](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/gate-hour-04.md))
was `accept_retained_record_dependent_local_scope`, and the agenda cell is
`retire-success`. Three limits were named there and in the review packet’s
`unreviewed_generator_obligations`:

| Left open | Why it mattered | State after this review |
| --- | --- | --- |
| No full radius-generator replay | BC-241 was forbidden to run `isolation_radius`; BC-199’s record froze no generator hash and has no `--replay` mode, so the three agreeing runs of session 086 were the only executions | Closed: fourth execution, value-for-value match |
| All-face witness gap | The per-branch weighted modulus is a minimum over 66 face LPs; BC-199 retains the argmin face’s exact vertex but not the other 65 faces’ dual lower bounds, so the record alone certifies an upper bound on each branch modulus and only the generator’s word for the lower bound. This is a real obligation for the first clause | Discharged by computation twice (generator replay, `capture_radius` on all 8,448 faces), not by a retained witness |
| Weighted aggregate not recovered from every face | Per-branch weighted values are retained as 32-digit decimals; the exact aggregate rational could not be rebuilt by the checker | Closed: the replay recomputes the exact aggregate and it matches the retained rational; the control matches the decimal on every branch |
| Gap and symmetry producers not rerun | Retained as exact premises; the inactive-feature cap is load-bearing for the first clause (it is what puts every nearby packing into one of the 128 branch systems) | Rerun by the generator replay with identical output; still single-source (see residuals) |
| Closure disposition “pending” | The packet header, the review JSON `status`, and the `n-011.md` scope were never updated after the manager’s acceptance | Bookkeeping; wording proposed below |

The closure manager did not certify the controls a third time; the disposition text was
recorded in the gate file but never integrated into the packet, the frontier scope, or
the ledger prose, which is why every downstream record reads “pending”.

## What Ran

All commands from `packing/` in worktree `w3-review` at `99582155c`, project Python
3.14.7, two processes at a time alongside other lanes.

| Command | Wall | Result |
| --- | ---: | --- |
| `uv run --frozen --all-extras --group dev python -m cases.trump11.isolation_radius --record ../attic/bc241/isolation-radius-replay.json` (defaults: box `1/64`, threshold `1/8`, 128 branches, weighted and identity passes, refine limit 6, the BC-199 configuration) | 474.5 s (BC-199: 350.4 s) | exit 0; `attic/bc241/compare_replay.py` reports 0 unexpected differences over 4,954 leaf values; one expected difference, `inputs[tangent_cones.py]` `31f1c09f` to `17302de5` |
| `uv run --frozen --all-extras --group dev python -m cases.trump11.capture_radius --record ../attic/bc241/capture-radius-replay.json` (exp-227’s command) | 510.3 s (exp-227: 446.1 s) | exit 0; 2,978 leaf values identical to the retained exp-227 record; `modulus_control.weighted_modulus_min_lower_decimal` = `0.00404257348533135396598905037166` over 8,448 faces; per-branch weighted modulus, argmin face and exact flag match BC-199 on all 128 branches |
| `uv run --frozen --all-extras --group dev python -m devtools.review_trump_local_theorem` | 37.1 s | disposition `accept_retained_record_dependent_local_scope`; mutations `active_row_coefficient`, `separating_axis_sign_retaining_stress`, `per_row_factor_2_over_K_to_1_over_K` all rejected; four selected faces with exact zero primal-dual gap |
| `pytest tests/test_trump_isolation_radius.py tests/test_review_trump_local_theorem.py` | 60.5 s | 12 passed |

Headline constants, exact rational match in both directions: `rho_uniform =
288616983/125000000000`, `rho_row = 808514697/200000000000`, `C_uniform =
2808470331/125000000`, `C_row = 2574612531/200000000`, `K = 4972105219/500000000`, gap
cap `5875508797/1000000000000` (short form), symmetry radius `1/16`. The two modulus
classes are unchanged: 64 branches at `0.011480272061` and 64 at `0.016423844897`
(uniform), `0.004042573485` and `0.005760353017` (weighted), decided by contact (9,
10)’s option, argmin face `theta_10 = -1` in every binding branch.

Source drift, checked directly:
`git show 01ca830a:packing/cases/trump11/isolation_radius.py` hashes to the
record-producing `56a2c6f4`, and its diff against the current `3b4f754b` is three hunks,
the expanded Archimedes comment and two `exact_pivot_rows` calls dropping the removed
`field` argument, exactly as the BC-240 packet declares.

## Independence, Stated Plainly

- The generator replay is an independent *execution*, not an independent
  *implementation*: same source, different host, different operator, nineteen days
  apart. It rules out nondeterminism, host dependence and record tampering; it cannot
  catch a logic error shared with BC-199.
- `capture_radius` shares the witness loading, row identification and per-row curvature
  `K_j` with the generator and has its own face LP, far-normalised dual and exact vertex
  code. Its modulus control is therefore a second implementation of the face layer only.
- The BC-241 checker is source-distinct throughout: it rebuilds all 56 distinct row
  gradients from the exact witness, recomputes `K_j` on the declared box for each,
  checks every branch’s stress residual and constants, and re-solves four faces exactly.

Together, the row and curvature layer is source-distinct-verified, the face layer has
two agreeing implementations on every face, and the whole pipeline has four agreeing
executions. Under [epistemics.md](../../../epistemics.md) that is `C3`, not `C4`: no
second method exists for the theorem as a whole.

## Residuals

1. **No retained per-face witnesses.** Both tools compute exact dual lower bounds on all
   8,448 faces and retain only the minima.
   A reader who wants to check the first clause without rerunning a 500 s computation
   cannot. This is the one item from BC-241 that is not closed, and it is a packaging
   choice, not a doubt: a `--retain-faces` mode on `isolation_radius` would produce
   roughly 8,448 rational dual vectors of 42 entries.
2. **The inactive-feature gap cap is single-source.** `gap_radius` and the box-aware
   Lipschitz constants in `elementary_functions` have been run four times and are
   exercised by `test_gap_and_symmetry_certificates_hold`, but no source-distinct code
   recomputes them. The cap (`0.005875...`) exceeds `rho_row` by a factor of 1.45 and is
   not binding, so an error would have to be large to matter; a source-distinct
   recomputation is a bounded task of about an hour and belongs in a BC cell, not in
   this review.
3. **The generator has no `--replay`.** The comparison that closed this review lives in
   `attic/bc241/compare_replay.py`; OR-1 says it should become
   `isolation_radius --replay RECORD` so the next replay is a command in the record, and
   so the radius can carry a replay command if it is ever registered.

None of these bears on the rung leaves: the reader in `fixed_angle_tree_check.py` uses
only the first clause (a packing of side at most `U` whose image lies within `rho_row`
of the labelled pose is the pose), never the quadratic constant.

## Recommended Disposition and Wording

**Agenda-026, BC-241, closure disposition** (coordinator-owned; the cell already reads
`retire-success`, so this is the `follow_up` and the packet header):

> Accepted at local scope on 2026-09-06 and closed on 2026-09-24 after a full
> radius-generator replay (474.5 s, 4,954 values identical to BC-199) and the
> method-distinct `capture_radius` control (all 8,448 faces, 32-digit agreement).
> The first clause is verified, exact.
> Per-face dual witnesses are recomputed on demand, not retained; the inactive-feature
> gap cap remains single-source and non-binding.
> See docs/project/reviews/review-2026-09-24-bc241-closure.md.

**`isolation-theorem.md` status line**: replace “awaiting the source-distinct BC-241
review” with “BC-241 accepted 2026-09-06; generator replayed 2026-09-24 (review
2026-09-24-bc241-closure)”. Leave `bc-241-trump-local-theorem-review.json` as the
historical terminal packet.

**`n-011.md` rigidity scope**, last sentence, replacing “which the source-distinct
BC-241 review accepted at retained-record-dependent scope without an independent
radius-generator replay and with its closure disposition still pending”:

> which the source-distinct BC-241 review accepted on 2026-09-06 and a full
> radius-generator replay on 2026-09-24 reproduced value-for-value on all 128 branches,
> with the weighted modulus confirmed on all 8,448 faces by the method-distinct
> capture_radius control; the first clause is verified, exact, with per-face dual
> witnesses recomputed rather than retained.

**H-236 and exp-232**: drop “pending BC-241”. The verdict reason should read “the local
theorem it relies on is BC-240’s first clause, accepted by the source-distinct BC-241
review and replayed in full on 2026-09-24”, and the confirmation stands at “verified,
exact”. The same replacement applies to the rung-0 contract review’s scope row and to
X-045’s premise table, whose “no independent full radius-generator replay” is no longer
true.

**Not recommended**: registering `rho_row` in the frontier `rigidity` block.
That needs an evidence entry with a replay command and passing status, which the
generator cannot supply until residual 3 is built.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
