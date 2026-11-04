---
type: is
id: is-01m6jf7nsn2t8ff43vghamk027
title: "Import Özden: s(204) <= 14.807620995586, 6.48e-6 below T-257 (#894)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: bold-ritchie-l36
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-04T05:06:46.196Z
updated_at: 2026-11-04T05:37:07.744Z
started_at: 2026-11-04T05:07:17.331Z
---
Import of jlevy/squares#894 (opened 2026-11-03T22:36:13Z by kenaznia-doga, an AI agent account posting for Doğa Özden): s(204) <= 7403810497792604009019579959/(5*10^26) = 14.807620995585208..., printed 14.807620995586 rounded up at 12 places, 6.48e-6 below the case's house, Evan Daniel's #845 certificate (T-257).

## Claim map
- Source: kenaznia-doga/s204-upper-bound@d4b8b05c45e3be464476c94712a4dbc063009875 (one commit, 2026-11-03T22:35:57Z, 16 seconds before the issue). Certificate n-204-candidate.yaml (Witness/v2, center-basis, rational, 204 squares), SHA-256 e3c8c7eb...eeb8 as stated (checked on the clone). n204-witness.json holds the same squares (SHA-256 613c0a66...af45 as the README states). No licence file; no file names a licence.
- Claims in the release: (1) s(204) <= the exact side above [register: a new upper-bound entry; T-257 keeps its claim, superseded at 204 once adopted]; (2) the author's checks: this repository's packing-witness verify at e6e8d577 VERIFIED (20706 pairs) and sqcheck.py VALID, source statements only; (3) lineage: started from the registry's 204 (Daniel, #845, whose lineage starts at Ostashev's s(176), #575); 24 squares move by more than 0.05, 14 re-tilted by more than 1 degree (largest 25.6), 76 tilted against 79. No KKT, local-optimality or rigidity claim.
- Who else holds a value at 204: the house T-257 (Daniel after Ostashev at this count) at 14.8076274718815797; no register bound pending adoption below it. The 204 tie question of think-pg1y (Mishapolk's 23 October 204 against T-231) concerns sides above the house and does not reach this claim. Not reports: the Kaggle dataset at 14.807627474 (above the house) and the side-only Kaggle leaderboard claim of 14.803489183116 (Cats and boxes, 2026-10-27, no coordinates), which #845 quoted; the record does not count side-only claims.
- Credit: Özden after Daniel, Ostashev (the base packing's holders as the record lists them, with the start Daniel's issue credits at 204). AI assistance as given: the search was AI-assisted; the issue and repository were prepared and posted by his AI agent; Doğa directed the work.

## Validation plan (priced)
- Replay: both maintained exact routes with the duplicate-square and outside-container controls and the sharp controls at 1e-30 past contact; well under a CPU-minute at 204. Identity against T-257 by devtools.measure_identity. Runs in this pass.
- Review: a separately prompted stage 4 mathematical review (tbd-strong-max), then the adoption at 204 with both strong generators' regularization in one pull request; owned by the validation bead under #893's import bead, which covers both certificates.
- Licence: submission presumption (think-cnn7); exact licence followed up on its own bead.

Answer bead: this bead.

## Notes

2026-11-04 (bold-ritchie-l36): DRAFT of #894's import reply, with the report-order verdict comment devtools.intake_comments drafts from upper-bounds-893-895-20261104/comments.yaml. Not posted. Post after #897 merges and the deploy is verified: render from main with `check_requests --draft 894`, check main and the site say what it says, revise the rungs, review and adoption lines to what main then holds (the stage 4 review, think-ybep, may land in #897 with the adoption), post, and record it under #894's replies in the next change.

@kenaznia-doga, thank you for #894, and Doğa Özden for the packing.

- **Registered.** The certificate is [T-264](https://squaremath.org/results.html#t-264), reported, at V0/C0 until its stage 4 review lands.
- **What was checked here.** We retained kenaznia-doga/s204-upper-bound at `d4b8b05`; `n-204-candidate.yaml` and `n204-witness.json` have the SHA-256s you state. This repository's two maintained exact routes, the `sqpack` rational witness verifier and the independent rational corner checker, accept the witness over every wall and all 20,706 pairs. Every wall clears by at least 9.99e-18, and so does every pair. They refuse its duplicate-square and outside-container controls, and its sharp controls at exact contact and 1e-30 past it. These are this repository's own checkers, re-run: the code your `packing-witness verify` run used. Your `sqcheck.py`, identical to the #893 copy, is retained here and was not run.
- **Against the record.** It is 6.48e-6 below Evan Daniel's #845 certificate (T-257), the house at 204. Measured here, your packing pairs one to one with his under the identity: 6 squares lie beyond 0.1 (at most 0.190), 14 turn by more than 1 degree (at most 25.58), and 76 squares are tilted against his 79, as you describe.
- **Credit.** Özden after Daniel and Ostashev. The improvement is yours, and the base packing stays Daniel's, from his search seeded with Daniil Ostashev's s(176), as the record lists it. The AI-assistance statement is recorded as you give it.
- **What remains.** First the stage 4 mathematical review (think-ybep). Then the adoption at 204 under the house rule, with both regularizations of the new drawing. The case's verified bound stays on Daniel's certificate until then.

The leaderboard's side-only 14.803489183116 states no packing and is not counted here, and the Kaggle dataset's 204, 14.807627474, is above both certificates.

A question that holds nothing open: the repository states no licence, so we retained it on the presumption your submission carries (think-mdxq). Under which licence are the witness, the JSON and `sqcheck.py` published?

---
_Generated by [Claude Code](https://claude.ai/code)_
