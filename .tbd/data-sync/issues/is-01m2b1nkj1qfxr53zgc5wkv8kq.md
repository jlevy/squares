---
type: is
id: is-01m2b1nkj1qfxr53zgc5wkv8kq
title: Source-distinct review of the integrated calibration repair
kind: task
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: Astra Max source-distinct calibration correction review; root integration
labels:
  - n11
  - calibration
  - review
dependencies:
  - type: blocks
    target: is-01m2app5e71qnp9z5vfp9vppbp
parent_id: is-01m2app5e71qnp9z5vfp9vppbp
created_at: 2026-09-12T14:52:14.272Z
updated_at: 2026-09-12T15:49:31.014Z
closed_at: 2026-09-12T15:49:31.013Z
close_reason: Source-distinct review completed with retained refusal report; five concrete successor defects remain separately tracked under CAL-2 through CAL-6.
resolution: null
duplicate_of: null
---
After all seven CAL-1 through CAL-7 fixes and the admitted preflight and partial-direction repairs are integrated, independently replay the retained adversarial controls and audit the exact terminal state, dilation, partial-set, lifecycle, transaction, metrics, and settings contracts on the combined revision. Confirm the n=2 fixture remains mathematically exact, run the focused Python 3.14 gates, retain a review report, and do not run a positive full-shape profile or BC329. This review is distinct from think-1mma, which later admits three measured profiles.

## Notes

Completed source-distinct review at exact head `d924a4bfff54fad8a039ae0cde2103a0e4817848`; retained report `/private/tmp/bc329-calibration-integrated-correction-review.md`. Verdict: refuse admission. CAL-1 and CAL-7 close. CAL-2 through CAL-6 retain five concrete blockers: omitted Condition 5′, incompatible partial dilation identities, SIGINT launch-window orphan, unchecked final-publication deadline, and weaker-than-documented positive RSS sampling. The exact n=2 fixture was independently rederived; 53 maintained calibration tests passed. No positive full-shape profile or BC329 target ran.
