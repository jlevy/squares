---
type: is
id: is-01m59p1hzmgp0y1911hhv6sk5w
title: "PR #671 E1: repair article revision date and generated URL records"
kind: bug
status: closed
priority: 1
version: 3
delegate: codex-671-integration-20261018
labels: []
dependencies: []
parent_id: is-01m59p0xxqme014n9dyzqwcw4w
hold: null
hold_until: null
created_at: 2026-10-19T08:56:54.003Z
updated_at: 2026-10-19T09:07:07.608Z
started_at: 2026-10-19T08:57:21.436Z
closed_at: 2026-10-19T09:07:07.607Z
close_reason: Fixed in394f9d9eaee8e08b16d2a5e76aaef31422b2aee2; original failures reproduced,52complete records and146focusedtests pass; markedEreply https://github.com/jlevy/squares/pull/671#issuecomment-6263635591 verified. Finalhostedacceptance remains withroot.
resolution: null
duplicate_of: null
---
Medium E1, release.py:707 and site URL generated views. https://github.com/jlevy/squares/pull/671#pullrequestreview-5569051173. At6c26 hosted artifact-date tests require article-history October13 instead ofOctober19; URL YAML/document stale. Keep v0.4.8 release/event date, restore article date, generate URL views from full inputs and confirm existing contracts.
