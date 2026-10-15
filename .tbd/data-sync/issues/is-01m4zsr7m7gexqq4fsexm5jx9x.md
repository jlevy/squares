---
type: is
id: is-01m4zsr7m7gexqq4fsexm5jx9x
title: "F1: remove automatic fast-check reuse based on unauthenticated artifact names"
kind: bug
status: closed
priority: 1
version: 11
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels:
  - pr-620
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
child_order_hints:
  - is-01m4zvpghgeyb11h0bba3v59r6
hold: null
hold_until: null
created_at: 2026-10-15T12:49:18.470Z
updated_at: 2026-10-15T18:55:27.068Z
started_at: 2026-10-15T12:49:26.605Z
closed_at: 2026-10-15T18:55:27.068Z
close_reason: "Source delivery completed in PR620: reviewed head 32ffac9dd8d8756ec619e808d0d3034b58640e6d merged as 4c9af6902e517bfff7d9f50d7cd6a042a15f60ed. Exact-head ordinary Packing 38787870695 and Pages 38787870830 passed; actual JUnit confirms all 46 targeted policy/selection controls passed without skips. Final reviews O5538212826, P5538213019 and Q5538223370 have no open findings and carry unchanged earlier M/N coverage. The historical full43 aggregate remains failed on CALL timing, while its actual 241 slow-lane nodes including all five moved operations passed. Hosted policy now explicitly reports at12s and enforces45s; strict/local/enforce remain12s, and mathematical/functional/child-deadline guards remain. The bounded retrospective, safety removal, supervision, invocation-local input sharing, measured-node placement, native ownership and selection fixes are delivered; no controlled speedup or three-minute success is claimed. Post-merge publication and complete native main coverage remain OPEN and owned in think-bmix; broader measured CI program remains open in think-kxmq/think-jpto/think-h96x. Evidence retained in primary .codex/regularization-closeout-evidence-2026-10-13/."
resolution: null
duplicate_of: null
---
Independent review found the same live source-authentication gap in baseline fc2ceae79: verified_merge_tree.py accepts a self-named tree artifact with successful native run/job names, without authenticating the executed PR merge source. Deferred work stays cold, but allowlisted fast checks can be skipped on main. Remove the automatic reuse path and its dead producer/verifier plumbing rather than introducing a provenance framework. Preserve every fast/scientific check, budgets and normal PR selection. Update the shared guide and meaningful workflow/selection controls. More main fast work may run, but no new proof API overhead or trusting self-declared artifact names. The retired deferred candidate and review evidence are preserved separately.

## Notes

Current head43ee60f6 ordinary PR checks and Pages passed, but selected full38763716551 failed: integration-suites11 CALL ceilings, all remaining full owners including slow lane passed. Quick wall1602.67s vs prior1041.54, matched successful nodes show broad ~1.62x shift; one Atlas node0.57→27.72s is a distinct cold-cache outlier under diagnosis. No merge/waiver/green full claim. Public copy/spacing requested separately in think-gs7g on isolated branch.
