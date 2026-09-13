---
type: is
id: is-01m2bmgwstxv2rcj2xpte71d2k
title: "One word, two quantities: 'size' means tokens in receipts and sites in the model"
kind: bug
status: in_progress
priority: 3
version: 4
delegate: verifier_review
labels:
  - n11
  - research-tooling
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-12T20:21:42.842Z
updated_at: 2026-09-13T07:48:10.003Z
---
devtools/plateau_reader.py's AtomVerdict.record() writes 'size': sum of multiplicities -- the TOKEN total -- while sqpack.fractional.threshold.ThresholdAtom.size is the distinct-SITE count. Every retained receipt under agenda-034 therefore says 'size': 7 for a five-site atom. Two live modules use one word for two quantities that differ exactly when an atom is weighted, which is the confusion the weighted-atom admission exists to separate; devtools/replay_weighted_atom_source.py has to carry a comment explaining which one it is comparing against. The new orbit-admission receipt reports support_size and token_count separately, which is the naming to converge on. Renaming the retained receipts is not an option -- archived evidence is never edited -- so the fix is in the producer plus a note wherever a reader consumes the old key.
