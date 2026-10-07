---
type: is
id: is-01m4an50xkpgh4scw7zqh9vwsz
title: Replace SQUISH receipt hashes with exact semantic input binding
kind: task
status: in_progress
priority: 1
version: 4
delegate: codex@17e132e9b179
labels: []
dependencies: []
parent_id: is-01m4ajdxfkfqyr1yj5d4wm5npt
hold: null
hold_until: null
created_at: 2026-10-07T07:44:51.635Z
updated_at: 2026-10-07T08:20:19.877Z
started_at: 2026-10-07T07:45:48.472Z
---
W7 engineering after OR16/OR18 senior review: remove bindings to repository-owned
generated facts/certificates; bound and compare canonical exact checker inputs directly.
Preserve external raw-source SHA provenance.
Generate and check safe-ceiling normalized release/supplement claims with exact rational
S. Re-certification and full independent replay required; no registry edits.

## Notes

Implemented exact semantic receipt binding v2 in the reported checkout, replacing
byte/SHA comparisons of generated certificates and normalized facts.
Receipts and both negative controls directly retain full bounded decision input: n,
exact side/unit, rational corner frame, ordered IDs/corners; exact-algebraic dispatch
enforced, metadata excluded.
Removed eleven acquisition facts_sha256 fields, preserved external source_sha256
provenance. Source admission remains 1 MB, exact receipt/certificate reads bounded at 4
MB (full11 inputs measured 1.58 MB JSON). Complete certify generates release/supplement
normalized claims with safe decimal ceiling and original exact S/source display.
Atlas accepts only source display or prescribed ceiling, with n126/n130 rejection
controls. Related37 tests passed in10.25 s, new semantic10 tests passed0.51 s;
Ruff/BasedPyright zero, integrity ceremony passed without exception/baseline increase.
Astra math and senior reviewed semantic boundary as sound.
Parent must copy code/tests/acquisition to confirmation checkout and run complete
recertification and full replay before final confirmation validation; no new source
certificates or receipts created in reported branch.
