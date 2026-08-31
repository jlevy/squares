---
type: is
id: is-01m136kmh8k5cr6vexcf5wr227
title: "Registry: n=29 verified bound is stale in three prose sites"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - packing
dependencies: []
parent_id: is-01m136khr29m0p8t6q8kybd562
created_at: 2026-08-28T03:28:55.326Z
updated_at: 2026-08-28T03:46:17.496Z
closed_at: 2026-08-28T03:46:17.494Z
close_reason: "Landed in PR #51 (squashed to main)."
resolution: null
duplicate_of: null
---
README.md:513, frontier/n-029.md:86 (blocker detail) and frontier/n-029.md:129 state s(29) <= 5.93388579986236485799813026, but frontier/n-029.md:44-45 frontmatter and witnesses/schadt-n029-2025-rational.yaml say 5.93388579981302587863645209. Difference is 4.9339e-11, exactly the Schadt relaxation that session 032 tightened, so these are the pre-tightening value and the tightening never propagated to prose. frontier/n-029.md now contradicts its own frontmatter. NOT a defect: the two occurrences in tests/test_frontier_assurance_contract.py:291,303 are synthetic inputs unit-testing compact_bound/same_bound, not registry assertions.
