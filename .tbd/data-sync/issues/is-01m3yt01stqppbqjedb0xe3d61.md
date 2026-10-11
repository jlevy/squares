---
type: is
id: is-01m3yt01stqppbqjedb0xe3d61
title: "W2-A: sqverify_fast soundness design, Rust crate and Milestone A (rectangle-density certificates)"
kind: task
status: closed
priority: 1
version: 3
labels:
  - verifiers
dependencies: []
parent_id: is-01m3yrezbcgcr728c37fq49bvf
created_at: 2026-10-02T17:18:38.394Z
updated_at: 2026-10-02T23:01:18.724Z
closed_at: 2026-10-02T23:01:18.723Z
close_reason: "Milestone A complete at 67d7179fe: 27 of 27 replayed rectangle certificates verified at 201 directions, controls refused, gate step wired."
resolution: null
duplicate_of: null
---
Clean-room Rust verifier for wand125/Tokoharu rectangle-density certificates at the 201-direction net: soundness design (outward-rounded intervals, structural lower-bound lemmas), exact-oracle differential tests, CLI with per-direction JSON receipts; verify every replayed rectangle certificate and refuse the mutation controls plus own mutants.

## Notes

Crate packing/sqverify_fast with SOUNDNESS.md, INDEPENDENCE.md, README (how to resume). Gate step 'measure verifier Rust (sqverify-fast)'. Census in benchmarks/measure-verifier/census: 27 replayed certificates (24 wand125 + 3 Tokoharu) at 201 directions; controls refused (check_sqverify_fast, census/controls-c2.txt).
