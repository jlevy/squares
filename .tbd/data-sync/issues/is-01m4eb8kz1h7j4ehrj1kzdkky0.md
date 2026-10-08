---
type: is
id: is-01m4eb8kz1h7j4ehrj1kzdkky0
title: "PR456 D1: reject global popover ID shadows"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4e37ersbgmvw7ana72wd5an
hold: null
hold_until: null
created_at: 2026-10-08T18:09:01.306Z
updated_at: 2026-10-08T18:12:57.717Z
started_at: 2026-10-08T18:12:57.695Z
---
Initial Astra correctness review findingD1, Medium, fixed before head3d266f8cc81efb54826d80f3d9921d2d26c5d529. Index first raw opening IDs globally including completed, unclosed and void elements; require one target ID. Six final shadow controls passed;99 author cases and15 independent controls passed. Public review https://github.com/jlevy/squares/pull/456#pullrequestreview-5460905451
