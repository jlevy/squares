---
type: is
id: is-01m4km35x00gep6e2r5fcqf8ab
title: Diagnose truncated macOS reachable-test failures with retained test receipts
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-10T19:19:32.510Z
updated_at: 2026-10-10T19:19:32.510Z
---
On contributor-profile PR #490, commit 40ddcb6f7672594d0653356ab4b6c483b935cb58 against af17208c0, the local 231-file reachable-test run selected 8699 normal-lane cases and timed out at 900 seconds around 76%. Captured progress contains four F markers (completion positions 3991, 4125, 5565, 6398), but termination prevented node IDs and tracebacks; do not infer their cause from dot positions. The command was packing-validate --push --since origin/main --only "type floor" --only "browser floor" from packing, on Python 3.14.7 with ten pytest workers and task-local external-volume caches. Type and browser floors passed. Required hosted PR checks, including all four shards and slow-lane checkpoint coverage, passed. Narrow reproductions so far: 164 negative-control tests passed; first neighborhoods passed 162 tests with 17 skips and 1 expected xfail, then 114 tests; all 7 contributor schema corpus/mutation/inclusion checks passed; 4 later schema neighbors passed. A bounded ten-worker reproduction is being completed and will be recorded on PR #490. Next action: reproduce with PACKING_VALIDATION_ARTIFACT_DIR outside the checkout, retained per-test progress/JUnit and streamed failure details; record actual failing node IDs and compare on the base before proposing code changes. The normal gate supplies the documented Homebrew Cairo library path; direct diagnostic runs must supply it too. This is an unresolved local validation observation, not an established contributor regression. Separately, full checkpoint run 38076495683 exceeded three per-test wall limits; its exact timing-only verdict is recorded on PR #490 and should not be conflated with these unidentified F markers.
