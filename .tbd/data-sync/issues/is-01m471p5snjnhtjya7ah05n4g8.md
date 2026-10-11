---
type: is
id: is-01m471p5snjnhtjya7ah05n4g8
title: "Import evand #375: exact rational optima of 48 known-best packings (upper bounds 3e-13..5e-11 below the register) and exact certificates for 321 records at 13ee36e; n = 17's certificate held"
kind: task
status: closed
priority: 1
version: 7
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m46g4yac7ewc22drc7twjhy5
hold: null
hold_until: null
created_at: 2026-10-05T22:06:58.868Z
updated_at: 2026-10-06T02:41:33.060Z
started_at: 2026-10-05T22:08:15.283Z
closed_at: 2026-10-06T02:41:33.060Z
close_reason: Done in jlevy/squares#369 (merged 34e87a86b); verdict replies posted 2026-10-06
resolution: null
duplicate_of: null
---

## Notes

Stage 1 (triage), 2026-10-05: acknowledgement posted
https://github.com/jlevy/squares/issues/375#issuecomment-6004562871 (22:35:10Z), recorded in
result-requests.yaml (#375, answer bead think-ybmt).

Provisional register id renumbered by the coordinator from T-099 to T-098 (T-095 to T-097 are
s(12), s(18), s(66)); the branch uses T-098 throughout.

Stage 2 (retain): packet packing/resources/web/evand-square-packing-2026-10-05 written by
devtools.acquire_source from a blobless clone at 13ee36e; 58 files retained (48 improving
certificates, verify_cert.py, verify_cert2.py, exactsolve.py, geom.py, verify_all.sh,
reproduce.sh, results.md, results.json(.gz), both READMEs), 632 pinned by digest; n = 17's
certificate, input and test-set outputs left out of the scope (think-x4v4).
Key [evand exact optima 2026-10-05]; credit Daniel after Couzo, de Winter, Ellsworth, Levy;
lineage builds-on-project.

Stage 3 (record): T-098 upper-bound, 48 counts; evidence E-evand-exact-optima-2026-10-05-report,
-exact-replay, -source-replay; verifiers V-evand-verify-cert-py, V-evand-verify-cert2-py,
V-evand-exact-certificates. Case records written by devtools.apply_exact_optima, a layer
composed into apply_upper_bound_packets and generate_frontier_case; source-coverage selects
the packet (claims record: the retained certificate directory). Atlas pictures the finder's
pose (pictured_source_key).

Stage 4 (replay), 320 certificates (all but n = 17):
- first-party: sqpack exact_verify + check_rational_witness_independent, all VALID, 2,820 CPU s
  on 2 workers (802 for the 48); least wall clearance 5e-21, least pair gap 1e-20.
- source checkers verify_cert.py + verify_cert2.py: all accept, 202 CPU s (55 for the 48).
- comparison: all 48 below the earlier printed side by 3.53e-13 to 4.97e-11, matched one to
  one; largest displacement 1.44e-3 (free squares), non-free 4.14e-5 (n = 263).
- finding: verify_all.sh's first leg (grep -q VALID) also matches INVALID.
Follow-up opened: think-70bh (the 78 trailing ceilings the other certificates could lift).

--- Triage notes ---
Stage 1 (triage), 2026-10-05, lane F of think-fg6g, worktree squares-lanes/exact,
branch claude/ecstatic-pascal-pothtx-exact (base 4fa04caf2).

Source pinned: evand/square-packing 13ee36e5807727d12a5da36b9b90a96bdba272bf
(committed 2026-10-05T20:54:59Z; head at 22:08Z and 22:22Z), s12/search/exact/.
The head is 2 commits past the 7ff3b211 pin: ab2bf47 (WISHLIST section G and a literature
note on the degree of s(n); nothing to import) and 13ee36e (this import).

Claim map (issue #375, body only, no comments):
- exact-optima-48: s(n) <= S'_n at n = 68, 102, 103, 106, 110, 123, 126, 131, 132, 152,
  154, 155, 156, 172, 177, 180, 181, 182, 199, 206-211, 228, 236-241, 259, 263,
  268-273, 297, 301-307; S' rational, 3.5e-13 to 5.0e-11 below the record's reported
  side. Register action: one new upper-bound entry (provisional T-099, now T-098) whose scope covers
  the 48, with a reported entry and replay entries; the case records' reported and
  verified upper lanes move to S' (the T-088 and T-092 precedents: an optimization or a
  later release that lowers a side is a new entry, the earlier ones keep their claims and
  the case records decide which is current). Who else holds each value: Couzo's printed
  sides (T-056 at 40 counts, T-092 at 208, 209, 228, 263, 272, 303, 306), de Winter's
  n = 211 (T-057), and n = 126, de Winter's packing via the Kingbird catalogue, whose
  verified ceiling is the 12 x 12 grid today.
- certificates-273: exact certificates at the 272 other certified counts (n = 17 held),
  1e-20 to 1e-14 above the printed sides; the author asks for nothing. Register action:
  none ("below the standing bound and asking for no work"); retained by digest, replayed
  with the rest, and noted as a possible later use where the verified ceiling trails.
- kkt-local-minima: 315 of 321 (44 of the 48) numerically KKT local minima; numerical
  evidence, recorded as reported in T-099 and its evidence, not verified.
- n105-descent: n = 105's witness may not be a local minimum (first-order descent with
  corner-corner slips); numerical observation, no register action.
