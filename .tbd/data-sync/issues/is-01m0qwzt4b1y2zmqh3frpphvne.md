---
type: is
id: is-01m0qwzt4b1y2zmqh3frpphvne
title: "Engine anchors: sqsearch must recover s(n) at the trivial n, and budget must be monotone"
kind: task
status: open
priority: 0
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0pw8698kc2bqm7d7fy0xydy
parent_id: is-01m0pw7redm194km37gpb3cvmf
created_at: 2026-08-23T18:09:09.771Z
updated_at: 2026-08-23T19:46:43.048Z
---
Two anchors on the search engine itself, at the cases whose answers predate the code. An engine that cannot recover s(n) where s(n) is proved has not earned an opinion about n = 11.

PARTLY STANDING ALREADY (checked 2026-08-23, so this bead is smaller than it looks):

sqsearch's selftest check 7 is a positive control on s(5) = 2 + 1/sqrt(2), asserting both that a 300k-step chain reaches it within 1e-3 and -- the more valuable half -- that it never BEATS it, which is the pre-registered "beating a proved value means you have a bug" rule. Check 8 asserts the reported packing is overlap-free. Check 2 pins the n = 4 grid valid at s = 2 and invalid just below. The gate runs the selftest, and skips loudly by name if the binary is absent.

WHAT IS ACTUALLY MISSING:

1. The rest of the ladder. n = 1, 2, 3 and 9 are not anchored at all, and n = 10 is deliberately excluded from the selftest because one chain needs a real budget to land it -- the comment says it is "measured as a recorded baseline round rather than here", which is a promise the record should be checked against rather than taken on trust. n = 16 is untested.

2. Budget monotonicity -- nothing anywhere asserts that more budget never returns a worse best. This is the half that matters most and the half that does not exist. D-030 is why: there, more budget bought essentially nothing (12, 40, 120 and 400 sweeps gave 3.078187, 3.078175, 3.078175, 3.078174) and that flatness was the ONLY visible symptom of a quench that could not converge. A monotonicity anchor turns "more budget did not help" from an observation someone happens to make into a signal the gate raises.

Note the shape difference: a best-so-far over a longer run is monotone by construction WITHIN one chain, so the check has to compare across independent runs at different budgets, and must therefore state a tolerance and a seed policy rather than asserting exact monotonicity. Cheapest honest form: same seed, budgets B and 4B, assert best(4B) <= best(B) + tol over a handful of seeds, and report the distribution rather than only the verdict.
