---
type: is
id: is-01m4znhtfbdwfewvssggm76b6q
title: Require a real writable task scratch directory before closure browser checks
kind: bug
status: closed
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zmmp3v11y25f6b8c6fjgvq
hold: null
hold_until: null
created_at: 2026-10-15T11:35:54.090Z
updated_at: 2026-10-15T11:37:18.517Z
started_at: 2026-10-15T11:36:27.773Z
closed_at: 2026-10-15T11:37:18.517Z
close_reason: Corrected local closure preparation with independent review and executed validation. T1 unsupported printed-legend count sentence removed and senior-confirmed clear. External TMPDIR/Cargo/cache directories now exist with writable preflight in tutorial-closure env.sh; pinned Chromium required. Four existing News interaction/facet cases passed55.62s, no skips. Separate109source cases passed49.41s. Earlier4skip/4setup-error receipts retained; no assertion weakened. Parent delivery beads remain open until hosted publication.
resolution: null
duplicate_of: null
---
Local News browser validation first skipped and then correctly failed when Chromium was required: TMPDIR pointed to a task tmp subdirectory that had not been created. Create dedicated external tutorial-closure scratch/tmp/Cargo/cache directories after verifying the mounted volume, verify TMPDIR exists and is writable before launch, rerun the four existing browser cases with pinned Chromium required, preserve skipped/error receipts and report only the final executed pass. Do not change assertions or browser availability refusal.
