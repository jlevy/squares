---
type: is
id: is-01m1x56p1wy6w3h2bj0h58kkrp
title: Keep optional attic scratch files outside repository content checks
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-07T05:24:37.557Z
updated_at: 2026-10-06T08:30:05.198Z
closed_at: 2026-10-06T08:30:05.198Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): All three cited failures fixed on origin/main: check_readme reads tracked files (6bc9a99dd), test_verified_upper_bound_contract SKIPPED_PARTS excludes attic (a4bdfae4c), no-Git fixtures isolated with GIT_CEILING_DIRECTORIES (0e28267bc, test_session_gate.py)
resolution: null
duplicate_of: null
---
The repository documents and git-ignores attic as a scratch area, but an in-place pre-push run on 921ddb84 failed because check_readme.meaningful_top_level_entries demanded attic in the durable layout tree and test_verified_upper_bound_contract scanned copied test snapshots in attic as undeclared consumers. A no-Git fixture below the repository also discovered the parent Git history. Reproducer and failed log: attic/n11-hybrid-review-publication/push-integrated.log. Running the same commit in an isolated tracked checkout under attic, with fixture and log directories as siblings and GIT_CEILING_DIRECTORIES set to the fixture root, passed all 45 selected steps. Follow up by defining consistent scratch exclusion and fixture isolation, with negative controls preserving scans of repository-owned content. This is separate from the documentation-only hybrid strategy PR; no checker or registry behavior was changed there.
