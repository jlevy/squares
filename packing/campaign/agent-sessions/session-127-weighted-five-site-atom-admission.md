---
title: session-127 — Weighted five-site threshold atoms, stages one and two
softschema:
  contract: packing.squares:AgentSession/v2
  schema: ../schemas/agent-session.schema.yaml
  envelope: session
  status: enforced
session:
  id: session-127
  title: Weighted Five-Site Threshold Atoms, Stages One and Two
  date: '2026-09-12'
  started_at: '2026-09-12T19:44:00Z'
  deadline_at: '2026-09-12T23:44:00Z'
  branch: claude/n11-w7-weighted-atom-admission
  primary_bead: think-zvr3
  status: completed
  goal: Carry explicit integer token counts into the production threshold-atom model and both of its exact coverage routes, then reproduce every retained weighted-atom charge from the family geometry, so the representation is admitted without any scientific target being registered or run.
  budget:
    wall_minutes: 240
    max_cycles: 8
    orientation_minutes: 15
    checkpoint_minutes: 20
    slice_minutes: 30
    finalization_minutes: 30
  stop_conditions:
  - Stage one and stage two of the weighted-atom admission review are complete with executable controls, or the unfinished stages are named with their explicit dependencies.
  - No BC327 hypothesis, experiment or scientific target is registered or run in this block, whatever the replay reproduces.
  - An all-ones atom is byte-identical to the unweighted atom it replaces, in both its record and every derived figure, or the change is not admissible.
  workflow_phases:
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    bead: think-zvr3
    objective: Extend the threshold-atom representation with per-site integer token counts, audit every budget and expansion call site the change reaches, and hold the event and direct coverage routes equal on weighted atoms.
    status: completed
    entered_by: session_start
    switch_reason: null
    budget_minutes: 90
    started_at: '2026-09-12T19:44:00Z'
    deadline_at: '2026-09-12T21:14:00Z'
    expected_output: A weighted ThresholdAtom with a token count, a weighted D4 key, a versioned record, and controls over all 32 site masks plus the five named mutations.
    validation_command: uv run --frozen --all-extras --group dev packing-validate --records
    kill_condition: A legacy all-ones atom changes any derived figure or gains any record key, or the two coverage routes disagree on a weighted atom.
    fallback: Keep the token count out of the production model and carry the representation as an admission-only object beside it.
    outcome: The model carries multiplicities, token_count, a token budget, a token-keyed orbit and a variant-gated record; the sweep expands site rectangles to token rectangles and the direct route paints each site with its count; the int64 headroom bound now reads the token count, where five sites understated the retained motif's expansion mass as 9 against its true 209.
    evidence: [packing/src/sqpack/fractional/threshold.py, packing/tests/test_weighted_threshold_atoms.py]
    stop_reason: Every figure the review publishes for the retained motif is reproduced by the model, and both coverage routes agree on weighted atoms while still differing from the same atom read unweighted.
    next_action: Replay the retained receipts against their families through this model.
  - workflow: pipeline-improvement
    focus: correctness
    recording: contemporaneous
    clock_role: work
    bead: think-zvr3
    objective: Reproduce the retained weighted-atom token total, budget, charge and charged-placement list from each family's exact placement geometry, and bind the receipt to the family by content.
    status: completed
    entered_by: evidence_checkpoint
    switch_reason: The model reproduced its published figures, so the retained evidence became the next thing it could be held to.
    budget_minutes: 60
    started_at: '2026-09-12T20:00:00Z'
    deadline_at: '2026-09-12T21:00:00Z'
    expected_output: A maintained replay tool with a receipt, run over every retained reader and family pair, plus mutation controls showing each comparison is load bearing.
    validation_command: uv run --frozen --all-extras --group dev python -m devtools.replay_weighted_atom_source READER.json FAMILY.json
    kill_condition: A declared figure cannot be reproduced and the discrepancy is not an exact, explainable difference.
    fallback: Record the exact discrepancy and leave the weighted target unrun; do not substitute coordinates or candidates.
    outcome: All four retained receipts reproduce exactly — seven tokens, threshold four, budget one, charge 3/2, and each charged-placement list — through the production model on exact rational coordinates up to 965 characters wide. Both inputs are now sha256-bound, which nothing retained did.
    evidence: [packing/devtools/replay_weighted_atom_source.py, packing/tests/test_replay_weighted_atom_source.py]
    stop_reason: Stage two's accept rule is met on every retained pair, and eleven mutation controls show the replay fails when it should.
    next_action: Carry stages three and four forward; they need controls this block did not build.
  progress:
    metric: Admission stages completed against the weighted-atom review's staged accept rules, with no scientific target run.
    before: Multiplicity support existed only in devtools.plateau_reader. The production model refused repeated points, measured its threshold and budget in distinct sites, and expanded inclusion--exclusion over site subsets, so no production reader could hold the retained seven-token motif at all.
    after: Stages one and two are complete. The production model carries token counts through its budget, orbit key, record, event sweep and direct count grid; three readers that cannot price a weighted atom now refuse one instead of reading it as lighter; and all four retained receipts reproduce exactly. Stages three and four are unstarted and named. The frontier register and the global bound are unchanged.
  delegations:
  - task: Map the exact ThresholdAtom and CeilingCertificate model, its D4 handling, its budget chain, and every importer, before any edit.
    operator: Claude Code Explore delegate, read-only
    status: completed
    recording: contemporaneous
    phase: 1
    outcome: Found the three load-bearing uses of point distinctness, the positional rectangle cursor that assumes one rectangle per site, and the int64 headroom bound derived from unweighted subset counts — the three places a naive rename would have broken.
    evidence: [packing/src/sqpack/fractional/threshold.py]
    files: []
    checks: [Reported a shadow ThresholdAtom type in tests/test_verify_threshold_claim_oracle.py that any added field must not diverge from.]
    uncertainty: Reported against a wrong package path at first; corrected mid-task to the src layout.
    elapsed_seconds: 221
    elapsed_quality: platform_measured
    next_action: None; its findings decided the representation.
  - task: Map the existing orbit admission instrument, its record shape, error taxonomy, CLI and every registry it is wired into.
    operator: Claude Code Explore delegate, read-only
    status: completed
    recording: contemporaneous
    phase: 1
    outcome: Found that the instrument stamped its own output kind from the start but checked no declared input kind, while its sibling always has; also found a dead negative-weight branch that Placement refuses first.
    evidence: [packing/devtools/admit_threshold_atom_orbits.py]
    files: []
    checks: [Enumerated the registries a new devtool must join and verified the negatives, including that no check requires a devtool to have a test.]
    uncertainty: The absence claims are pattern searches over a large suite rather than exhaustive proofs.
    elapsed_seconds: 403
    elapsed_quality: platform_measured
    next_action: None; the kind gap was closed in this block.
  - task: Find the existing implementation behind each phrase the bead uses, or report plainly that no precedent exists.
    operator: Claude Code Explore delegate, read-only
    status: completed
    recording: contemporaneous
    phase: 1
    outcome: Named the direct, event and interval routes and their existing agreement control; confirmed five precedents; reported that the common row and point manifest has none and that the lossy old verifier survives only as archived text.
    evidence: [packing/tests/test_fractional_threshold_interval.py, packing/devtools/decide_threshold_certificate.py]
    files: []
    checks: [Ranked confidence per item and stated what was searched, so the two weak items were not taken as precedent.]
    uncertainty: Items six and seven were reported low and medium confidence respectively, and both held up.
    elapsed_seconds: 484
    elapsed_quality: platform_measured
    next_action: Stage three will need the three-route agreement controls this mapped.
  - task: Derive the complete ordered checklist of registries a new devtool and test must satisfy, from the code of the checks rather than from prose.
    operator: Claude Code Explore delegate, read-only
    status: completed
    recording: contemporaneous
    phase: 1
    outcome: Established that a plain printing, test-covered devtool needs no registry entry at all, and that the T201 waiver set is asserted by equality so a new per-file waiver would fail CI.
    evidence: [packing/tests/test_lint_floor_contract.py, packing/tests/test_change_scoped_selection.py]
    files: []
    checks: [Measured the tier step counts live against the working tree rather than reading them from documentation.]
    uncertainty: Marked the controls.yaml entry as conventional rather than gated, which matches what was found.
    elapsed_seconds: 509
    elapsed_quality: platform_measured
    next_action: None; the new devtool needed no registration.
  - task: Report exactly what retained data exists for an independent source replay, and whether any input is missing.
    operator: Claude Code Explore delegate, read-only
    status: completed
    recording: contemporaneous
    phase: 2
    outcome: Found the motif complete as data in four retained receipts with their three distinct families, and established that no digest anywhere binds a receipt to a family; also found that two families are byte-identical, so four receipts cover three families.
    evidence: [packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a6-loop-reader-2.json]
    files: []
    checks: [Verified that floor_atom_columns is archived text and not live code, and that multiplicity appears nowhere in the production modules.]
    uncertainty: None material; its verdict that stage two was achievable was confirmed by running it.
    elapsed_seconds: 361
    elapsed_quality: platform_measured
    next_action: The missing inputs it named all lie downstream of stage two.
  outputs:
  - packing/src/sqpack/fractional/threshold.py
  - packing/src/sqpack/fractional/threshold_interval.py
  - packing/devtools/replay_weighted_atom_source.py
  - packing/devtools/admit_threshold_atom_orbits.py
  - packing/devtools/decide_threshold_certificate.py
  - packing/devtools/admit_fixed_support_dual.py
  - packing/tests/test_weighted_threshold_atoms.py
  - packing/tests/test_replay_weighted_atom_source.py
  - packing/tests/test_admit_threshold_atom_orbits.py
  - packing/tests/test_fractional_threshold_interval.py
  - packing/campaign/agent-sessions/session-127-weighted-five-site-atom-admission.md
  checks:
  - Baseline 4d00ab68, the head of PR 149; origin/main was fetched before the branch was created.
  - 'The retained motif''s published figures were reproduced before any test was written: token total 7, budget 1, expansion over 64 token subsets with absolute coefficient mass 209.'
  - 'The same atom read as five sites reports expansion mass 9, a 23-fold understatement; this is pinned as a control rather than left as a comment.'
  - All four retained reader and family pairs reproduce token total 7, threshold 4, budget 1, charge 3/2 and their exact charged-placement lists.
  - Eleven mutation controls over the replay, including a heavy site read as light, which moves the charge while leaving the budget at one.
  - 'Ruff and ruff format clean over the tree; basedpyright reports zero errors and zero warnings.'
  - The threshold, interval, admission, certificate, dilation and plateau suites were run together; their result is recorded in the report below.
  - 'full gate: fast at 6cb9eebd: passed (585.26s of a 600s ceiling at 4 cpus, --jobs 3 --inner-jobs 1; ALL CHECKS PASSED and 4997 tests passed; the only failing step was this declaration''s own absence, which this line supplies. Additions over that commit are records only: these rollups, the close report, and the regenerated synopsis, re-checked by a clean --records run)'
  resource_rollups:
  - packing/campaign/resource-usage/f37f604c-3212-50e9-b7f7-4b00b94bfcc0.yaml
  - packing/campaign/resource-usage/agent-ac97342e4ca35e69e.yaml
  - packing/campaign/resource-usage/agent-ab1bed639a6db6acc.yaml
  - packing/campaign/resource-usage/agent-a9b644d4541443deb.yaml
  - packing/campaign/resource-usage/agent-a4306d8d044623c7c.yaml
  - packing/campaign/resource-usage/agent-a106b43671ede9c00.yaml
  stop_reason: Stages one and two of the weighted-atom review's staged admission are complete with executable controls, and the remaining two stages need coverage and paired-runner controls that are their own work rather than an extension of this one. No scientific target was registered or run, which the bead forbids until every stage passes.
  next_action: Continue under think-8c9e, the weighted-atom coverage mechanics, which cover the direct, event and interval controls including the boundary and undercharged-core cases and the interval route's stall handling. Stage four's paired runner and exact common manifests are tracked separately and blocked on it.
