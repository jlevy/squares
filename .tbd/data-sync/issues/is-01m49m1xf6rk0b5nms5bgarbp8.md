---
type: is
id: is-01m49m1xf6rk0b5nms5bgarbp8
title: "Lane: generic contact-system driver (witness -> active set -> half-angle system -> resultant) in the exp-245 pattern"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: claude-code@vm
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m131v6x68y5sdrap8s7zyv0a
  - type: blocks
    target: is-01m49m1ygce7mpg7fb4seamava
parent_id: is-01m49m0enx3qf7mm1kyrra0z10
hold: null
hold_until: null
created_at: 2026-10-06T22:06:26.790Z
updated_at: 2026-10-06T23:03:16.178Z
started_at: 2026-10-06T22:23:13.646Z
closed_at: 2026-10-06T23:03:16.178Z
close_reason: "devtools.recompute_side_polynomial built (commits 1bf3c92b6, 5aab67a98, 496ceeda5). Controls: n=11 and n=17 from witnesses reproduce the octic and the degree-18 catalogue polynomial; n=28 from the certificate reproduces the sextic; dropping an essential incidence is refused or fails S agreement. 12 tests in tests/test_recompute_side_polynomial.py, ruff/format/basedpyright clean."
resolution: null
duplicate_of: null
---
W7. Generalize check_n17_catalogue_polynomial / make_n17_root_certificate: active set from exactsolve or sqpack.promote.contacts, half-angle chart, resultant elimination, factor, isolate, irreducibility. Controls: n=11 and n=17 reproduce known polynomials. Related: think-3lro.
