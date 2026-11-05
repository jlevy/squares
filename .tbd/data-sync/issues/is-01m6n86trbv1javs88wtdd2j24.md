---
type: is
id: is-01m6n86trbv1javs88wtdd2j24
title: "Import Özden: s(94) >= 2493/250 by rescaling Hosono's mixed_n94_L995 onto a 4,972-direction net (#910)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: bold-ritchie-l49
labels:
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
child_order_hints:
  - is-01m6na15dgp4fwgm2d24mcwk2w
  - is-01m6na2ne3zs2jq13j0b5n3a7x
hold: null
hold_until: null
created_at: 2026-11-05T07:01:41.771Z
updated_at: 2026-11-05T07:34:22.402Z
started_at: 2026-11-05T07:01:46.219Z
---
Import of jlevy/squares#910 (opened 2026-11-05T06:51:55Z by kenaznia-doga, an AI agent account posting for Doğa Özden): s(94) >= 2493/250 = 9.972, above T-262's 1993/200 by 7/1000. An exact rescaling of Hiroaki Hosono's mixed_n94_L995 measure by 4986/4975 onto a declared net of 4,972 half-angles (step 1/12000), decided by the lab with this repository's unmodified sqverify-fast; "not a new packing arrangement".

## Claim map
- Source: kenaznia-doga/s94-lower-bound-9972@7d21f9bdf707102dd4ebf47e52f81b502a01004d (one commit, 2026-11-05T06:51:31Z, 24 seconds before the issue). Certificate certificate/n94-L9972.json.gz (format M; L = 2493/250, B = 24872661/24875000, proof_net step 1/12000, last 4971; 853 orbits, mass 9399999/100000). Stated digests: .gz f59d4c95...360c (native input_sha256), JSON text d1df3bc6...951c; Hosono's candidate.json at wand125/square-packing-bounds@797bdf6e 64d81953...0667a, its retained gzip df3ae678...d27c; complete receipts .gz 041284d5...7a59 and JSONL 02906bb0...312a; 99/100 mutant .gz 2f72d2dd...1532; LICENSE.md 5b8e1449...a18da4c.
- Claims in the release: (1) s(94) >= 2493/250 [register: a new lower-bound entry; T-262 keeps its claim, superseded at n = 94 once adopted]; (2) native sqverify-fast receipts (crate source d97758bb, rustc 1.98.0, release) VERIFIED at all 4,972 directions, assembled from six disjoint-selected native streams A-F, least certified bound 1.0000000000003892 at r = 3663; (3) a two-direction 99/100 mass control refused natively at r = 0 and 1198 with an exact witness at 1198 capturing 0.991109005346039... (not a whole-net control); (4) the lab's exploratory C checker at all 4,972 directions (not interval arithmetic; supplementary, not offered as evidence); (5) answers to #890's review notes F3-F5 (the quadrant via the D4 symmetry; growth m_old(t) - m_new(t)/lambda, not rho(1 - 1/lambda); the n = 31 aside not reused) and to #890's second question (the route ceiling 99500/9977 stays; no claim for the 49,707-direction 9.97285 partial).
- Consequence: s(95) >= s(94) settles nothing (n = 95 and 96 are proved = 10, T-191).
- Who else holds the value: nobody; the record's best at n = 94 is 1993/200 (T-262, V3/C3), verified and reported.
- Credit: Doğa Özden after Hiroaki Hosono, Tokoharu and this project (T-262's form). AI assistance as given: AI agents in Özden's lab (Claude and OpenAI Codex agents) constructed and rescaled the certificate, ran the checks, audited the receipts and prepared the submission under his direction.
- Licence: LICENSE.md, byte-identical to the declaration #890's packet retains (blob 9803370f): CC BY 4.0 for certificates, witnesses, receipts, data and write-ups; MIT for the lab's code. Hosono's MIT notice and the crate's own licence retained.

## Validation plan (priced)
- Replay: this repository's sqverify-fast (reviewed source d97758bb) through devtools.sqverify_fast_census over all 4,972 declared-net directions, then the whole-net control (--control). Priced on the validation bead under this one.
- Review: a separately prompted stage 4 mathematical review (tbd-strong-max), briefed on its own bead under this one.

Answer bead: this bead.
