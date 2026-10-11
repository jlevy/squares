---
type: is
id: is-01m251b13sgjhq5d31fnmyt9pm
title: Bind universal parent replay to exact derived frames and reject duplicate extrema
kind: bug
status: closed
priority: 2
version: 7
spec_path: docs/project/specs/archive/plan-2026-09-10-n11-overnight-three-blocks.md
delegate: parent_replay_guard_fix
labels: []
dependencies:
  - type: blocks
    target: is-01m24tw1hadnzxyw7rdvp3vmms
  - type: blocks
    target: is-01m25430wcdx8wn8f3qs7b4qjv
parent_id: is-01m24tw1hadnzxyw7rdvp3vmms
created_at: 2026-09-10T06:51:01.111Z
updated_at: 2026-10-10T23:05:20.508Z
closed_at: 2026-10-06T08:35:14.733Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): Both refusal controls landed in cc98c7740 (2026-09-10): packing/devtools/wall_owner_parent_compatibility.py refuses duplicate extremum indices; tests test_universal_replay_rejects_old_domain_as_extremum_source, ..._duplicate_extremum_rows and ..._requires_exact_nonempty_extremum_indices
resolution: null
duplicate_of: null
---
Independent Astra Max source review of the private parent-domain adapter confirmed two missing refusal controls: universal replay accepts a differently shaped old Z_B source and duplicated extremum rows. This is a replay integrity defect; no false normal-evaluator exclusion or research-target result was demonstrated. Repair the pure private prototype, bind rows to freshly reconstructed derived frames, require the exact unique nonempty index inventory, retain the literal-gap comparison, add the two mutation controls, and request independent correction review before source admission. Review: /private/tmp/n11-parent-adapter-independent-review.md. Target/receipt binding remains under the parent bead; PR139 is unaffected.

## Notes

Sol high private repair is complete. Astra Max independent correction review passes: original two mutation controls plus four targeted checks, including shared-error refusal, all pass. Unique complete nonempty index inventory, full FrameExtremum binding and independent literal-gap comparison are preserved, with no geometric calculation change found. Reports: /private/tmp/n11-parent-adapter-prep/replay-guard-correction.md and /private/tmp/n11-parent-adapter-correction-review.md. The correction is ready for adoption on the new branch; full source-manifest and target admission remain under think-fx2y. No scientific target ran.
