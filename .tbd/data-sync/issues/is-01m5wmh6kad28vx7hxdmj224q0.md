---
type: is
id: is-01m5wmh6kad28vx7hxdmj224q0
title: One rule for an asset's address, in one place
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies:
  - type: blocks
    target: is-01m5wmh7vpm45bwrkkr7963679
parent_id: is-01m5wmghkt8vpnawbxzpbkm19e
created_at: 2026-10-26T17:36:03.690Z
updated_at: 2026-10-26T17:36:14.393Z
---
Write the owner's rule once rather than at four literals.

- One URL on the asset: `squaremath.org`.
- A credits line with room for both: the site first, then the repository, as
  `squaremath.org · github.com/jlevy/squares`.

`build_known_best_atlas` holds `SUMMARY_REPOSITORY` and builds three further strings from
it; `render_overview.SITE_URL` already holds the site. The pair belongs beside the other
print constants, with the separator and the order fixed there, and every drawn line and
retained description reading it. A test should fail a printed line that names the
repository without the site.

Depends on the survey (think-….1), since which lines are credits lines is its answer.