---
# Session 127 — Weighted Five-Site Threshold Atoms, Stages One and Two

This is a W7 `pipeline-improvement` block on
[`think-zvr3`](../../../docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md),
the root blocker of `think-yc80`, `think-zoik` and `think-45xk`, and the prerequisite
for the second-ranked continuation in
[X-027](../explorations/X-027-stromquist-fractional-and-structural-strategy.md).
It admits a representation.
It registers no hypothesis, runs no experiment, and moves no bound.

## What Was Not Possible Before

The retained object is a five-site threshold atom with token counts $(2, 2, 1, 1, 1)$ at
threshold four: seven tokens, budget $\lfloor 7/4 \rfloor = 1$, and a charge of $3/2$
against its source family.
The production model could not hold it at all.
`ThresholdAtom` refused repeated points, measured its threshold and budget in distinct
sites, and expanded inclusion--exclusion over site subsets.
Multiplicity existed in exactly one place in the repository,
[`devtools/plateau_reader.py`](../../devtools/plateau_reader.py), which is how the $3/2$
charge came to be recorded in the first place.

So the gap was not that the mathematics was unsettled.
[The weighted-atom review](../../../docs/project/reviews/review-2026-09-10-n11-weighted-five-site-atoms.md)
had already specified the representation, the two globally valid charges, the resource
proof, and a staged admission with falsifiable accept rules.
The gap was that production lagged it.

