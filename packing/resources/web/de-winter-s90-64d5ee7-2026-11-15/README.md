# Joost de Winter’s Superseded s(90) Certificate at 64d5ee7

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/64d5ee762a1159248d375973fb33825d51da637d)
at `64d5ee762a1159248d375973fb33825d51da637d` (committed 2026-11-15T11:27:26Z), which
[issue #996](https://github.com/jlevy/squares/issues/996) names (opened at 11:30:13Z).
The author superseded it in [issue #997](https://github.com/jlevy/squares/issues/997)
(12:08:33Z) by the certificate at `fa53fb0`, 9.09 × 10⁻⁸ smaller, asking that `fa53fb0`
be pinned and this commit disregarded.
The [fa53fb0 packet](../de-winter-s90-upper-bound-2026-11-15/README.md) retains the
replacement, which the record registers as T-304; nothing registers this certificate.
This packet keeps it as history and for the measurements against it, which the fa53fb0
packet makes.

Intake lane L181 (think-32cl) fetched the repository at 12:01Z, when its head was
`9cafa33`, and retained this packet then.
The next commit, `0c9bcd2` (11:27:49Z), adds `n90/REGISTRATION.md` and `n90/SHA256SUMS`;
`9cafa33` (11:29:27Z) renames the model named for the local search from “OpenAI Codex
(GPT-6 Astra)” to “GPT-6.1 Sol Max (OpenAI)”, the name the issue gives.
Neither changes the certificate, and `SHA256SUMS` at `9cafa33` states the digests of the
seven other files of `n90/` at this pin, which match.

## What It States

- `n90/n90_exact.json`: 90 unit squares as `[center_x, center_y, cos, sin]` rows of
  exact rationals with the side 199880777150913904183/20000000000000000000 =
  9.99403885754569520915, which #996 rounds up at 12 places, 9.994038857546, 4.2383 ×
  10⁻³ below T-303, jazivxt’s packing and the house at 90. `n90/n90_witness.yaml`: the
  same packing as a corner Witness/v2, its corners listed from the vertex opposite the
  one this repository’s corner reader starts from.
- The construction, the local optimum, the Kaggle note, the checkers, the credit and the
  AI assistance are as the fa53fb0 packet’s README gives them from #997, except that
  this README counted 49 leaning squares in T-303 and 37 here, named seven squares in
  the upper left with a new angle and five along the left wall made axis-aligned, and
  gave a smallest gap of 10⁻¹²; #996 says each of the author’s checkers reports 202
  close pairs.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json): the licence, the root
README and the whole of `n90/`, 9 files, 6 retained under [source/](source/) and 3
pinned by digest (`LICENSE`, against the copy the
[227, 229 and 260 packet](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)
retains, and the two figures).
`verify_exact.py` and `check_area.py` are retained as data and never opened or run here;
the fa53fb0 packet pins its identical copies against these.
Everything here is published under the MIT licence, copyright (c) 2026 Joost de Winter,
by `LICENSE` at the pin.

## What Was Checked Before the Replacement

Before #997 was read, lane L181 replayed this certificate under the packet name the
fa53fb0 packet now carries, with 3 gross and 11 sharp controls stated in a plan hashed
at 12:03:58Z (SHA-256 `b441e936…c7ea3`, recorded on the bead), and committed the
receipts at 12:17Z. Both maintained exact routes accepted it through
`center-direction-json` and refused both gross controls; all 11 sharp controls came out
as stated, the branch for a touching square taken.
Squares touch the left or bottom wall exactly; the right and top clearance is
9909955765625015940074994030630443123/1953125000000000000000004987507812500000000000000000000000,
about 5.07 × 10⁻²¹; the least pair gap is about 1.0641 × 10⁻¹², squares 2 and 40.
T-303’s contraction margin, 1.0988 × 10⁻¹¹, is about 3.9 × 10⁸ times smaller than the
gain, and this certificate’s own is 9.533 × 10⁻¹² (squares 2 and 40). Against T-303 it
is the same arrangement moved by a local search: under the identity 6 squares move
beyond a tenth (largest 0.646), and each of its 40 tilted squares pairs with one T-303
tilts the same way. The L step carries it nowhere.
Those receipts left the record with the replacement; the fa53fb0 packet’s receipts
replace them, and the history of this branch keeps them.

## Stage 4 Review

The stage 4 review of 15 November 2026
([review-2026-11-15-de-winter-996.md](../../../../docs/project/reviews/review-2026-11-15-de-winter-996.md),
lane L180, under think-uhav), written blind to the import lane, reviewed this
certificate and accepted it, with thirteen findings, all notes, and 26 of 26 controls as
stated. The import lane read its frozen findings at 12:39Z, after its replay, controls,
measurements (12:17Z) and registration (12:38Z) were committed, and its final head at
12:43Z, before #997 was read.

Read against the replay’s receipts, the review’s least pair margin (1.06410355706 ×
10⁻¹², squares 2 and 40) was the replay’s exactly.
Its 18 wall contacts, nine at the left and nine at the bottom, square 10 among them,
were the replay’s, and its right and top clearance was the amount the sharp controls
lowered the side by.
Its twin, listed from C + (u + v)/2, its tilts (50 squares 1.831 × 10⁻¹⁰ degrees
clockwise of upright, 40 turned 22.90 to 30.99 degrees), its contraction margins and its
identity against T-303 (89, 34 and 6 squares beyond a thousandth, a hundredth and a
tenth, largest 0.646, 16 turned beyond a degree) were the replay’s measurements.
No disagreement.

Its findings that outlive the replacement: the corner adapter’s refusal of the twin
(F11), which the readers `witness-corners` and `witness-corners-opposite` now answer;
the JSON naming neither the box nor the rotation sense (F7); the counts of leaning
squares (F6, F10), which the author corrected at `fa53fb0` to 44 and 40; and the AI
named at the pin (F12). Its addendum (lane L182) ran the frozen checker and controls on
the fa53fb0 certificate and accepts it; the fa53fb0 packet’s README reconciles it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
