---
type: is
id: is-01m51fayepg6n4wt17qynt441n
title: "Validate: evand #639 exact sides, verify_exact.py replay of 23 data files at 7d1407a with mutated controls (~0.6 CPU-h; after stage 2)"
kind: task
status: open
priority: 2
version: 4
delegate: user-eb-intake-1016
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m51e5rvjrd61yaww8djj1nzz
created_at: 2026-10-16T04:25:46.198Z
updated_at: 2026-10-16T05:53:59.676Z
---
Validation part of think-phyb (#639, Evan Daniel's exact algebraic sides at 23 counts). Record-changing at the 16 counts the report-order rule records (88, 102, 123, 126, 175, 199, 204, 232, 258, 259, 266, 267, 292, 295, 301, 302), and evidence for RP-3 at 70, 153 and 207.

## Validation
- Claim: for each n of 23, s(n) <= S*, S* the root of the integer polynomial p in its isolating interval, realised by an exact configuration over K = Q[t]/f, in evand/square-packing 7d1407a0b66c46e32cdbcbd5619586fe2bdd52a1 search/exact/cur/data/n-N.minpoly.json.gz (23 files, 21,474,827 B, each pinned by SHA-256 in think-phyb); checker search/exact/verify_exact.py (SHA-256 a0f38ca8...bab4, stdlib Fraction arithmetic).
- Run: after stage 2 retains the source (packet evand-exact-cur-2026-10-16, think-phyb): read verify_exact.py, then from the retained copy run it on each data file (the source's verify_data.sh does `python3 verify_exact.py cur/data/n-N.minpoly.json.gz` with xargs -P), and require 23 VALID lines equal to data/verify.txt; then two mutated inputs per checker (a square moved by 1e-6 at one count, and S's interval replaced by one below S*), each refused. Optional: irreducibility of each p over Q (FLINT or sympy), which decides the minimality the source asserts.
- Cost: about 0.6 CPU-h at most: the source's 4 minutes wall on 8 processes; 263 and 297 (9 MB and 7 MB of data) dominate. Irreducibility: seconds to minutes, unmeasured. Basis: the source's README; nothing measured here.
- Budget status: gated on stage 2 retention (a records slice, no owner decision); within the 40 CPU-h cap.
- Possible subset under the cap: n/a.
- Depends on: think-phyb's stage 2 packet. A second route here (sqpack.witness.exact_verify over number fields) needs a converter of evand's minpoly format, a W7 slice with no bead yet; its cost at field degrees 12 to 41 is unmeasured.
- Done when: the receipts (23 VALID, controls refused) are committed in the packet and registered as replay evidence on the stage 3 entry (same-implementation: the source's checker), and listed for RP-3 at 70, 153 and 207.
- Machine note: 4 CPUs shared with gates; about 10 to 20 wall-minutes at 2 to 4 processes; can share the machine with an edit-tier gate, not with a full gate.

blocked_on: none

## Notes

2026-10-16 ~05:58Z OWNERSHIP TRANSFER by the owner's word to the overnight coordinator user-eb (epic think-hg5s): "We have some changes with the regularization and a couple other things from another agent that you should take over and incorporate into your work." The ecstatic-edison lanes should stop work on this bead and its branch, and record any unpushed state in a note here. user-eb's lanes fetch before every push and stop if the branch moved.
