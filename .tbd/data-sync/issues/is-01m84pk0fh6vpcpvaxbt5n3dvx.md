---
type: is
id: is-01m84pk0fh6vpcpvaxbt5n3dvx
title: "Reconcile GeiserX adoption #1090 with the published atlas and release gates"
kind: task
status: in_progress
priority: 2
version: 4
delegate: codex-geiserx-repair-1123
labels:
  - intake
  - validation
dependencies: []
parent_id: is-01m7xcphnxzwwaqtcamh0c8h35
hold: null
hold_until: null
created_at: 2026-11-23T17:17:19.216Z
updated_at: 2026-11-23T21:00:11.287Z
started_at: 2026-11-23T17:17:20.166Z
---
Continue the suspended draft #1090 with its local follow-up at 8707ab11b1 preserved. Repair retained-member custody and scoped adoption/coverage tests, reserve final T-344 after sibling T-341/T-342/T-343, and reconcile the three generated-file conflicts with main before checking and publishing. Work only in the reused external checkout. Parent intake ownership and original user branch stay intact.

## Notes

Preserved the unpushed 8707ab11b1 in the isolated external branch codex/geiserx-adoption-repair-20261123. Source custody now identifies the retained original compressed member independently of derived algebraic facts. Seven focused adapter tests passed under guard and a measured shard admission resolved the prior uncovered-cost gate. T-344 is reserved for the two counts. Atlas regeneration paused safely under system memory pressure without modifying generated files; checkpoint repair-checkpoint-03.patch is retained and retry is scheduled.

23 November final integration: #1090 merged at 7690c7a4b67effd89ae754e0a3cbae36902b73b8 after all required GitHub checks and scoped review G on 38b0913730da. Production run 45262101571 verified the deploy. Both live T-344 SVGs match the checked files byte for byte, and both cases, the result, homepage and repository synopsis agree. The partial #1037 reply is live at https://github.com/jlevy/squares/issues/1037#issuecomment-7113804892. The News and receipts are on #1104 at eaf7a349d7c77fce971aa2fc6fabc92ff6b5480a, pending hosted checks and publication, then close this repair bead. The broader #1037 lane remains tracked on think-36ui.
