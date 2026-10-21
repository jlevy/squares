---
type: is
id: is-01m5ftsx292fked2gcgpkv6a5x
title: Audit profile coverage against significant results and PDF credits
kind: task
status: in_progress
priority: 2
version: 12
delegate: profiles-data-integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
child_order_hints:
  - is-01m5fv9qe49khtked4475v71ad
  - is-01m5fv9qzs8r5mgkh1468q3hf6
  - is-01m5fvcn6qa3h2w5n16vp19yge
  - is-01m5fvrszq8xvv9pfy2zhgk89a
  - is-01m5fvv3q5eanmq05ddeg2vv28
hold: null
hold_until: null
created_at: 2026-10-21T18:15:32.680Z
updated_at: 2026-10-21T20:32:29.004Z
started_at: 2026-10-21T18:15:42.083Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
Audit both directions: existing profiles must link all evidenced authored results and credited results; S5/S4 results and published PDF author/acknowledgment credits must resolve to appropriate person profiles. Distinguish missing identity joins, missing profiles, and original work missing a result record. Retain evidence, do not fabricate authorship or promote citations to results. Implement evidence-backed gaps with Sol agents and validate PDF/site alignment.

## Notes

The approved bounded coverage audit is complete. The reusable profile_coverage CLI distinguishes missing joins, missing identities, authored sources without primary T attribution, existing source/beyond-horizon records and pending PDF inspection. Reviewed structured names and the approved published PDF/diagram credit batch are reconciled across the 75 profiles. Exact alias candidates remain diagnostic rather than automatic identity joins. The durable review is docs/project/reviews/review-2026-10-21-profile-coverage.md.

This closure does not claim an exhaustive PDF credit census: 146 full-PDF inspections remain pending under the open population work think-m7il. Historical mathematical registration review remains separate under think-jtp4; source-claim projection, dated contributions and unresolved identity exceptions remain explicitly tracked by think-mdb2, think-0ltn and think-0v9j.

Final integration receipt: commit 7b566ae73 is pushed to https://github.com/jlevy/squares/pull/578. The final rerun covered 77 previously failing cases: 76 passed in 166.02 seconds; the remaining quote-parser case was fixed and passed separately in 8.05 seconds. The coordinator reports all 68 other selected checks, the complete 121-test module run, 53 UI checks and the browser floor clean. Hosted CI remains pending under think-zpfo.

Reopened: The bounded PR 578 audit is complete, but this coverage parent has unfinished children, including think-0ltn. Keep the parent live until those follow-ups are resolved; preserve all completed-work receipts and child states.

Tracker hierarchy correction: this coverage parent is reopened and remains live because its children include the open dated-contribution model think-0ltn and in-progress profile batches think-8wj0, think-2ccx and think-eigy. The completed bounded PR 578 audit, implementation and verification receipts above remain valid; they do not complete the parent's remaining children or the broader PDF coverage. No child was closed or reparented. Historical intake and the overall hosted-CI handoff remain open.
