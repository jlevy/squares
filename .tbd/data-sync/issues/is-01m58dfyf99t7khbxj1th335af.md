---
type: is
id: is-01m58dfyf99t7khbxj1th335af
title: "PR #406 C1: bound both Git metadata streams during capture"
kind: bug
status: in_progress
priority: 1
version: 13
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4mv0ysrv4te0kgnpxn0wfwp
child_order_hints:
  - is-01m59yp4esa47wba0kwj0y730x
  - is-01m5a6vkthqxkjgnng3vp4zgvy
  - is-01m5a7wewtf8ky7n5kbs7y47jr
  - is-01m5a8frn6a2fhvd9qar6v9ars
  - is-01m5a92xfsgxjb7480g09mkq82
  - is-01m5a9znvp10awr1kf6s9f9ph9
  - is-01m5aaexwh6kw61bgmtr7mkq0d
  - is-01m5abczyr52cdwv3njq9jqee5
  - is-01m5abvzd0xk8vvwh8qgavt7yz
hold: null
hold_until: null
created_at: 2026-10-18T21:08:13.927Z
updated_at: 2026-10-19T15:18:19.807Z
started_at: 2026-10-18T21:08:20.463Z
---
Security preflight S1 at PR #406 head 8811bd763d437aaf8d75dc5d1dd4ac761a1bc39d: packing/devtools/check_added_blobs.py:_git currently uses subprocess.run(capture_output=True), buffering unlimited stdout and stderr before checking MAX_METADATA_BYTES. Consume both streams concurrently with an enforced per-stream cap, kill/reap the child immediately on excess, retain the existing deadline and fail-closed errors, and add focused small-cap oversized-stdout/stderr regressions proving early termination in packing/tests/test_added_blob_guard.py. Coordinator root owns publishing and schedules focused tests after #676 Stage 3 releases the heavy slot.

## Notes

Implemented and locally verified in commit 218de505257e0c58175863c142ebf9f667c3675e on branch codex/pr-406-security-s1-20261018, parent 8811bd763d437aaf8d75dc5d1dd4ac761a1bc39d. Security preflight S1 is formal Review C finding C1: https://github.com/jlevy/squares/pull/406#pullrequestreview-5565072172. Only packing/devtools/check_added_blobs.py and packing/tests/test_added_blob_guard.py committed (131 insertions, 15 deletions); tracked working diff empty after commit. Capture drains stdout/stderr concurrently using POSIX selectors with per-stream bounded buffers and a one-byte overflow probe, writes supplied stdin in nonblocking PIPE_BUF chunks, checks query/protocol deadlines including after selector wakeup, and kills/reaps the child on overflow or timeout. Three real-child regression cases cover stdout overflow, stderr overflow, and timeout, with blocked stdin and explicit SIGKILL/closed-pipe assertions. Red witness loaded only pinned-head _git into the module in memory: exactly 2 overflow failures (old query-timeout remedy) and 1 timeout pass; no source files reverted. Final Python 3.14.7 verification from packing: python -m pytest -q --tb=short -o cache_dir=$TMPDIR/pytest-cache tests/test_added_blob_guard.py => 51 passed in 7.68s, covering normal stdin-driven cat-file too; python -m ruff check --no-cache devtools/check_added_blobs.py tests/test_added_blob_guard.py => pass; python -m ruff format --check --no-cache on the same files => 2 files already formatted; python -m basedpyright --pythonpath /Users/levy/wrk/github/squares/packing/.venv/bin/python3 on the same files => 0 errors, 0 warnings. Final combined verification wall 10.28s with a hard 120s process-group timeout enforced. Earlier scoped style/type/fixture findings were corrected; no child-design hang or external I/O stall occurred. Normal-hook commit passed lefthook 2.1.10, pinned Flowmark 0.4.0, and paper-title contract (11.90s hook, 12.30s total); no bypass. Env: /Volumes/spud-ext1/agent-scratch/squares-406-security-20261018/env.sh; main established project interpreter used with this worktree packing and packing/src explicitly on PYTHONPATH. No code push, PR edit, CI dispatch, disposition reply or rebase performed. Leave open pending coordinator main integration, full --push gate, hosted CI and formal disposition.