- n17-certificate: held by the owner (think-x4v4); not retained, replayed or recorded.

Validation plan, priced:
- The source's checkers verify_cert.py and verify_cert2.py (stdlib Fraction): measured
  54.6 CPU s for the 48 retained; about 4 CPU min for all 320.
- First-party: devtools.evand_exact_certificates converts each certificate exactly
  (t -> (c, s)) to a rational center-basis Witness/v2 for sqpack.witness.exact_verify and
  to rational corners for devtools.check_rational_witness_independent; measured 2.1 s at
  n = 68 and 33 s at n = 307; about 70 CPU min for all 320.
- Controls: per improving certificate, the tightest pair overlapped by its gap plus one
  unit of the side's denominator, the box shrunk past its least clearance by one unit
  (both must be refused by all four checkers), and the box shrunk by one unit alone.
- Comparison: S' against the earlier holders' printed and verified sides, and each pose
  against the known-best witness, square for square.
- Optional reproduction sample with reproduce.sh (about 1-2 CPU h for all; sample only,
  2 threads, nice).
- One separately prompted adversarial review.

Exit, 2026-10-06 (branch claude/ecstatic-pascal-pothtx-exact at c18fca891, not pushed):
- T-098 at V3/C3 (status confirmed), S2 confirmed by the review. Replays: first-party
  2,820 CPU s for 320 certificates (802 for the 48); source checkers 202 CPU s (54 for
  the 48); controls 3,276 s wall on two workers; reproduction sample (n = 68, 102, 126,
  211, 270) 178.3 CPU s, same S', not byte-identical (centres <= 2.5e-24, tangents
  <= 3.3e-24), each decided valid.
- Review docs/project/reviews/review-2026-10-06-evand-exact-optima.md (adversarial,
  defect-open on EX-1, n = 126's conjecture above the new ceiling); fixes in 65bb9851b;
  fix check review-2026-10-06-evand-exact-optima-fix-check.md (confirming,
  defects-resolved); FX-1..FX-7 handled in 6f84e2783. Both stored byte-identical and
  excluded from flowmark. Neither reviewer could execute code.
- New: sqpack.assurance refuses a decimal conjectured_optimum above the verified ceiling
  by more than half a unit; result_status.latest_review takes the last listed of
  same-day reviews (used by check_results and check_requests).
- Translation-escape screen re-run (33 min, two workers): only the 48 reported_side
  strings changed.
- #375 verdict reply posted: issuecomment-6007913483, recorded as kind confirmation.
  n105-descent remains a reply due for the reply from main.
- Open: think-5n3o (EX-9, reported-lane witness), think-70bh (78 trailing ceilings),
  think-x4v4 (n = 17 hold). Contiguity of register ids fails until the coordinator
  reconciles T-095..T-097; with T-098 renumbered into a contiguous slot every
  check_results-driven test passes.
