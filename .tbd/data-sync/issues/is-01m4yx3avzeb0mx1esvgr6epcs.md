---
type: is
id: is-01m4yx3avzeb0mx1esvgr6epcs
title: Record each control's mutated output before and after a worker-content change
kind: task
status: in_progress
priority: 2
version: 5
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
hold: null
hold_until: null
created_at: 2026-10-15T04:28:33.534Z
updated_at: 2026-10-15T15:30:55.254Z
started_at: 2026-10-15T13:49:13.893Z
---
From review A7 of PR #611 (https://github.com/jlevy/squares/pull/611#issuecomment-6184210564). Unmutated equality (run_negative_controls --baseline) shows a checker reads the same before a mutation, and '174 fire' shows no control went green. Neither shows each control fires for the same reason: a dropped file read only on a mutated path, whose absence happens to print the expected message, passes both. Extend --baseline (or add a mode) to record each control's mutated stdout/stderr in a worker and diff main against a head that changes what workers hold. Done when: the mode exists with a test, and one prune or copy-back change is shown with mutated outputs equal apart from wall times.

## Notes

2026-10-15 current-source audit at main 31eaf633 / PR620 cf9003e0 confirms this is unimplemented. run_one captures mutation stdout/stderr, scores it, then returns only boolean/detail. Successful mutated output is discarded; --timings retains status/detail/wall and --baseline records only unmutated output. Small next slice: extend the existing harness and tests to retain per-control mutated outcomes without changing scoring, cleanup or scientific inputs. Then require both unmutated and mutated before/after outputs to agree for one bounded input-copy change. Do not create a second framework. Real worker acceptance needs adequate external scratch; no snapshot/test/build was run in this read-only audit. Evidence: assurance-followup-current-source.json.

2026-10-15 final-head follow-up: Prepared separate branch codex/assurance-control-outputs in reused news-significance worktree, main31eaf633. Exactly two files: existing harness plus tests. Optional pre-scoring outcome callback preserves run_one tuple/scoring/restoration; existing journal retains control_outcome; --baseline-mutated records every control including shared commands, both streams/exit/timeout/detection without dedup. Seven red controls against old harness;13 final synthetic guards pass2.13s, zero skips; Ruff/format/types clean. No real snapshots yet;48KiB dedicated external scratch. Independent security/source review is running. nns5 input closure remains separate, and the parent acceptance requiring real before/after worker-content transcript equivalence is not yet met.

2026-10-15 verification follow-up: Independent security review cleared transcript retention; independent senior review clears combined491-addition/27-deletion two-file patch including63k0 submodule metadata handling. Actual before/after mutated captures now prove the diagnosed kpress baseline correction, but outcomes intentionally differ, so they DO NOT satisfy this bead acceptance requiring equality for a genuine worker-content reduction. Keep parent open; no arbitrary extra prune manufactured. All source and decoded output evidence retained.
