---
type: is
id: is-01m5mt0y75v87kt05bbdnb5xea
title: Write a gist-shaped source URL in upper_bound_reports' derived facts
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T16:38:06.821Z
updated_at: 2026-10-23T16:38:06.821Z
---
devtools/upper_bound_reports.py (line 1166 at claude/intake-2026-10-23-755) writes each derived fact's source.url as f"{source_url}/blob/{source_commit}/{path}", GitHub's repository form. For a gist source (first: amundsk-n303-2026-10-23, issue #755, T-238) that address does not resolve: gists have no /blob/ path; a revision's page is https://gist.github.com/OWNER/ID/REVISION and a file's raw bytes https://gist.githubusercontent.com/OWNER/ID/raw/REVISION/PATH. Fix the writer for gist URLs (devtools.intake_sweep._GIST already recognizes them), then re-derive the one affected fact with derive --checkout (its bytes change, so its README Compressed Files row and the T-238 artifacts digest move) and re-run its tests. Found by the #755 import lane (c-lane-755-1023, think-tqb5); deferred because it is a shared-tool change outside the import's scope.
