---
type: is
id: is-01m1tqpqa49xy36ytnn6f57zz0
title: "C4: 'one of 21 new results' overcounts what is new"
kind: bug
status: closed
priority: 2
version: 3
labels:
  - review-claude
dependencies: []
parent_id: is-01m1tqpgrh5ym0r6e5apbke7p8
created_at: 2026-09-06T06:50:14.210Z
updated_at: 2026-10-06T08:24:26.797Z
closed_at: 2026-10-06T08:24:26.796Z
close_reason: "Done: PR 94 (merged 2026-09-06, 3e1fd715d) implements C4: 'one of 21 results the framework has registered so far, 14 of them apparently new', both counts read from the register."
resolution: null
duplicate_of: null
---
explainer-article.md opening: 'This is one of {{N_RESULTS}} new results of the framework so far.' The register scores 7 of the 21 as previously-published (verified and registered, not found) and 14 as apparently-novel. Fix with computed counts: the coordinator adds an N_NOVEL placeholder to render_explainer.py (results whose novelty is apparently-novel or confirmed-novel); the sentence becomes 'This is one of {{N_RESULTS}} results the framework has registered so far, {{N_NOVEL}} of them apparently new.' Keep the author's voice otherwise.
