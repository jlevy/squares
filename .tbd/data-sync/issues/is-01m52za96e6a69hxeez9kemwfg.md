---
type: is
id: is-01m52za96e6a69hxeez9kemwfg
title: "PR #645 C12: restate T-194's next_rung and notes under the V/C rule once #645 and #658 land; retitle think-r109 to C3"
kind: task
status: in_progress
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-10-15-formal-proof-verification-rubric.md
delegate: c-coordinator-014ZKp7R
labels: []
dependencies: []
parent_id: is-01m51hy2vfa71y9mv1bc8be41q
hold: null
hold_until: null
created_at: 2026-10-16T18:24:16.078Z
updated_at: 2026-10-20T02:06:43.508Z
started_at: 2026-10-16T18:24:24.757Z
---
Deferred from PR #645 review C, finding C12 (Low): https://github.com/jlevy/squares/pull/645#pullrequestreview-5550797548

Once #645 (formal-proof V/C rubric) lands, T-194's register text restates the rule #645 replaces. T-194 is on main since #651 (`packing/frontier/results.yaml`, T-194):

- `next_rung` says "V3 and C3 need a complete build of the theorem's import closure ... here or by a third party whose build is retained here (think-nqnl)". Under #645's rule, V3 needs an inspected complete execution record (the source's own, or a build here or by a third party), and C3 needs a complete build beyond the producer. The packet's kernel replay is not a complete source rebuild (plan-2026-10-15, Incoming n = 19 Packet), so T-194's V0 stands; only the wording of what each rung needs changes.
- `notes` say "no build of the proof is retained here" as the reason for V0; the reason under #645 is that no complete execution record, of any origin, is retained.

PR #658 (`claude/intake-2026-10-16-records-193-194`, "map the s(19) review onto T-194 (C1)") rewrites the same T-194 entry, so the edit belongs to whichever of #645 and #658 lands second, or to a follow-up after both. Also retitle bead think-r109 ("... for T-154's V3/C3") to name C3 only, since T-154 holds V3 on its source build after #645.

Waits on: #645 and #658 both merged (or one merged and the other rebased onto it).
