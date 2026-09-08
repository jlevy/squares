---
type: is
id: is-01m1w4kw3yb1fdft5m01ckprtk
title: "PR #100 review R2: new review sits first in the document map, above README"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m1w4krded865yyd393yn5my5
created_at: 2026-09-06T19:55:06.750Z
updated_at: 2026-09-06T19:55:30.679Z
closed_at: 2026-09-06T19:55:30.679Z
close_reason: Fixed in d663da6d on the PR branch.
resolution: null
duplicate_of: null
---
docs/project/document-map.yaml:12 placed the dated review record as the first entry, so the rendered SYNOPSIS table led with it. Moved into the reviews block and re-rendered in d663da6d.
