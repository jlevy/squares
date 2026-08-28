---
type: is
id: is-01m131v6jfzt21ggvn3ngskjgr
title: Assemble, reduce, and close the contact equations from an accepted contact structure
kind: feature
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-28-numeric-symbolic-round-trip.md
labels:
  - packing
dependencies: []
parent_id: is-01m0tyy5k7e4ags20c1fxqth7f
created_at: 2026-08-28T02:05:40.302Z
updated_at: 2026-08-28T02:26:37.463Z
---
Steps 3 and 4 of the symbolic promotion route, both unbuilt.

Step 3: the unreduced system still contains the centres. For several published rigid constructions the contact graph lets one eliminate the centres and leave only s and the distinct non-axis-aligned angles -- two unknowns at n=11, three at n=17. That reduction must be derived from the particular graph; an angle-class count alone does not perform it.

Step 4: the system is underdetermined until closed. A local extremum of s on the constraint manifold forces a rank drop, so the missing equations are Jacobian-determinant conditions, Lagrange or Fritz-John in determinant form. The condition is necessary rather than sufficient, so roots that are not extrema are culled when the reconstruction is verified.

The practical reason for the determinant form is not elegance: it keeps the problem root-finding, which reaches thousands of digits, rather than minimization, which does not reach the precision step 5 needs.

Blocked on think-zmh8: there is nothing to assemble until a contact structure is accepted.
