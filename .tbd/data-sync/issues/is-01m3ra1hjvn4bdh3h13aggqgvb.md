---
type: is
id: is-01m3ra1hjvn4bdh3h13aggqgvb
title: Consolidate proof verification and decouple the validation pipeline
kind: epic
status: in_progress
priority: 1
version: 20
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3qw8b5q2xgjp85cxx24134c
child_order_hints:
  - is-01m3razbt8p1kktnnzvqbdjv74
  - is-01m3razc6hwms10f04btg028vv
  - is-01m3rb0sr8p2xn3m96v3cs96cx
  - is-01m3rb0t4zqdze43drjkx9cqx2
  - is-01m3rbmdd2knptgfj454y4exak
  - is-01m3rkt99p9bxh8csj2v58nh9p
  - is-01m3s6fg7h4a51s61zzk4k37qp
  - is-01m3s98kgj0s9pg4ybk685nc7t
  - is-01m3sk1aq5e7wm2hzghg3wf499
  - is-01m3sken298psm0jfn7tmbcqp9
  - is-01m3snf059ca48fjmqh0vrb7e8
  - is-01m3sp12jsvbfsveyd1cqq2msj
  - is-01m3sq5aphftxdvr0spvz9sbny
  - is-01m3tyjy9bax7sa7xjqjv212c5
created_at: 2026-09-30T04:44:23.504Z
updated_at: 2026-10-01T05:21:53.947Z
---
Consolidate the independently confirmed n11 proof and its reusable verification tools, with separate contracts for proof geometry, source/receipt admission, evidence composition, and repository CI. Initial size audit at0dda2856e found 59,419 added lines across240 files; that is a planning baseline, not current scope. Completed work includes lossless evidence compression (93,389 plaintext ledger lines removed), shared field and exact geometry kernels, all T060 mathematical executions/review atS5/V4/C5, a first-principles tooling overview, and measured CI/diagnostic improvements. Final integration/merge is think-pd17; shared diagnostic admission think-nxd8 is implemented/reviewed in an isolated follow-up; fresh chained replay think-e2ot, rectangle native performance think-3cwg, and cross-provider PR249 reconciliation think-d15x remain separately tracked. Preserve accepted source and evidence identities; no blanket verifier rewrite, unique evidence deletion, or new framework is required.

## Notes

Implemented shared field geometry/runner and independently reviewed integer and indexed exact kernels; generic exclusion, capture, local isolation and final composition remain separate contracts. Deterministic compression has removed 93,389 plaintext ledger lines while preserving decoded bytes and acceptance credit. Final composition is implemented with missing-premise refusal and observed-execution disclosure. Current work finishes the remaining proof executions and complete audit; it does not require a blanket verifier rewrite, a new workflow engine, or a PR-history split. The optional Rust rectangle backend is complete but slower on the matched external probe; measured performance follow-up remains think-3cwg and cannot block T-060. Keep the planning baseline in the spec distinct from current acceptance in the mathematical review.

2026-09-30: T-060 and within-PR integration are complete at the previously green 180326e81. The new first-principles overview separates proof execution, evidence composition and CI. The 66c37b255 diagnostic closes think-r97y negatively, with complete retained evidence. Packaging remains focused: think-e2ot for a thin fresh replay entry point, think-nxd8 for shared diagnostic frontier admission, and think-d15x for actual cross-PR merge/ID reconciliation. Accepted proof sources and receipts remain unchanged.
