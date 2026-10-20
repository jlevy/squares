---
type: is
id: is-01m4xtz3gjt6835xehbx6rv4br
title: "News604 review B1: decouple result kinds from topic vocabulary"
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4xm9zrn7p4nygg25gwy9cxw
hold: null
hold_until: null
created_at: 2026-10-14T18:32:03.344Z
updated_at: 2026-10-14T18:51:18.987Z
started_at: 2026-10-14T18:32:42.718Z
closed_at: 2026-10-14T18:51:18.974Z
close_reason: Fixed in pushed News604 repair d08551e0aba9cc92eb4d17389bb8c7a4bd1cdf81; B dispositions https://github.com/jlevy/squares/pull/604#issuecomment-6175849755; accepted-kind and corrected real rigidity regression, all 6 affected browser cases, full overview/rung/publication contracts and scoped static checks pass. Parent coordinator owns final hosted CI and review D; tbd sync reserved to root.
resolution: null
duplicate_of: null
---
Review B correctness at8c465d209 https://github.com/jlevy/squares/pull/604#pullrequestreview-5522754233 demonstrates fullschema-valid S5 rigidity record T012 passes result schema and selection but raisesValueError unknownNewsTopic inhomepage. Define explicit justified subject mapping independently of resultkind, omit subject where sixlabelvocabulary hasnoaccurate match, retain actualkind/status/claim/credit. Cover valid resultkind boundary without weakening news_topics enum rejection.
