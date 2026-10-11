---
type: is
id: is-01m3xqak9dr1e1r1z9ydv5gdf7
title: Replay chelokot's Lean proof of s(n^2-2) = n with an axiom receipt
kind: task
status: closed
priority: 1
version: 5
labels:
  - research
dependencies: []
parent_id: is-01m3xgkna3m3w1w50ky6gqyxyk
created_at: 2026-10-02T07:12:43.821Z
updated_at: 2026-10-02T20:45:53.574Z
closed_at: 2026-10-02T20:45:53.574Z
close_reason: "Replay passed: squareMinusTwo_isMinimumSide at 753079eb depends only on propext, Classical.choice, Quot.sound; receipt and replay_chelokot_lean --check in the records tier (dc7867f1f); T-069 records it at V3/C3. Green on PR 305 at 730f4f2e1."
resolution: null
duplicate_of: null
---
From the 2026-10-02 Nagamochi review (docs/project/reviews/review-2026-10-02-nagamochi-lemma1-karakus.md, section on chelokot's Lean archive): chelokot/square-packing-archive at 753079eb (6 Sep 2026) states a Lean theorem giving s(n^2-2) = n for n >= 2 via a compensation measure; the statement and Geometry.lean definitions were read and match the register's s(N); its CI asserts standard axioms (ManifestEvidence.lean, 79 assert_standard_axioms, Lean v4.33.0, Mathlib db584cd6), but no build or axiom receipt exists here. Build the archive at that commit with its pinned toolchain (lake exe cache get for Mathlib), retain the build log and a #print axioms receipt for the final theorem, and record the replay. A passing replay supports s(k^2-2) = k at V3/C3 (V5 needs a human formalization review) and lets the re-grounding bead keep the k^2-2 exact values; a failure leaves them at V0/C0.
