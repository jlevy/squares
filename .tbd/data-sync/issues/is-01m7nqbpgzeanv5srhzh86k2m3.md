---
type: is
id: is-01m7nqbpgzeanv5srhzh86k2m3
title: "PR #953 A7 (suggestion): OR-16 and review packets' outputs/program-digests.sha256"
kind: bug
status: open
priority: 3
version: 3
labels: []
dependencies: []
parent_id: null
created_at: 2026-11-17T21:42:11.743Z
updated_at: 2026-11-17T23:05:17.744Z
---
Suggestion A7 of review A on PR #953 (https://github.com/jlevy/squares/pull/953#issuecomment-6938296720): outputs/program-digests.sha256 in review packets is a SHA-256 manifest beside committed programs, binding the scratch copy that ran to the committed files; OR-16 (operating-rules.md) asks not to add checksums for a local handoff. Thirteen review packets on main now carry one and nothing reads it. A disposition belongs to the rule, not to a PR: either OR-16 names this record as allowed, or later reviews cite the Git revision instead. Deferred: waits on that decision (process owner).
