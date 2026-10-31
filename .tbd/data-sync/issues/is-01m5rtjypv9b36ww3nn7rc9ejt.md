---
type: is
id: is-01m5rtjypv9b36ww3nn7rc9ejt
title: "Validate Daniel's s(29) degree-7213 minimal polynomial (T-246, #816, #817): replay, independent checks, packing at the exact side"
kind: task
status: open
priority: 3
version: 8
delegate: null
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-25T06:04:54.875Z
updated_at: 2026-10-31T07:02:21.103Z
started_at: 2026-10-25T15:41:58.506Z
---
The validation of Evan Daniel's degree-7213 minimal polynomial of the s(29) record side, T-246, from the release exact-data-2026-10-12 of evand/square-packing (tag commit 31523f87316bdfda00f5459dd9077928e264f133), tracked by the owner's issue #816 and delivered on draft PR #817 (branch claude/friendly-einstein-gf9z0h-s29-validation), owner w-s29-validate-1025.

**Inputs.** s29-minpoly.tar.zst, 87,237,962 bytes, SHA-256 708e1b8b45894667f90a0d18b55bb35ed6079b84d33f9656976fd5cfa6f3729c, pinned in packing/resources/web/evand-exact-data-2026-10-12/acquisition/release.json; fetched 25 October into scratch, every member held to the pinned digest. The source's scripts at ad86d42 in packing/resources/web/evand-exact-and-local-reports-2026-10-12/.

**Budget.** The owner's per-item cap of 25 October: 10 CPU-hours, revised to 3, then 5.

**Steps and status (25 October).**
1. Same-implementation replay (C3): DONE, 10/10 steps passed (replay.json, 1.63 CPU-h): krawczyk, link, irred (12 primes), contacts_mod (21), verify_mod (10 fresh random primes, not 50), and four controls that refuse.
2. Independent irreducibility and root isolation: DONE. devtools.check_exact_side_minpoly: distinct-degree factorization modulo 5 primes near 40000 empties the degree certificate (1,300 CPU-s); exactly one root of p in S_mid +- 2e-48, in exact integer arithmetic (290 CPU-s).
3. Deterministic identities: PRICED, not run. Exact route about 717 CPU-hours (numerators up to 11.8 GB); modular route about 1.1e8 primes. Both far over the cap; the identities stay Monte Carlo.
4. Non-overlap at the exact side: DONE, deterministic. devtools.check_exact_side_packing: the configuration at the unique zero t* of F in the Krawczyk box is a packing; the whole contact system is consistent at t* by exact elimination over Q(t). So s(29) <= S* with no Monte Carlo step.
5. Against T-195: DONE. sigma < T-195 exact rational by 3.90143354777e-799 (812-place exact bracket, p negative at T-195); S* below it by the same (Krawczyk box re-certified to 2e-2618). Head 83ec0f062. Open: step 6 review, the register records, step 3 deterministic identities (priced).
6. Review document: OPEN. CPU used about 2.95 of 5 CPU-h.

## Notes

2026-10-31 bold-ritchie-l5 (intake pass of 31 October, epic think-3guf, lane L5), taking over from w-s29-validate-1025, silent since 25 October: draft PR #817 brought up to date and step 6 written. Commits on claude/friendly-einstein-gf9z0h-s29-validation: e2bad14f0 merge of origin/main 3978a7f61 (conflicts: result-requests.yaml keeps #816 before #819 and #824; release.py is main's with #816's no-change record appended); 34fbb28ba the review docs/project/reviews/review-2026-10-31-evand-s29-minpoly-validation.md (mapped; SYNOPSIS map rendered) and the record measured again at e2bad14f; bae6f8df1 #816's ask gains `source: body` (check_requests after the merge); bfb16dc53 the record measured again at bae6f8df (43 methods-survey files byte-identical x3). No compute was run: the deterministic identities stay priced (about 23 CPU-hours for the sample Sn = x Sd, about 717 for all six), and the session cap of 25 October (5 CPU-hours, 2.95 used) is not reopened.

**Verdict (the review):** accepted, with one Monte Carlo step. Decided deterministically: irreducibility (irred.py replay, and independently DDF mod 40009..40039), the Krawczyk zero (replay, and independently sqpack.promote.krawczyk to 2e-2618), the root (link.py replay, and independently exactly one root in S_mid +- 2e-48), the packing at t* (first-party, new), sigma and S* below T-195 by 3.90143354777e-799. Monte Carlo: F_k(tau) = 0 and Sn(tau) = x Sd(tau) in Q[x]/(p) (verify_mod 10 fresh primes, contacts_mod 21). Findings F-1 (identities, major, record), F-2 (s(29) <= S* deterministic, 3.9e-799 below T-195, major, owner), F-3 (N29.md writes s(29) for the record side), F-4 (10 of 50 primes), N-1 (free squares' chosen poses).

**Rung:** C1 (read) on E-n029-evand-minpoly-7213-report via this review as external_review; not C3/V3 while the identities are Monte Carlo (no evidence method represents a random-prime identity check). The register records (verifiers, evidence entries, T-246 to C1 with the review) are proposed in the review and not written: the records lane's, after #817 merges.

**Draft reply on #816 (post after #817 merges, from main):** "Status of the six steps, on main with their receipts under packing/resources/web/evand-exact-data-2026-10-12/receipts/validation-2026-10-25/: (1) the author's replay passed, 10 of 10 steps, with the source's own scripts (10 of the 50 verify_mod primes, under the cap); (2) irreducibility and the root were decided again with independent code; (4) the configuration at the unique zero t* of the five consistency polynomials is a packing, decided without any Monte Carlo step, so s(29) <= S*, where S* = S(t*); (5) S* and sigma both lie 3.90e-799 below T-195's exact rational, and agree with each other to about 810 places; (3) the identities that make sigma equal to S* exactly are still checked modulo random primes only: a deterministic check is priced at about 23 CPU-hours for one identity and about 717 for all six; (6) the review (docs/project/reviews/review-2026-10-31-evand-s29-minpoly-validation.md) accepts the chain with that one Monte Carlo step. Two decisions are yours: whether to register s(29) <= S* as an upper bound below T-195 and re-kind T-246, and whether to fund the deterministic identities."
