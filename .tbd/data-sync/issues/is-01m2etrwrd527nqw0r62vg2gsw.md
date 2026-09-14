---
type: is
id: is-01m2etrwrd527nqw0r62vg2gsw
title: "Owner decision: choose the BC329 calibration execution head (PR156, PR157 supplement, or main)"
kind: task
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - decision
  - bc329
dependencies: []
parent_id: is-01m2etr75jfh3t3ry7kj1ccqrb
created_at: 2026-09-14T02:08:39.692Z
updated_at: 2026-09-14T02:26:52.562Z
closed_at: 2026-09-14T02:26:45.818Z
close_reason: "Owner decision, 2026-09-14: no calibration execution head is chosen because the BC329 calibration profiles and target are deferred. BC329's prospective gain is about 0.000274 over T-026, which falls under the owner's hold on heavy computer-assisted work for very small improvements. The run sheet and PR157 supplement remain retained records bound to their PR identities; any future revival needs a main-bound identity block and fresh integrated-head admission. The macOS EPERM reaper fix (think-tdfl) therefore lands with the stack."
resolution: canceled
duplicate_of: null
---
Owner decision required: where do the three BC329 fixed-core calibration profiles execute?

Why it is a decision: a calibration receipt is bound to one exact commit through the 23-file source closure (source-distinct reader, evidence commit whose sole parent is the execution commit). PR157 changes five closure paths (runner and threshold modules, including MATH-05 resource caps that apply to ordinary atoms), so a #156-only calibration does not vouch for the integrated runner and vice versa. The run sheet (docs/project/specs/active/plan-2026-09-13-n11-bc329-three-profile-run-sheet.md) requires local HEAD == live PR156 head; the PR157 supplement (docs/project/specs/active/plan-2026-09-13-pr157-integrated-calibration-launch-supplement.md on #157) requires PR157 OPEN with base = the #156 branch and #156's head unchanged. Merging #156 breaks both identity checks, so calibration timing and merge timing are one decision.

A1 — calibrate on #156 before merge: closest procedure; #156 frozen for calibration plus independent readback; evidence commit on #156 forces back-merges into #161–#166, #157, #167; after #157 lands, BC329 must run at the historical #156 revision or recalibrate.
A2 — calibrate on #157 via the supplement before merge: calibrates the future-main runner; #156 and #157 frozen and the chain cannot merge until done; supplement still says "draft".
B — merge first, calibrate on main: unblocks the stack, calibrates the code everything will run from, lets closure-file fixes (EPERM reaper bug) land first; requires rewriting both identity blocks to bind a main commit, plus independent review of that rewrite (on top of the integrated-head admission every option already owes).

Coupled to think-bt5b: option B requires a yes there. Record the choice here and in the run sheet's admission table owner bead (think-vy5i), then close.
