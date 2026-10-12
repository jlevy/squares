---
type: is
id: is-01m4fdxxmb9djrbnegf3hrg48c
title: Bring test_overview novelty-label test under its unchanged 12s call wall
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T04:14:51.019Z
updated_at: 2026-10-09T04:51:58.251Z
started_at: 2026-10-09T04:20:33.848Z
closed_at: 2026-10-09T04:51:58.250Z
close_reason: "Call-wall cause fixed at #442 by fixture placement; full checkpoint qualification tracked by think-zjlo"
resolution: null
duplicate_of: null
---
#442 full run 37877186650: test_overview.py::test_each_row_detail_names_its_novelty_label took 12.08s against 12s. Make it faster with a production or test-structure fix; keep the 12s limit.

## Notes

Fixed on #442: b81fb8f78 (novelty-label and old-paper-links tests take module result_bodies fixture) and 9b19f93c6 (determinism test takes page/results fixtures). Cause: first-in-file-order call paid the cached 126-body render (cProfile 20.49/20.56s in result_popover_html). Call times local 7.75->0.06s, 9.28->0.19s, 5.56->2.57s; module 286 passed; ruff/basedpyright clean. Wall QUICK_TEST_WALL_BACKSTOP_SECONDS=12.0 (validate.py:345) unchanged; enforced on main/schedule/full, advisory on PR. Hosted PR run 37884559660: suites a-d pass, no call >= 12s; frontend failed on CLS 0.134 frontier 1280-dark (think-cmjh). Full checkpoint on final #442 head still required. Optional follow-up: overview render recomputes citations/packets per chain step (2,566 calls for 126 results), results_carrying 10M in_scope calls, repo_links._inside 38k Path.resolve.
