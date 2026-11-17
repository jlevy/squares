# Özden’s and de Winter’s Certificates of #1005, #1006 and #1007: Stage 4 Mathematical Review

**Date:** 2026-11-17 UTC. **Subject:** four packings in eight files, from three reports
of 16 November 2026:

- issue [#1005](https://github.com/jlevy/squares/issues/1005), by Doğa Özden
  ([@dogaozden](https://github.com/dogaozden)), filed by his agent’s account
  kenaznia-doga: `n-292-candidate.yaml` and its JSON twin `n292-witness.json` of
  [kenaznia-doga/s292-upper-bound](https://github.com/kenaznia-doga/s292-upper-bound/tree/dec930bdaa5f58077af6c05bc13c0fca0a58a3ed),
  claiming $s(292) \le 17.590104218682$;
- issue [#1006](https://github.com/jlevy/squares/issues/1006), by Joost de Winter
  ([@JoostdeWinter](https://github.com/JoostdeWinter)): `n292/n292_exact.json` and
  `n292/n292_witness.yaml` of
  [JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/796ff3b76e7816f9df24bf4f6ef0bb3b9cacef24),
  claiming $s(292) \le 17.590016442847$;
- issue [#1007](https://github.com/jlevy/squares/issues/1007), by Joost de Winter:
  `n262/n262_exact.json`, `n262/n262_witness.yaml`, `n295/n295_exact.json` and
  `n295/n295_witness.yaml` of
  [the same repository](https://github.com/JoostdeWinter/square-packing/tree/853b92ee2236f418160782dd2871d38ea75271a4),
  claiming $s(262) \le 16.699693441904$ and $s(295) \le 17.699693441716$.

Each commit is the one its issue pins.
The files’ digests are in the packet’s README and `frozen/checker-frozen-digests.txt`.
#1005 states the digest of its candidate, which is the file’s; the other two issues
state none.

**Reviewed at:** `main` at `f9ddfeeef` (the merge of #1004), where this lane’s branch
starts, and the pins above.

**Reviewer:** Claude (AI review), the `tbd-strong-max` tier the runbook names, at the
maximum reasoning setting its agent definition configures, the stage 4 mathematical
review lane R1 (c-review-1005-1117) of the 17 November intake pass, separately prompted
and blind to the import.
The model ID its system prompt names is `claude-fable-5-2` (Fable 5.2); it is stated
here because the owner asked on 17 November that the latest mathematical assessments run
on Fable 5.2. It read the sources as data and ran only programs of its own, kept with
their receipts in
[`packing/resources/web/ozden-de-winter-1005-1007-review-2026-11-17/`](../../../packing/resources/web/ozden-de-winter-1005-1007-review-2026-11-17/README.md).
Its checker is a clean-room implementation written for this review: it reuses no code
from any earlier review.
It took the review of #1001 by lane L186 as the model for method, controls, freeze
protocol and layout, read its text, its packet’s README and its two frozen digest lists,
and did not open the programs of that review or of any other.
It is not a human oversight record.

## Summary for the Authors

**Verdict on the bounds: accepted at all three counts, for all four packings.** No
finding is blocking or major.

| Report | n | Pairs | Touching pairs | Wall contacts | Least pair gap | The fourth wall’s clearance | Claim | Verdict |
| --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| #1005, Özden | 292 | 42,486 | 0 | 5, each at one corner (left 2, bottom 2, top 1) | $2.01869 \times 10^{-13}$ (154, 155) | right, $2.705 \times 10^{-16}$ | 17.590104218682, the ceiling | accept |
| #1006, de Winter | 292 | 42,486 | 0 | 3, each at one corner (left, bottom, top) | $3.03125 \times 10^{-12}$ (278, 279) | right, $3.228 \times 10^{-13}$ | 17.590016442847, the ceiling | accept |
| #1007, de Winter | 262 | 34,191 | 0 | 4, each along an edge (left 1, bottom 1, right 2) | $4.47681 \times 10^{-12}$ (33, 37) | top, $4.68 \times 10^{-14}$ exactly | 16.699693441904, the ceiling | accept |
| #1007, de Winter | 295 | 43,365 | 0 | 4, each along an edge (left 2, bottom 1, right 1) | $1.52004 \times 10^{-12}$ (55, 56) | top, $7 \times 10^{-16}$ exactly | 17.699693441716, the ceiling | accept |

- **How the bounds were checked.** A clean-room exact checker, written and frozen for
  this review before your READMEs, checkers, outputs and licences, or this repository’s
  witness, verifier and promotion code, were read, decided all eight files: every
  square, every wall and every pair, with no distance filter and no tolerance, by two
  methods that share only the readers.
  They are separating axes in Python integers, on each square’s corners written over one
  denominator, and the exact intersection of each pair in GMP rationals, built by
  enumerating its vertices, which also gives the intersection of each square with the
  outside of each wall.
  They agree on all 325,056 pair decisions and all 9,128 square–wall decisions of the
  eight files.
- **Each report’s two files hold one packing.** The JSON twin of #1005 equals its YAML
  candidate value for value, and each of de Winter’s witness files lists, square for
  square in file order, exactly the corners that the centres and directions of his exact
  file give.
- **Controls.** All 340 controls stated in advance came out as stated: 51 on each
  report’s first file and 34 on its twin.
  They were written as rules over each certificate’s exact facts and hashed before any
  program read a certificate.
  They include a duplicated square, a square moved out of the box, a square off unit by
  $10^{-30}$, the side lowered by $10^{-30}$ and by one unit of its own denominator, the
  tightest eligible pair closed to exact contact and $10^{-30}$ past it, a square at
  each wall pushed to it and $10^{-30}$ past it, every one of the 162,528 pairs closed
  along its centre line to exact contact and past, and every square taken to each of the
  four walls and past.
- **The claims.** Each claimed side is the 12-place ceiling of the file’s exact side,
  between $1.7 \times 10^{-13}$ (#1005) and $7.8 \times 10^{-13}$ (295) above it.
  The same squares in the box of the claimed side are accepted by both methods (S1e), so
  each certificate proves its claim as printed; the 12-place floor is refused (S1f).
- **The side is the extent.** In every file squares touch the left and bottom walls and
  one of the other two (top in both 292 packings, right at 262 and 295), so the side is
  exactly the packing’s extent in one direction; the other direction has
  $2.7 \times 10^{-16}$ to $3.2 \times 10^{-13}$ of slack.
- **No pair touches.** Each packing is a near-contact arrangement held open: by about
  $2 \times 10^{-13}$ in #1005 (398 pairs between $2.02 \times 10^{-13}$ and
  $2.49 \times 10^{-13}$, the next at $7.9 \times 10^{-7}$), by $3.0 \times 10^{-12}$
  and up in #1006 (245 pairs below $10^{-9}$ with no break above them), by
  $4.5 \times 10^{-12}$ to $1.8 \times 10^{-11}$ at 262 (753 pairs, the next at
  $8.6 \times 10^{-5}$) and by $1.5 \times 10^{-12}$ to $3.1 \times 10^{-12}$ at 295
  (850 pairs, the next at $1.1 \times 10^{-6}$). #1006’s “smallest gap of 3e-12” is the
  least margin found here, $3.03125 \times 10^{-12}$.
- **The two reports at 292.** #1005 was filed at 15:27:38Z and #1006 at 15:39:16Z, 11
  minutes 38 seconds later.
  De Winter’s side is the lower, by $8.77758 \times 10^{-5}$. The files hold different
  packings: 64 squares turned beyond 1° in Özden’s, 59 one way and 5 the other, against
  59 in de Winter’s, all one way; how far they differ square by square is measured after
  the freeze.
- **For Joost de Winter: the 295 file is not the 262 file with a border, and it proves
  more at 262 than the 262 file does.** #1007 says the 295 packing is the 262 packing
  with an L-shaped border of 33 axis-aligned squares, “so its side is larger by exactly
  1”. The two sides differ by $1 - 1.882962 \times 10^{-10}$, and the 262 squares inside
  the border of the 295 file are not those of the 262 file: no centre is equal, 244 lie
  within $10^{-9}$ and 17 have moved by more than $10^{-3}$, up to 0.021. They are
  tighter: the first 262 squares of the 295 file, as they stand, are accepted by both
  methods in the box of side $16.6996934417125687$ exactly, which is
  $1.90949 \times 10^{-10}$ below the 262 file’s side (F8, F9).

## Scope

**Read.**

- Issues #1005, #1006 and #1007 through the REST API, with their comments and events
  (fetched at 01:34Z, before any program was written, and at 04:13Z, before the findings
  were frozen; the bodies unchanged and no comments; at first one event each, the label
  `intake`, and by 04:13Z three more each, references from commits of other branches,
  which this lane did not open).
- The eight files at the pins, as data: first their structure with `head`, `tail`,
  `sed`, `grep`, `wc` and `awk` (keys, line kinds, scalar forms and quoting, tabs and
  line ends, the first and last entries, the format sentence), to write the readers, and
  then through the frozen programs.
  The pinned trees’ file lists, with blob ids and sizes.
- On `main`: `packing/witnesses/witness.schema.yaml`, for the format’s keys and meaning;
  `packing/campaign/result-import.md` (the intake pass, stages 1, 3 and 4),
  `epistemics.md` and `attribution.md`; and, to place and commit this review’s files,
  the Ruff and BasedPyright exclusions of `packing/pyproject.toml`, `biome.json`,
  `lefthook.yml` and the agent definition `.claude/agents/tbd-strong-max.md`. None of it
  is witness, verifier or promotion code.
- The model: the review of #1001 by lane L186,
  `docs/project/reviews/review-2026-11-16-joegun-1001.md`, with its packet’s README and
  its two frozen digest lists.
  Not its programs, plan or receipts.
- The lane’s three briefs.

**Run.** Fourteen Python programs and modules of my own, importing nothing from this
repository or the sources ([What I Ran](#what-i-ran)). They decide the certificates
twice, compare each report’s two files, run a self-test, run the controls, describe the
files, and decide the squares inside the border of the 295 file as a packing of their
own.

**Seen before my findings were written**, disclosed as the runbook asks:

- the lane’s briefs, which state the three issues, their pins, filing times, authors and
  claims; that #1005 discloses a side-only leaderboard entry below both 292 claims; that
  at 262 and 295 the standing houses are classical exact constructions, $16 + \sqrt2/2$
  and $(22 + 22\sqrt2)/3$; that Mykhailo Polkovskyi’s #1009, filed later the same day,
  also claims 262, 292 and 295 and is reviewed by another lane; and the checks to make
  after the freeze;
- issue #1005, which states the exact side to 43 places; the record’s verified bound at
  `main` `f9ddfeee`, 17.5913781454976982, and the gain, 0.00127392681586354; that the
  record is credited to Nate Chaoweeraprasit, improved by Evan Daniel; the candidate’s
  digest; that this repository’s `packing-witness verify` reports 42,486 pairs and an
  independently implemented checker, `sqcheck`, reports the file valid; that the raw
  decimal pose is interval-certified with pair margin at least $2.02 \times 10^{-13}$
  and wall margin at least $1.02 \times 10^{-13}$; that the corners come from this
  repository’s `promote --strategy robust-rational` with `center_dilation` 1; the search
  (a column-band designer, Evan Daniel’s quench and an operator named `segkick`); that
  the packing has 64 tilted squares against the record’s 49, that 203 of 292 centres
  move by more than 0.001 against the record and 115 by more than 0.05, and that 77
  retilt by more than 1°; the public values the author found; and the licence and AI
  assistance;
- issue #1006, which states the exact side as a fraction; the record’s value and
  `T-146`; the gain, 0.00136; that `verify_exact.py` and `check_area.py` each report 292
  squares and 668 close pairs and this repository’s
  `check_rational_witness_independent.py` reports 42,486 pairs; what the checkers share;
  that a linear program found no first-order improvement; the smallest gap, 3e-12; the
  lineage (a ribbon of 59 tilted squares extending the ribbon of 37 in the record’s 146
  packing, credited to David W. Cantrell, with 233 axis-aligned squares); and the AI
  assistance;
- issue #1007, which states both exact sides as fractions; the record’s values,
  $16 + \sqrt2/2$ and $(22 + 22\sqrt2)/3$, and the gains, 0.00741 and 0.00454; the
  checkers’ pair counts (558 and 626 close pairs; 34,191 and 43,365 pairs); the
  construction (a band of 72 squares tilted by 25° to 30°, four wide and 18 long, with
  190 and 223 axis-aligned squares); that the 295 packing is the 262 packing with an
  L-shaped border; and the AI assistance;
- 31 lines of `packing/campaign/result-requests.yaml` printed by a search for “RV-3”,
  which concern earlier reports at 172, 199 and 270 and say of one earlier report that
  its results at “262, 292 and 298, are recorded and not registered”; the entry was not
  opened;
- the names of the directories under `packing/resources/web/` that hold earlier packets
  of these two authors, from a listing made to name this packet;
- the model review named above, which concerns five other counts.

**Not read before my checker was frozen** (03:46:57Z) **or my findings were frozen**:
the sources’ `README.md` files, their checkers (`verify_exact.py`, `check_area.py`,
`verifier/sqcheck.py`), outputs (`verify-292.txt`, `sqcheck-292.txt`, `checks/*.json`),
`SHA256SUMS`, `REGISTRATION.md`, licence files, the decimal pose, the hit files and the
images (all identified only by their blob ids in the tree listings); this repository’s
`sqpack` witness, verifier and promotion code, its devtools that read witnesses, and the
Rust crates; the register entries, case records and house witnesses at 146, 262, 292 and
295; issue #1009 and every other open issue and pull request; any import lane’s work;
and the model review’s programs.

**Not run here.** Any of the authors’ code, `packing-witness`, or the maintained routes.

## The Claims and What They Need

The three issues claim $s(n) \le C$ for four packings, each $C$ the 12-place print of
the certificate’s side $S$, rounded up.
Each certificate proves $s(n) \le S$: there are $n$ closed unit squares, rotated freely,
with pairwise disjoint interiors inside the closed square $[0, S]^2$. The claim follows
when $C \ge S$, and directly when the same squares are accepted in $[0, C]^2$.

The files come in three forms.

- **A witness file as YAML** (#1005’s candidate, and de Winter’s three
  `nNNN_witness.yaml`): a softschema envelope (`contract: packing.squares:Witness/v2`)
  around a Witness/v2 record with `representation: corners`, `scalar.kind: rational`,
  `origin: lower-left` and `axes: x-right-y-up`: four rational corners per square.
- **The same record as JSON** (#1005’s `n292-witness.json`).
- **A centre file** (de Winter’s three `nNNN_exact.json`): `n`, `side`, `square_size`, a
  `format` sentence and `squares`, each square four rationals
  `[center_x, center_y, cos, sin]`, where by the sentence “(cos, sin) is the unit
  direction of one edge”.
  The square is then the set $c + a u + b v$ with $\lvert a\rvert \le 1/2$,
  $\lvert b\rvert \le 1/2$, $u = (\cos, \sin)$ and $v = (-\sin, \cos)$. The file does
  not say where the box is; this review reads it as $[0, S]^2$, the reading its twin
  states, and the bound itself needs only that both extents of the packing are at most
  $S$.

The hypotheses are five:

1. **The reading.** One document, read strictly.
   As YAML: block style only, with no anchors, aliases, explicit tags, directives, flow
   collections, duplicate keys, tabs or carriage returns, holding only strings, plain
   decimal integers, mappings and sequences; every corner scalar read a second time,
   line by line, with the same result.
   As JSON: no duplicate key, no number that is not an integer, no `null` or boolean.
   For a witness: the envelope above, the witness keys inside the schema’s list with
   every required key present, `square_size: '1'`, the squares each with exactly an id
   and four corners of two scalars, the ids distinct.
   For a centre file: exactly its five keys, `square_size` the string `1`, the format
   sentence exactly as quoted above, each square exactly four scalars.
   Every scalar is a string `p` or `p/q` with no sign but an optional minus, no leading
   zero and $q \ge 1$. Lowest terms are recorded, not required.
2. **The count.** $n$ squares, the number the file states.
3. **Unit squares.** Each square’s four corners, in the order listed, are a unit square;
   in a centre file, the direction is a unit vector.
4. **Containment.** Each square lies in $[0, S]^2$; the origin is the lower-left corner.
5. **Disjoint interiors.** No two squares’ interiors meet.

`r1_check.py` decides the first two through the readers, and the next three twice.

- **Method A** (`r1_axes.py`, Python integers) writes each square’s eight coordinates
  over their least common denominator $D$, so its corners are integer points $Q_k/D$ and
  its edges $E_k = Q_{k+1} - Q_k$ integer vectors.
  The square is accepted when $E_0 \cdot E_0 = E_1 \cdot E_1 = D^2$,
  $E_0 \cdot E_1 = 0$, $E_2 = -E_0$ and $E_3 = -E_1$; the sign of $E_0 \times E_1$ is
  the sense of its listing.
  For a centre file the direction is first required to satisfy $\cos^2 + \sin^2 = 1$ on
  the file’s own numbers, and the corners are $c + (\pm u \pm v)/2$. On each of the four
  edge directions of a pair the two squares’ corner projections give intervals whose
  separation is an exact distance, decided over an integer denominator.
  The margin, the greatest of the four separations, is kept as an exact fraction:
  positive is apart, zero is contact with disjoint interiors, negative is overlap.
  Two convex polygons have disjoint interiors exactly when a line parallel to an edge of
  one of them weakly separates them (the origin then lies outside the interior of their
  Minkowski difference, whose edges are parallel to theirs), so the three signs are
  exactly those three classes.
  A wall’s clearance is the signed distance from the square’s extreme corner to it.
- **Method B** (`r1_area.py`, `gmpy2.mpq`) is handed points and nothing else; for a
  centre file it forms the corners itself, from the half-diagonals $(u + v)/2$ and
  $(u - v)/2$. Four points are a unit square in cyclic order when all four sides have
  squared length 1 and both diagonals squared length 2; the shoelace sum, $\pm 2$, gives
  the sense, and a clockwise listing is reversed.
  A pair is decided by building its intersection: the convex hull of the corners of each
  square that lie in the other and of the points where an edge of one meets a
  non-parallel edge of the other, all with closed tests.
  An extreme point of the intersection that is a corner of neither square lies inside an
  edge of each, and those edges cannot be parallel, so the hull is the whole
  intersection. No point is apart; a hull of zero area is contact, since the interior of
  an intersection of convex sets is the intersection of their interiors; positive area
  is overlap, by that area.
  Each wall is classed the same way, by intersecting the square with the closed
  half-plane outside it, and containment is decided apart: a unit square lies in the box
  exactly when its intersection with the box has area exactly 1. This is vertex
  enumeration, not the successive clipping the model review and de Winter’s
  `check_area.py` are said to use.

The two share only the readers (`r1_read.py`), which hand them exact rationals in the
file’s own terms. The verdict is `ACCEPT` only when both methods accept every square,
wall and pair, with equal classes everywhere; `r1_decide.py` runs both over every
square, wall and pair, and `r1_check.py` adds the file’s digest and the claim’s
arithmetic.

## The Certificates Decided

Each report’s two files give the same facts, to the last digit, so one column stands for
both.

| Quantity | 292, #1005 | 292, #1006 | 262, #1007 | 295, #1007 |
| --- | --- | --- | --- | --- |
| The side’s digits (numerator, denominator) | 217, 216 | 56, 55 | 18, 17 | 17, 16 |
| The side to 30 places | 17.590104218681834619591884457986 | 17.590016442846414712648179532764 | 16.6996934419035177 exactly | 17.6996934417152215 exactly |
| Scalars, all in lowest terms | 2,337 in each file | 1,169 (exact), 2,337 (witness) | 1,049, 2,097 | 1,181, 2,361 |
| Squares, unit by both methods | 292, all counterclockwise | 292, the same | 262, the same | 295, the same |
| Pairs decided, apart by both methods | 42,486 of 42,486 | 42,486 of 42,486 | 34,191 of 34,191 | 43,365 of 43,365 |
| Sum of all pair overlap areas (method B) | exactly 0 | exactly 0 | exactly 0 | exactly 0 |
| Least pair margin | $2.01869100306 \times 10^{-13}$ (154, 155) | $3.03124912001 \times 10^{-12}$ (278, 279) | $4.47680780529 \times 10^{-12}$ (33, 37) | $1.52004062681 \times 10^{-12}$ (55, 56) |
| Positive pairs below $10^{-12}$, $10^{-11}$, $10^{-10}$, $10^{-9}$, $10^{-6}$, $10^{-3}$, $10^{-1}$ | 398, 398, 398, 398, 404, 873, 955 | 0, 1, 206, 245, 330, 801, 939 | 0, 2, 753, 753, 753, 754, 836 | 0, 850, 850, 850, 850, 853, 952 |
| Wall contacts | left 72, 73; bottom 122, 214; top 201 | left 231; bottom 71; top 205 | left 81; bottom 164; right 233, 245 | left 77, 82; bottom 89; right 291 |
| How they touch | each at one corner | each at one corner | each along an edge (upright squares) | each along an edge (upright squares) |
| The untouched wall’s least clearance | right $2.70526034059 \times 10^{-16}$ (280, 281, 283, 284) | right $3.22778745283 \times 10^{-13}$ (253) | top $4.68 \times 10^{-14}$ (152) | top $7 \times 10^{-16}$ (16 squares of the top row) |
| Least positive clearance at any wall | $6.981 \times 10^{-17}$ (67, left) | $9.013 \times 10^{-16}$ (122, left) | $9 \times 10^{-16}$ (80, left) | $7 \times 10^{-16}$ (top) |
| The packing’s width and height | $S - 2.71 \times 10^{-16}$ and $S$ | $S - 3.23 \times 10^{-13}$ and $S$ | $S$ and $S - 4.68 \times 10^{-14}$ | $S$ and $S - 7 \times 10^{-16}$ |
| Claim less side | $1.65380408115 \times 10^{-13}$ | $5.85287351820 \times 10^{-13}$ | $4.823 \times 10^{-13}$ exactly | $7.785 \times 10^{-13}$ exactly |
| Verdict, both files | `ACCEPT` | `ACCEPT` | `ACCEPT` | `ACCEPT` |

- **Reading.** All eight files read strictly, and every scalar is in lowest terms.
  #1005’s two files number their squares 1 to 292; de Winter’s witness files name them
  `square-1` to `square-n`, in order.
  #1005’s candidate and de Winter’s 292 witness write a fraction as a plain scalar and
  an integer as a quoted string; his 262 and 295 witnesses quote every scalar, the side
  included. Each envelope is `packing.squares:Witness/v2` with `status: enforced`.
  #1005’s `claim` block says `coordinate_provenance: verified` and
  `method: exact-algebraic`, and its `certificate` block `kind: exact-rational-sat`,
  `rational_digits: 36`, `center_dilation: '1'` and `pairs_tested: 42486`; de Winter’s
  say `coordinate_provenance: reported`. Those blocks are the authors’ and are data here
  (F10).
- **Twins.** `r1_twin.py` compares each report’s two files as sets of four corners per
  square, in fractions.
  #1005’s JSON equals its YAML in every value, geometric or not, with the same listing.
  Each of de Winter’s witness files holds, square for square in file order, the corners
  his exact file’s centre and direction give: listed counterclockwise from
  $c + (u + v)/2$ at 292, and from $c - (u + v)/2$ at 262 and 295.
- **Squares.** Every square is a unit square by both methods, and every witness file
  lists every square counterclockwise.
- **Walls.** Every square lies in its box by both methods, with area exactly 1 inside,
  and the two methods’ classes agree on all 9,128 square–wall decisions.
  Every file touches the left and bottom walls and exactly one of the right and top, so
  its side is exactly the packing’s extent in one direction (F4). The contacts of both
  292 packings are single corners of tilted squares; those at 262 and 295 are edges of
  upright squares.
- **The untouched wall.** It is cleared by $2.7 \times 10^{-16}$ (#1005),
  $3.2 \times 10^{-13}$ (#1006), exactly $4.68 \times 10^{-14}$ (262) and exactly
  $7 \times 10^{-16}$ (295). Positive clearances below $10^{-9}$ at any wall number 31,
  29, 57 and 61.
- **Near pairs.** No pair touches (F5).
  - #1005: 398 pairs lie between $2.019 \times 10^{-13}$ and $2.494 \times 10^{-13}$
    (median $2.059 \times 10^{-13}$, 306 distinct values); the next pair is at
    $7.91 \times 10^{-7}$ (63, 264), and 469 more lie between $10^{-6}$ and $10^{-3}$.
  - #1006: 245 pairs lie below $10^{-9}$, from $3.031 \times 10^{-12}$ to
    $9.56 \times 10^{-10}$ (median $1.058 \times 10^{-11}$, all distinct), with no break
    above them: the next is at $1.07 \times 10^{-9}$ (224, 225), one of 85 between
    $10^{-9}$ and $10^{-6}$, and 471 lie between $10^{-6}$ and $10^{-3}$.
  - 262: 753 pairs lie between $4.477 \times 10^{-12}$ and $1.841 \times 10^{-11}$
    (median $1.48259 \times 10^{-11}$, 323 distinct values); the next is at
    $8.58 \times 10^{-5}$ (10, 11).
  - 295: 850 pairs lie between $1.520 \times 10^{-12}$ and $3.121 \times 10^{-12}$
    (median $2.6656 \times 10^{-12}$, 344 distinct values); the next is at
    $1.06 \times 10^{-6}$ (40, 43).
- **Tilts** (`r1_describe.py`, `r1_tilts.py`; they decide nothing).
  - #1005: 56 squares are exactly upright; 135 are turned by less than $10^{-13}$
    degrees, 30 by $10^{-5}$ to $10^{-3}$ degrees and 7 by $10^{-3}$ to 0.39 degrees; 64
    are turned beyond 1°, 59 of them by 40.70° to 44.80° (all but three below 40.78°)
    and 5 the other way, by 40.76° to 40.77°. The issue’s “64 tilted squares” are those.
  - #1006: 17 squares are exactly upright; 151 are turned by $1.2 \times 10^{-8}$ to
    $10^{-6}$ degrees, 7 by $10^{-4}$ to $10^{-3}$ degrees and 58 by $10^{-3}$ to 0.049
    degrees; 59 are turned by 39.82° to 42.40°, the issue’s ribbon.
    The issue’s “233 axis-aligned squares” are axis-aligned to within 0.05° (F11).
  - 262 and 295: 190 and 223 squares are exactly upright and 72 are turned by 24.94° to
    29.73°, as the issue says.
    At 262 the 72 form one block joined by gaps below $10^{-6}$.
  - Every turned square’s direction is a rational point of the circle; the denominators
    of the cosines have 69 to 107 digits in #1005 and 15 to 21 in de Winter’s files.
- **Number forms.** At 262 and 295 every centre coordinate is a decimal of at most 16
  places and both sides are 16-place decimals; at 292 de Winter’s centres are fractions
  with denominators of 20 to 36 digits.
  #1005’s corners have numerators of up to 224 digits.

The margins and clearances are exact fractions in the receipts; the prints here are
truncated.

`r1_selftest.py` holds the readers, both methods, the closed form of `r1_frame.py`, the
decision, the twin comparison and the printing to 24,389 checks and passes:

- edge contacts of two parallel squares, upright and turned by $(3/5, 4/5)$,
  $(5/13, 12/13)$, $(8/17, 15/17)$ and $(20/29, 21/29)$, across each of the four edges
  at an offset of 0, $1/3$ and $2/3$ along the edge, translated and mirrored, and
  corner-to-corner contacts along each diagonal, each at a gap $\delta$ of $10^{-30}$,
  0, $-10^{-30}$ and $\pm 1/7$; the margin is $\delta$ by method A, both ways round, and
  by the closed form, and the overlap areas, derived by hand, are
  $\lvert\delta\rvert(1 - \tau)$ for an offset $\tau$ and $\delta^2$; the same with both
  squares listed from each corner in both senses;
- a 3-4-5, a 5-12-13 and an 8-15-17 corner on an upright edge, margin $\delta$, areas
  $\tfrac{25}{24}\delta^2$, $\tfrac{169}{120}\delta^2$ and $\tfrac{289}{240}\delta^2$;
  duplicates (margin $-1$, area 1); an upright square against its concentric turn by
  $(3/5, 4/5)$ and $(5/13, 12/13)$, margins $-6/5$ and $-15/13$ and areas $5/6$ and
  $13/15$;
- each wall at $10^{-30}$ inside, at contact, $10^{-30}$ out and $1/100$ out, for
  squares at five angles, with the area outside derived by hand and method B’s
  containment;
- the unit test and listing sense at five angles in eight listings, nine shapes both
  methods must refuse (a corner off by $10^{-30}$, a bowtie listing, a rhombus with unit
  sides, a $1 \times (1 + 10^{-30})$ rectangle, a square of side 2, a point, a repeated
  corner, a folded rhombus, a parallelogram) and six directions that are not unit
  vectors;
- 400 random pairs with Pythagorean directions of up to 15 digits, on which method A’s
  margin, both ways round, equals the closed form, method B’s class is its sign, and
  method B’s area equals the area found by successive clipping, an algorithm method B
  does not use; each pair then closed along its centre line to $10^{-30}$ short of
  contact, to it and $10^{-30}$ past it, with margins exactly those by both A and the
  closed form and B’s class to match; 120 random turned squares taken to each wall,
  short of it, at it and past it;
- 75 malformed files the three readers must refuse, each mutation checked to have
  changed the text, valid files written and read back in each form, and a side out of
  lowest terms read and flagged; and whole-file decisions in each form: a $2 \times 2$
  grid (six touching pairs, eight wall contacts), that grid in a box $10^{-30}$ too
  small, a $3 \times 3$ grid tight and loose, a duplicate square, a 3-4-5 square
  touching all four walls of its box, a square that is not unit, the patched decision
  against a fresh one, and the twin comparison on equal, shifted, reordered and resized
  packings.

Fourteen deliberately broken copies fail it, each made by one stated replacement in a
program’s source: method A using only the first square’s two directions (1,636
failures), counting a zero margin as apart (357), measuring the separation on one side
only (2,988), dropping perpendicularity from its unit test (1) and taking the right
clearance from the least $x$ (647); method B with its point-in-polygon and crossing
tests both open (2,234), skipping the edge crossings (2,695), dropping the diagonals
from its unit test (2), calling fewer than three contact points apart (527) and with an
open wall test (527); the closed form with its half-extent doubled (4,039); the YAML
reader letting a duplicate key through (1); the witness reader ignoring the stated count
(3); and the decision ignoring wall crossings (6). Method B finds a point of contact
twice, as a corner of one square lying in the other and as a point where two edges meet,
so opening either test alone changes nothing; the broken copy opens both.

## Controls

`programs/controls-plan.json` states 51 controls, and the outcome of each as a rule over
the certificate’s exact facts (method A’s margins and clearances), since those facts
were unknown when it was written.
It was hashed with the checker at 03:46:57Z and pushed at 03:47:22Z, before any program
of this lane read a certificate.
Each report’s first file runs all 51: #1005’s candidate and de Winter’s three exact
files. Its twin runs 34: the 17 others (G4 to G10, W2, PALL and WALL) only repeat full
decisions of the same squares, and control T0 is what says the twin holds them exactly.
`r1_controls.py` evaluates each rule exactly and compares it with what both methods
decide on the modified packing; a decision in which the methods disagree fails its
control. Whole-packing controls write the modified packing in the file’s own form and
read it back through the reader.
“Contact” is a margin or clearance of exactly 0, and “past” is $10^{-30}$ beyond it; $W$
is the least clearance at the right or top wall.

| Control | Stated | Outcome in the four packings |
| --- | --- | --- |
| C0. The closed form by centres and half-extents recomputes every margin and clearance | equal to method A everywhere | as stated: 0 mismatches over every pair and square |
| K1. The claim against the side | the claim is at least the side and is its 12-place ceiling | as stated |
| T0. The report’s other file, square by square | the same packing: $n$, the side and every square’s corner set equal | as stated |
| T1. Square 1 moved by $(10^{-30}, 0)$, against the twin | not the same packing; exactly square 1 unequal | as stated |
| R1. The last square’s entry deleted | the reader refuses: $n$ stated, $n - 1$ listed | as stated |
| R2. The side written as $2p/2q$ | read; values equal; only the side flagged out of lowest terms | as stated |
| R3. A second square given the first’s id (witness); a fifth scalar in the first square (centre file) | the reader refuses | as stated |
| R4. The side written as the number 17.5 | the reader refuses | as stated |
| R5. The first scalar of the first square given a leading `+` | the reader refuses | as stated |
| R6. A second `side` key with the value $S + 1$ | the reader refuses: duplicate key | as stated |
| R7. `origin: container-center` (witness); “sin, cos” in the format sentence (centre file) | the reader refuses | as stated |
| G1. Square $n$ given square 1’s place | refused: overlapping exactly $(1, n)$ at margin $-1$, B area 1; each $(k, n)$ at the original $(1, k)$ | as stated |
| G2. Square 1 translated by $(S, 0)$ | refused: the only crossing square 1 at the right wall, at $R_1 - S$ exactly; its area inside 0; no overlapping pair | as stated |
| G3. Square 1 off unit by $10^{-30}$ (a corner’s $x$, or the cosine) | refused: square 1, and only square 1, not a unit square by A and by B | as stated |
| G4. Every square listed in reverse, or every direction negated | the original’s verdict; margins and clearances identical; senses exchanged in a corners file | as stated |
| G5. Every square listed from its second corner, or every direction turned a quarter | the same, senses unchanged | as stated |
| G6. Transposed | margins identical; clearances $(L, B, R, T) \to (B, L, T, R)$ | as stated |
| G7. A quarter turn about the box centre | margins identical; clearances $(L, B, R, T) \to (T, L, B, R)$ | as stated |
| G8. Mirrored, $x \to S - x$ | margins identical; clearances $(L, B, R, T) \to (R, B, L, T)$ | as stated |
| G9. Every centre multiplied by $99/100$ | margins equal the closed form’s; refused with an overlapping pair | as stated: 902, 891, 769 and 882 overlapping pairs |
| G10. Every square made upright about its centre | margins equal the closed form’s; refused with an overlapping pair | as stated: 111, 133, 134 and 134 overlapping pairs |
| S0. The side lowered by 1 | the side rule; refused | as stated |
| S1a. The side lowered by $10^{-30}$ | the side rule: right and top clearances lowered by exactly $\delta$, the left and bottom and the margins unchanged, crossings exactly those of the new clearances | as stated: refused in every file, the squares at the touched right or top wall crossing |
| S1b. The side lowered by $1/q$, $q$ its denominator | the side rule with $\delta = 1/q$ | as stated: refused in every file |
| S1c. The side lowered by $W$ | the side rule; accepted, a square at the right or top wall exactly | as stated: $W = 0$ in every file, so the original |
| S1d. The side lowered by $W + 10^{-30}$ | the side rule; refused | as stated |
| S1e. The side set to the claim | the side rule with $\delta = S - C$ | as stated: accepted in every file |
| S1f. The side set to the claim’s 12-place floor | the side rule with $\delta = S - C + 10^{-12}$ | as stated: refused in every file |
| S2c. The packing moved to the corner, the side set to its larger extent | the original’s verdict; margins identical; contacts at the left, the bottom and the right or top | as stated: no move and no lowering in any file |
| S2p. The same with the side $10^{-30}$ lower | refused; crossing exactly the squares at the touched wall | as stated |
| P0p. The first touching pair pushed $10^{-30}$ past | refused, that pair overlapping at exactly $-10^{-30}$ | no subject: no pair touches in any file |
| P1c. The tightest eligible pair closed along its centre line to exact contact | the original’s verdict; that pair’s margin exactly 0, touching by A, B and the closed form; one touching pair more | as stated |
| P1p. The same, $10^{-30}$ past | refused: overlapping pairs exactly that pair, margin exactly $-10^{-30}$ | as stated |
| W1c. At each wall, the eligible square nearest it moved to it | the original’s verdict; that clearance exactly 0, the opposite one raised by the move | as stated at all four walls |
| W1p. The same, $10^{-30}$ further | refused: the only crossing that square at that wall, by exactly $-10^{-30}$ | as stated at all four walls |
| W2c. The whole packing translated to each wall | the original’s verdict; margins identical; clearances shifted by exactly the move | as stated at all four walls |
| W2p. The same, $10^{-30}$ further | refused: crossing exactly the squares nearest that wall | as stated at all four walls |
| PALL. Every pair closed along its centre line to contact and past (pair-level) | A’s margin, both ways round, and the closed form’s exactly 0 and $-10^{-30}$; B touching and overlapping, both orders agreeing | as stated: 162,528 pairs, 325,056 closings |
| WALL. Every square moved to each wall and past (square-level) | A’s clearance exactly 0 and $-10^{-30}$; B touching and crossing; B’s area inside 1 and below 1 | as stated: 1,141 squares, 9,128 moves |

All 340 came out as stated: `EVERY_CONTROL_AS_STATED` in each of the eight receipts, 51
of 51 on the four first files and 34 of 34 on the four twins.
The W1, W2 and S rows count one control for each wall or each lowering; the plan lists
them singly.

How each rule landed:

| Control | 292, #1005 | 292, #1006 | 262 | 295 |
| --- | --- | --- | --- | --- |
| S1a, S1d and S2p: crossing | 201, top | 205, top | 233 and 245, right | 291, right |
| S1b: $1/q$; crossing | $8.2 \times 10^{-216}$; 201, top | $5.2 \times 10^{-55}$; 205, top | $10^{-16}$; 233 and 245, right | $5 \times 10^{-16}$; 291, right |
| S0: square–wall pairs crossing | 37 | 37 | 35 | 34: the 33 squares of the border, its corner square at both walls |
| S1e: the claim less the side; contacts that remain | $1.65 \times 10^{-13}$; left and bottom | $5.85 \times 10^{-13}$; the same | $4.82 \times 10^{-13}$; the same | $7.79 \times 10^{-13}$; the same |
| S1f: the side less the floor; square–wall pairs crossing | $8.35 \times 10^{-13}$; 19 | $4.15 \times 10^{-13}$; 8 | $5.18 \times 10^{-13}$; 30 | $2.22 \times 10^{-13}$; 33 |
| P1: pair, square moved, margin | (154, 155), 155, $2.019 \times 10^{-13}$ | (278, 279), 279, $3.031 \times 10^{-12}$ | (33, 37), 37, $4.477 \times 10^{-12}$ | (55, 56), 56, $1.520 \times 10^{-12}$ |
| W1: squares at left, bottom, right, top | 72, 122, 280, 201 | 231, 71, 253, 205 | 81, 164, 233, 152 | 77, 89, 291, 263 |
| PALL closings; WALL moves | 84,972; 2,336 | 84,972; 2,336 | 68,382; 2,096 | 86,730; 2,360 |

- **The touching-wall branch.** Every certificate touches the right or the top wall, so
  $W = 0$: S1c is the certificate itself and S1d is S1a. The side lowered by any
  positive amount, down to one unit of its own denominator ($8.2 \times 10^{-216}$ in
  #1005), is refused, and only the squares at the touched wall cross.
  The packing already sits in the corner with its larger extent equal to the side, so
  S2c moves nothing.
- **P1.** In every file the tightest pair is eligible: the square moved clears
  everything else by more than the move.
- **W1.** At every wall an eligible square was found.
  A touching square was pushed $10^{-30}$ past its wall; at the untouched wall the
  nearest square was moved by its clearance, $2.7 \times 10^{-16}$ to
  $3.2 \times 10^{-13}$, and then $10^{-30}$ past.
- **PALL and WALL.** All 162,528 pairs, not only the near ones, were closed along their
  centre lines: square $j$ was moved toward square $i$ to the time
  $\tau^* = \max_w \bigl(1 - (m^* + H_w)/\lvert d \cdot w\rvert\bigr)$ over the four
  edge directions with $d \cdot w \ne 0$, $H_w$ the two half-extents on $w$ and $d$ the
  centre difference, which makes the margin exactly $m^*$ ($0$ or $-10^{-30}$) whatever
  the other directions do.
  Every pair has distinct centres, so every pair was closed.
- **The priors.** The plan’s six predictions held in every file: each is accepted, each
  claim is the 12-place ceiling of its side, each report’s two files hold one packing,
  $W = 0$ with the left and bottom walls touched, S1e is accepted and S1f refused, and
  G9 and G10 are refused.

## The 295 File and the 262 File

#1007 says: “The packing for n = 295 is the packing for n = 262 with an L-shaped border
of 33 axis-aligned squares, so its side is larger by exactly 1.” `r1_inner.py` examined
that on the two exact files.
It was written after the checker was frozen; it selects squares and hands them to the
frozen decision.

- **The sides.** $S_{295} - 1 - S_{262}$ is $-941481/(5 \times 10^{15})$, that is
  $-1.882962 \times 10^{-10}$: the 295 side is less than the 262 side plus 1.
- **The border.** The 33 squares of the 295 file whose centres lie within 1 of the right
  or top wall are its last 33, squares 263 to 295, all exactly upright.
  Of the four corners of the box, that is the one whose remaining squares have the least
  extent.
- **The squares inside.** The other 262 are the file’s first 262 squares.
  Their bounding box starts at the origin, and its width and height are
  $16.6996934417125687$ and $16.6996934417125648$ exactly.
- **They are a packing of their own.** Written as a centre file of 262 squares with side
  $166996934417125687/10^{16}$ and decided by the frozen `r1_decide.py`, they are
  accepted: 34,191 pairs apart by both methods, least margin $1.52004 \times 10^{-12}$,
  contacts at the left, bottom and right walls, the top cleared by
  $3.9 \times 10^{-15}$. So the 295 file proves $s(262) \le 16.6996934417125687$, whose
  12-place ceiling is 16.699693441713, $1.90949 \times 10^{-10}$ below the 262 file’s
  side and 191 units of the twelfth place below the issue’s claim, 16.699693441904.
- **They are not the 262 file’s squares.** Paired by nearest centre, the two sets match
  one to one and in the same order, but no centre is equal: 244 lie within $10^{-9}$,
  one more within $10^{-3}$, and 17 have moved by more than $10^{-3}$, the farthest
  (square 144) by 0.021. Of the 72 tilted squares one has the same direction in both
  files. The gaps say the same: the median near gap is $1.48 \times 10^{-11}$ in the 262
  file and $2.67 \times 10^{-12}$ in the 295 file.
- **The border’s cost.** $S_{295} - 1$ exceeds the inner packing’s extent by
  $2.6528 \times 10^{-12}$, the gap left between the inner squares and the border.
- **The derived packing was checked like a certificate.** `r1_inner.py` wrote it in both
  forms (digests in its receipt); `r1_check.py` accepts both, `r1_twin.py` finds them
  one packing, and the frozen controls, applied unchanged through
  `programs/controls-plan-derived.json`, came out as stated: 51 of 51 and 34 of 34. The
  files are not kept here: they are the 295 file’s first 262 entries with `n` and the
  side changed, and the README gives the command that writes them.

## What This Review’s Checker Shares

- **With other checkers.** It shares no code with any other checker, and it was written
  and frozen before the authors’ checkers, `packing-witness`, or any of this
  repository’s witness, verifier or promotion code was read.
  It reuses nothing of any earlier review’s programs, none of which it opened.
  Method A follows the mathematics the model’s text describes, separating axes in
  integer arithmetic on corners over one denominator, and implements it afresh.
  Method B differs from the model’s in algorithm: it enumerates the intersection’s
  vertices and takes their hull, where the model clips one square by the other’s four
  half-planes in turn; the unit test by sides and diagonals, the wall classes by the
  outer half-plane and containment by area are the model’s ideas.
  The closed form by centres and half-extents is a third formulation, used for the
  controls’ moves and checked against method A on every pair and wall (C0). The controls
  follow the model’s list, stated as rules as the model’s are; the twin, duplicate-key,
  stated-meaning, extent, whole-packing wall, contraction and upright controls are
  added, and the wall sweep takes every square to all four walls.
  It shares the mathematics above and the formats’ meaning (corners in order, or a
  centre with a unit edge direction; the lower-left origin; the box $[0, S]^2$), taken
  from the schema text, the format sentence and the files.
- **With the authors’ tools.** #1005 says the corners came from this repository’s
  `packing-witness promote` and were checked by `packing-witness verify` and by the
  author’s `sqcheck`. #1006 and #1007 name `verify_exact.py`, a separating-axis test on
  pairs with centres closer than $\sqrt2$, `check_area.py`, a clipped area on the same
  pairs, and this repository’s `check_rational_witness_independent.py`. This checker
  shares no code with any of them and was frozen before any was read; it shares the
  files and the definitions (unit square, box, disjoint interiors).
  Unlike the two scripts as the issues describe them, it decides every pair.
- **Its trust base.** CPython 3.14.7’s integers and `fractions`, GMP 6.3.0 through
  `gmpy2` 2.3.1, PyYAML 6.0.3 for scanning and parsing only (the readers build their own
  tree from its events and resolve scalars themselves, taking only its implicit tag
  table), the `json` module, and the facts its self-test exercises.
  Its two methods share the readers and nothing else.
- **Authorship.** #1005 says the search, checks and filing were AI-assisted throughout
  and names a Claude Sonnet 5.5 director; #1006 says the construction and search ran
  with Gemini Carbon and the checking with Claude Fable 5.2; #1007 says Gemini Carbon
  and Claude. This review was written by a Claude agent, as was the model review, on the
  model #1006 names for its own checking; the independence claimed here is of code and
  of what was read.

## Findings

| Id | Severity | Where | Finding |
| --- | --- | --- | --- |
| F1 | note | the eight files | each is an exact packing at its side by both methods, every square, wall and pair, with no distance filter; every pair strictly apart; 5, 3, 4 and 4 wall contacts |
| F2 | note | the controls | all 340 stated controls came out as stated |
| F3 | note | the claims | each claim is the 12-place ceiling of its side; the squares are accepted in the box of the claim and refused in the box of its floor |
| F4 | note (records) | the sides | each side is the packing’s extent exactly: the left and bottom walls and the top (both 292 packings) or the right (262, 295) are touched; the fourth wall is cleared by $2.7 \times 10^{-16}$, $3.2 \times 10^{-13}$, $4.68 \times 10^{-14}$ and $7 \times 10^{-16}$ |
| F5 | note (records) | the near pairs | no pair touches: least gaps $2.01869 \times 10^{-13}$, $3.03125 \times 10^{-12}$, $4.47681 \times 10^{-12}$ and $1.52004 \times 10^{-12}$; how this bears on the record’s padding question is measured after the freeze |
| F6 | note (records) | each report’s two files | one packing, square for square: #1005’s JSON equals its YAML in every value; each of de Winter’s witness files holds exactly the corners of his exact file |
| F7 | note | the two reports at 292 | #1005 was filed 11 minutes 38 seconds before #1006; #1006’s side is lower by $8.77758 \times 10^{-5}$; the two files hold different packings |
| F8 | minor (author) | #1007, “Construction” | the 295 file is not the 262 file with a border: the sides differ by $1 - 1.882962 \times 10^{-10}$, no centre of the inner 262 squares equals the 262 file’s, and 17 squares differ by more than $10^{-3}$ |
| F9 | note (records, author) | `n295_exact.json`, squares 1 to 262 | the 295 file proves $s(262) \le 16.6996934417125687$, $1.90949 \times 10^{-10}$ below the side of the 262 file the same report claims with; both methods accept the derived packing and its controls are as stated |
| F10 | note (records) | #1005’s candidate, `claim`, `source` and `certificate` blocks | the file calls its coordinates `verified` and names `n-292-decimal-pose.yaml` as its source and `W-segkick-sonnear-n292` as its parent; these are the promotion tool’s words, written by the author’s run, and the record states its own provenance and source |
| F11 | note (author) | #1006, “Lineage and credit” | of the “233 axis-aligned squares” 17 are exactly upright; 216 are turned by $1.2 \times 10^{-8}$ to 0.049 degrees |
| F12 | note (records) | de Winter’s exact files | a centre file states no origin; it is read here in $[0, S]^2$, as its twin states, and the squares lie there |

**F1. Feasibility.** Each file is an exact packing at its side: 162,528 pairs in the
four packings, each decided by both methods in both of its files with equal classes and
strictly apart, and every one of the 1,141 squares a unit square inside its box by both,
with area exactly 1 inside.
The bounds $s(292) \le S$ (twice), $s(262) \le S$ and $s(295) \le S$ hold at the four
sides.

**F2. Controls.** As [Controls](#controls) gives them: 51 of 51 on each first file and
34 of 34 on each twin.

**F3. The claims.** Each $C$ is the ceiling of $S$ at 12 places, above it by
$1.65 \times 10^{-13}$, $5.85 \times 10^{-13}$, $4.823 \times 10^{-13}$ and
$7.785 \times 10^{-13}$. Control S1e decides each claim directly: in the box of side $C$
the squares are accepted by both methods, with the contacts at the touched wall opened
by $C - S$. Control S1f shows that the floor would not do: the square–wall pairs at the
right and top that lie within $S$ less the floor of their wall, 19, 8, 30 and 33 of
them, cross it. A record can therefore hold each bound as the 12-place decimal its issue
prints, with the certificate’s own squares as its proof.

**F4. The side and the extent.** No certificate states a side above its packing: each
packing touches the left and bottom walls and one of the other two, so $S$ is the
packing’s height (both 292 packings) or width (262, 295) exactly.
The squares fit no box smaller than $S$ in place or translated, since a box must hold
the packing’s larger extent, which is $S$ (S2c, S2p). The other extent is smaller by
$2.71 \times 10^{-16}$, $3.23 \times 10^{-13}$, $4.68 \times 10^{-14}$ and
$7 \times 10^{-16}$. #1005 says its side comes from translating the packing to the
corner and recomputing the extent, which is what the file shows.
Nothing in the bound depends on it.

**F5. Margins of $10^{-13}$ to $10^{-11}$.** No pair of any packing touches, and the
gaps differ in kind.
#1005’s 398 near pairs lie in a band 23% wide around $2.06 \times 10^{-13}$, as a
uniform opening of an exact contact arrangement would leave, and the issue says the
decimal pose was certified with a pair margin of at least $2.02 \times 10^{-13}$. De
Winter’s 262 and 295 near pairs lie in bands around $1.5 \times 10^{-11}$ and
$2.7 \times 10^{-12}$; his 292 pairs have no band at all, 245 below $10^{-9}$ and then a
continuum up to $10^{-3}$, which fits the issue’s account of a numerical optimization
rounded to rational coordinates.
The wall contacts are exact in every file: each touched wall has a corner or an edge
whose coordinate is exactly 0 or exactly the side.
The contraction margin of each certificate, and of the record’s houses that the gains
are measured against, is measured after the freeze.

**F6. One packing in two files.** #1005’s issue calls `n292-witness.json` the “same
witness as JSON”, and it is: the same values in the same listing, with the same `claim`,
`source` and `certificate` blocks.
De Winter’s issues call each witness file “the same packing”, and each is, exactly: the
four corners of every square of the witness file are the four points
$c + (\pm u \pm v)/2$ of the exact file’s centre and direction.
Either file of a report can stand as its certificate.

**F7. Two reports at one count.** #1005 reached this repository at 15:27:38Z and #1006
at 15:39:16Z. #1005’s side, $17.59010421868183\ldots$, is the higher; #1006’s,
$17.59001644284641\ldots$, is lower by $8.77758354199 \times 10^{-5}$. Both are below
the record’s value the two issues quote, 17.5913781454976982. The packings are not one
arrangement in two roundings: #1005 has 64 squares turned beyond 1° (59 by 40.70° to
44.80° and 5 the other way) and #1006 has 59 (39.82° to 42.40°); #1005’s near pairs all
lie within a quarter of $2.06 \times 10^{-13}$, and #1006’s spread from
$3 \times 10^{-12}$ to $10^{-3}$ without a break.
How far they differ square by square, and how each stands to the record’s packing and to
the 146 packing #1006 names, is measured after the freeze.

**F8. The stated relation of the 295 and 262 packings.** As
[The 295 File and the 262 File](#the-295-file-and-the-262-file) gives it.
The 295 packing has the 262 packing’s plan, the band of 72 tilted squares and the same
190 upright squares in the same order, with a border of 33 upright squares along the
right and top walls; it is a second solution of that plan with smaller gaps, not the 262
file’s squares with 33 added, and its side is not the 262 side plus 1. The claim at 295
does not depend on the sentence: the 295 file is decided on its own.

**F9. A better bound at 262 from the 295 file.** The first 262 squares of
`n295_exact.json`, untranslated, lie in $[0, 16.6996934417125687]^2$ with disjoint
interiors, by both methods.
That is a certificate of $s(262) \le 16.6996934417125687$, from the same report and the
same author, $1.90949 \times 10^{-10}$ below the side of `n262_exact.json`. It does not
weaken the 262 file, which proves what it claims.
Whether the record states the 262 bound from the 262 file, as the issue claims it, or
from the 295 file’s squares, which prove more, is for the import to decide; the
difference is $1.1 \times 10^{-11}$ of the side.

**F10. The files’ own claims.** #1005’s candidate says `coordinate_provenance: verified`
and `method: exact-algebraic`, and its `certificate` block `kind: exact-rational-sat`
with a `replay` command for `packing-witness verify`. The issue says the file is the
output of this repository’s promotion tool, run by the author.
The record should state its own provenance for a retained copy (here, reported
coordinates confirmed by this review’s replay), and its own source, since `source.path`
names the author’s decimal pose file and `derived_from` a witness id that is not in this
repository. De Winter’s witness files say `coordinate_provenance: reported`, which needs
no change; their `softschema.schema` is a URL of this repository’s schema on `main`.

**F11. “Axis-aligned”.** #1006 describes 233 axis-aligned squares beside a ribbon of 59
tilted ones. In the file 17 squares are exactly upright; the other 216 are turned, each
by its own angle (the file has 276 distinct orientations): 151 by $1.2 \times 10^{-8}$
to $10^{-6}$ degrees, 7 by $10^{-4}$ to $10^{-3}$ degrees and 58 by $10^{-3}$ to 0.049
degrees. The bound does not depend on it; a description of the packing, or a
regularization of it, would.

**F12. The box of a centre file.** De Winter’s exact files give centres and directions
and state no origin.
Read with the origin at the lower-left corner, as each twin says, every square lies in
$[0, S]^2$, touching the left and bottom walls.

None changes a verdict.
F8 asks the author to correct a sentence, and F9 is new information for the record; the
rest are notes.

## Verdict

**Accepted as upper bounds at all three counts.** Each certificate proves $s(n) \le S$
at its side exactly, and each of the issues’ claims, $s(292) \le 17.590104218682$
(#1005), $s(292) \le 17.590016442847$ (#1006), $s(262) \le 16.699693441904$ and
$s(295) \le 17.699693441716$ (#1007), is decided directly by both methods (S1e).

- Every hypothesis holds exactly, for every square, wall and pair, by two methods that
  agree everywhere.
- Every control is decided as stated beforehand.
- No defect of the certificates or of their mathematics is open; F8 is a sentence of an
  issue, and every other finding is a note.

Mapped as an adversarial review with verdict `accepted`, it supports `V3` and `C3` at
each count for each report, provided `r1_check.py`’s runs are registered as
exact-algebraic evidence replayed here with full coverage of each certificate.
That reads as confirmed, independently re-implemented, clean room, by a Claude agent.
`V4` and `C4` would need a second accepted adversarial review by a distinct reviewer and
a human oversight record.

## What I Ran

All with CPython 3.14.7, the project interpreter, as `python -I -B` under `nice -n 19`,
from this review’s packet, at most two at a time.
The programs, the frozen files and the receipts are in
[`packing/resources/web/ozden-de-winter-1005-1007-review-2026-11-17/`](../../../packing/resources/web/ozden-de-winter-1005-1007-review-2026-11-17/README.md),
whose README gives the commands.

| Program | Receipt | CPU |
| --- | --- | ---: |
| `r1_selftest.py` | `out/selftest.json`: `PASSED`, 24,389 checks, 14 broken copies failing | 27 s |
| `r1_check.py`, eight runs | `out/check-*.json`: `ACCEPT` in all eight | 30.9, 30.9, 9.0, 9.5, 3.1, 3.2, 3.8, 3.9 s |
| `r1_twin.py`, four runs | `out/twin-*.json`: `SAME_PACKING` in all four | under 2 s each |
| `r1_controls.py`, four first files | `out/controls-*.json`: 51 of 51 as stated in each | 897, 277, 92, 113 s |
| `r1_controls.py`, four twins | `out/controls-*.json`: 34 of 34 as stated in each | 168, 58, 20, 25 s |
| `r1_describe.py`, five runs, and `r1_tilts.py`, four | `out/describe-*.json`, `out/tilts-*.json`: the tilts, blocks, wall contacts and number forms; they decide nothing | under 3 s each |
| `r1_inner.py` | `out/inner-1007-n295.json`: the inner 262 squares of the 295 file, `ACCEPT` at side $16.6996934417125687$ | 4 s |
| `r1_check.py`, `r1_twin.py` and `r1_controls.py` on the derived packing | `out/check-derived-*.json`, `out/twin-derived-n262.json`, `out/controls-derived-*.json`: `ACCEPT`, `SAME_PACKING`, 51 of 51 and 34 of 34 | 3.0, 3.2, 1, 93, 20 s |
| `r1_tables.py` | prints this review’s tables from the receipts; decides nothing | under 1 s |

What went wrong along the way, and was redone before the freeze it precedes:

- The session’s worker process restarted between about 01:58Z and 03:04Z, after the
  readers, the two methods and the self-test were written and before the controls
  program or the plan existed.
  Nothing had been frozen and nothing was lost; the lane checked its files and the
  pinned sources’ digests, reran the self-test and went on.
  The first commit, of the programs as they stood, was made and pushed then.
- Two shell lines run from the worktree’s root named an interpreter path that does not
  exist there and fell through to the project interpreter under `packing/`; nothing else
  ran.
- The self-test’s first run showed two of its broken copies passing.
  Opening method B’s point-in-polygon test alone changes nothing, since a point of
  contact is also found where edges meet; the copy now opens both tests.
  The witness reader compared the number of distinct ids with the stated count, so a
  wrong count was refused for the wrong reason; it now compares them with the number
  listed.
- The printing helper first formed a power of ten with a negative exponent, a float; it
  was rewritten in integers before any receipt was written.
- The controls program was run on synthetic packings, in scratch space, before the
  freeze: grids tight and loose, a tilted band, a packing clear of every wall, a refused
  packing, a wrong claim and a twin differing in one square.
  One synthetic packing was itself wrong (a tilted square crossed its wall), which the
  check refused. A trial on a synthetic packing of realistic size took 13 minutes of CPU,
  and the plan gained its two tiers before it was hashed: the 17 controls that repeat
  full decisions run on each report’s first file only.
  No program of this lane read a certificate before the freeze.
- `r1_inner.py`, `r1_tilts.py` and `r1_tables.py` were written after the checker was
  frozen and before the findings were frozen; they are not in the checker’s digest list.
  The first version of `r1_inner.py` took the first corner of the box at which 33
  squares lay within 1 of the two walls, the lower left, where one of the 33 is a tilted
  square of the band and the rest do not fit a smaller box; it now takes the corner
  whose remaining squares have the least extent.
  Its first receipt was overwritten.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
