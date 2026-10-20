---
type: is
id: is-01m59khvbyx370mcm1z4t18tyy
title: "Codex: diagnose recurrent serial deployed-forwarder wait at main289"
kind: bug
status: closed
priority: 1
version: 10
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
assignee: codex-forwarder-hang-diagnosis-20261019
delegate: claude-forwarder-fix-20261020
labels: []
dependencies: []
parent_id: is-01m50kwed71nqmh914z0mh5103
child_order_hints:
  - is-01m5abdk4yben7cenfr24rs3ms
hold: null
hold_until: null
created_at: 2026-10-19T08:13:22.174Z
updated_at: 2026-10-20T05:48:11.391Z
started_at: 2026-10-19T08:13:31.974Z
closed_at: 2026-10-20T05:48:11.391Z
close_reason: "Fixed by #693 (merged a5acd5708): forwarder_arrivals opens a context per visit and closes it in a finally; the hang was Page.close on a page in a shared context mid-navigation (captured at check_published_site.py:1483, run 39345866613). Verified: main Packing validation 39373931375 green at a5acd57, and check_published_site --commit a5acd57 passes 4708/4708 against the live site including all 27 forwarder checks."
resolution: null
duplicate_of: null
---
Bounded read-only diagnosis by Codex /root/forwarder_hang_diagnosis. Main 2891494ee6b097aef023fcf5cbf43fd623768dbf full run39216687680 timed out at18 serial forwarder cases, matching PR679c78 run39191999508 active deployed-forwarder call. Trace pinned test/server/Playwright lifecycle and retained progress; preserve selections/assertions/caps. Own artifact .codex/intake-resume-20261019/forwarder-hang-diagnosis.json. No source edits, checkout, browser run, full rerun, commit, or source push authorized in this slice. Parent and other agents retain ownership.

## Notes

2026-10-19 after #685 (14fd9e27f) merged with serial-forwarder wire diagnostics: main Packing validation 39314934108 validate job passed, forwarders included (output cut to 65,536 of 2,627,967 bytes; full log in artifact command-914186f41c8b4546b508d3183909dbf3.log). No recurrence on this run; per handoff a pass does not resolve the cause — keep open until a recurrence is captured or a cause is established.

2026-10-20 01:20Z (cloud coordinator session_014ZKp7R, evidence only — owner lane untouched): forwarder hang RECURRED on main b16ddeb0a, Packing validation 39345866613 job validate, step 'site table layout in Chromium' (901 s); serial forwarder command timed out after 633.4 s. The #685 wire diagnostics CAPTURED it. Full log: artifact validation-timings-validate-1, file command-84cc509702894d7b854c81adfe070883.log (1,410,662 B; the 64 KiB step tail is filled by 60 s faulthandler dumps, so read the artifact). Progress: 19 started/18 finished; stuck test tests/test_site_forwarders.py::test_the_deployed_site_check_follows_the_same_forwarders (setup done 00:16:41.077Z). Unanswered RPC: SEND id 749 guid page@a04d59a5... method 'close' apiName Page.close timeout 0, caller packing/devtools/check_published_site.py:1483 (forwarder_arrivals' page.close()), wallTime 00:16:41.444Z. Immediately before: page.goto(.../n11-optimality/?review=fonts#fn-1, commit) and wait_for_url(.../papers/n11-optimality-review.html?review=fonts#fn-1, commit) both returned; the browser then delivered domcontentloaded, load (00:16:41.445) and networkidle (00:16:41.945) for that page's frame AFTER close was sent, then no further wire traffic for the remaining ~10 min. Other unanswered ids 739/744-747 are __waitInfo__ notifications (no reply expected). Reading: Page.close issued while the forwarded navigation was still loading never resolves; close has no timeout, so it waits on the shared deadline. Candidate repairs (owner's call): wait for 'load' before close, close via the context with a bounded wrapper, or reuse one page per context. Python faulthandler stacks show only the preview_site server idle in serve_forever and the main thread in Playwright's asyncio select.
2026-10-20 02:10Z: owner directed session_014ZKp7R to take over all intake work and open PRs; delegate transferred from codex@spud10 to claude-forwarder-fix-20261020 (fix the captured Page.close hang).
