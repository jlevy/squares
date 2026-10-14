---
type: is
id: is-01m4xtz3gjt6835xehbx6rv4br
title: "News604 review B1: decouple result kinds from topic vocabulary"
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4xm9zrn7p4nygg25gwy9cxw
hold: null
hold_until: null
created_at: 2026-10-14T18:32:03.344Z
updated_at: 2026-10-14T18:32:42.720Z
started_at: 2026-10-14T18:32:42.718Z
---
Review B correctness at8c465d209 https://github.com/jlevy/squares/pull/604#pullrequestreview-5522754233 demonstrates fullschema-valid S5 rigidity record T012 passes result schema and selection but raisesValueError unknownNewsTopic inhomepage. Define explicit justified subject mapping independently of resultkind, omit subject where sixlabelvocabulary hasnoaccurate match, retain actualkind/status/claim/credit. Cover valid resultkind boundary without weakening news_topics enum rejection.
