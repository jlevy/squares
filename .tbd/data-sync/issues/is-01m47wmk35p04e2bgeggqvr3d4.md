---
type: is
id: is-01m47wmk35p04e2bgeggqvr3d4
title: "SOUNDNESS.md: a_r names two things (the Theorem's core half-width and lemma N0's bin floor); rename the bin floor"
kind: task
status: open
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m482krnapg9vxqd91zjrg171
created_at: 2026-10-06T05:57:58.501Z
updated_at: 2026-10-06T07:42:53.688Z
---
Finding FN-7 of docs/project/reviews/review-2026-10-06-wand125-finer-net-n18-n19.md (note, non-blocking): packing/sqverify_fast/SOUNDNESS.md uses a_r = B(cos theta_r + sin theta_r)/2 in The Claim (lines 33-35, 62-63, 79, 180-184) and a_r = max(0, t_r - D/2), the per-bin floor of the half-angle tangent, in lemma D/N0 and Floating Point (lines 54, 136-139, 356). The mathematics is right; rename the bin floor (for example f_r) in its six occurrences. Lane R2 did not make the edit: the file is in the clean-room crate's directory and R2's session read the source's checker code.
