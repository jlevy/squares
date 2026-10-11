---
type: is
id: is-01m3vd42145pps62hm52e3xheg
title: "Math markup: run check_github_math over all 1,472 migrated files"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T09:35:54.892Z
updated_at: 2026-10-01T09:35:54.892Z
---
From the math recovery agent's report at da122be09 (jlevy/squares#254, merged 2026-10-01): both placements GitHub leaves as dollars that no rule covered were found by running check_github_math on a handful of files (a formula at a line start inside a parenthesis opened on the previous line; a formula ending in ')' directly before ')'). Run the check over every migrated file, in batches against a pushed ref, and add a probe case and a tool rule for each new placement found.
