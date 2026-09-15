---
type: is
id: is-01m2hcszcm7y828gwnasgdjxj8
title: "PR #125 review D23: run_arm_sweep reports unverified and below-record sides but never enforces"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb401yy3ph99cfn5mhpcv4
created_at: 2026-09-15T02:02:18.387Z
updated_at: 2026-09-15T02:13:46.986Z
closed_at: 2026-09-15T02:13:46.985Z
close_reason: "Fixed in 39bb08bb: statistics from oracle-accepted poses only, exit 1 with stderr refusals on unverified arms or below-record runs, rebuilt gate recorded as not recorded."
resolution: null
duplicate_of: null
---
Review source: PR #125 review F22 (Medium); triage row D23.

packing/devtools/run_arm_sweep.py reports unverified and below-record sides but never enforces: the docstring (:22-24) promises below-record candidates are flagged separately, but `summarise` (:129-153) averages every engine-reported side, a failed verify() changes nothing, and the exit code is 0 (reproduced with a fake engine claiming side 1.9 at n = 4). `rebuild` (:190) hard-codes "gate": {"passed": True}, so `render` prints "Engine gate: passed" for any archive.
Related: think-gdt9.
