---
type: is
id: is-01m59qh007kff1dhc70dzjav46
title: "PR #671 F1: refuse linked retention ancestors before publication"
kind: bug
status: open
priority: 1
version: 1
delegate: codex-671-integration-20261018
labels: []
dependencies: []
parent_id: is-01m59qg9h21shapzappev8ng64
created_at: 2026-10-19T09:22:48.444Z
updated_at: 2026-10-19T09:22:48.444Z
---
High security F1; fine_net_followup.py retain/check_retained. https://github.com/jlevy/squares/pull/671#pullrequestreview-5569330296 . Pre-existing release/acquisition/nested certificate parent symlinks redirect writes outside packet and checker accepts. Bound every destination to permitted resolved root, preflight all parents before member publication, revalidate publication, preserve no-clobber/atomic controls, document trusted single-writer tree and add no-external-change/no-partial regressions.
