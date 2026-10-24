---
type: is
id: is-01m3vbj45kvj8zb7g4g1tzrdrf
title: Represent infinite theorem families explicitly in result and evidence schemas
kind: task
status: open
priority: 2
version: 5
spec_path: packing/campaign/result-import.md
labels: []
dependencies: []
parent_id: is-01m3v9vq36ykk2jdzce75req44
child_order_hints:
  - is-01m5fxr6nyj5hvxpgf0rwfftjp
created_at: 2026-10-01T09:08:38.700Z
updated_at: 2026-10-24T02:46:40.340Z
---
Current Result and Evidence scopes accept finite n_values or intervals only; Oct1 evand claim s(k^2-3)=k for all integers k>=6 is recorded with finite projection n<=324 and explicit universal statement. Design a schema/checker representation for parameterized families without conflating finite case coverage and universal proof. Preserve generated per-case consequences and assurance of premise/reduction separately.

## Notes

2026-10-24 c-review-pending-1024 (think-rh4j, branch claude/intake-2026-10-24-review-pending): the smallest schema step for one family, taken so that T-163's theorem-wide scope has a recorded answer.

- `record_scope.assessment`, in asymptotic-waste-bounds.schema.yaml: `current`, the `smallest` and `tied` runs of k, the `compared` statements, `recomputed_by`, `assessed` and a `note`. Without one the link still exposes unassessed currentness under this bead.
- packing/cases/asymptotic/deficiency_family.py recomputes the assessment from every statement of `deficiency_upper_bounds`, plus Arslanov, Mustafin and Shangitbayev's k - 1, with the maintained functions: `fang_excess_inventory.theorem_two` and `.ams`, and `ryu_upper_l_packing.count` for Ryu's Theorem 1.3 at its best b. It decides every k from 15 to 90 one by one, and k >= 91 by an integer-checked tail lemma.
- Freshness: a deficiency row it does not name, or a `upper_bounds` row that gains a `constant`, refuses the assessment. `devtools.profile_records.family_record_facets` recomputes it on every read and raises on drift, and tests/test_deficiency_family.py holds it in CI.
- Result: T-163 is current. Its bound is strictly the smallest at k = 15-68 and 70-75. It ties Ryu's Theorem 1.3 at 69 and 76, where the tie stays with Ryu's earlier report (9 October), and it is larger from 77. Fang's profile no longer shows Review pending.
- Not done here, and still this bead's: an infinite parameter scope in results.yaml and evidence.yaml themselves. T-163's scope stays its finite projection, and no evidence entry yet holds the universal theorem, which is why its V3 still needs a published-proof or Lean-build entry (think-494l, think-dgrc). Only the deficiency family has a maintained comparison; any other section's record_scope assessment is refused. think-e953's preconditions (comparable scopes, a maintained competitor set, freshness validation) are met for this family only, and it compares theorem-wide statements, not finite certificates.
