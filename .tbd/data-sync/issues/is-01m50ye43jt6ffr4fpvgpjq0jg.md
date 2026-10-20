---
type: is
id: is-01m50ye43jt6ffr4fpvgpjq0jg
title: "PR #627 B6: suggestion: a site cut cannot complete the push tier on the shared host"
kind: bug
status: open
priority: 2
version: 3
delegate: ecstatic-edison-address-627
labels: []
dependencies: []
parent_id: is-01m50gnwbxd5kxbynyx9nd162p
hold: null
hold_until: null
created_at: 2026-10-15T23:30:24.498Z
updated_at: 2026-10-15T23:58:21.135Z
started_at: 2026-10-15T23:30:50.134Z
---
Suggestion. PR #627, review B (https://github.com/jlevy/squares/pull/627#pullrequestreview-5541117145). An edit to only the release history, impacts, no-change records and pins reaches the whole quick suite. Fix: a bead under think-wnsv to narrow what such an edit reaches.

## Notes

Deferred from PR #627 review B (B6 suggestion). An edit only to PUBLICATION_HISTORY, RELEASE_IMPACTS, RELEASE_NO_PUBLIC_CHANGES and the two pins reaches the whole quick suite through release.py, so a site cut's push tier cannot finish under its 1800 s cap on the shared host (lane A lost about 74 of 155 minutes to two such timeouts; OR-14, OR-17). Narrow what such an edit reaches to the release, cut, pin, impact and claim-verifier modules. Waits on a change to the reachable-tests map; not this PR's scope.
