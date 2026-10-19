---
type: is
id: is-01m51fayepg6n4wt17qynt441n
title: "Validate: evand #639 exact sides, verify_exact.py replay of 23 data files at 7d1407a with mutated controls (~0.6 CPU-h; after stage 2)"
kind: task
status: closed
priority: 2
version: 6
delegate: user-eb-intake-1016
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m51e5rvjrd61yaww8djj1nzz
created_at: 2026-10-16T04:25:46.198Z
updated_at: 2026-10-19T22:51:41.055Z
closed_at: 2026-10-19T22:51:41.055Z
close_reason: "Done on PR #651 (receipts committed, 23 VALID, 76 controls refused, every polynomial squarefree and irreducible); registered as E-evand-639-verify-exact-replay and cited from T-193 by PR #658 (merged 926cd764a), which raised T-193 to V3/C3. #639 is answered and closed (issuecomment-6278993243); the 70/153/207 ties are staged under think-ot5c."
resolution: null
duplicate_of: null
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

2026-10-16 ~08:10Z user-eb-intake-1016: DONE on PR #651 (bab830317, receipts committed). verify_exact.py read in full, then run unchanged from the retained copy (evand-exact-and-local-reports-2026-10-12/source/search/exact/verify_exact.py, SHA-256 a0f38ca8...bab4) by packing/resources/web/evand-exact-cur-2026-10-16/review/replay_verify_exact.py, each form in its own python -I process, 2 workers, nice 10, CPython 3.14.7: 23/23 VALID matching data/verify.txt (1,254 CPU s; 263 492 s, 297 308 s, 204 213 s, 267 123 s; walls 4x CPU under host load ~13); 76/76 controls refused at the 19 retained forms (moved square through its wall, side +1e-6 in K, side interval below root, duplicate square; 52 CPU s); the four pinned-only forms have no controls (--controls-at all would add them at near a positive each); SymPy 1.14.0 factor_list: all 23 p irreducible. Total about 0.36 CPU-h counted; plus about 0.25 CPU-h lost when the first invocation hit the session's 30-minute background limit (the driver now caches each run and resumes). Receipt receipts/replay-verify-exact.json; evidence E-evand-639-verify-exact-replay (same-implementation, coverage full); verifiers V-evand-verify-exact (external, decides) and V-evand-639-replay-driver (first-party, premises); control test packing/tests/test_evand_exact_cur.py (n = 51: positive, moved square, duplicate square). check_results derives T-193 at V3/C3. Also covers 51, 70, 153, 207, 172, 263, 297 (not recorded): at 70, 153 and 207 a second exact route to T-174's algebraic sides, for RP-3 (said in the evidence limitations; no separate entry). A review of the replay (separate lane, not run) would need: a read of verify_exact.py's soundness (interval enclosure with outward rounding, identities mod f with 1+u^2 denominators, separating-axis and disc tests, root isolation and S(t*) in [Sa,Sb]), the observation that it never checks len(squares) == n (exact_sides.py does), the driver's input custody and controls, and the T-193 credit/identity mapping; V4/C4 need two such accepting AI reviews and the owner's oversight record. This bead can close when #651 merges (T-193 cites no unfinished confirmation naming it).
