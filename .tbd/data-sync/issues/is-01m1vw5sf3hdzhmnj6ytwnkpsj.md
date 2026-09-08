---
type: is
id: is-01m1vw5sf3hdzhmnj6ytwnkpsj
title: Integrate PR97 after the active owner checkpoint
kind: task
status: open
priority: 2
version: 3
labels: []
dependencies: []
parent_id: null
hold: blocked
hold_until: null
created_at: 2026-09-06T17:27:36.675Z
updated_at: 2026-09-06T18:02:07.722Z
---
Integrate PR97 after its active owner produces a checkpoint. Do not land the currently reviewed snapshot as the owner's final disposition.

Reviewed snapshot: ad60089654e9bbc1c86fe9e48cc070b8713d90a9, branch codex/post-381-t2-t10, PR https://github.com/jlevy/squares/pull/97. Required hosted checks passed on that head; deep/exhaustive skipped. No GitHub reviews, issue comments, or inline review comments were present when inspected.

Active owner: Codex task "Squares plan X-016", id01a07341-211d-7f20-95e8-4e1332179ccb, working in /Users/levy/wrk/github/squares on the PR branch. At inspection it was in progress with edits to SYNOPSIS.md, docs/project/document-map.yaml, continuation handoff, agenda024 gate-hour04 decision, and a new research-sequence plan. No message was sent to that task.

Known integration conflicts versus combined PR94/96/95: SYNOPSIS.md; packing/src/sqpack/fractional/certificate.py; and four generated atlas binaries packing/atlas/known-best/known-best-1-100-card.png, known-best-1-100.pdf, known-best-1-100.png, known-best-1-100@2x.png. Merge current main into the owner-approved checkpoint. Preserve the newer research handoff, T022's weak limit scope, PR94's certificate-specific publication semantics, PR95's diagnostic-only CPU contract, and PR96's precise bound audit. Regenerate binaries from merged renderer/data; regenerate embedded claim documents from combined verifier.

Bounded tooling review: 87 focused tests passed, 1 slow retained-theorem review deselected; no confirmed new tooling defect found. Separate mathematical review is being handed to the coordinator. Artifacts: /private/tmp/pr97-integration-notes.md and /tmp/pr97-tooling-review.md. These are snapshot evidence, not an integrated-head approval.

Before landing: fresh exact-head review/status and ownership check; resolve six conflicts; required push validation and records/doc checks; affected verifier refusals and full retained n11 decision because verifier boundaries change; T022 full source replay/record drift check; new retained-theorem audit if changed since its recorded passing run; merged artifact drift and deployed end-to-end checks. Select relevant expensive families explicitly rather than rerunning unrelated n5/n40 mathematics by default. Leave this item open until integration and verification are complete.

## Notes

Await the active owner checkpoint before integrating. Main now contains PR94, PR96, and PR95 at edccf294be375d209c431f4fb8f2eb892f22fd56. GitHub confirms the six anticipated conflicts. The bounded mathematical review is complete at ad600896: no confirmed blocker in T022 support/scaling/density or core-shrink scope; 81 focused tests passed, 14 deselected. The independent tooling review passed 87 focused tests with one slow audit excluded. Neither review reran the full certificate/Lean/novelty surfaces, and neither approves the unfinished or newly integrated branch. Review artifacts: /private/tmp/pr97-proof-review-ad600896.md and /tmp/pr97-tooling-review.md. The ready PRs were merged and their deployed site passed production/browser/consumer-verifier checks.
