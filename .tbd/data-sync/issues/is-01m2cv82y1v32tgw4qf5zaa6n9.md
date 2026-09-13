---
type: is
id: is-01m2cv82y1v32tgw4qf5zaa6n9
title: "PR #157 review READ-02 (High): additive weighted record lets older readers erase counts"
kind: bug
status: closed
priority: 1
version: 2
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:28.673Z
updated_at: 2026-09-13T08:41:10.341Z
closed_at: 2026-09-13T08:41:10.340Z
close_reason: "Fixed on both sides, and the finding's LITERAL claim is rebutted. Production side (e6b954cb): weighted atoms serialise as {variant, weighted_points, threshold, weight} with no points key, so a reader predating token counts fails on a missing required field instead of admitting the lighter atom; all-ones atoms keep the legacy shape byte for byte. Standalone side: measured at the reviewed head, load_certificate did NOT read the new shape as its lighter all-ones self -- it already raised TypeError 'each threshold atom must be an object with a points array', because removing points rather than extending it is exactly what e6b954cb bought. What WAS genuinely accepted: the withdrawn additive spelling beside points (320 atoms, read as all-ones) and a bare variant tag beside points (tag ignored). Both are refused by name now. The prior refusal was also only incidental -- a complaint about a malformed array, not a statement that this reader cannot price tokens. Went past the three named spellings: THRESHOLD_ATOM_KEYS (line 66) plus refuse_unreadable_threshold_atom (line 149) refuse ANY unrecognised field on a threshold atom, because a reader that skips what it does not know is precisely how the additive spelling got through. Refusal rather than token pricing, for three reasons: the verifier prices per distinct point throughout (budget w floor(|S|/k), one rectangle per point, expansion over |S| indices); no retained claim contains a weighted atom (all 320 threshold atoms in all three certificates are 2-of-3 all-ones) so a parsing path would never run; and unexercised verification code in the one file whose value is third-party readability is worse than a refusal. Still imports only the standard library, asserted by test_the_refusal_is_implemented_locally_and_imports_no_repository_code, which I verified independently. Historical decoding unchanged, measured twice: full sweep of certificate.json (181 directions, 1,044,374,137 cells) gives md5 e0d17eb767cb678d97d9005177d17d5e before and after with identical least charge and witness, and the slow interval-route replay of the same retained bytes also passes."
resolution: null
duplicate_of: null
---
packing/src/sqpack/fractional/threshold.py:259-271 preserves all old required fields and only adds keys, so the actual base revision decoder silently returns the lighter atom. packing/cases/n11_threshold_certificate/verify_claim.py:179-201 also ignores the new fields. Fix per the review repair format: weighted atoms become structurally incompatible with the legacy points shape. Preserve all-ones legacy output; retain explicit refusals at current admission/publication readers; test the historical decoding shape and the current standalone parser.
