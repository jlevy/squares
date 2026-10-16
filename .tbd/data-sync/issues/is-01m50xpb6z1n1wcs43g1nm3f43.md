---
type: is
id: is-01m50xpb6z1n1wcs43g1nm3f43
title: Preserve Markdown destinations and literals when abbreviating News names
kind: bug
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m50wb1kss9b0h32m4fg0kv1f
hold: null
hold_until: null
created_at: 2026-10-15T23:17:25.342Z
updated_at: 2026-10-16T02:52:25.389Z
started_at: 2026-10-16T01:06:56.679Z
closed_at: 2026-10-16T02:52:25.389Z
close_reason: Completed in reviewed formal stack635, PR633/634 merged atomically as3685616df5d92de94b9f7081233c8c357bbc3e67. Final source reviews F/G/H/I had no findings; both PR Packing/Pages workflows passed. Exact main Packing38839566286 passed all14 jobs (including original integration owner and241 slow tests); Pages38839566396 deployed sitev0.7.12 and passed4517/4517 live checks. Actual main required forwarders51passed/0skip/error/failure, completed under one900s deadline with retained journals. Current surnames/Markdown/link limits and both new S3 V0/C0 stories verified live. Unique raw evidence preserved in .codex/regularization-closeout-evidence-2026-10-13/final-intake-closeout-20261016/main-368-final-success.json. Original causal stalls and broader3min cost goal remain open underthink-yops/ht59/kxmq. New canonical-home-card and navigation fixes continue as think-1rry/yhsw; parentthink-e70v stays active. Delegate codex@spud10.local is the same resumed agent/host as codex@spud10.
resolution: null
duplicate_of: null
---
Independent surname review A1 found that abbreviation before Markdown parsing can rewrite a valid link destination containing a person name and can alter code spans. Apply an optional name transform only to ordinary text tokens in the existing inline_html renderer. Preserve URL/title attributes, inline code and math; still shorten normal name link labels. Add focused boundary controls and obtain independent final-delta review. No current selected claim triggers the defect; fix before publishing the surname release.
