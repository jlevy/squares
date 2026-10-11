---
type: is
id: is-01m494b27nbmm6dd2sw2f3qk7c
title: Certify exactly the six rational closed-form packings whose ceiling T-118 leaves one unit above the report (n = 50, 171, 198, 230, 261, 293)
kind: task
status: open
priority: 3
version: 4
labels: []
dependencies: []
parent_id: is-01m482krnapg9vxqd91zjrg171
created_at: 2026-10-06T17:31:49.365Z
updated_at: 2026-10-06T17:48:00.819Z
---
T-118 (think-70bh) carried Evan Daniel's exact certificates (evand/square-packing 13ee36e) to the verified ceilings at 77 counts. At 55 the catalogue prints a closed form, and the ceiling trails it by one unit of the fourteenth decimal. 49 of those forms are irrational; six are rational: n = 50 (53/7), 171 (13 + 4/7), 198 (14 + 4/7), 230 (15 + 28/41), 261 (16 + 28/41), 293 (17 + 26/41). An exact certificate of the packing at that side would reach them, rational where the packing's exact point is rational, and the ceiling would then agree with the report (the fix check's FC-1: only n = 50 has been looked at).

The review of 6 October (EC-1, docs/project/reviews/review-2026-10-06-evand-exact-ceilings.md) found n = 50's certificate to look like such a rational point scaled by 1 + 1e-20: undone, its side is 53/7 rounded up, every non-free tangent is 0 or 1/3, and 42 of the 44 non-free centres lie on a 1/350 grid; squares 24 and 25 sit 8e-17 off it along their 3-4-5 edge, and the six free squares would need placing (packing/tests/test_evand_exact_certificates.py holds these figures).

Build the contact-exact certificates (undo the scaling, snap the non-free squares, place the free ones with clearance), decide them with sqpack.witness.exact_verify and devtools.check_rational_witness_independent (both accept contact), add controls, and register them as an exact upper bound at the closed form (a new entry or an evidence update per packing/campaign/result-import.md). Note that sqpack.assurance.bounds_agree_at_declared_precision compares exact forms as strings, so the verified lane would need the report's spelling of the form. The other five forms (k + 4/7, k + 28/41, k + 26/41) suggest 3-4-5 and 9-40-41 rotations; check each certificate first. n = 17 is not involved.
