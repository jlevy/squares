---
type: is
id: is-01m2evs21mvxf79h8jhnne4src
title: Treat macOS EPERM from killpg as a live process group in every reaper
kind: bug
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - validation
  - macos
dependencies: []
parent_id: is-01m2etr75jfh3t3ry7kj1ccqrb
created_at: 2026-09-14T02:26:13.683Z
updated_at: 2026-09-14T03:43:15.197Z
---
On macOS, `os.killpg(pgid, 0)` and group signal sends raise PermissionError (EPERM) rather than ProcessLookupError (ESRCH) while a group's last member is exiting and not yet reaped. Measured on this Mac with sysctl(KERN_PROC_PGRP): the remaining member was a grandchild reparented to launchd with P_WEXIT (0x2000) set; EPERM lasted 0.1–22 ms, then ESRCH. The UNIX03 kill() reports "group found, no signalable member" as EPERM. A post-reap SIGKILL send also returned EPERM in 6/60 probe trials. Linux is unaffected, which is why hosted CI never saw it.

Consequence: `_group_exists` (packing/devtools/calibrate_fixed_core_packet.py:3483) and `supervise_worker.group_exists` / `reap_descendants_after_leader_exit` / `terminate_group` (packing/devtools/fixed_core_packet.py ~4100) let PermissionError escape, so `test_timeout_kills_and_reaps_a_termination_resistant_process_group` failed about 2 local runs in 10 (the recurring local `--push` failure previously filed under think-cczy as sandbox-only).

Fix for the two packet reapers: commit 1f43e5c6 on claude/n11-stack-ci-stabilization (cherry-picked from a3160f5d). EPERM reads as "group still present", sends tolerate EPERM, only ESRCH proves reaping, deadlines and the "remained alive after SIGKILL" refusal unchanged; four regression tests (EPERM then ESRCH; EPERM forever → existing refusal). Loop evidence: unfixed 2/10 failed; fixed 20/20 and 50/50 (3 runs crossed an EPERM window). Both modules are in the BC329 23-file source closure; the owner deferred BC329 calibration (think-zwlf), so no receipt is invalidated.

Remaining identical patterns (killpg sends suppressing only ProcessLookupError), not yet changed: packing/src/sqpack/cli/validate.py lines 318, 339, 343, 709, 723 (behind packing-validate); packing/devtools/run_negative_controls.py 385, 390; packing/benchmarks/validation_timing.py 53, 58. Apply the same rule with a macOS control, keeping strict absence assertions.

## Notes

2026-09-14 independent review of #168 (ACCEPT): nit — EPERM on SIGKILL is now suppressed before an unbounded process.wait() (calibrate_fixed_core_packet.py:3507-3508, fixed_core_packet.py:4152-4153); a leader that is alive but unsignalable (another uid) would hang instead of raising. Not reachable with the Python workers launched here; suppress EPERM only when process.poll() is not None. The suppressed SIGKILL after TimeoutExpired lacks a direct test. Packet-reaper fix merged into the stack top at 1ea28da4.
