---
type: is
id: is-01m3r1dp2anhxes2fesns7bhdf
title: "W5: avoid rebuilding every atlas witness for evidence-only edition changes"
kind: task
status: closed
priority: 1
version: 6
spec_path: docs/project/reviews/review-2026-09-29-n11-optimality.md
labels: []
dependencies: []
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
created_at: 2026-09-30T02:13:44.137Z
updated_at: 2026-10-01T14:31:10.427Z
closed_at: 2026-10-01T14:31:10.426Z
close_reason: Reusable guarded --restamp-only path implemented and independently reviewed;6focusedcontrols,19combinedrelease/restamptests,strictsource/claim/exportpreflight andpostflight pass. Actual two-composite export17.41s with no324witnessgeometryrebuild; evidence retained4f312e21e. No controlledspeedupratio claimed.
resolution: null
duplicate_of: null
---
Supporting integration efficiency only. Current evidence review annotation changes DATA_REVISION and requires refreshing stamped exports; existing atlas --update re-derives324 witness renderings even when geometry/composite data is unchanged. Measured245.08s wall/874.67s aggregate CPU with4 workers at8f5fff; proof lanes continued. Investigate a bounded restamp path using retained verified source, preserve identical SVG and PNG/PDF receipt contracts, retain mutation tests refusing stale or changed geometry. Do not weaken revision/data integrity or block proof checks on this optimization. Evidence packing/campaign/agent-sessions/session-164-validation/atlas-restamp-8f5fff.txt.

## Notes

Final integration slice after research targets: implement guarded stamp-only publication update without324witnessgeometryrebuild. CI b8e3e170f solefailure staleDATA_REVISION; source/toolpreflight and mutationcontrols required; no export launched yet.
