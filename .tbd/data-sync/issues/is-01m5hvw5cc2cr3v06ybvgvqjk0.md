---
type: is
id: is-01m5hvw5cc2cr3v06ybvgvqjk0
title: "Import chelokot and Evan Daniel: Lean proofs that s(5) = 2 + 1/√2, and s(2) = s(3) = s(4) = 2 (no issue)"
kind: task
status: in_progress
priority: 3
version: 2
delegate: c-lean-1023
labels:
  - result-import
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-22T13:12:44.171Z
updated_at: 2026-10-23T06:19:01.857Z
started_at: 2026-10-23T06:19:01.857Z
---
Stage 1 triage, read-only, by c-triage-1022b from the 12:20Z sweep of 22 October 2026, at
`main` `76496462b`. No issue reports either.

**The record today** (verified):

- `n-005.md`'s verified lower bound rests on `E-n005-gobel-proof`. Its Verification Code
  table lists it as "a published proof, no code".
- No register entry exists for s(2) to s(5). T-154 (s(17)) is the one `formalization`
  entry.

**chelokot, first** (chelokot/square-packing-archive, Apache-2.0).

- `formal/SquarePackingArchive/Records/Square5.lean` proves:
  - `s5_le_goebel : HasPacking 5 (2 + √2/2)`;
  - `s5_ge_goebel : IsLowerBound 5 (2 + √2/2)`, by Friedman's four-point set;
  - `s5_eq_goebel : IsMinimumSide 5 (2 + √2/2)`.
- First committed at `4f4ece1`, 2026-08-29T18:39:38Z.
- `4f4ece1` is an ancestor of `753079eb`. The `chelokot-nagamochi-counterexample-2026-09-05`
  packet pins that commit, and this repository built its tree on 2026-10-02 for T-086
  (`devtools.replay_chelokot_lean`). Axioms were printed for `squareMinusTwo` only, never
  for `s5_eq_goebel`.
- **The sweep does not watch this repository.** The packet has no acquisition record and
  no register source gives its URL.
- The head `e1e9ef5` is 34 commits past `753079eb` (4 to 7 October). They prove s(1..9),
  including s(5) and s(6) ≥ 3, in Bend as well (subjects read, not the proofs).

**Evan Daniel, second route** (evand/square-packing, read through `7051f4e`).

- `lean/Sqpack/Rect5Pts.lean`, `e96ab69` (2026-10-21T20:10:45Z): `rect5_pts_lower`, for
  `2 ≤ a, b < 2√2` and `a + b < 4 + √2`, proves `¬ RectPacks 5 a b`. At a = b this is
  s(5) ≥ 2 + 1/√2, by four unavoidable points.
- `rect2_iff`, `rect3_iff` and `rect4_iff` (`74937b0`, `b7d9b1b`, `ee4d2cc`) give, at
  w = h, s(2) = s(3) = s(4) = 2.
- "Standard axioms only", per the source. `lean/Axioms.lean` lists `#print axioms`.
- The full `rect5_iff` (`5a82f28`) also rests on generated strip certificates that the
  square case does not need.
- Rectangles themselves are outside this record.

**Stage 1 steps.**

1. **Pin both sources.**
   - chelokot at `753079eb`, or at `e1e9ef5` if the Bend proofs are taken in too.
   - evand at `7051f4e`.
2. **Claim map.** One `formalization` entry at n = 5, with s(2) to s(4) in its scope.
   - chelokot is credited first (29 August).
   - Evan Daniel's is a second machine route, as T-084 and T-086 carry chelokot's.
   - Novelty: `previously-published` for the values (Göbel 1979; Friedman DS7).
   - Draft significance: S2.
3. **Price.**
   - Two kernel axiom receipts: `#print axioms s5_eq_goebel` on chelokot's pinned
     toolchain, and `rect5_pts_lower` plus `rect2_iff` to `rect4_iff` on evand's
     `lean/`. Mathlib's cache is used, and only the modules these import are built.
   - Two statement-binding reads: `IsMinimumSide`, and `RectPacks` at w = h, against the
     record's closed unit squares with disjoint interiors.
   - Under 1 CPU-hour, plus one W2 review lane.
4. **Retain.**
   - chelokot's `Records/Square5.lean` and the files it imports, with the licence, and
     an acquisition record, which makes the repository watched.
   - evand's `Rect.lean`, `RectChain.lean`, `Rect5Pts.lean`, `Rect3.lean`, `Rect4*.lean`,
     `Axioms.lean`, the note `literature/s5-proofs-2026-10-21.md`, LICENSE and CREDITS.
5. **Watch.** Add a read of chelokot's head to `intake-watch.yaml`, or add a register
   source with its URL, so the sweep watches the repository.

S2, so no tracking issue is required.

blocked_on: none
