---
type: is
id: is-01m16gtcngd2d91zf7hx3304a8
title: "Close the exact route at n=11: minimal polynomial back to a verified packing"
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-08-29T10:25:05.712Z
updated_at: 2026-08-29T16:02:39.494Z
closed_at: 2026-08-29T16:02:39.494Z
close_reason: Duplicate. think-2q2c existed on the shared tbd-sync branch all along; this container's freshly materialized local bead store did not have it. The BC-067 work is recorded on think-2q2c.
resolution: duplicate
duplicate_of: is-01m169k6tppmcm63fw0gqa9cp0
---
agenda-006 BC-067, advancing the promotion spec's phase 4. Discharge a recovered minimal polynomial all the way back to a verified packing rather than only to an isolated root: build a NumberField from the candidate, solve the pose unknowns exactly, rebuild the packing, verify under exact_sign, and compare the reconstructed side against the input.

Created in session-044. agenda-006 named a bead 'think-2q2c' for this commitment that was never created; this replaces that dangling reference.
