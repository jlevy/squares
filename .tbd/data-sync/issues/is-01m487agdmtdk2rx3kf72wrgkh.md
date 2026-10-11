---
type: is
id: is-01m487agdmtdk2rx3kf72wrgkh
title: "T-084: register chelokot's Lean squareMinusOne_isMinimumSide as a second machine route (axiom receipt, statement reading)"
kind: task
status: open
priority: 3
version: 1
labels:
  - result-import
dependencies: []
created_at: 2026-10-06T09:04:42.420Z
updated_at: 2026-10-06T09:04:42.420Z
---
T-084's s(k^2 - 1) = k has a second machine route that the record already half-holds. chelokot's Lean development proves it by an augmented measure, `SquarePackingArchive.Records.NearSquare.squareMinusOne_isMinimumSide`. The replay of 2 October 2026 retained for T-086 (packing/campaign/series/series-000-smoke-and-calibration/results/chelokot-lean-replay/build.log, line 218) compiled it, and the archive's Audit.lean printed its axioms as exactly propext, Classical.choice and Quot.sound. The replay's own axiom step (ReplayAxioms.lean) and the receipt cover squareMinusTwo only, and no statement-fidelity reading of squareMinusOne_isMinimumSide is retained. T-084's next_rung said before 6 October that this route "was not built here". That is wrong about the build and right about the evidence.

How to finish: extend devtools.replay_chelokot_lean's axioms and definitions steps to name squareMinusOne_isMinimumSide, rerun it (about 1 minute with Mathlib's cache; it clones the archive at 753079eb), read the statement against IsMinimumSide, and register an evidence entry (proof-assistant-checked, replayed-here, same-implementation) cited by T-084 beside E-karakus-strip-measure-interval. It would be a second machine method beside T-084's rung and would move no rung.
Expected CPU: a few minutes; disk for the toolchain and Mathlib cache (several GB).
