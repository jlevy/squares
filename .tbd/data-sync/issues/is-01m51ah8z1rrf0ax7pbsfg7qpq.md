---
type: is
id: is-01m51ah8z1rrf0ax7pbsfg7qpq
title: Bind SETTLED's witness identity to source.url and retrieved where a source pins no revision (Kingbird)
kind: task
status: open
priority: 3
version: 1
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdrbfnwsq05w150az5z88
created_at: 2026-10-16T03:01:50.688Z
updated_at: 2026-10-16T03:01:50.688Z
---
From PR #636 review B5 (https://github.com/jlevy/squares/pull/636#pullrequestreview-5542412946). Every Kingbird witness shares source.path (resources/web/known-best-packings/sources.json) and has no revision, so default_drawings.SETTLED's exemptions at 39, 55, 290 and 291 bind to source key and side only (290 and 291 have identical identity tuples). Add source.url and retrieved to witness_identity, Settled and IDENTITY where a source pins no revision. Waits on a data commit: the change regenerates packing/atlas/known-best/default-drawings.json and edits default-drawings.schema.yaml (both under DATA_PATHS), so DATA_REVISION is re-pinned with it; PR #636 keeps its pin. In the same data commit, update the schema's state description so regular-as-published also says no strong view of the count has lapsed (review B2 of #636 changed the code, policy and guide; the schema sits on a data path).