## Sites Are Not Tokens

One distinction carries the whole change.
`size` counts distinct sites and `token_count` counts tokens; geometry is per site,
while the threshold, the budget and the expansion are per token.

The review warned that a single careless rename “can make a sweep consume seven
rectangles when it created five”, and an audit of every `.size` use found exactly that
split, with no overlap:

| Call site | Reads | Why |
| --- | --- | --- |
| the sweep’s rectangle cursor | sites | one membership rectangle per distinct coordinate |
| the direct route’s rectangle slice | sites | the same rectangles, painted with their counts |
| `budget` | tokens | disjoint cores consume disjoint site tokens |
| the inclusion--exclusion expansion | tokens | subsets are subsets of token indices |
| the `int64` headroom bound | tokens | its bound is that expansion’s coefficient mass |
| the orbit admitter’s per-image budget | tokens | the same budget, priced per image |
| the interval route’s member row | tokens | its boolean gather counts what the row holds |

The sharpest evidence that this matters is the headroom bound.
Read as seven tokens the retained motif expands over 64 subsets with absolute
coefficient mass 209, which is the figure the review publishes.
Read as five sites the same atom reports mass 9. A headroom check given the smaller
number would pass a term list it cannot hold, and it would do so silently, so the
23-fold gap is pinned as a control rather than described in a comment.

