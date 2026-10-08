---
type: is
id: is-01m4cb6ahrz0vp5f6pt2aanam2
title: "PR #427 A4 — Medium: the external raw-source digest boundary is not registered."
kind: bug
status: closed
priority: 2
version: 3
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4cb68shtz5h0braprdqj1qb
hold: null
hold_until: null
created_at: 2026-10-07T23:29:17.368Z
updated_at: 2026-10-08T00:20:40.435Z
started_at: 2026-10-08T00:20:32.636Z
closed_at: 2026-10-08T00:20:40.435Z
close_reason: Source fixes9ff422a/6c615115 at f1d7 are independently reviewed E/F/G/H with0newfindings and hosted final-head CI30SUCCESS26documentedSKIP. Focused379+190+3+11owner checks passed; selected broad assertions completed with original capability failure retained and unchanged supported profiler/heavy completions. Actual broad allowance1800 is unchanged. These source findings are fixed; parent422 intake/confirmation/deployment remain open until atomic stack merge and publication.
resolution: null
duplicate_of: null
---
Review https://github.com/jlevy/squares/pull/427#pullrequestreview-5449633758 head83748.

**A4 — Medium: the external raw-source digest boundary is not registered.**
`packing/devtools/squish_second_update_packets.py:568` compares externally supplied raw
bytes with the acquisition digest.
The full gate’s `check_integrity_ceremony` rejects this new site because
`packing/devtools/integrity-ceremony.yaml` registers the first-update adapter but not
this one. Reading the comparison confirms a genuine external-input custody check, not an
internal self-digest that should be removed.

**Fix:** register the narrowly described external-checkout boundary for this adapter,
following the first-update entry, and run the integrity checker and its
boundary-contract tests.
Retain the actual raw-byte comparison.
