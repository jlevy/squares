---
type: is
id: is-01m70ga5pgpeaz5emqpaqrabqb
title: "Import #935, #936: Doğa Özden's s(172) and s(270) upper bounds (kenaznia-doga, 9 November)"
kind: task
status: in_progress
priority: 1
version: 7
delegate: bold-ritchie-l71
labels:
  - intake
  - result-import
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-11-09T15:54:58.640Z
updated_at: 2026-11-09T19:18:36.137Z
started_at: 2026-11-09T15:55:06.608Z
---
#935 s(172) <= 13.614689853287 (kenaznia-doga/s172-upper-bound @ 2ce1f7c7, n-172-candidate.yaml sha256 0df5ae79...), 3.246e-3 below T-257; #936 s(270) <= 16.928148603343 (s270-upper-bound @ 78ab8cec, sha256 f2b62bf0...), 1.365e-5 below T-224. Both opened 2026-11-09T15:28Z, promoted with packing-witness promote --strategy robust-rational @ ef1af493; repos carry LICENSE.md (CC BY 4.0 / MIT) and Daniel's MIT notice. Precedent: #927-#931 (think-463r, PR #932).

## Notes

L71 (bold-ritchie-l71), 2026-11-09. PR #937 (draft, labels intake, S3), branch claude/bold-ritchie-xo28us-l71.

Done:
- Packets ozden-s{172,270}-upper-bound-2026-11-09 retained at 2ce1f7c and 78ab8ce (decimal poses retained; diff PNG, verifier README, sqcheck.py and Daniel's LICENSE pinned identical_to earlier copies). Digests match.
- Replay on both maintained routes + gross and 22 sharp controls: all as stated. Pair gaps 2.008e-13 / 2.016e-13; walls touch.
- Identity: 172 further arrangement of T-257 (15 beyond 0.1; nearest centres miss one to one by one shared centre); 270 one to one with T-224 (1 beyond 0.1, square 59 straightens from -32.3 deg).
- Contraction: house margins 1.36e-19 (T-257) and 1.69e-19 (T-224); gains 2.4e16 and 8.1e13 times; own margins 2.53e-12 / 3.21e-12. Receipts retained with main's module.
- Ledger upper-bounds-935-936-20261109 records both.
- L72's review (think-qqyg) cherry-picked (07bc1fc20, 133a73572, 7f4301070 -> 4e7306cb0, a33361561, 6065a6bf9) and mapped: V-ozden-935-936-review-check, E-ozden-935/936-review-exact-feasibility, reviews items; T-282 S3, T-283 S2 (borderline). F15 fixed; F4/F5/F12/F13 noted.
- Merged main 20f844dbf (#934, T-280/T-281) at 355b81085.
- Adopted 172 (T-282 from T-257) and 270 (T-283 from T-224), LATER_PASSES 2026-11-09. Regularization: 172 Evan Daniel's view drawn; 270 decided-no-better (SETTLED), axis tool refuses it (new SLIDE_DIGITS guard: its slide limits pass 4,300 digits). Solves 2.63e-12 / 3.25e-12 below held at row 3 -> new bead think-wju3.
- Derived: rigidity screen and blocks, SCREEN_FINDINGS, bound citations, composite, X049 censuses, custody receipt, closed form, exact-side register, case verifier sections, research tables, certificate reach, URL registry, PRINT_CREDIT_HELD, credit curation, workflow sparse checkout, t-180 page budget, KNOWN_TILTS for 270.
- Three no-public-change records; DATA_REVISION re-pinned to e570f7ab.
- Local: --records and --edit pass at b94cc8f61. Hosted CI on b94cc8f61 failed overview (t-180 budget) and suite-d (refused-tilts), fixed in e267c0fb8.

Owed after merge: replies on #935/#936; follow-ups on #845 (T-257 named current) and #703 (T-224 reported house).

Final (19:40Z): head 75c9570e0; hosted packing-required and pages-required green, every job that ran green. Local --records passes at 75c9570e0, --edit 71/71 at b94cc8f61. PR #937 body updated (cost about 3 CPU-hours plus L72 about 0.2). Follow-up bead think-wju3 (solves held at row 3; draws 270 regularized if registered). Scratch cleaned.
