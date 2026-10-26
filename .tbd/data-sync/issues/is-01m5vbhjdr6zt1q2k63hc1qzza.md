---
type: is
id: is-01m5vbhjdr6zt1q2k63hc1qzza
title: Build Daniel's S12HLower in the Lean kernel with an axiom receipt, or record the owner's decline (#535)
kind: task
status: open
priority: 2
version: 1
labels:
  - validation
dependencies: []
parent_id: is-01m4pff4kjeeg11941am6tb84v
created_at: 2026-10-26T05:39:44.184Z
updated_at: 2026-10-26T05:39:44.184Z
---
The kernel build of Evan Daniel's S12HLower, s12_ge_15680_3951 : (15680/3951 : ℝ) ≤ minSide 12, registered on 26 October 2026 as a reported formalization of T-049 (#535, think-oyd4, w-imports-1026). The source and its closure (9 modules, receipts/s12h-lean-closure.json) are retained in packing/resources/web/evand-exact-and-local-reports-2026-10-07/ at evand/square-packing f58a017; the proof was first committed at 513bb66 (2026-09-28).

## Validation
- Claim: SquarePacking.s12_ge_15680_3951 from certificates/s12_lower_3.9686.txt (1,736 points, total weight 11.9738036) through the generic BoxTree verifier; the 320 part files and Cov.lean are generated (gitignored) by lean/scripts/gen_data.sh S12H; checker: Lean v4.33.1's kernel, Mathlib 0df444a3.
- Run: stage s12/lean from the packet with the pinned toolchain and Mathlib cache; lean/scripts/gen_data.sh S12H; lean/scripts/build_parts.sh S12H Sqpack.S12HLower 1 14-15; #print axioms SquarePacking.s12_ge_15680_3951; retain the build log, the axiom output and the digests of the generated files in the packet's receipts.
- Cost: about 8 CPU-hours: 39 minutes of generation on one core and 7.3 CPU-hours of build (6 h 31 min wall on 2 cores), up to 30.6 GB resident, by the source's LADDER.md measurement; plus the Lean and Mathlib setup, about 5 GB of disk.
- Budget status: gated on decision. Under the owner's 40 CPU-hour item cap, but above this host's 15 GB of memory, and #535's close condition asks either the build's receipt or the owner's decline: the owner decides whether to build it on a 32 GB host or decline.
- Possible subset under the cap: none that substantiates the bound; a build of the Pts module alone checks the certificate's data facts and moves no rung.
- Depends on: the owner's decision (#535; the 11 October budget line on #543); a host with at least 32 GB of memory.
- Done when: the build's receipt and axiom output are retained, an evidence entry with origin replayed-here is cited by the formalization entry (T-248), and check_results derives its rungs; or the owner's decline is recorded on #535 and in result-requests.yaml.
- Machine note: one part at a time peaks at about 31 GB; it cannot share a 15 GB host with anything.
