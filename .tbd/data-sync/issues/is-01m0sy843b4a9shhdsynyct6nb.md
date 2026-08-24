---
type: is
id: is-01m0sy843b4a9shhdsynyct6nb
title: H-010 retained record must not depend on raw platform floats
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/campaign/hypotheses/H-010-stromquist-triple.md
labels: []
dependencies: []
parent_id: is-01m0srsphtekzmgp8vrs05v8n5
created_at: 2026-08-24T13:09:39.562Z
updated_at: 2026-08-24T13:17:59.904Z
closed_at: 2026-08-24T13:17:59.903Z
close_reason: H-010 records now store only stable labeled display strings for non-decisive diagnostics; all verdict-bearing signs remain exact. Generate/replay, Ruff, and BasedPyright pass; D-155 records the correction.
resolution: null
duplicate_of: null
---
Record robustness gap found and fixed before the scientific run. The first H-010 draft serialized raw libm diagnostics and then required exact JSON replay, so harmless last-bit platform drift could reject exact evidence. Acceptance: retain only labeled stable display strings for non-decisive diagnostics, keep all verdict decisions exact, add D-155, and replay the record under the corrected contract.
