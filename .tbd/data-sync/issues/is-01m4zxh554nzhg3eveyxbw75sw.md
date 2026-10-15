---
type: is
id: is-01m4zxh554nzhg3eveyxbw75sw
title: Measure restored main integration work and assess native fast-job fan-out
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels:
  - pr-620
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-15T13:55:20.867Z
updated_at: 2026-10-15T18:55:27.110Z
started_at: 2026-10-15T13:55:48.324Z
closed_at: 2026-10-15T18:55:27.110Z
close_reason: "Source delivery completed in PR620: reviewed head 32ffac9dd8d8756ec619e808d0d3034b58640e6d merged as 4c9af6902e517bfff7d9f50d7cd6a042a15f60ed. Exact-head ordinary Packing 38787870695 and Pages 38787870830 passed; actual JUnit confirms all 46 targeted policy/selection controls passed without skips. Final reviews O5538212826, P5538213019 and Q5538223370 have no open findings and carry unchanged earlier M/N coverage. The historical full43 aggregate remains failed on CALL timing, while its actual 241 slow-lane nodes including all five moved operations passed. Hosted policy now explicitly reports at12s and enforces45s; strict/local/enforce remain12s, and mathematical/functional/child-deadline guards remain. The bounded retrospective, safety removal, supervision, invocation-local input sharing, measured-node placement, native ownership and selection fixes are delivered; no controlled speedup or three-minute success is claimed. Post-merge publication and complete native main coverage remain OPEN and owned in think-bmix; broader measured CI program remains open in think-kxmq/think-jpto/think-h96x. Evidence retained in primary .codex/regularization-closeout-evidence-2026-10-13/."
resolution: null
duplicate_of: null
---
F1 correctly removes unauthenticated fast-check reuse. In final full run38744311408 the complete integration job is the remaining critical path after the dedicated workers pass, so retain its actual cost and assess a small native same-workflow alternative: can existing fast PR jobs execute on non-PR events with an exact complementary integration selection and aggregate? No cross-run proof/API/attestation framework, duplicated checks, cap increases, source waivers or speculative speed claim. First inventory the nonfast steps still owned by validate and prove exact partition before proposing implementation. Keep this investigation separate from frozen PR620 unless a real failure requires a fix.

## Notes

2026-10-15 14:20 UTC: Actual integration receipt retained in pr620-full-validate.log: wall 2301.62 s; shard C 315.92 s, A 314.35 s, B 304.79 s, D 242.31 s; site layout 283.35 s, types 91.90 s, workbench browser 83.47 s, atlas sample 58.42 s. Four shards failed only on seven strict CALL>12 s verdicts; splitting alone cannot fix them. All ten dedicated workers and macOS passed. Topology analysis retained; any implementation must preserve exact partition, per-test guard, deadlines and worker/checkpoint cost accounting.

2026-10-15 grouped repair snapshot: Implementation selected after measured topology review: ONE new non-PR integration-suites worker, not four. It runs the same four quick Steps serially at jobs=1/inner_jobs=2 with existing -n4 loadfile recipe, strict 12 s CALL guard and 900 s command deadlines. Residual integration skips exactly those four; native aggregate requires both owners. It adds one real history/submodule, uv, Node/Chromium and artifact setup; preserves existing native floors and PR commands. Four workers would add three setup lifecycles to save only about 53 s in the recorded shape (residual about 1124 s versus four suites about 1177 s), excluding setup/runner effects. New 1390 s worker wall is a derived reporting-only estimate, not measurement; existing full3600/checkpoint3430 ceilings stay. Exact parser/partition/refusal controls green; a fifth existing exact-argv/bootstrap contract is being updated after its genuine failure. Final hosted selected/node/skip roster comparison is required, not just Step-name coverage.
