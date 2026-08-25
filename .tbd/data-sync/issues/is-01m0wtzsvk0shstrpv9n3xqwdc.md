---
type: is
id: is-01m0wtzsvk0shstrpv9n3xqwdc
title: "D-320: stale second unprotected-fix aggregate in SYNOPSIS escaped the single-match drift check"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m0wtz4vb81vyh3665rt33xh2
created_at: 2026-08-25T16:10:24.499Z
updated_at: 2026-08-25T16:14:25.143Z
closed_at: 2026-08-25T16:14:25.143Z
close_reason: "Fixed on claude/pr-34-soundness-review-8fkoce: D-320 (stale second unprotected-fix aggregate corrected to the derived count; check_synopsis now validates every occurrence and the mutation control expects the mutated count) and D-321 (rejoined 'Mutation-control commands' in development.md). Both recorded in defects.yaml with regenerated defects.md and synchronized SYNOPSIS aggregates and controls."
resolution: null
duplicate_of: null
---
SYNOPSIS.md line 1984 said 'Ninety-eight fixes left no regression check behind' while the derived count was 106 (line 1831 was correct). check_synopsis accepted the document because its unprotected-fix pattern required only one matching occurrence. Recurrence of D-305. Fix: correct the stale sentence and make check_synopsis validate every occurrence of the aggregate phrase.
