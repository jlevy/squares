---
type: is
id: is-01m2hcsyah4pva5vdsfv8f1wc6
title: "PR #125 review D03: the engine selftest's control comparison cannot fail"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb401yy3ph99cfn5mhpcv4
created_at: 2026-09-15T02:02:17.296Z
updated_at: 2026-09-15T02:02:50.679Z
closed_at: 2026-09-15T02:02:50.678Z
close_reason: "Fixed in 37309cae: selftest step 5b compares the control bitwise against a frozen pre-arm move loop (packing/sqsearch/src/control.rs), with a stream-shifting negative control; the unconditional-draw mutant now fails the selftest (exit 1) and the cargo test."
resolution: null
duplicate_of: null
---
Review source: PR #125 review F7 (High), pinned to 7b06254c; triage row D03 (attic/reviews/triage-stack-2026-09-14.md).

The engine selftest's "control chain unchanged by the arm flags" comparison cannot fail: it compares the control `p` against `Params { p_perturb: 0.0, mu0: 0.0, mu1: 0.0, ..p.clone() }`, which are p's own default values, so both runs have identical parameters. The review's mutation (unconditional perturbation draw, `search.rs` `let whole = rng.f64() < p.p_perturb;`) still printed SELFTEST PASSED.

Files: packing/sqsearch/src/main.rs selftest step 5b (about :477-506 at 6f30d5b7); packing/sqsearch/src/search.rs anneal guards.
Related: think-gdt9 (the arms feature record, whose description still says the selftest pins a literal).