## Two Routes, Still Independent

The sweep expands each site’s rectangle into one rectangle per token and signs the
subsets; `itertools.combinations` works by position, so two tokens on one site stay two
distinct indices even though their rectangles are equal.
The direct route does not reuse that expansion at all: it paints each site’s rectangle
with its own integer count and thresholds the total.
They share nothing past the event grid, which is what makes their agreement evidence.

A second control guards against the way that agreement could be worthless.
Two routes that both ignored the token counts would agree perfectly, so the tests also
require the weighted routes to differ from the same atom read unweighted.

## Where a Weighted Atom Is Refused

Three readers cannot price a weighted atom, and each now says so rather than reading a
lighter object:

- [`decide_threshold_certificate.py`](../../devtools/decide_threshold_certificate.py)
  parses the token counts and then refuses them under `variant: threshold`, which is the
  review’s own prescription: give weighted records a variant the unweighted gate
  refuses.
- [`admit_fixed_support_dual.py`](../../devtools/admit_fixed_support_dual.py) prices
  ordinary orbit columns, whose budget and orbit key both change under token counts.
- The interval route refuses an atom above a declared token cap before it allocates,
  since its member row accumulates into one `int16` lane.

The marker is required rather than inferred, and that is not a new idea here.
[`dilation_corollary.py`](../../devtools/dilation_corollary.py) already carries a
record-level variant for the same reason one level up: the point decoder “would silently
ignore its `threshold_atoms` and decide a weaker object”.
The archived reader behind the retained charge did read a bare `multiplicities` field,
coercing it through `int` under a float membership slack, so this is a hazard with a
worked example rather than a precaution.

