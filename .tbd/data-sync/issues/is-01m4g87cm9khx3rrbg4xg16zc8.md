---
type: is
id: is-01m4g87cm9khx3rrbg4xg16zc8
title: check_documentation does not check links under packing/resources/web
kind: bug
status: in_progress
priority: 3
version: 2
delegate: codex-survey-tracker-repair
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T11:54:24.264Z
updated_at: 2026-10-09T20:39:30.227Z
started_at: 2026-10-09T20:39:30.227Z
---
Follow-up review on stack 430: a stale relative link in packing/resources/web/couzo-followup-refinements-2026-10-08/README.md to a renamed sibling packet passed check_documentation because packing/resources/web/** is excluded from its link checks. Decide whether packet READMEs' relative links to sibling packets should be checked.
