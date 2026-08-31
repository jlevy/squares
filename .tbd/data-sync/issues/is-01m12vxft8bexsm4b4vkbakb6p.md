---
type: is
id: is-01m12vxft8bexsm4b4vkbakb6p
title: "n=29: eliminate the retained six-equation system for an exact side"
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T00:22:03.847Z
updated_at: 2026-08-28T01:26:23.417Z
---
resources/papers/kingbird-square-29-provenance.svg retains Ellsworth's full construction: six defining equations f1..f6 in six unknowns (s,a,b,c,d,i), solved at line 24 with FindRoot at WorkingPrecision 200 -- numerically, never eliminated, so no degree was ever published. cases/kingbird29/verify_svg.py replays the equations numerically only.

This is the one missing-degree case that is neither a transcription omission nor a dead end: the complete specification is in the repository and a Groebner/resultant elimination would yield the minimal polynomial without any new source. Note that integer-relation recovery cannot substitute: a PSLQ scan over the retained 99-digit side finds nothing, but the same scan also fails on n=51 whose degree-12 polynomial we already hold, so the negative carries no information. Witness sides run 45-99 digits, far short of the ~1500+ that the degree-42/44 neighbourhood would need.
