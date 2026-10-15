---
type: is
id: is-01m4zs1cht3n97c4bmnqqv0qyh
title: "PR619: validate, merge and verify the tutorial, News, atlas and paper closure release"
kind: task
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
hold: null
hold_until: null
created_at: 2026-10-15T12:36:49.849Z
updated_at: 2026-10-15T13:17:34.443Z
started_at: 2026-10-15T12:37:26.588Z
closed_at: 2026-10-15T13:17:34.443Z
close_reason: Delivered in PR619, merged 31eaf6333c5d5b6b3d111241768cdd3d30982588. All 43 executed PR checks and selected Deep38735581202 passed. Main Pages38739226771 published site v0.7.7, shared infographics v0.6.1 and lower-bounds paper v0.4.7; actual deployment audit job116439283652 passed 4460/4460 checks. Main full Packing remains independently in progress; no three-minute performance claim. Focused CI safety and performance work continues under think-3d1m and think-kxmq.
resolution: null
duplicate_of: null
---
Deliver PR619: https://github.com/jlevy/squares/pull/619. Frozen head 3a00b00438e0b7ae4276eb2b38a6e45dd94b3701, base fc2ceae79f462fe707ebbad1b94eb7cc306797b8; 28 changed paths. Independent senior review A (5533156549) and security review B (5533156744) cover the current head with no open findings. Ordinary Packing38735580267 and Pages38735580297 passed; selected full Deep38735581202 is still running. Finish the full checkpoint, discovery sweep, matching-head merge and main publication audit, then close the owned closure beads. Site v0.7.7, infographics v0.6.1 and lower-bounds paper v0.4.7 are independent; the other three paper editions are unchanged.

## Notes

The broad local run at4dd remains failed:729.90s total,10,930 passed,49 skipped,one xfailed,two stale atlas assertions and one Ruff finding. The two repaired tests passed in1.86s; canonical Ruff passed, and the generator's complete AST is unchanged by its escaped spelling. Final paper artifact check passed against a fresh render:22 pages,867,741 bytes and19 embedded fonts, with the original page ceiling intact. Independent extraction confirms all text is preserved. No repeated broad local run was started after external scratch fell to77MiB. The final hosted checks supply the required current-head coverage. The separate live fast-proof safety fix is think-3d1m; the retired deferred reuse prototype did not ship.
