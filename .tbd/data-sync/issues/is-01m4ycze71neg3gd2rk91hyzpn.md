---
type: is
id: is-01m4ycze71neg3gd2rk91hyzpn
title: "SYNOPSIS.md drifts on every commit: its generator writes a straight apostrophe in T-174's row (\"PingYou Ltd's\") that the flowmark hook makes typographic"
kind: bug
status: open
priority: 2
version: 1
labels:
  - pipeline
dependencies: []
created_at: 2026-10-14T23:46:48.672Z
updated_at: 2026-10-14T23:46:48.672Z
---
Since #602 or #608, the pre-commit hook's whole-repository flowmark pass rewrites one row of the generated SYNOPSIS.md on every commit: the T-174 row's 'PingYou Ltd's' straight apostrophe becomes a curly one. The renderer (close_session --render or the synopsis generator) writes the straight form, so committing the hook's output would fail the synopsis drift check, and agents have restored the file by hand each time. The records lane of #608 and the #609 branch both hit it.

Fix, one of:
(a) have the synopsis renderer emit the typographic apostrophe flowmark produces, the way other generated views are written in flowmark's form;
(b) add SYNOPSIS.md to .flowmarkignore with a reason, if it is a renderer-owned view like the other generated files listed there.
Measure which the policy wants: AGENTS.md says exclusions are evidence-based, and generated files whose renderers drift-check them are excluded.
