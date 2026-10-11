---
type: is
id: is-01m4ph7dfnsqweryt753f6rrcq
title: Restore bounded website feedback and repair test selection scope
kind: task
status: open
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
hold: null
hold_until: null
created_at: 2026-10-11T22:27:08.917Z
updated_at: 2026-10-11T22:34:16.593Z
started_at: 2026-10-11T22:29:47.262Z
---
User-requested review after PR513 took excessive time. Three read-only review lanes confirmed: (1) generic precommit-process and code-review-and-commit require the full suite before publication, contrary to OR-3; reconcile project forks, AGENTS and development stage ownership, retaining full evidence at final pre-merge/research checkpoints. (2) Existing selector CLI chooses 114 of 756 test files for only packing/tests/test_readme.py; source attribution is one changed test plus 113 unconditional walker/dynamic-import selections. Temporary-directory walks and native-extension imports are misclassified as whole-repository inputs. Add audited explicit walker input scopes, conservative unknown-scope fallbacks and structured selection explanations; retain import closure and configuration/parse fallbacks. (3) Hosted Packing38179357602 measured428s, frontend414s with328.24s layout step (301.27s functional tests +25.79s HTTP cases). Fixtures cost77.99s homepage,77.33s atlas,34.04s result columns and33.52s cases. Process-local render reuse already exists; share immutable prepared inputs across workers and establish one explicit browser worker budget. Current four-core jobs2 configuration permits three layout workers plus two workbench browsers; contention impact still needs a controlled comparison. (4) Existing behavioral capacity task think-2hm6 still leaves shard C373s on critical path. Preserve cheap coverage; reduce redundant setup, then rebalance capacity. Pages run38179357651 measured294s; six page builds were legitimately selected by shared typography/nav changes, so no broken Pages selector established. (5) First local full checkpoint3613.46s and push1047.81s (behavioral900s timeout) were serialized before CI by coordinator; the redundant second broad local run was stopped under the users latency objection. Repair workflow ownership and enforce bounded ordinary preflight with visible selection cost. Budget overruns remain advisory under existing think-g4n9/think-ht59; do not solve by arbitrary timeout raises or dropping independent evidence. CLI evidence and audit notes are in external task scratch squares-site-cleanup-01a12c91. Review complete; implementation belongs to the existing website-loop plan, with no CI architecture changes in PR513.
