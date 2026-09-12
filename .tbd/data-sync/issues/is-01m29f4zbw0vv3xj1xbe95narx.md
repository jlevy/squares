---
type: is
id: is-01m29f4zbw0vv3xj1xbe95narx
title: "P4: nothing checks the page after it deploys"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m29f3zcv8kfcf70ra7fpkd1j
created_at: 2026-09-12T00:09:20.507Z
updated_at: 2026-09-12T00:09:20.507Z
---
`pages.yml` proves a great deal about the page it BUILDS -- deterministic, self-contained, no external references -- and nothing at all about the page that ends up at the URL.

The gap is small but it is the one that bites: an artifact-upload path that is subtly wrong, a Pages configuration that serves a different directory, a deploy that half-succeeds. Every one of those leaves a green workflow and a broken or stale URL.

A post-deploy smoke check closes it cheaply: fetch `/workbench/`, confirm it returns 200, confirm the body carries `window.atlasTransitions`, and confirm its sha256 matches the artifact that was uploaded. The explainer at `/` deserves the same and may already have it -- check before adding a second mechanism.

Low priority because the failure is visible the moment anyone opens the link. Worth doing because 'anyone opens the link' is not a gate.
