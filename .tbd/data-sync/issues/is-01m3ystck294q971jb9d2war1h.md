---
type: is
id: is-01m3ystck294q971jb9d2war1h
title: "Independent measure verifier, slice 3: two adversarial reviews"
kind: task
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-10-02-independent-measure-verifier.md
labels:
  - verifiers
dependencies:
  - type: blocks
    target: is-01m3ystff276btdyf2nxewyzyc
parent_id: is-01m3yrezbcgcr728c37fq49bvf
created_at: 2026-10-02T17:15:32.834Z
updated_at: 2026-10-03T20:38:31.257Z
closed_at: 2026-10-03T20:38:31.257Z
close_reason: null
resolution: null
duplicate_of: null
---
Two reviewers, distinct from W2 and from each other, read the plan spec, W2's implementation and, as they choose, the authors' checkers; each writes a review in docs/project/reviews/ with a verdict on soundness (every lemma's obligation discharged in code), on the clean-room record, and on the acceptance receipts. Findings become beads. Starts when W2 declares a family complete. Exit: both accept, or findings fixed and re-reviewed.

## Notes

2026-10-03 05:12 Review RA (soundness; branch claude/review-ra-sqverify-fast @0e38246a9; review-2026-10-03-sqverify-fast-soundness.md): REJECT on S1 (blocking): axis.rs direction-0 minimum ignores NaN (value.lo < min_lower false for NaN); admissible format-T certificate with overflowing slope sums reports verified while exact capture is 0. S2: --inject-fault-at-node can exit 0 'verified' without recording the injection. S3: SOUNDNESS N2 wording. S4: other interval primitives drop NaN (not reached outside S1). Mathematics otherwise holds. Fix sent to W2 (NaN fatal everywhere, admission caps, re-run census and controls); RA to re-review after the fix. Review RB (testing/independence) still running.
2026-10-03 05:55 Review RB (testing and independence; claude/review-rb-sqverify-fast @299ce0681; review-2026-10-03-sqverify-fast-testing-and-independence.md): ACCEPT. 9,726 exact-false certificates all refused (deficits to 3.9e-121); 6,772 probes, no certified bound above the exact capture; independence: nothing traceable to the authors' checkers. Non-blocking: TI-1 audit sliver false alarms (sound), TI-2 gzip trailing bytes admitted, TI-3 certificate.D overrides format L's net, TI-4 no independence-record.yaml and fuller reads than spec 2.2-2.4 allow, TI-5 session trailer. Question: format M bins may need B(1+D/(1-D^2/4)) < 1. All sent to W2 with RA's S1-S4; after the fix, RA re-reviews; then the census becomes independent-implementation evidence (think-3ok2).
2026-10-03 14:50 W2 fixed every review finding (claude/lane-w2-fast-verifier-wip @4ddf37d9c): cfb653a2f RA S1-S4 (non-finite refused, admission caps density 2^96 / net 2^16 / 10^6 rows, SOUNDNESS lemma F3 bounds intermediates below 2^200, NaN-carrying min/max and R2/Z1/Z2, fault injection never verified, N2 folds at pi/4); 61acc9dcb RB TI-1/TI-2/TI-3 and format M (N3 with B(1+D)<1 in half-angle form; admission checks B(1+D/(1-D^2/4))<1); 82332fee4 TI-4 independence-record.yaml (hand-written). 36 crate tests, 46 checks/controls, edit tier pass; exp-017 cost -1.0% instructions. Re-run of 16 certificates with the fixed build: all VERIFIED, nodes and bounds identical. RA asked to re-review 4ddf37d9c at 14:50; SP2 told to merge it into #311. Census resumes (n66, n90, n92, n50 trio, rect sets 10-01/09-28/09-27).
2026-10-03 14:55 RA re-review: ACCEPT at 4ddf37d9c (claude/review-ra-sqverify-fast @ca6ea4cd7). S1-S5 closed, four new reproducer variants hold, lemma F3 and the admission caps sound, format-M N3 sound in half-angle form with B(1+D)<1, no new path to a false verified. Non-blocking: R1 N2's 'delta <= atan D' sentence is false under the half-angle assignment; R2 representation_slack makes the audit tolerance vacuous near the density cap (audit only decides refusals). Both sent to W2. Both reviews now ACCEPT: the census can become independent-implementation evidence once complete (think-3ok2).
