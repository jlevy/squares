---
type: is
id: is-01m5a4mms1m7w430tkb7h7af6d
title: "Codex: qualify PR665 recurrent serial forwarder hang"
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
assignee: codex-pr665-forwarder-diagnosis-20261019
delegate: codex-pr665-forwarder-diagnosis-20261019
labels: []
dependencies: []
parent_id: is-01m50kwed71nqmh914z0mh5103
hold: null
hold_until: null
created_at: 2026-10-19T13:11:59.520Z
updated_at: 2026-10-20T05:58:31.234Z
started_at: 2026-10-19T13:12:10.782Z
closed_at: 2026-10-20T05:58:31.234Z
close_reason: "Diagnosis complete (.codex/intake-resume-20261019/665-forwarder-hang-diagnosis.json); the hang it qualified is fixed by #693 (merged a5acd5708): forwarder_arrivals now closes a per-visit context in a finally instead of Page.close on a shared context mid-navigation. Main validation 39373931375 green and the live site passes 4708/4708 including all forwarder checks."
resolution: null
duplicate_of: null
---
Bounded read-only diagnosis of PR665 frozen head3f20a4584c50d95c02eab7c59193876afb0dd66a, run39255359447 attempt1 frontendjob118069169274. Audit selected155827-byte artifact12188805520 for exact unfinished node and compare forwarder/browser/helper sources to passing a571515ca and current main; preserve historical failures and original think-yops/think-3gfi owners. No frozen source edits, checkout, builds, broad tests, CI wait/rerun, GitHub publication, commit or source push. Diagnostic evidence only; any real repair remains a proposed patch until coordinator assigns a separate tree.

## Notes

Bounded report complete: .codex/intake-resume-20261019/665-forwarder-hang-diagnosis.json. Artifact12188805520 (155827bytes) confirms18passed finishes then test_the_deployed_site_check_follows_the_same_forwarders setup13:01:47.123454Z with no CALL/teardown/finish/JUnit through13:08:13.183324Z (386.05987s incomplete CALL). Command5d8404c61d5c46dab4de3897357ee84d allocated430.389496s, actual431.390468s; frontend901s actual deadline. Journal tests merge d4f629b0, whose tree d478e0c8 equals frozen3f20 head. Ten selected test/browser/helper/renderer/lock files and _site_layout_tests function are identical at passing a571515ca, failed3f20 and main0ee05f4f3. Generated inputs differ; no cause/unrelatedness inference. Main stack is Playwright dispatcher, HTTP handlers wait for request bytes; exact outstanding RPC remains unknown. No local browser/build or source change. Already-running single rerun can qualify current tree only with all51 required cases and load assertions plus required jobs passing; preserve attempt1 and historical failures. Retry success is no causal explanation. If same wait repeats, stop blind retries; separate tree should add serial-forwarder-only pytest-s and DEBUGP1/DEBUGpw:api/PYTHONUNBUFFERED1 to expose RPC IDs while preserving original deadlines/assertions/workers. Detailed patch described only, not applied. Parent and think-3gfi owners preserved; this slice complete, causal work remains open; agent slot released.
