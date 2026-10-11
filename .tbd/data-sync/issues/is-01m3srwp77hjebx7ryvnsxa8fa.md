---
type: is
id: is-01m3srwp77hjebx7ryvnsxa8fa
title: Keep terminal synopsis handoff and mutation anchor aligned after formatting
kind: bug
status: closed
priority: 2
version: 8
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3sk1aq5e7wm2hzghg3wf499
created_at: 2026-09-30T18:23:07.481Z
updated_at: 2026-09-30T23:49:13.770Z
closed_at: 2026-09-30T23:49:13.766Z
close_reason: PR253 merged as 5ddb1cda; fresh main Packing validation run 36765676235 completed successfully, including deferred-controls-finer and post-merge-required. Focused local negative control also passed. This confirms the expected-error repair, not a new proof replay.
resolution: null
duplicate_of: null
---
PR250 run36757489226 at7c8ed1116 failed synopsis and negative-control checks: Flowmark joined the handoff opening onto the previous paragraph, defeating the line-anchored parser, and controls.yaml still targets think-niqx instead of selected think-e2ot. Repair the paragraph boundary and registered mutation anchor, then run the two affected behavioral controls and source checkers after normal formatting. No mathematical checker change.

## Notes

Focused fix in PR253, head 52f62f5ab on main48d30ff33: only packing/devtools/controls.yaml expected text niqx→e2ot changed. Actual isolated selected negative control fired 1/1 (3.222 s control wall; 164.2 MiB snapshot), unmutated check_synopsis and diff-check passed, normal hook ran. PR evidence comment https://github.com/jlevy/squares/pull/253#issuecomment-5918098013. Root accepted cancellation requests for superseded main runs36762224141 and36764534873; neither is a pass/failure of this fix. Completed main failure36761793749 remains retained. PR253 all applicable hosted checks passed and merged 2026-09-30T19:26:21Z as 5ddb1cdaebfe9580570f949075a62f55973625f8. Deferred control was skipped on PR; fresh automatic main verdict remains pending, so no deferred PASS or full checkpoint credit yet.
