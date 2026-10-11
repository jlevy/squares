---
type: is
id: is-01m3xhkkyewysj9dz2wb8tk6w8
title: "W2: review T-007 against Karakuş 2026's counterexample to Nagamochi's Lemma 1 (s(k^2-2) = k and the 238 Nagamochi floors)"
kind: task
status: closed
priority: 1
version: 3
labels:
  - research
dependencies: []
parent_id: is-01m3xgkna3m3w1w50ky6gqyxyk
created_at: 2026-10-02T05:32:47.950Z
updated_at: 2026-10-02T07:12:52.933Z
closed_at: 2026-10-02T07:12:52.933Z
close_reason: "W2 review concluded: docs/project/reviews/review-2026-10-02-nagamochi-lemma1-karakus.md. Lemma 1 false for every a > 3, b > 2 (Karakuš's K_t, verified exactly by devtools.check_nagamochi_lemma1_counterexample, 35 tests); the gap reaches T-007 for every N >= 10; Karakuš Theorem 1.1 re-derived with no gap found, giving s(k^2-1) = k and a strictly weaker general floor; s(k^2-2) = k rests on chelokot's unreplayed Lean proof. Consumer inventory: devtools.audit_t007_consumers (287 records cite the bound; 224 beyond T-007's registered scope). Register changes are think-xucp; the Lean replay is think-ym34. No register value was changed."
resolution: null
duplicate_of: null
---
Found by the X-049 literature lane (think-zfxi) and verified by the coordinator on 2026-10-02 at https://arxiv.org/abs/2609.37410: H. Karakuş, 'A counterexample to Nagamochi's scoring lemma and a new rectangle packing bound' (29 Sep 2026). The abstract states that counterexamples to the scoring assertion in Nagamochi 2005 Lemma 1 show the published proof of the rectangle bound is incomplete, 'but do not disprove the bound itself'; an independent strip-measure proof recovers s(k^2-1) = k for every k >= 2 and 'does not establish Nagamochi's full rectangle bound or the identity s(k^2-2) = k'. chelokot's Lean archive reportedly also has a counterexample and re-proves s(n^2-2) = n for square containers (reported in the evand s12 literature note; unchecked here; docs/project/reviews/review-2026-09-27-evand-s32-s12.md section 5 records it as unchecked).

Why it matters: T-007 (V3/C1) is the register's most load-bearing external argument. Nagamochi's closed form is the verified lower bound at 238 of 261 open cases (packing/frontier/README.md), and the k^2-2 exact values rest on it. Scope: archive the preprint (three-format discipline) and the chelokot note; decide whether the Lemma 1 gap reaches Theorem 2 as T-007 states it; for each consumer of T-007 (the 238 floors, every s(k^2-2) = k case, the k^2-1 cases now independently re-proved), record whether an independent proof exists (Karakuş for k^2-1, chelokot reported for k^2-2, case certificates in the register) and what the epistemic rung becomes. Do not change any register value before the review concludes.
