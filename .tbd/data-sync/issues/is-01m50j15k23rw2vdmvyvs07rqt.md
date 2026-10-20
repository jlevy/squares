---
type: is
id: is-01m50j15k23rw2vdmvyvs07rqt
title: "Import pingyou: s(29) exact rational certificate, 1.57e-36 below T-155 and 7.32e-90 below #574's N29 (#622)"
kind: task
status: open
priority: 2
version: 29
delegate: user-eb-intake-622
labels:
  - result-import
dependencies: []
parent_id: is-01m50gnwbxd5kxbynyx9nd162p
child_order_hints:
  - is-01m53b204zznqg15rajytfq813
  - is-01m53h0rqh401n0wc2kyky8m5b
  - is-01m53hjsd71tqn0p43d5bkxfpw
hold: null
hold_until: null
created_at: 2026-10-15T19:53:37.121Z
updated_at: 2026-10-20T09:30:07.999Z
started_at: 2026-10-15T23:31:02.497Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
Stage 1 triage of pull request jlevy/squares#622 (BuddenPing, PingYou Ltd, "data: submit a tighter exact N29 packing certificate", opened 2026-10-15T18:43:54Z, no comments or reviews when read at about 19:50Z). A result submitted as a pull request, treated as an intake report as #574 was (think-9v2k): never merged, approved, pushed to or commented on here. Lane D of the 2026-10-15 evening intake pass (think-wnsv, think-ykg6), read-only.

## Pin

