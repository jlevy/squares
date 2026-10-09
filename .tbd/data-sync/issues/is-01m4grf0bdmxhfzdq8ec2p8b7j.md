---
type: is
id: is-01m4grf0bdmxhfzdq8ec2p8b7j
title: Unify PDF text colors and information-block spacing
kind: task
status: in_progress
priority: 2
version: 6
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T16:38:11.050Z
updated_at: 2026-10-09T18:06:14.957Z
started_at: 2026-10-09T16:38:41.898Z
---
Apply the latest print-only refinement systematically to both n=324 and n=100 PDFs: render the title and any retained subtitle in gray, make all remaining explanatory/legend/credits/closing text black, and use consistent whitespace between information blocks, including before Best packings due to. Preserve semantic result/angle/contact marks, the latest printable unlinked closing text and consistent typography, n=324 complete triangle layout and n=100 Grid layout. Keep the previously removed 324 subtitle removed. Regenerate both PDFs through maintained producers, inspect actual PDF text colors and block geometry and preview the resulting exports, then include the change in PR474 with current review and CI. Coordinate disjoint source ownership with think-e49r.

## Notes

Frozen print source uses shared annotation rendering, weight700/leading1.50 and equal ink-to-ink block gaps3body ems. Title/problem/counts gray; ordinary text black; semantic red and angle/contact colors retained. Exact two-line definition breaks after can with properly italic s/n and roman parentheses, no final period; credits no period, unique and newest first. Grid100 footer annotations and plain black inline project/address below title; complete right-aligned Triangle324 and upper-left information/closing. Own legend denominators100/324 actual PDFs verified:45,97,3,14,81 /100 and77,292,32,22,297 /324. All three Medium review findings fixed and accepted: Grid100 stale golden, host-dependent ink metrics, and native Quartz per-card italic family. OFL LiberationSans2.1.5 bold/bolditalic retained under unique SquaresAtlasPrint names with license/provenance, matching design metrics, process-local native registration and verification, and explicit trusted self-contained SVG CSS opt-in.22 final focused tests passed10.43s, native card test failed pre-fix then passed independently2.98s; lint/format/types clean. Dedicated gpt6-astra xhigh security review approves maintained path; Low validator-description wording fixed/accepted, no generic hostile-font sanitizer claim. Root regenerated BOTH retained-identity styling drafts after final math fix, rendered via Poppler and visually inspected full pages/readable information; these are drafts, not canonical release exports. Files in external final/web-compact-20261009/print, current2400x3201 Grid and8347x6602 Triangle, row pitches252/360 unchanged. Row-height0.25box increase/decrease and gap-reduction0.125box axis still await required user clarification; no elapsed-time assumption. Root owns remaining schema/docs/layout records/pin/canonical generation, current-head gates and PR474 publication. No source commit/push this iteration, no new scientific values/constructions, no GitHub merge.
