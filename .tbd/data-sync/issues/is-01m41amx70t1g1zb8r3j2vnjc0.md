---
type: is
id: is-01m41amx70t1g1zb8r3j2vnjc0
title: "Register: a declared superseded_by field, whole or in part, with its checks"
kind: task
status: closed
priority: 2
version: 9
labels: []
dependencies: []
parent_id: is-01m41amwkn2j6r6jh6de7as7fb
created_at: 2026-10-03T16:48:07.904Z
updated_at: 2026-10-04T02:55:10.871Z
closed_at: 2026-10-04T02:55:10.870Z
close_reason: null
resolution: null
duplicate_of: null
---
Schema field superseded_by on a result: a list of {result, extent: whole|part, what, since}. Checks: the named result exists, is not the entry itself, was registered no earlier, shares an n in scope; extent part requires what; a bound (kind in BOUND_KINDS) does not declare it, since its supersession is derived, unless the derivation agrees.

## Notes

Merged to main in jlevy/squares#315 at 965a02cd5 on 2026-10-04 02:34 UTC; deployed by Pages run 37171500896 (publish, deploy and verify-deployment passed).
