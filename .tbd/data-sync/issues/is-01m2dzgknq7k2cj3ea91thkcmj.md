---
type: is
id: is-01m2dzgknq7k2cj3ea91thkcmj
title: Publish independently accepted BC303 T1 reader as a separate stacked PR
kind: task
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - pr
  - bc303
dependencies: []
parent_id: is-01m2b8watk22ejr9s0zhgrdd17
created_at: 2026-09-13T18:12:16.695Z
updated_at: 2026-09-13T19:57:24.057Z
---
After think-3jsz reaches exact-head acceptance, base a new research branch on the current PR156 head, cherry-pick or port only the T1 source-bound replay, retained review, and narrow research record. Open a separate PR stacked above PR156, measure its unique diff and validation/cost separately, and keep the local counterexample distinct from BC329 calibration. Do not claim T2/global owner routing or a stronger n11 bound.

## Notes

Read-only stack prep retained at /private/tmp/bc303-t1-stack-prep.md. Isolated clean T1 head 74ec773c has two T1-only commits 88d54d85 then 74ec773c touching reader/tests. Final Astra Max exact-head review ACCEPTED 377-atom source-bound literal replay after 17 retained-record and 10 provenance controls, but new branch must replay at its new execution HEAD and retain a fresh receipt. Keep this separately costed draft above final pushed PR156. Candidate retrospective H-159/exp-157 record IDs and agenda cell require schema/ID verification. Claim only rejection of named BL role-C universal T1 inequality; no T2/global routing/new n11 bound. PR publication awaits PR156 final base.
