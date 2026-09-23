---
type: is
id: is-01m360kkkhtzfex7be5g633j77
title: Signal-reaping tests race the launch window under load
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-23T02:13:09.872Z
updated_at: 2026-09-23T02:13:09.872Z
---
Two tests fail under a loaded machine and pass standalone, so they are timing-dependent rather than broken:

  tests/test_fixed_core_packet.py::test_posix_signal_reaps_a_live_worker_and_closes_the_preflight_receipt[1-launch]
  tests/test_fixed_core_packet_calibration.py::test_real_supervisor_signal_reaps_worker_including_launch_window[1-launch-default]

Measured 2026-09-22 on the push tier at 10 jobs while captures and renders were in flight (load average 21): 'assert supervisor.wait(timeout=3.0) == expected_status' gave 129 where -1 was expected, at test_fixed_core_packet_calibration.py:2194. 129 is 128 + SIGHUP, the status a process reports when it exits on the signal itself; -1 is what Python reports when the child is terminated by signal 1 without handling it. Both failing parameters are the 'launch' window, which is exactly the interval where the signal can arrive before or after the child installs its handler, so the two outcomes are a race rather than a disagreement about the contract.

Run directly on a quieter machine (load 8) both files pass: 6 passed in 2.35s. They are unrelated to the branch that surfaced them (claude/publish-the-ascent-video changes a README, a spec and an HTML template).

Either the supervisor should report one status for a signal arriving anywhere in the launch window, or the test should accept both encodings of 'killed by signal 1' and say why. Decide which before relaxing the assertion.
