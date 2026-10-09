---
type: is
id: is-01m4hb5kpcaqpmr59xa13fcgyp
title: fixed_core_packet process-group reaping tests fail on clean main in the restarted cloud container
kind: bug
status: open
priority: 3
version: 1
labels:
  - ci
dependencies: []
created_at: 2026-10-09T22:05:06.124Z
updated_at: 2026-10-09T22:05:06.124Z
---
test_fixed_core_packet.py::test_nonzero_leader_exit_reaps_a_sigterm_ignoring_grandchild and test_fixed_core_packet_calibration.py::test_timeout_kills_and_reaps_a_termination_resistant_process_group fail with 'process group remained alive after SIGKILL' on a clean d3860c97a worktree in a restarted Claude Code cloud container (2026-10-09); hosted CI passes them. Check whether reaping relies on init/subreaper or cgroup behaviour the container lacks, and either make the tests robust or document the environment precondition. Also seen: Playwright expects chromium_headless_shell-1234 while /opt/pw-browsers has 1194 (two test_site_column_measurement tests).