A legacy all-ones atom is unchanged in every respect, including gaining no record key,
so retained records and their digests do not move.

## Stage Two: The Retained Charges Reproduce

[`replay_weighted_atom_source.py`](../../devtools/replay_weighted_atom_source.py)
rebuilds a retained receipt’s declared atom as a production `ThresholdAtom` and derives
the token total, budget, charge and charged-placement list again from the family’s exact
placement geometry. All four retained receipts reproduce exactly:

| Receipt | Token counts | Charged placements | Result |
| --- | --- | --- | --- |
| `lane-a6-loop-reader-2` | $(2, 2, 1, 1, 1)$ | 8 | reproduced |
| `lane-a6-reader-saturated-symmetric` | $(1, 2, 2, 1, 1)$ | 10 | reproduced |
| `lane-a6-loop-reader-1` | $(1, 2, 2, 1, 1)$ | 10 | reproduced |
| `lane-a6-reader-saturated-153-40` | $(2, 2, 1, 1, 1)$ | 5 | reproduced |

Every one reports seven tokens, threshold four, budget one and charge $3/2$, on exact
rational coordinates up to 965 characters wide.
The second and third families are byte-identical, so these are four receipts over three
distinct families.

Two details matter more than the agreement.
First, nothing retained binds a receipt to a family by content — the `source` fields
name scratch paths that no longer exist — so the replay digests both files it is given,
and the digests are what a later record can pin.
Second, a replay that cannot fail confirms nothing, so eleven mutation controls move
each declared figure in turn.
The instructive one reads a heavy site as light: six tokens still floor to a budget of
one, so the budget alone would not catch it, and the charge is what moves.

One comparison was removed for the same reason.
The declared threshold was being checked against itself, since the rebuild takes it as
input, and a check that can never fire is the same false assurance as the dead
negative-weight branch this audit found in a sibling reader.
A wrong threshold is caught by the budget it implies.

## Findings Worth Recording Separately

Three findings are carried as beads rather than written into
[`defects.yaml`](../../defects.yaml), because two other open branches already change
that file’s `count` and a third edit would make the reconciliation worse rather than
better:

1. The orbit admission instrument stamped `KIND` on its receipts from the start but
   checked no declared input kind, while its sibling always has.
   A record of another shape whose field names lined up would have been admitted
   silently. Closed in this block, with a control.
2. That instrument’s negative-weight branch is unreachable: `Placement` refuses first,
   and the existing test matches the other message.
   Not fixed here.
3. The retained receipts write the token total under the key `size`, where the
   production model’s `size` means distinct sites.
   Two live modules use one word for two quantities, which is the confusion this block
   exists to separate.

## What Is Not Done

Stages three and four of the review remain, and their accept rules name work this block
did not do: the boundary and undercharged-core controls across all three coverage
routes, the interval route’s stall handling, the exact common row and point manifests,
and the paired runner’s cap, deadline and forged-witness refusals.
The review’s own instruction for this case is to carry the unfinished dependencies
forward and keep the target unrun, which is what the handoff now says.

The third of those has no precedent in the repository to follow.
A common row and point manifest is named as missing evidence in two documents and does
not exist in code, so stage four builds it rather than extends it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
