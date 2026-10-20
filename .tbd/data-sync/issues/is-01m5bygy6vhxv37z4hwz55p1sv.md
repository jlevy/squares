---
type: is
id: is-01m5bygy6vhxv37z4hwz55p1sv
title: "Reclaim killed pytest sessions off Linux: a kernel-boot identity for macOS"
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - efficiency
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-10-20T06:03:35.514Z
updated_at: 2026-10-20T06:03:35.514Z
---
Follow-up from think-46yk / PR #695 review A1. devtools.pytest_tmp releases a killed session's numbered directory only when its owner record names the lock's PID in this kernel boot and PID namespace (Linux: /proc/sys/kernel/random/boot_id plus /proc/self/ns/pid). Off Linux pid_scope() is None, so on the owner's macOS host a killed session's tree still waits pytest's three days (failed-only retention keeps each such tree to its session-scoped fixtures and in-flight tests, about 200-500 MiB in the measured quick lane). macOS has no PID namespaces, so a boot identity suffices: kern.boottime (sysctl, via ctypes or a cached subprocess) or kern.bootsessionuuid. Acceptance: pid_scope() returns a boot-unique key on macOS, the macos-portability job runs the killed-session tests instead of skipping them, and a session from before a reboot is still kept.
