---
type: is
id: is-01m14m52h6braaheedkwcesgcc
title: "Change-scoped verification: check what the change can reach, not everything"
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-08-28T16:44:52.645Z
updated_at: 2026-08-28T16:44:52.645Z
---
D-355. packing-validate has no mapping from a changed path to the steps that change can affect, so the full gate becomes the reflex after every edit. Measured 2026-08-28: a two-file rigidity-assessor edit was verified with a 979.79s full gate; the two steps it can affect run in 12.06s together, an 82x overrun. Build a change-scoped selector that is conservative by construction (unrecognized path selects the full gate, never an empty set) and negative-controlled (perturb a source, the selector must pick a step that fails on it). The full gate keeps its role at commit and merge boundaries; this changes the edit loop, not the contract. Efficiency may simplify process but never weaken assurance, so this must preserve coverage, not trade it.
