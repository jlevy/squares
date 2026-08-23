---
type: is
id: is-01m0r8an6kbyaqpwkwtx78jdyd
title: "Correct two overstated claims in shipped docstrings: closed-form recognition, and closest_pair"
kind: task
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-23T21:27:19.507Z
updated_at: 2026-08-23T21:27:19.507Z
---
Both raised by the PR #15 review (F-16, F-20) and both conceded after re-checking. These are documentation defects in code that is otherwise fine, so the fix is prose plus a narrowed contract -- not new machinery.

1. sqpack/closed_form.py claims oracle status from a coincidence argument: a bounded search space of ~3.1e5 candidates gives ~3e-6 at 1e-11 tolerance. The arithmetic is right; the inference is not. Optimizer outputs are NOT uniform random reals -- they concentrate on low-height algebraic numbers, which is exactly why the recogniser works. The defensible claim is that a match is supporting evidence of arrival at a structured point. It is not evidence of local optimality and it does not exclude a censored point. Rewrite the module docstring accordingly and stop calling it an oracle anywhere.

2. sqpack/atlas.py:23 says two basins closer than the 1e-11 floor are "not currently distinguishable". D-021 bounds error in the SCALAR SIDE; it says nothing about distance between configurations. The review refutes this with our own data: the n=5 golden holds two rows at an identical serialized side. Rename the field to closest_side_gap, describe it as a descriptive statistic with no identity authority, and fix the same inference in atlas/atlas.schema.yaml and in canonical.py's quantum justification.
