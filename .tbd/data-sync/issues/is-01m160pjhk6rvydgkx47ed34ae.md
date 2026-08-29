---
type: is
id: is-01m160pjhk6rvydgkx47ed34ae
title: "Block 8: derive the stationarity conditions"
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-08-29T05:43:23.443Z
updated_at: 2026-08-29T07:07:02.727Z
closed_at: 2026-08-29T07:07:02.727Z
close_reason: "Closed in session-041, and the answer was that there were none to derive at either large size. edge-edge was assembled as one equation where collinearity in the plane is two, so the shortfall close reported (4 at n=11, 7 at n=29) was an assembly bug, not a property of the packings. With both endpoints on the line the contact Jacobian reaches full rank: 34/34 at n=11, 88/88 at n=29, residuals unmoved at 8.9e-16 and 1.3e-15, and close refuses at both. Recorded as D-361 (soundness, conservative). n=5 has no edge-edge contact, is untouched, and keeps a genuine shortfall of one — the only remaining derivation. Unblocks BC-060."
resolution: null
duplicate_of: null
---
agenda-006 BC-060. close() currently sizes the rank shortfall without deriving the determinant conditions. Derive them for n=5 (one condition) and n=11 (four).
