---
type: is
id: is-01m1wwwnma811qb4fkntj3y972
title: Add the [Burns--Massaccesi n17] resource to the n = 17--19 case files and settle their reported lane
kind: task
status: open
priority: 3
version: 1
labels:
  - n17
  - frontier
dependencies: []
parent_id: is-01m1wwrjmnkeq6xgkwcz4ha3zs
created_at: 2026-09-07T02:59:20.842Z
updated_at: 2026-09-07T02:59:20.842Z
---
BC-151 (docs/project/reviews/review-2026-09-03-bc151-4-5058-adoption-independent-review.md, 'Discretion exercised') left reported_lower_bound at Nagamochi for n = 17, 18, 19 because the cases' named source sets do not include the blog posts, and called adding the [Burns--Massaccesi n17] resource plus a coverage entry 'a separate, reversible edit'. That edit has not happened: n-017.md, n-018.md and n-019.md carry no Burns or Massaccesi resource, and source-coverage.yaml / source-availability.yaml have no entry, while the evidence entries E-n017-massaccesi-source-replay and E-n017-fractional-certificate cite that source key. Decide the reported lane (the frontier README says it holds the strongest literal claims in the named source set) and make the resource, coverage and any reported-lane change in one reversible commit, regenerating STATUS/RESULTS/INVENTORY.