- Pull request head 31155575ce1e6b461f77bfc9f3e201adf101115b of BuddenPing/squares, branch pingyou/n29-certificate-20261015, three commits of 2026-10-15 (b6bef2e 18:42:20Z, 44d9d04 18:43:03Z, 3115557 18:43:33Z) on base 73d254272da7 (the merge of #621, on main). It adds four files only: packing/hosted/pingyou-n29-certificate-2026-10-15.yaml and packing/resources/web/pingyou-n29-certificate-2026-10-15/{README.md, claims.json, comparison.json}.
- Geometry outside Git: release data/pingyou-n29-certificate-2026-10-15-v1 of BuddenPing/square-packing-certificates (tag at 318ab94e821ba7280a68fa8ce2942c9ecdbda41d, published 2026-10-15T18:35:51Z), one asset pingyou-n29-certificate-2026-10-15.zip, 430,075 bytes, SHA-256 0dc9bcd1cf5f2806a4d2e0c4c1c07e4903d91bbea611b8b938bda770b9782537: the manifest's size and digest, GitHub's asset digest, and the digest of the copy downloaded here all agree. 34 members; read with zipfile, nothing extracted or executed.
- The certificate: n29-certificate/certificates/n029.cert.json, SHA-256 a01428c51875679fbe78c11a803742b8d99f44b916a660ab6801bb0fcf76951b (as claims.json states), n = 29, 29 squares with rational centres and frames, s_exact a fraction of 2,399 and 2,398 digits, equal to claims.json's side_exact. Its provenance says CERTIFICATE_REDUCTION_ONLY: an 800-digit realization of the known construction, with Evan Daniel's s(29) polynomial file n29_poly_q4.json (SHA-256 0cba5ea2..., the file think-6gti measured) among its inputs.

## Every claim

One: s(29) <= S, S the exact rational side above, about 5.9338334626769291896894606163520191384338341810778869746388259150802542368798 (upward at 40 places 5.9338334626769291896894606163520191384339, the same print as #574's v2 row). Classification certificate_refinement_of_known_nominal_construction: the Kingbird packing of Thomas Schadt, improved by David Ellsworth; no new construction, no optimality. It asks to replace #574's N29 certificate. Credit asked: PingYou Ltd for the refinement, Schadt and Ellsworth for the construction, Evan Daniel for source tools and data, this project's regularization as a baseline. AI assistance: not stated in the pull request; #503's answer ("PY", PingYou's agentic AI) covered #503 and #504 only.

## Map to the register (exact, Fraction, here)

- n-029.md: reported 5.93383346267692 (Kingbird print, exact_form null); verified T-155, 296691673133846459484473030817600957/5e34. S is 1.566e-36 below T-155, 7.32e-90 below #574's v2 N29 side, 5.93e-20 below evand's batch n-29.cert, and 9.19e-15 above the reported print read as a number.
- T-174 (#574) does not register 29. The 14 October ledger left #574's N29 row undecided against the reported lane, and think-abjj's exact pass kept 29 gated: the reported lane's exact side is the root sigma of Evan Daniel's degree-7213 polynomial (#545), which the record does not yet hold (think-6gti).
- By the report-order rule, #622 is later and stronger than #574's N29 row, and below the verified lane; against the reported lane it is undecided until the record holds sigma. S is a rational realization of the same packing, so it is expected just above sigma, as 14 of the 17 #574 comparisons think-abjj decided exactly were above the standing side (3 equal, none below): if so, it is not recorded, unless the owner names a key reason. Register action if recorded: a new entry (a bound the record does not hold), refinement credited PingYou Ltd after Schadt and Ellsworth.
- Draft significance: S1, a padding refinement of a packing the record holds.

## Price

- Feasibility replay: one rational count, 29 squares and 406 pairs, on both maintained exact routes with controls (devtools.upper_bound_reports, the #574 route); under 0.1 CPU-h at 2,400-digit sizes (unmeasured; #574's 192 jobs ran at about 1.6 ms a pair decision on smaller rationals). Within the owner's 40 CPU-h cap; not run in this pass.
- The deciding comparison: the sign of Daniel's polynomial at S against sigma's isolating interval (polynomial retained by digest in evand-exact-data-2026-10-12), or sigma's Krawczyk box once narrowed below 1e-90. Seconds to minutes with FLINT, unmeasured. No new tool needed beyond reading the polynomial.
- Retention (stage 2): the archive by digest under OR-18 (a hosted manifest naming the author's release), the certificate as a derived exact fact.

blocked_on: think-6gti

Waits for the record to hold sigma (think-6gti's import of #545), or for the owner's decision on the undecided comparison at 29, before stage 3 registers or declines it.

## Draft acknowledgement (not posted; stage 7 posts it after the pull request carrying this triage merges)

@BuddenPing, thank you for the N29 submission. We have pinned this pull request at 3115557 and your release data/pingyou-n29-certificate-2026-10-15-v1: pingyou-n29-certificate-2026-10-15.zip, 430,075 bytes, SHA-256 0dc9bcd1…, which matches your HostedData manifest and GitHub's digest. In triage we read n29-certificate/certificates/n029.cert.json (SHA-256 a01428c5…): 29 squares with rational coordinates, and its exact side equals the side_exact in claims.json. Compared exactly, it is 1.57 × 10⁻³⁶ below T-155, this project's exact side for the same Schadt–Ellsworth packing, and 7.32 × 10⁻⁹⁰ below your #574 certificate at 29, which the 14 October ledger left undecided. Whether it is recorded turns on the comparison that ledger could not make: the record's reported value at 29 is the catalogue's print 5.93383346267692, whose exact side is the root of Evan Daniel's degree-7213 polynomial (#545). Your certificate realizes that same packing, so we expect it just above that root, as most of #574's decided rows were. We will decide it exactly, replay the certificate on our two exact routes, and report the verdict here. Merging the pull request is the owner's call; the import goes through the record's own packet, as #574's did.

**A question for the record.** This pull request makes no statement about AI assistance. Your answer on #503, that those solutions were AI assisted by "PY", an unreleased agentic AI offering by PingYou Ltd, covered #503 and #504. Which account applies to this certificate?

## Notes

2026-10-20: import done (#661) and #622 closed with its final reply (recorded by #696), but kept open: it parents an open child (standing logic reads a reported print as exact) and main's result-requests.yaml #622 entry names it as a deferral owner. Close after reparenting that child and updating the record.
