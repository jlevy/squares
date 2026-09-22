---
type: is
id: is-01m351e1qhspbttamjkt3rcnpv
title: "Certification block 1: extend the Goebel strip to a = 9..16 and certify n = 104..296"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-22-upper-bound-certification-blocks.md
labels: []
dependencies: []
parent_id: is-01m350mb40w609b2j8aksv4gq6
created_at: 2026-09-22T17:08:21.872Z
updated_at: 2026-09-22T17:08:21.872Z
---
Validation block per the spec (section The validation block), group A, rule-independent. W6 slice with a W7 build phase; one 30-minute slice. Instrument: packing/cases/gobel_strip (build(a) already general; only SUBJECTS = (4..8) in verify_exact.py:42 limits it). Batch: a = 9..16 gives n = 104, 125, 149, 174, 201, 231, 262, 296 at side a + 1 + sqrt(2)/2, matching each record's reported exact_form (measured with the module's own count rule on 2026-09-22); n = 295 by deletion of one named square from the n = 296 packing, decided by the verifier itself and declared in CERTIFIES. Criterion, declared before running: every pair and containment decided by exact sign over Q(sqrt 2) at the exact side, and the existing one-more-diamond control refusing at every new size. First measure the replay wall (43,660 pairs at n = 296, about 11x n = 89) and keep it out of the fast tier if it would breach the exact-verification step's ceiling (OR-17). Record: extend E-gobel-strip-upper (or a sibling entry) in packing/frontier/evidence.yaml; move verified_upper_bound, append evidence, remove only the upper-bound mathematics blocker and rewrite the body in the nine packing/frontier/n-NNN.md; update CERTIFIES, validate.py _exact_verification comment, TRAILING_BY_CORPUS (-9) in packing/tests/test_verified_upper_bound_contract.py, and price_gobel_family CEILING if it gates anything. Regenerate STATUS.md (render_research_tables), INVENTORY.md (render_evidence_inventory --update), composite-figure.json (build_composite_figure_data --update), and the citation data once think-zb78 exists. Check packing-validate --records then --push; W2 review by a non-author before commit. Stop: batch certified and green, or refusals recorded per size, or a checker blocker if the build does not fit the clock. Nothing about optimality.
