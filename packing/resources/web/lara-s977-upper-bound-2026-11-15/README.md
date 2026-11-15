# Miguel Lara’s s(977) Construction at 26d5695

This packet retains
[larasmiguel/square-s977](https://github.com/larasmiguel/square-s977/tree/26d5695abca2f8a005856e3c1ddc47171d661e9b)
at `26d5695abca2f8a005856e3c1ddc47171d661e9b` (committed 2026-11-15T06:24:28Z), the
repository’s `main` when it was fetched at 07:00Z on 15 November 2026, for
[issue #992](https://github.com/jlevy/squares/issues/992), opened by the account
`larasmiguel` at 06:03:49Z.
The issue names no commit and asks that the submission be pinned to the full commit once
it is made, so the packet pins the head.
Eight commits from `8b91a7e` (06:00:25Z) to `3e9b410` (06:00:38Z) each add one file, the
side first in `README.md`, 3 minutes 24 seconds before the issue.
Three commits after the issue, `4520fab`, `aa9a144` and `26d5695` (06:24:24Z to
06:24:28Z), add to `README.md`, `SUBMISSION.md` and the certificate a section
acknowledging Frits Göbel’s construction; the construction, the coordinates and the
checker are unchanged.
Every commit is the account’s.
This is the account’s first contribution to this repository: #992 is its only issue,
with no comment when read.

## What the Source Claims

- **The bound.** `certificates/n977_certificate.md` states s(977) ≤ 17 + 21/√2, about
  31.8492424049, below the 32 × 32 grid’s 32, by a construction in prose: 441 unit
  squares in a 21 × 21 array turned 45 degrees and centred in the container, whose union
  is the diamond |x − L/2| + |y − L/2| ≤ 21/√2 with L = 17 + 21/√2, and 536 axis-aligned
  squares in four corner staircases of 134.
  The bottom-left staircase has its lower-left corners at (c, r) for 0 ≤ r < 15 and 0 ≤ c
  < w_r, with w = 15, 15, 14, 13, …, 2, every cell inside x + y ≤ 17, where the diamond’s
  edge lies; the other three are its images under quarter turns about the centre.
  The certificate argues the disjointness: each staircase lies in x + y ≤ 17 at its corner
  and reaches at most 15 from it, while L/2 > 15.
  An upper bound only: no optimality claim.
- **The numerical artifacts.** `certificates/n977_coordinates.csv` lists the 977 centres
  and angles in IEEE-754 doubles at the relaxed side 31.85, not the claim’s;
  `verification/verify_977.py` reads it with Shapely, and
  `verification/n977_verification.json` records its output: nothing outside the 31.85
  container and no pair overlapping by more than an area of 10⁻¹¹, over 2,932 candidate
  pairs, under Python 3.13.5 and Shapely 2.1.2.
  The issue and the certificate call these numerical artifacts and one checker, not an
  exact certificate.
- **Lineage.** The issue, opened before the later commits, calls the side better than the
  grid’s and says the best published bound at 977 had not been established, and asks for
  credit to Miguel Lara for the construction, subject to priority checks.
  From `4520fab` on, the repository says the bound is not a new record: Göbel’s square
  (a, b) = (15, 21) packs 921 at 16 + 21/√2, an L-shaped border adds 2⌊16 + 21/√2⌋ + 1 =
  61 for 982 at 17 + 21/√2, and five fewer give 977, citing Göbel (1979) and Erich
  Friedman’s survey DS7; it asks that Miguel Lara be credited for this computational
  reconstruction, its coordinates, code, checking and documentation, and not as
  discoverer of the bound.
- **AI assistance.** The issue, `README.md` and `SUBMISSION.md` say OpenAI ChatGPT was
  used extensively for exploratory geometry, generating and debugging C++ and Python,
  writing the verification code and drafting the reasoning and documentation, with Miguel
  Lara directing the investigation and requesting independent checks.
  The record credits people, not AI agents
  ([attribution.md](../../../../attribution.md)), and states the assistance in the
  source’s words.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the whole tree, 8 files: 7 retained under [source/](source/) and 1 pinned.

| File | Bytes |
| --- | --- |
| `certificates/n977_certificate.md` | 4,370, the construction and its argument |
| `certificates/n977_coordinates.csv` | 65,629, the numerical squares at side 31.85 |
| `verification/verify_977.py`, `verification/n977_verification.json` | 2,852 and 501, the Shapely checker and its recorded output, as data |
| `README.md`, `SUBMISSION.md`, `requirements.txt` | 3,561, 3,025 and 16, the author’s notes and the checker’s one requirement |
| `visualization/n977.svg` | 193,282, pinned by digest: a drawing of the CSV that decides nothing |

[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
No source program ran here.

**Licence.** The repository states no licence: the tree has no `LICENSE`, and neither
`README.md` nor `SUBMISSION.md` states reuse terms.
The account submitted the source in #992, so the owner’s presumption of 24 October 2026
that a source its author submits may be retained and imported applies (think-cnn7), as
for #989’s packet; think-cszb is the follow-up, and the stage 7 reply asks the author.
The construction and the coordinates are factual data under the owner decision of
2026-10-09 as well.

## The Construction Decided Exactly

`devtools.construction_checker` cannot read this recipe: it tiles or borders a replayed
certificate with a rational side, and this side is irrational and builds on no
certificate. So `devtools.diamond_staircases` writes the certificate’s own statement as
a Witness/v2 over Q(√2), the minimal polynomial x² − 2 with its root in (1, 2), at side
17 + (21/2)√2: the 441 turned squares at the centres the certificate gives, (L/2 + (u −
v)√2/2, L/2 + (u + v)√2/2) for u, v from −10 to 10, with basis (√2/2, √2/2), then the
bottom-left staircase’s 134 cells by row and their three quarter turns.
Nothing is taken from the CSV.
`python -m devtools.diamond_staircases witness OUT.yaml` writes the file for
`packing-witness verify`.

Both maintained exact routes over a number field decided it on 15 November 2026,
`sqpack.witness.exact_verify` and `devtools.check_algebraic_witness_independent`, the
second sharing no field arithmetic, geometry or verification code with sqpack’s by its
own account ([receipts/exact-decision.json](receipts/exact-decision.json)).
Each accepts the construction with squares touching walls and each other exactly: 3,540
touching pairs on both routes, sqpack deciding all 476,776 pairs and the independent
route the 4,414 its sweep leaves, and sqpack’s least wall clearance and pair gap exactly
zero.

The controls were stated in a plan hashed before any run of the construction, at
07:05:48Z, its SHA-256 recorded on think-ud9e
(`7cbe1f461f002ed510f5ebc7f6d29975a8d6af25239bac00ca38db52cba0c891`); the plan is
retained byte for byte as
[receipts/controls-plan-n977.txt](receipts/controls-plan-n977.txt), and Git keeps it
from here.
Both routes refused each control as stated:

- **Gross.** The last square replaced by a copy of square 1 (overlap), and by an
  axis-aligned square at (15, 1), one cell past row 1 of the bottom-left staircase, whose
  corner lies inside the diamond (overlap).
- **Sharp.** The side lowered by 10⁻³⁰ with every square kept (container); the 441
  turned squares moved by (−10⁻³⁰, −10⁻³⁰), toward the staircase cells whose corners
  touch the diamond’s edge x + y = 17 (overlap); and square 1’s basis lengthened by
  10⁻⁵⁰ (shape; sqpack also names an overlap, its touching pairs falling from 3,540 to
  3,537).

The six decisions took 1,019 route CPU-seconds, almost all of it sqpack’s, which decides
every pair; `decide --write --jobs 2` wrote the receipt from 07:18Z to 07:28Z, and again
from 08:26Z to 08:34Z after the senior review (L176) took out of its Göbel section a key
that was true by construction, every decision unchanged; `decide --check` decides every
control again and compares it.
`tests/test_diamond_staircases.py` decides a 41-square recipe of the same shape with
every control and holds the receipt to its plan.
sqpack prints a small nonzero margin without its exponent (think-526p), so the receipt
keeps sqpack’s margins only as exact zeros and the independent route’s as it prints
them.

## Göbel’s Construction

`devtools.diamond_staircases` compares the side with Göbel’s families exactly
(`goebel` in the receipt):

- `devtools.goebel_construction` reads Göbel’s construction at 977 as 17 + 11√2, about
  32.556, the Göbel square (16, 22) of 1028, which is above the grid’s 32; the claim is
  √2/2 below it, so it is not marked above a classical construction, but that reading
  decides nothing at 977.
- The claim’s side is the Göbel square (15, 21) of 921, at 16 + (21/2)√2, with one
  L-border, which adds 2⌊16 + (21/2)√2⌋ + 1 = 61 for 982, as the source’s later commits
  say. Friedman’s DS7 states that L lemma beside Göbel’s family.
  The module applies no L-border, so it omits this side; whether L-border extensions of
  Göbel’s members join Göbel’s construction is think-7j3i’s question for the owner,
  beside think-zkxy and the 27 L-border extensions of Göbel’s squares that Francisco
  Couzo’s `23aff0c` index states, which the history walk holds; two of them, at 981 and
  982, are this side.
- The author’s own layout is not that one. It is the (16, 21) arrangement, outside the
  family’s condition a − 1 < (b/2)√2, since 15 > (21/2)√2, whose depth-16 staircases
  of 136 would meet end to end, with each cut to depth 15, 134 cells, so that neighbouring
  staircases clear: 441 + 4 × 134 = 977.

## The Record at 977

Not recorded. The [ledger of 15 November](../../../campaign/issue-intake/upper-bounds-992-20261115/README.md)
reads Francisco Couzo’s #763 certificate at 977 (couzo-issue763-2026-10-23),
31.765989508190, the count’s current row since 23 October, 8.33 × 10⁻² below the claim,
so by the report-order rule the claim is not recorded and takes no row.
Every report the record holds at 977, from Couzo’s packet of 14 October on, is below it.
No evidence entry is written, since no row or entry rests on this decision.

## The Stage 4 Review

The [stage 4 review of 15 November](../../../../docs/project/reviews/review-2026-11-15-lara-992.md)
(lane L174, think-u58c) was written blind in a separate lane, with its checker, controls
plan and findings frozen before it read the record; its programs and receipts are in
[lara-s977-992-review-2026-11-15/](../lara-s977-992-review-2026-11-15/README.md).
This lane committed and pushed its own determination, this packet, the exact decision,
the ledger and the requests entry, by 07:40Z, then read the review’s final head at 07:40Z
and merged it in the same minute.

It accepts the bound, nothing blocking, by two clean-room methods of its own, separating
axes in Z[√2] and exact clipping in GMP rationals, over all 476,776 pairs.
The two lanes agree: 3,540 touching pairs, as both routes here find, and 120 wall contacts
on 116 squares, which is sqpack’s 240 corner coordinates on the boundary, two to a
contact; its eight controls, like the six here, came out as stated.
It also finds what this lane did not check or did not measure:

- **981 fit** at the same side (F6, A981): each side’s outer row leaves L − 30 ≈ 1.849
  free between two staircases, below the diamond.
- **The (16, 21) arrangement** overlaps in exactly four pairs, the end cells of
  neighbouring staircases, and #992 is it less those eight cells, square for square
  (F10, G985); the L-bordered Göbel square (15, 21) of 982 is a packing (G982).
- **The border audit** (F11): L-borders on Göbel’s members undercut
  `devtools.goebel_construction` at 910 of the 1,676 counts from 325 to 2000, and four
  current rows, at 534, 581, 741 and 796, lie within 6.2 × 10⁻¹¹ above a bordered side;
  that is for think-7j3i and think-zkxy, and changes nothing here.

Its F12 agrees that `devtools.construction_checker` cannot read the recipe.
Its remark that the record maintains no checker over Q(√2) is mistaken, since Witness/v2
states number-field scalars and both maintained routes decide them, as they did here;
what was missing was a reader of this recipe, which `devtools.diamond_staircases` is for
its shape.
It retained none of the source’s bytes, finding no licence; this packet retains them
under think-cnn7’s presumption, and the review’s question 4 is think-cszb’s.
Its F8 is the ledger’s verdict, not recorded, and it proposes S1, a routine consequence of
a classical construction.
Its six questions for the author go into the stage 7 reply and hold nothing open.
