---
type: is
id: is-01m1vrfsdfsjpz6gx78wv9w5wd
title: "PR #95 review PR95-R3: reconcile serial defaults and performance claims"
kind: bug
status: in_progress
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1vr1dfvqt3eegay29jsnx4f
created_at: 2026-09-06T16:23:09.999Z
updated_at: 2026-09-06T16:40:41.774Z
---
Senior review https://github.com/jlevy/squares/pull/95#issuecomment-5560540217. CLI help, workflow/validator comments, docs, and PR body still claim PACK_JOBS enables pools despite measured serial-default rollback; remove D472-refuted census causal claim.

## Notes

Implemented in 08087a18 and 72c0df47: serial defaults and explicit --jobs documented/tested, unsupported pool-causality claims removed, SYNOPSIS and slow-marker docs corrected, populated baseline comments corrected. Focused suite and final 31-step records tier pass. Parent will update PR body and publish disposition after push.
