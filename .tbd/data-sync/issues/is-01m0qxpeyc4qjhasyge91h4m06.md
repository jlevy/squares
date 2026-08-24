---
type: is
id: is-01m0qxpeyc4qjhasyge91h4m06
title: Synthesize unavoidable-set lower bounds by cutting planes
kind: feature
status: open
priority: 1
version: 4
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - pr-14
  - creative-alternative
  - focus-insight
dependencies:
  - type: blocks
    target: is-01m0qxpf8pe8qze02qp1nrz58x
parent_id: is-01m0r7q4h688g8gx54wk0vmrhp
created_at: 2026-08-23T18:21:31.979Z
updated_at: 2026-08-24T03:05:22.498Z
---
Category: creative alternatives. Turn lower-bound discovery into a master-separation loop: a master LP or MIP selects points or fractional weights; a separation oracle finds a unit-square pose avoiding them; interval global optimization certifies when no violating pose remains. Preserve the dual as the candidate proof certificate.

Acceptance: the falsifier reproduces the Stromquist ten-point escape and the twelve-point no-escape control; the certified lane machine-checks at least one published n = 10, 13, 22, 33 or 46 lower bound; generated point sets and dual weights are independently replayable; and the first new target is n = 12 or a restricted m^2-3 case. Reconcile with think-yrvm, think-28sq, think-72gr, and think-dsef.

## Notes

H-034 separates continuous fractional piercing from integral points and requires two-sided discretization certification; H-039 carries the checked s(12) CEGIS target behind source-faithful H-010.
