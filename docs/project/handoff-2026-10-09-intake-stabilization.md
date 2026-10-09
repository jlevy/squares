# Intake stabilization handoff, 2026-10-09

The owned intake source branches are preserved in normal commits and published draft
PRs. The stack is not yet qualified for merge.
Resume stabilization from the lowest failing layer, then merge each qualified prefix; do
not repeat completed mathematical reviews merely because a parent was integrated.

This is a checkpoint requested by the owner, not an intake-completion verdict.
Live GitHub status can change after this record.
Local evidence references below are relative to the durable external source directory
unless explicitly stated otherwise.

## Entry point and ownership

Read this handoff, `development.md` validation tiers, and
`packing/campaign/result-import.md` before resuming.
Run `tbd prime`, `tbd policy show`, and `tbd sync`, then pull and start the relevant
bead before editing it.
The parent is `think-mx4n`; handoff/stabilization tracking is `think-yij0`. Session
instructions authorize editing, formal stacks, subagents and merging when ready.
Recheck effective project policy in a new session.

Root was the sole publisher and merger.
Sol workers owned separate source branches; Astra performed scoped source, engineering
and mathematical reviews.
The team has four concurrency slots including root.
Attempts to replace a completed agent with a faster Sol administrative agent hit the
thread limit. A fresh session can use Sol at medium reasoning for CI/status/bookkeeping
and higher reasoning for fixes, with Astra reserved for changed mathematical or
substantial engineering scopes.

The primary checkout `/Users/levy/wrk/github/squares` is another owner’s
`codex/n17-state-review` branch.
Do not reset its index, switch its branch or discard its changes.
Use the existing external worktrees and coordinate any shared commit hooks.

The external source directory is
`/Volumes/spud-ext1/source-worktrees/squares-import-resume`:

- `import-ryxu-432`: this standalone handoff branch
- `import-asymptotic`: `codex/import-couzo20-custody-1545`, PR #466
- `import-refinements-preserved`: optional font diagnostic branch
- `review-notes`: unique logs, review packets, receipts and PR bodies
- `intake-preparations`: preserved original source inputs, outside disposable scratch

Inspect `git worktree list` for the remaining branch locations; do not create another
full checkout unless necessary.
Worktrees contain source; they are not disposable build outputs.
The recent external and internal free space was only several GiB.

Verify `/Volumes/spud-ext1` is mounted and writable.
For each task set `TMPDIR`, `CARGO_TARGET_DIR` and `UV_CACHE_DIR` beneath
`/Volumes/spud-ext1/agent-scratch/<task-id>/`, with a distinct Cargo target per
worktree. Pause disk-heavy work if the volume is unavailable.
Python is 3.14.7: use the project `packing/.venv/bin/python3` or the frozen uv
environment; never PATH `python3`. Keep unique source and evidence outside scratch.
Use `fdu` and `trash` only for eligible unused large builds; do not empty Trash or
assume moving files there frees disk blocks.

## Landed work and current main

This continuation merged #434, #439, #440 and #441 after their applicable exact-head
checks and full checkpoints passed.
Earlier intake #427, #429, #431, #433 and #437 was already merged.
#427 and #429 were the two saved #422 branches.

The qualified intake prefix ended at main `d43ea686d555efe3d866e88b960f60c9d2e0a7d1`,
whose tree equals the qualified #441 tree.
A fresh fetch now sees main `3213d651b880d7768bce8506efaf75c2089aeb4f`, the merge of
another owner’s #458 survey.
The remaining intake heads include d43, not this new main.
Merge `origin/main` normally into the owning lowest layer and propagate normal parent
merges; preserve independent changes, resolve conflicts, update actual DATA pins and
qualify changed heads.
Do not rebase, force-push or relax gates.

## Formal stack 430

430 is a native GitHub stack number, not a PR or issue.
Inspect it with `gh api 'repos/jlevy/squares/stacks?pull_request=466'`. Local
`gh stack view` tracking is not authoritative for remote membership.
Existing merged members are 427 → 429 → 434 → 439 → 440 → 441.

