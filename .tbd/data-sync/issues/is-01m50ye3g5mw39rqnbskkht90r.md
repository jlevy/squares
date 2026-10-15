---
type: is
id: is-01m50ye3g5mw39rqnbskkht90r
title: "PR #627 B5: suggestion: the explainer's live register count forces a no-change record on every intake PR"
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
created_at: 2026-10-15T23:30:23.876Z
updated_at: 2026-10-15T23:58:17.635Z
started_at: 2026-10-15T23:30:49.651Z
---
Suggestion. PR #627, review B (https://github.com/jlevy/squares/pull/627#pullrequestreview-5541117145). release.py no-change records at four places. Fix: a bead under think-wnsv (declare the count as the explainer's only register input, or move it to site data).

## Notes

Deferred from PR #627 review B (B5 suggestion). Every intake PR needs a rendered no-change record for the n11 explainer because its live register count ('one of N results the framework has registered so far') reads results.yaml (records in release.py's RELEASE_NO_PUBLIC_CHANGES, four so far). Options: declare the count as the explainer's only register-derived input so check_release_impact can decide this case itself, or move the count to site data so registering a result is not an explainer input. Waits on that choice (owner or a release-tooling lane); not this PR's scope.
