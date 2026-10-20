---
type: is
id: is-01m5abczyr52cdwv3njq9jqee5
title: "PR #406 F1: isolate Git fixture environment and sentinel repositories"
kind: bug
status: closed
priority: 1
version: 3
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m58dfyf99t7khbxj1th335af
hold: null
hold_until: null
created_at: 2026-10-19T15:10:08.855Z
updated_at: 2026-10-19T15:16:02.944Z
started_at: 2026-10-19T15:10:18.141Z
closed_at: 2026-10-19T15:16:02.943Z
close_reason: "F1 implementation delivered locally in 3e5cdb0c7a24b62968a33e73d2cebcb76d7cb625, tree f8c1c07e2ab4f2fe3796095d296f0bb3c7d99a2c, parent 032987ac6a2170c168683d0e88ef338a7989b801. Exactly one test file changed: scoped autouse Git environment isolation and two real sentinel cases. Both cases failed before the fix in 0.88 seconds; final 10 focused cases passed in 2.94 seconds. Scoped Ruff/types and normal hooks passed; all seven other PR objects, 46 original function ASTs, policy and eight recovery refs remain unchanged. Full durable report: /Users/levy/wrk/github/squares/.codex/intake-resume-20261019/406-f1-fix/report.md. Close only this implementation child; F1 and parent think-dqmn remain coordinator-owned pending fresh Astra F follow-up. No release, push, GitHub action, CI or merge."
resolution: null
duplicate_of: null
---
Fix only High F1 from /Users/levy/wrk/github/squares/.codex/intake-resume-20261019/406-actualmain-security-f.md at head032987ac6a2170c168683d0e88ef338a7989b801/tree2a9c61af9c5f702884738760cbddacbdf025d7e3. Own only packing/tests/test_added_blob_guard.py. Isolate redirecting Git environment before fixture initialization/writes and through guard calls; preserve production alternate-index semantics and 5MiB/48MiB policy. Tiny real sentinel regression must protect foreign index and GIT_DIR/GIT_WORK_TREE, checking unchanged sentinel index/refs and changed fixture index/history. Observe red then green with 15-second bounded focused selection, existing primary3.14.7-B environment/external scratch only; normal local commit and durable report, no broad gates, publication, release, merge or subagents. Root owns fresh Astra F follow-up; close only this implementation child and keep dqmn open.