| PR | Current saved head | Parent | Purpose | Remaining qualification |
| --- | --- | --- | --- | --- |
| [#442](https://github.com/jlevy/squares/pull/442) | `830cd91d903cf57b7177017aaa510011878827a5` | main | Ry–Xu rational/radical import | Required PR checks green; full failed on 12.08s test and stale bead snapshot |
| [#443](https://github.com/jlevy/squares/pull/443) | `2bd8d96a9860657149a1e47ae5ce0bddc34208b3` | #442 | FN1 full-input and receipt custody | Required PR checks and exact-head full checkpoint passed; parent and fresh-main integration remain |
| [#448](https://github.com/jlevy/squares/pull/448) | `11bef7da1eb7c1817007bf9bcb1013ededcd1735` | #443 | Fourteen Gupta refinements | Packing green; Pages overview and full checkpoint failed |
| [#449](https://github.com/jlevy/squares/pull/449) | `0cae0729f41c2f9ecf16bddf7250a3398796ec5c` | #448 | Rehwaldt n68 v1.2 reports | Current automatic checks green; original Linux CLS failure has no causal fix; current full pending |
| [#450](https://github.com/jlevy/squares/pull/450) | `4585b8d5727b8986bbc37317bdd83224560c950c` | #449 | Fine-net reports and n17 status | Automatic checks green; current full pending |
| [#459](https://github.com/jlevy/squares/pull/459) | `75a483d0d9e7c26af5af28cb0160f6d2e6214427` | #450 | Independent Gupta confirmation | Current validate failed; current full pending |
| [#460](https://github.com/jlevy/squares/pull/460) | `324ff042c0d1412131ea388d100b21739f5881ed` | #459 | Eight Couzo rational reports | Current validate failed; current full pending |
| [#463](https://github.com/jlevy/squares/pull/463) | `c20e70f85c85bdb47d651cc7878027af436c094c` | #460 | Three dated source-only reports | Current suite A failed; current full pending |
| [#466](https://github.com/jlevy/squares/pull/466) | `6acce39a0badda1714e796444207f86a0569cd40` | #463 | Twenty outside-horizon source-custody reports | Source accepted; records timing ceiling exceeded; hosted checks failing/unfinished; full and public review binding pending |

All nine are drafts at capture.
GitHub reports the existing first eight as mergeable or unstable rather than conflicted;
this means Git can compose their declared parent, not that they are qualified for merge.
Read current required checks, full runs and published review bindings separately.
The optional diagnostic child is recorded below when published.

Current review bridges are actually published at these heads: #442 review5465247373,
#443 review5465349902, #448 review5465350209, #449 review5465468486, #450
review5465468798, #459 review5465468996, #460 review5465469320 and #463
review5465469648. They preserve the earlier four scientific scopes and identify the
changed source composition; they are not fresh full mathematical audits.

The five upper normal merges differ from their prior heads solely by the accepted
`packing/tests/test_site_rendering.py` blob `5722150c05db5adb0a931a866f0834f69cf79429`;
science, private inputs, own controls and DATA pins are unchanged.
Receipts: `review-notes/pr442-hpif-final-five-normal-composition.json` and
`review-notes/catalogue-stack-astra-20261008/pr442-hpif-final-five-astra-composition.json`.

## Failures to resolve without weakening limits

The #442 [full run](https://github.com/jlevy/squares/actions/runs/37877186650) failed:
`test_overview.py::test_each_row_detail_names_its_novelty_label` took 12.08s against
12s, and the fetched bead snapshot had closed `think-hh48` while the request ledger
still described it as open.
Root reopened/claimed/synced that bead; the maintained checker then passed.
Keep hh48 open until #466’s published reply ledger lands on main.
The run’s other scientific jobs passed.
This does not make the full run green.
The raw validate log is `review-notes/pr442-830-full-validate-113648368999.log`.

#443 full [37878602026](https://github.com/jlevy/squares/actions/runs/37878602026)
completed successfully at the saved 2bd8 head.
Its parent #442 remains blocked and new main is not yet integrated.
#448 full [37878605786](https://github.com/jlevy/squares/actions/runs/37878605786)
completed with validate and aggregate failure from the stale bead snapshot: open issue
#399 named closed hh48. The live bead has since been reopened and checked; a new
qualified head still needs its actual full result.
No duplicate full runs are needed for these saved heads.
The latest failing upper automatic runs are:

- #448 Pages [37878589945](https://github.com/jlevy/squares/actions/runs/37878589945),
  overview
- #459 Packing [37880004263](https://github.com/jlevy/squares/actions/runs/37880004263),
  validate
- #460 Packing [37880004518](https://github.com/jlevy/squares/actions/runs/37880004518),
  validate
- #463 Packing [37880003789](https://github.com/jlevy/squares/actions/runs/37880003789),
  suite A

The read-only audit captured actual failure causes in
`review-notes/handoff-ci-failures.json`:

- #448 frontier.html at 1280px dark has CLS 0.209 against 0.1, in job113652934218. This
  is a second real layout-shift failure, not the original #449 390px sample.
- #459 and #460 validate refuse three missing historical registrations for
  `papers/square-packing-methods-survey.html`, `.md` and `.pdf`. Their fast walls were
  below 150s. Fresh main #458 owns this survey; inspect the historical registry and
  normal main integration rather than attributing these to the earlier browser timeout.
- #463 suite A fails
  `test_result_status::test_superseded_is_marked_on_a_bound_and_where_a_later_result_is_declared`
  because its expected superseded set excludes T-129. There were 4,347 passes and eleven
  skips; the failing assertion is separate from its advisory wall overrun.
  Preserve the three source-only dated claims and audit the expected set semantically
  before fixing the control.
  Cancelled superseded jobs are not successful checks.
  The six known-bad full runs using the hanging browser test were cancelled only after
  their job receipts were preserved; their cancellation gives no qualification credit.

### Browser layout shift and diagnostic child

Original #449 head `4963448e33c39002a48593ef79999940b153f2c0` had a real Linux 390px
light-mode CLS of 0.2512375663 against the unchanged 0.1 limit in
[37875117402](https://github.com/jlevy/squares/actions/runs/37875117402). A dominant
shift occurred while fonts settled and navigation changed from two lines to one.
All 401 math-content controls passed and native timing was below 300ms. A current green
sample does not establish that the intermittent cause was corrected.

The optional font diagnostic records physical CDP font faces, computed styles, boxes,
held font URLs and two snapshots.
Its seven local controls passed.
A controlled Mac probe observed fallback-to-SourceSans transitions and CLS 0.04994; it
is an intervention, not a Linux reproduction or a normal gate pass.
No production metric fix exists yet.
Metric-compatible prose fallbacks exist in `site.css` but the papers assembly omits
them; a SourceSans change requires measured Linux face/weight evidence.

The diagnostic workflow is an explicit manual opt-in; default PR/push/manual-false jobs
and limits remain unchanged.
It must render the immutable original #449 inputs, not label the newer inherited data
with that revision. The worker is preserving the reviewed tool closure before checking
out the immutable input head in the same CI workspace.
Both input and tool provenance belong in the diagnostic artifacts.
No diagnostic was dispatched for this handoff.
Use its final source receipt and scoped Astra review before dispatching it in the next
session.

#466 automatic Packing
[37880910357](https://github.com/jlevy/squares/actions/runs/37880910357) has three
failing jobs. Validate and suite C refuse four new source-custody comparison sites
missing from the integrity baseline (Couzo checker lines 224, 226, 287 and 552).
Validate also refuses the three survey-history registrations.
Suite A has the same extra-T-129 expected-set assertion as #463. The shard walls exceed
advisory budgets, but these assertions are the functional failure causes.
Its current Pages run
[37880910382](https://github.com/jlevy/squares/actions/runs/37880910382) passed.
Resolve the integrity contract through the maintained baseline workflow with real
trust-boundary justification; do not suppress its test or register routine Git hashes as
assurance. No fix was made during this preservation checkpoint.

## Twenty-report custody child

#466 retains twenty reports for 327, 332, 335–342, 364, 369 and 372–379: 7,104 complete
poses, 21,312 coordinate tokens, 73 roles, 72 source blobs and three fixed upstream
trees.
It retains derived numerical facts; original TXT/SVG/source bytes stay in external
custody because redistribution licensing was not established.
It changes no selected case, T row, bound, geometry verdict or scientific grade.
Precision wording describes representation-compatible binary64 round-trip encoding, not
author computation precision.

Source commit `6068a049baeee5dfcb82cf82945049d71c672b4a`, pin commit
`bd11f8dce679a5b781389f3eed6e1dd31bef1884`, and final normal merge `6acce39a` are
committed. The actual DATA pin remains 6068a049; pin checks and normal hooks passed.
Astra accepted the final `bb76cc21e89fde9daf709a673b6579775eb84c00` tree.
Final records passed 49 selected steps functionally in 456.15s, exceeding 300s on a
10-CPU/jobs2/inner1 UNARMED host.
This is neither timing nor full/hosted qualification.
Live and Git selected snapshots agree at 200,080,424 of 201,326,592 bytes.
The ordinary 22-file source packet is excluded from that private snapshot by the
existing resources prune; it remains present in ordinary Git.

Direct Softschema checks passed for 24 new records.
A direct inherited evidence.yaml check refused aliases; the maintained repository schema
check passed. No global schema weakening was made.
The final receipt is `review-notes/couzo20-custody-1545/final-handoff.json` and records
log `review-notes/couzo20-custody-1545/final-parent-records.log`.

## What the reviews caught

Reviews found substantial defects, including a serialized algebraic interval whose
rounded center was inconsistent with its tiny radius, incorrect handling of a zero
linear root, and a source-pin write path needing fail-closed checks.
These fixes belong to the polynomial owner’s foundation and are source accepted; their
integration and CI remain that owner’s responsibility.
No counterexample to a standing best bound was established.

Other corrected engineering issues include the no-JavaScript stylesheet-injection hang,
a cache-sensitive behavioral assertion, expensive repeated population/witness work, a
mobile-grid expectation, a missing dated SQUISH source card, and a #466 schema read
occurring before its fixed input envelope was checked.
Scientific assertions remain separated from computational verification and proof.
Full CI, timing and independent proof obligations have not been replaced by review
prose.

## Remaining intake beyond this stack

A fresh `make intake` at d43 produced 58 action flags: 43 issue/ledger flags and 15
repository flags, plus 15 owned obligations, two resolved dependency flags and two
manual sources not freshly checked.
These counts are a sweep, not 58 new imports.
Comparing the pending #466 ledger accounts for 38 of the 43 issue flags.
Five replies still need complete read/classification and ledger reconciliation:
400/6071299059; 405/6069228392; 405/6070358282; 405/6071221013; 405/6073310240. Receipts
are `review-notes/main-d43-live-intake-sweep-20261009.md` and
`review-notes/main-d43-pending-bd11-issue-ledger-flag-comparison.json`. The new Kingbird
capture had zero changed counts and zero below-record entries.

Complete original follow-up custody is preserved under
`intake-preparations/couzo-followup-five-2d32a6e/`: immutable upstream
`2d32a6e96f55c5dc1a2dd0e3581098e7c0105252`, tree
`1e98bf6ddb40deac1874eabc0c109b30edb6e2ad`. Five rational certificates for 84, 86, 105,
175 and 270 contain 720 poses/119,049 bytes.
Two newer reported inputs for 375/378 contain 753 poses/54,556 bytes and are also
preserved. None has new geometry/adoption work.
The pending plan is `next-five-import-replay-plan.json`; beads `think-88r0` and
`think-1545` remain open.
Historical #466 facts and their pin are untouched by these preparations.

Still-unmapped watched changes include wand125 `82580ed6587d` triangle reports, Daniel
`77f3c0ab479b` changed paths, and SQUISH omissions e63e4e5/5e32bbd/d8c8db8. Some belong
to existing proof owners or earlier source custody, but complete mapping was not
established. The UnitSquare Release1 manual source needs a fresh check.
Source-only record merge readiness is distinct from the eleven T rows below full
verification/confirmation and the long-running owned independent replays.

## Other owners’ stacks

Formal447 is #403 → #435. Formal455 is #404 → #454 → #461. #403 and #404 are conflicted
with main; their children have failing or cancelled qualification.
Do not race their owners’ active branches or overwrite their commits.
Polynomial source worktrees are under `/Volumes/spud-ext1/agent-source/`; the owner has
newer local foundation/catalogue commits than the published refs.

The polynomial fixes and complete-input gzip design were reviewed as proposals; current
owner composition, source cap, Pages and full gates still need qualification.
#435’s finite static selector must preserve the complete historical polynomial rows.
The n17 selected source projections for #404/#454/#461 exceed the unchanged
201,326,592-byte cap.
Do not substitute a 224MiB limit.
Preserve the held proof branches and independent-replay beads, including ValidTilt9.
These are separate from stack430.

## Resume order and completion rule

1. Inspect live heads, stacks and existing run conclusions.
   Reconcile fresh main3213 by normal merges into the lowest owner, resolving conflicts
   without losing sources.
2. Fix the lowest common timing/browser failures with narrow production controls.
   Use the preserved diagnostic rather than launching another whole-site experiment.
   Keep 12s, 300ms, CLS0.1, source cap and scientific evidence boundaries unchanged.
3. Propagate accepted normal parent merges once, check actual DATA pins, and bind
   reviews to each changed head.
   Required CI and the appropriate full checkpoint must actually pass before removing
   draft status or merging an independently ready prefix.
4. Qualify #466 records timing and exact-head hosted/full gates, publish its scoped
   review bindings, then merge it only after its parents.
   Keep hh48 open until its ledger reaches main.
   Preserve raw custody outside Git and scratch.
5. Continue the five finite follow-ups and two outside-horizon inputs, reconcile the
   five missing replies and watched repository changes.
   Coordinate the foreign stacks with their owners.
   Close beads only for completed scope.

All source edits made by this team must be committed and pushed before handing off.
Raw upstream material and unique logs intentionally remain outside Git; their durable
paths are part of the handoff, not an assertion of public redistribution.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
