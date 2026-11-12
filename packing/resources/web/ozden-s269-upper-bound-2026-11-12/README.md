# Doğa Özden’s s(269) Certificate at f496016

This packet retains
[kenaznia-doga/s269-upper-bound-1688973007](https://github.com/kenaznia-doga/s269-upper-bound-1688973007/tree/f496016d3ebccb00c00cbf146efe85e0cc952dda)
at `f496016d3ebccb00c00cbf146efe85e0cc952dda` (committed 2026-11-12T03:00:02Z), the
repository’s one commit, which [issue #967](https://github.com/jlevy/squares/issues/967)
names 12 seconds later.
Doğa Özden’s AI agent, which uses the account kenaznia-doga, prepared and posted both on
his behalf. Seven seconds after the issue it pointed to it from his issue #947
([comment](https://github.com/jlevy/squares/issues/947#issuecomment-6813076182)), and a
second later from pull request #966, which adopted his #962 at this count
([comment](https://github.com/jlevy/squares/pull/966#issuecomment-6813076476)).

## What the Source Claims

- `n-269-candidate.yaml`, a `packing.squares:Witness/v2` file (corners, rational
  scalars, 269 squares), bounds s(269) by its exact side, a fraction whose 16-place
  ceiling is 16.8897300735956367. #967 prints its 12-place ceiling, 16.889730073596, and
  says it is 1.126e-02 below the record, T-290, the author’s own #947 certificate, and
  9.74e-3 below his #962, which PR #966 was adopting; it says it supersedes both.
  #966 merged at 07:08:09Z, so the house on `main` is now T-296, #962’s certificate.
  The issue and README also print the exact side as 16.889730073595636, the side
  truncated at 15 places, 6.9 × 10⁻¹⁶ below it.
  It claims an upper bound only: no KKT, local-optimality, rigidity or global-optimality
  claim.
- The exact coordinates were made by this repository’s own `packing-witness promote
  --strategy robust-rational` at `0352d755` from the lab’s decimal pose,
  `n-269-decimal-pose.yaml`, which the witness’s `source.path` names, with
  `center_dilation: '1'` and no dilation.
  The issue says the pair margins of about 2 × 10⁻¹³ are the decimal pose’s own, left by
  the final binary64 repair scaling of Evan Daniel’s quench (about 10⁻¹³ relative), that
  only the squares that set the left wall, the bottom wall and the side touch them
  exactly, and that other squares near a wall clear it by up to about 10⁻¹². Measured
  here, three squares touch a wall exactly: square 48 at the left, square 102 at the
  bottom and square 199 at the top, which sets the side.
  No square touches the right wall.
  Of the other square–wall clearances, 47 are below 10⁻¹² and at most 7.84 × 10⁻¹⁵, and
  10 lie between 9.16 × 10⁻⁶ and 9.32 × 10⁻⁴, beyond “up to about 1e-12”.
- `n269-witness.json` is the same file as JSON. `packing-witness-verify.txt` is the
  author’s run of this repository’s `packing-witness verify` at `0352d755` (VERIFIED,
  36,046 pairs); `sqcheck-output.txt` is the author’s run of `verifier/sqcheck.py`, an
  exact checker the source says was written separately from this repository’s code
  (VALID, exact rational, the exact side rounded up at 15 places).
  The issue says the two share only the unit-square, wall and non-overlap definitions,
  that `packing-witness verify` is not independent of how the coordinates were rounded,
  and that `sqcheck.py` certified the decimal pose in interval arithmetic at its own
  side before promotion.
  Those statements are the author’s; no source program ran here.
- The issue says the packing was found by an AI-run column-band designer, new for this
  filing, with no donor packing: tilted squares stand in columns across a band along the
  diagonal at unit pitch, each column a stack of one to three squares sliding on its
  own; the axis-parallel squares sit on the two wall-anchored staircase lattices; for a
  side fraction f and a band angle of 45 degrees minus delta an exact dynamic programme
  over the columns maximises the number of squares.
  The best design is quenched once with Evan Daniel’s ALM+SLP code from
  [evand/square-packing](https://github.com/evand/square-packing) (`search/packer`, MIT,
  at `bb4cc78e`), then kicked and quenched again.
  This packing came from the design f = 0.913469, band angle 42.8 degrees (delta 2.2),
  tolerance 0, 45 tilted squares, column offset 0.96875 and diagonal variant 14,
  quenched once to 16.890507465412; a kick of sigma 0.0222 and a quench gave
  16.889734433328, and a kick of sigma 0.001007 and a quench gave the filed side.
  The cloud job b2h269 reached 16.88973007359575, but its pack file was lost, and the
  filed packing is a local re-find the issue says has the same structure and a side 9 ×
  10⁻¹⁴ higher. The issue counts 45 tilted squares against the record’s 100: one band at
  about 42.1 degrees and a small cluster at about −44.9 degrees at the upper-right end.
  Against the registry packing, matched by assignment up to the square’s symmetries, it
  reports 261 of 269 centres beyond 1e-3, 137 beyond 0.05 (largest 1.879), 121 squares
  re-tilted beyond 1 degree (largest 44.4), and 45 squares tilted beyond 0.5 degree
  against the record’s 100.
- The issue describes the record, T-290, in two ways, as #962 did: in its claim
  paragraph as “built from Nate Chaoweeraprasit’s packing (itsnaka) improved by Evan
  Daniel and PingYou Ltd”, and in its lineage paragraph as found by transplanting Evan
  Daniel’s n = 304 packing.
  The register records T-290 as the second: a strip cut of Evan Daniel’s 304, below
  T-174, Nate Chaoweeraprasit’s packing as Evan Daniel and PingYou Ltd improved it,
  which was the house before it.
- The issue’s credit paragraph asks that “the band’s source packing” be credited to the
  registry’s n = 207 packing, to n = 70 (Ryan Xu; improved by Evan Daniel and PingYou
  Ltd) and to the lab’s own n = 179 of #954, while its lineage paragraph and the README
  say the designer used no donor packing and no registry packing as a seed.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is the whole tree, 11 files: 7 retained under [source/](source/) and 4 pinned
by digest.

| File | Bytes |
| --- | --- |
| `LICENSE.md` | 1,484 |
| `README.md` | 7,314 |
| `n-269-candidate.yaml` | 820,780 |
| `n-269-decimal-pose.yaml` | 28,459, the decimal pose the witness was promoted from |
| `n269-witness.json` | 812,482, the same packing as JSON, which the reader holds equal to the YAML |
| `packing-witness-verify.txt` | 559 |
| `sqcheck-output.txt` | 101 |
| `LICENSE-evand-square-packing.txt` | 1,068, pinned against the identical copy of Evan Daniel’s MIT notice the [evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains |
| `records/n-269-candidate-diff.png` | 308,205, pinned by digest: a raster comparison that decides nothing |
| `verifier/README.md` | 3,441, pinned against the identical copy the [3 November s299 packet](../ozden-s299-upper-bound-2026-11-03/README.md) retains |
| `verifier/sqcheck.py` | 17,654, pinned against the identical copy the [9 November s232 packet](../ozden-s232-upper-bound-2026-11-09/README.md) retains, never executed here |

The SHA-256s the issue states for `n-269-candidate.yaml` and the README states for it
and for `n269-witness.json` are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is about 1.8 megabytes in a checkout and far less as Git stores it, so it is
kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `45e2ecca2` on 12
November 2026):

- **269:** exact side 16.8897300735956367 rounded up at 16 places, below the case’s
  house (T-296, Doğa Özden’s own certificate of #962) by 9.739e-03, as the issue states,
  below T-290, the house before it, by 1.126e-02, as the issue states, and below T-174,
  the house before that, by 1.178e-02. No register bound is pending adoption at 269.

## Report Order

The
[ledger of 12 November for this lane](../../../campaign/issue-intake/upper-bounds-967-20261112/README.md)
walks every report at 269 in the order it reached this repository, from a start frozen
at `main` `45e2ecca2`, and records this packet’s claim at 269. The best public Kaggle
per-puzzle packing the issue quotes at 269, 16.901513582205 (kirilltym), is above this,
by 1.18e-2. The issue also quotes, and states first, a side-only Kaggle leaderboard
entry at 269, 16.889730079125 (team elegans, 5 November, from a cache of 9 November),
5.53 × 10⁻⁹ above this side, as the issue says.
It is unpublished and states no packing, so it is no report and is recorded as context
only.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-296’s packing, T-290’s,
T-174’s, the house witness and the regularized view, and wrote
[measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **Against T-296**, the house: no symmetry of the box pairs it one to one with T-296’s
  packing by nearest centres.
  The optimal assignment, under the identity of the box, moves every square beyond 10⁻⁶,
  266 beyond 10⁻³, 107 beyond 0.01 and 53 beyond 0.1 (largest 0.950002), and turns 102
  squares by more than 10⁻⁶ radians, by up to 44.77 degrees; aligned by box centres, 57
  squares turn by more than a degree.
  Tilted beyond a degree: 45 here, as in T-296, but a band of 41 at 41.60 to 42.06
  degrees and a cluster of four, squares 42 to 45, at −44.33 to −44.38 degrees at the
  upper-right end, against T-296’s 22 one way and 23 the other, 39.53 to 44.77 degrees.
  No square here is tilted between half a degree and one, so 45 are tilted beyond half a
  degree, as the issue says.
  The house witness measures as T-296, and its regularized view the same but for 125
  squares beyond 10⁻² under the assignment.
  So it is a new arrangement relative to T-296’s packing, not a further arrangement of
  it.
- **Against T-290**, the house before T-296: no symmetry pairs nearest centres one to
  one, and the optimal assignment moves 127 squares beyond a tenth (largest 1.25522);
  aligned by box centres, 122 squares turn by more than a degree.
  T-290 has 100 squares tilted beyond a degree, 18.70 to 36.11 degrees, all turned one
  way. It is new against T-290 as well.
- **Against T-174**, it is new: the optimal assignment moves 75 squares beyond a tenth
  (largest 0.91336); T-174 has 49 tilted squares.
- The issue’s band angles, “about 42.1°” and “about −44.9°”, are a little off: the band
  lies at 41.60 to 42.06 degrees and the cluster at −44.33 to −44.38. The issue’s own
  counts against T-290 (261 beyond 10⁻³, 137 beyond 0.05, largest 1.879, 121 re-tilted
  beyond a degree) are not those of the optimal assignment or of box-centred alignment,
  which give 268 and 269 beyond 10⁻³, a largest move of 1.25522 and 1.25512, and 122
  squares turned beyond a degree.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 216,276 pair decisions, 98.63 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 2.036e-13. `check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)), with the
expected verdicts stated before it ran, at 07:18:10Z on 12 November.
It lowered the side by the least far-wall clearance, closed the least-gap pair (squares
40 and 38) by its gap, and moved every square toward the nearer near wall by its least
clearance: both routes accepted each at contact with margin 0 and refused each past it.
It enlarged one square to its pair and one to its wall: both routes refused the first,
square 38, at contact for its shape alone and accepted the second, square 48, which
already touches its wall and so grew by 0, at contact; both refused each 10⁻³⁰ past it
for the overlap or the wall as well.
Both refused a duplicated square.
All 11 were as stated in advance.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the witness through the `witness-corners`
reader. The first route is the `packing-witness verify` the author ran on the same file,
so on that route the replay is reproduced with the producer’s code; the second shares no
verification code with it.
Neither is independent of this repository’s `packing-witness
promote`, which made the coordinates.
The source’s own `sqcheck.py` was not run.

## The Gain Against Padding

T-296’s certificate at 269, contracted uniformly about the origin to first contact and
boxed, loses 3.234 × 10⁻¹² of its side (1 − λ\* = 2.034 × 10⁻¹³, the binding pair
squares 10 and 13). The gain this certificate states, 9.739e-03, is 3.01 × 10⁹ times
that margin, so none of it is T-296’s padding; the owner’s open question about gains
inside a padding margin (RV-3, think-ruu2) does not reach it, and the entry is not held
at V0/C1 as T-285 and T-286 were.
T-290’s certificate, measured the same way in #962’s
[packet](../ozden-s269-issue962-2026-11-11/measure/contraction-n269.json), has 3.238 ×
10⁻¹² of padding, and the gain on it, 1.126e-02, is 3.48 × 10⁹ times that.
This certificate’s own margin, measured the same way, is 3.236 × 10⁻¹² (1 − λ\* = 2.036
× 10⁻¹³, the binding pair squares 38 and 40, the least-gap pair); contracted, it would
be a square of side 16.8897300735924008, which nobody reported and which is not
registered (RV-3). `devtools.contraction_margin` wrote the two receipts,
[measure/contraction-n269.json](measure/contraction-n269.json) and
[measure/contraction-n269-own.json](measure/contraction-n269-own.json), each contracted
packing decided on both maintained routes.

## The L Step

`devtools.l_step_scan`, with this side stood in for 269’s ceiling, finds the same L-step
and monotonicity consequences as on `main`: this bound carries to no other count
([measure/l-step-scan.json](measure/l-step-scan.json)).

## Stage 4 Review and Adoption

The stage 4 mathematical review of 12 November 2026
([review-2026-11-12-ozden-967.md](../../../../docs/project/reviews/review-2026-11-12-ozden-967.md)),
written in a separate lane (L127) that finished before this one began and so was blind
to it throughout, accepts the certificate with 15 findings, all notes, none blocking,
and scores it S3. Its clean-room checker decides every square, wall and pair by
separating axes in Python integers and by exact convex clipping in GMP rationals, with
20 controls stated before they ran, all 20 as stated, and accepts the same squares in
the box of the claim’s own side, 16.889730073596, and refuses them in the box of its
12-place floor (F3). Its programs and receipts are kept in the review-only directory
beside this packet,
[ozden-s269-967-review-2026-11-12](../ozden-s269-967-review-2026-11-12/README.md).
Read against this packet’s receipts once both were done, its least pair margin (2.03645
× 10⁻¹³, squares 38 and 40) and its three wall contacts are the replay’s exactly, its
contraction receipts for #962’s certificate (T-296) and for this one equal
[measure/contraction-n269.json](measure/contraction-n269.json) and
[measure/contraction-n269-own.json](measure/contraction-n269-own.json) in margin,
factor, binding pair and contracted side, and its identity measurement against T-290 and
T-296 equals [measure/identity.json](measure/identity.json) under nearest centres, the
optimal assignment and box-centred alignment, as do the tilt counts.
This lane’s brief had relayed the review’s T-290 and T-296 margins, the certificate’s
contracted side and the identity verdict before its runs, so on those the agreement is
two runs of the same tools, not a blind comparison.

The review finds the issue’s arithmetic right (F4): the claim is the side’s 12-place
ceiling, the gains on T-290 and #962 and the distance below the Kaggle entry are as
printed, and the issue’s 16.889730073595636 is the side’s 15-place floor.
The pair margins are the pose’s own, 2.04 to 2.79 × 10⁻¹³ of the centres’ separation,
median 2.13 × 10⁻¹³, about twice “about 1e-13 relative” (F5). The issue’s lineage counts
hold, all five, with T-290 reflected top to bottom in the new box, set against its
upper-left corner and paired by least summed move, a convention the issue does not name
(F6). The claim paragraph’s “built from Nate Chaoweeraprasit’s packing” misdescribes
T-290, as at #962 (F7). The certificate’s own squares, contracted by 1 − 2.036 × 10⁻¹³,
are accepted at side 16.8897300735924008, a side only RV-3 could register, and it is not
registered (F8). The band lies at 41.60° to 42.06° and the cluster, squares 42 to 45, at
−44.33° to −44.38°, not “about 42.1°” and “about −44.9°” (F12). The “9e-14 higher” side
of the local re-find is the decimal pose’s, 16.889730073595842, and the certificate’s
exact side is 1.13 × 10⁻¹³ below the cloud job’s (F13). The author’s comment on #947
gives this side as “9.74e-3 below this issue’s side”, where #947’s side is T-290’s and
the gap is 1.126 × 10⁻²; 9.74 × 10⁻³ is the gap on #962 (F14). The issue dates its
search for competing claims “2026-11-11 19:10 PST”, 03:10 UTC, ten minutes after it was
opened, against `0352d755`, which was `main`’s head throughout (F15). The witness’s
`softschema.schema` names `witness.schema.yaml`, which resolves to no file in the
author’s repository, and its `certificate.replay` names the file but not where to run
it, as at #947, #959 and #962; the adopted witness carries this repository’s own, and a
`sqpack` replay is the author’s first check run again (F11). The side is not s(m) + k
for any registry value below 269 and integer k up to 16 within 10⁻⁹; the nearest is
s(19) + 12, 4.1 × 10⁻³ away.

The issue credits the registry’s 207 and 70 and the lab’s 179 as “the band’s source
packing” while saying the designer used no donor packing (F10). The registry’s 207 and
70 witnesses come from PingYou Ltd’s PR 574 algebraic supplement, a release with no
licence file, kept here in the derived-only form.
If the band draws on them, whether a design taken from them needs a notice of its own is
the owner’s open decision on `think-71uq` (the review named `think-mdxq`, which closed
on 4 November). It is noted here, not decided.

Its eight questions for the author, informational and holding nothing open:

1. The margins and the pose’s side both point to a repair scaling of about 2 × 10⁻¹³, as
   at #947, #959 and #962. Was it that, rather than 10⁻¹³ (F5)?
2. The lineage counts reproduce with T-290 reflected in the new box’s horizontal
   midline, under the assignment of least summed move, as #962’s did with a reflection
   in its vertical midline.
   Is that the tool’s convention, and would the issue name it (F6)?
3. Would the author correct the claim paragraph’s and the README’s “built from Nate
   Chaoweeraprasit’s packing (itsnaka) improved by Evan Daniel and PingYou Ltd”, since
   the record and the issue’s own lineage paragraph have T-290 from a strip cut of Evan
   Daniel’s 304, below that packing (F7)?
4. The issue credits the 207, 70 and 179 packings as the band’s source while saying no
   donor packing or registry seed was used.
   What, if anything, does the designer take from them, and from which files (F10)?
5. The search for competing claims is dated 19:10 PST, after the issue was opened at
   19:00 PST. Which time was meant (F15)?
6. The comment on #947 gives the gap on #947’s side as 9.74 × 10⁻³; it is 1.126 × 10⁻².
   Would the author correct it (F14)?
7. Will the column-band designer be published?
   Would the lab promote with a contraction (`center_dilation` below 1), knowing that
   whether the record registers a side inside the repair dilation is its owner’s
   question (RV-3, F8)?
8. Would the author point `softschema.schema` at a file that resolves in his repository,
   and say in the replay line where to run it (F11)?

The case adopted the certificate as its house in the pass of 13 November 2026 under the
house rule, as T-297, in place of T-296, which keeps its certificate as history, with
Doğa Özden the packing’s finder; the registry’s 207 (PingYou Ltd), Ryan Xu’s n = 70
packing as Evan Daniel and PingYou Ltd improved it and his own n = 179 packing of #954
named as the band’s source packing, as the issue asks; Evan Daniel credited for the
optimizer; and T-296, his own band packing of #962, as the record it improves (the
review’s F9). The pass is dated by the day its pull request can merge at the earliest,
since the pass of 12 November had already moved 269 to T-296 and a day’s archive holds
one prior state a count.
Both strong generators ran on the new witness
([the runs](../../../cases/regularized_drawings/think-n73d-2026-11-12/README.md)), and
the selection, measured against this witness’s drawing, draws grid-slack’s 0.5-degree
view: light, uneven and near-axis squares, angle classes and hues 18, 54, 6, 19 and 19
against 0, 0, 0, 13 and 13, and full shared sides 729 and 781 against 842 and 864. Evan
Daniel’s driver refused its same-side view; his certified KKT solve lies 3.36 × 10⁻¹²
below the side, 1.04 of the certificate’s own contraction margin (3.236 × 10⁻¹²), held
at row 3 as a register candidate and not admitted, as at 156, 172, 179, 180, 199, 268,
270, and 269 for T-290 and T-296 (RV-3). The rigidity block, derived again on the new
witness, stays not rigid: 112 of its 269 squares translate, against 217 of T-296’s.

## What Is Not Established

- **Human oversight.** One AI review is retained; no human oversight record.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows.

## Credit and Licence

The packing is Doğa Özden’s, found by his lab’s column-band designer, which the issue
says took no donor packing, and quenched with Evan Daniel’s optimizer.
The issue asks that the improvement be credited to Özden, the band’s source packing and
the current record to their holders as the registry lists them, and the local optimizer
to Evan Daniel; it names the registry’s n = 207 packing, n = 70 (Ryan Xu; improved by
Evan Daniel and PingYou Ltd) and the lab’s own n = 179 of #954 as the band’s source
packing.
The record at 269 before this import was T-296, Doğa Özden’s own band packing of
#962, and before it T-290, his own packing from a strip cut of Evan Daniel’s n = 304
packing. The issue says the search and its code were written and run by AI agents
throughout and that the checks were run by code that did not produce the packing; it
says the issue and repository were prepared and posted by his AI agent, and that Özden
directed the work. The source makes its exact coordinates with this repository’s
promotion tool, so its lineage builds on this project.
The bibliography key is **[Özden s269 upper bound 2026-11-12]**.

The witness, the JSON, the decimal pose, the checker outputs, the README and the diff
image are published under CC BY 4.0, and `verifier/sqcheck.py` under the MIT licence,
copyright (c) 2026 Doğa Özden, as [source/LICENSE.md](source/LICENSE.md) states; it is
byte-identical to the `LICENSE.md` the lab added to its s299, s204 and s94 repositories
on 4 November 2026 and announced on #890
([comment](https://github.com/jlevy/squares/issues/890#issuecomment-6637821113)), and to
the one #962’s repository carries.
The diff image is pinned by digest only.
The source carries Evan Daniel’s MIT notice as `LICENSE-evand-square-packing.txt`, for
his quench code, byte-identical to the `LICENSE` the
[evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains, and
pinned against it.

## Commands

From `packing/`, with the project interpreter.
The identity measurement reads the house witness and its regularized view as they stood
at main 45e2ecca2, before this adoption replaced them, so it reproduces there; the
contraction margins read the packets and reproduce anywhere
`devtools.contraction_margin` is:

```bash
python -m devtools.acquire_source ozden-s269-upper-bound-2026-11-12 --checkout CHECKOUT
python -m devtools.acquire_source ozden-s269-upper-bound-2026-11-12 --check
python -m devtools.upper_bound_reports ozden-s269-upper-bound-2026-11-12 check-claims --write
python -m devtools.upper_bound_reports ozden-s269-upper-bound-2026-11-12 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ozden-s269-upper-bound-2026-11-12 check --replay
python -m devtools.upper_bound_reports ozden-s269-upper-bound-2026-11-12 sharp-controls
python -m devtools.measure_identity --n 269 'OZDEN=packet:ozden-s269-upper-bound-2026-11-12' \
  'T-296=packet:ozden-s269-issue962-2026-11-11' 'T-290=packet:ozden-s269-upper-bound-2026-11-11' \
  'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-269-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-269.yaml' \
  --out resources/web/ozden-s269-upper-bound-2026-11-12/measure/identity.json
python -m devtools.contraction_margin --n 269 'T-296=packet:ozden-s269-issue962-2026-11-11' \
  --against 'ozden-967=packet:ozden-s269-upper-bound-2026-11-12' \
  --out resources/web/ozden-s269-upper-bound-2026-11-12/measure/contraction-n269.json
python -m devtools.contraction_margin --n 269 'ozden-967=packet:ozden-s269-upper-bound-2026-11-12' \
  --out resources/web/ozden-s269-upper-bound-2026-11-12/measure/contraction-n269-own.json
python -m devtools.l_step_scan --with 269=S269 \
  --out resources/web/ozden-s269-upper-bound-2026-11-12/measure/l-step-scan.json
```

In the last command `S269` is the `exact_side` in the packet’s claim record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
