# Review: The Rational Upper-Bound Imports of 11 to 15 October (#506 to #607)

**Date:** 16 October 2026. **Verdict: accepted, for finite feasibility only.** The
seventeen certificates that six register entries cite, T-185 to T-190, prove the upper
bounds those entries state.
Every retained receipt job at the counts the entries cite reproduces here job for job,
as do the whole replayed rosters of four of the six packets; the third exact route
agrees with both maintained routes at every number they share; and every file of every
pinned scope was fetched here at its pin and found at the digest its packet records.
Each retained certificate is its upstream file, and each derived fact is the packing its
pinned source states, read again by the third route’s own readers.
The credit each entry states was measured pose by pose against the packing it names, and
thirteen findings are recorded, none blocking.
Every entry can take `V3`/`C3` with its confirming evidence entry and this review.
The houses should move at fifteen counts: to T-186 at 129, 154, 156, 175, 176, 204, 232,
264, 271, 302, 303 and 304, to T-187 at 146, to T-188 at 211 and to T-190 at 237
([Adoption per Count](#adoption-per-count)); T-185, above its case, and T-189, above
T-190, stay as history.
None can take `V4`/`C4` from this review alone.

This is the stage 4 review lane (W2) of the 16 October intake
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)), for
the six upper-bound entries registered on 15 October at `V0`/`C0`, written by an AI
agent (Claude, strong sub-agent tier, max reasoning) prompted separately from the import
and records lanes, with no shared context beyond their committed packets, register
entries and pull requests.
Its relation to the results is `project`. It moves no rung, writes no register row and
changes no case record; it says what the records lane should write.

## For the Authors

Francisco Couzo, Mykhailo Polkovskyi and Evan Daniel: each certificate below was decided
again here from the bytes this repository keeps, by two maintained exact routes and by a
third written separately, and each file was fetched again at its commit and found
unchanged. Every one is accepted as a finite upper bound at its exact side; nothing here
bears on optimality.

- **Francisco Couzo:** the 175 first committed in `f311f08` (held in #506’s release at
  `337078c`), the 211 of `487b058`, the 237 of #607 (`43ac7d2`) and the 237 first
  committed in `4e4c8ce`. Measured pose by pose, the 175 is your #488 packing at 175
  refined, no square moving more than 0.012; the 211 continues Daniil Ostashev’s #575
  arrangement as your #583 and #586 certificates did, five squares moving more than a
  tenth; both 237s refine Mykhailo Polkovskyi’s #593 packing, and the later one is the
  #607 packing with twelve squares moved by more than $10^{-3}$. Two questions.
  `certificates/n211.json` at `487b058` labels its seed as issue #501, but the seed
  certificate’s SHA-256, `7d35edaa…`, is that of Ostashev’s #575 `records/n0211.sqcert`:
  is #575 the seed you meant?
  And should the `4e4c8ce` 237 be recorded after #607’s, as it is now, or in its place?
- **Mykhailo Polkovskyi:** the twelve certificates of `70a033f` at 129, 154, 156, 175,
  176, 204, 232, 264, 271, 302, 303 and 304. Each places every square within
  $1.1 \times 10^{-3}$ of the certificate it tightens, so each is credited as a
  refinement of that packing, after the people whose packing it is.
- **Evan Daniel:** #606’s 146. It pairs square for square with Ryan Xu’s #432 packing
  and with Robert Barnett’s #505 refinement of it, nine squares moving more than a tenth
  and 137 staying within one, which agrees with your account of a different local
  minimum started from Xu’s packing.
  Your comparison of regularized views, agreement to about $10^{-7}$ outside a cluster
  of ten squares, is yours and was not re-run here; pose for pose, the certificates
  differ by more than $10^{-3}$ at 57 squares.

## Claims Covered

| Entry | Source and pin | Counts | Certificate kept |
| --- | --- | --- | --- |
| T-185 | Francisco Couzo, #506’s release, `franciscouzo/square-packing` at `337078c`, the 175 first committed in `f311f08` | 175 | retained `.cert`, no licence, as factual data |
| T-186 | Mykhailo Polkovskyi, no issue, `Mishapolk/square-packing-records` at `70a033f` | 129, 154, 156, 175, 176, 204, 232, 264, 271, 302, 303, 304 | derived facts from `.cert`, no upstream byte |
| T-187 | Evan Daniel, #606, `evand/square-packing` at `e006ce6` | 146 | retained `.cert`, MIT |
| T-188 | Francisco Couzo, no issue, at `487b058` | 211 | retained `.cert`, as factual data |
| T-189 | Francisco Couzo, #607, at `43ac7d2` | 237 | retained `.cert`, as factual data |
| T-190 | Francisco Couzo, no issue, at `58a7833`, first committed in `4e4c8ce` | 237 | retained `.cert`, as factual data |

Each entry’s claim prints its sides; the third route held each to its certificate, equal
or rounded up at the places printed (`registered_citations`), and found every print the
exact side. The packets’ other certificates, which no entry here cites, are not decided
by the third route: #506’s 304 and 305 (T-152, reviewed on 12 October), its unrecorded
308 and its beyond-horizon rows, the twelve counts of `70a033f` that PR #574 holds
smaller, and #607’s fifteen beyond-horizon rows, which T-189’s claim states and its
scope does not cover, and its seven Kevin Fang composites.
Those in a packet’s replayed roster were replayed with it, except #506’s and #607’s
uncited counts, priced below.

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) in a worktree at
`e2e018f32` (`origin/main`), niced, one process of this review at a time, on a four-core
host that other lanes shared at a load average of 2.5 to 17. `check` decides every
selected job serially in one process, through both maintained routes, and compares every
field with its retained row except the times; `--n` selects counts, and every run first
admits the packet’s whole receipt.
The importer has changed since 14 October in its comparisons and house readers only
(`a0eeee9d7`, `018e9de69`, `98df478e2`, `223b37a5f`, `15548357a`); its replay path, the
kernel of `devtools.evand_arrangement_reports` and both routes’ code are as the 14
October review ran them.

Each command is `python -m devtools.upper_bound_reports PACKET check --replay`, with
`--n` where shown; the 87 jobs replayed, 4,809,468 pair decisions in their receipts,
were all decided again and every one is equal to its retained row.
The replays that finished ran from 05:27:50Z to 06:12:20Z on 16 October, 2,454 seconds
of wall in all.

| Packet | Entries | Receipt jobs, pair decisions, job wall s | Replay here | Wall here |
| --- | --- | --- | --- | --- |
| `couzo-certificates-2026-10-11` | T-185 | 45, 5,234,106, 5,568.25; at 175, 3, 91,350, 58.79 | `--n 175`: every job equal, exit 0; the other 14 counts begun and stopped unfinished, below | 31 s, 05:30:13Z to 05:30:45Z |
| `mishapolk-kkt-refinements-2026-10-14` | T-186 | 72, 4,186,086, 2,194.11; at the twelve, 36, 1,912,890, 1,304.44 | `--n` the twelve: every job equal, exit 0; then `--n` the other 12 counts: every job equal, exit 0 | 1,337 s, 05:30:45Z to 05:53:01Z; 943 s, 05:56:37Z to 06:12:20Z |
| `evand-n146-2026-10-14` | T-187 | 3, 63,510, 21.33 | every job equal, exit 0 | 20 s, 05:27:50Z to 05:28:10Z |
| `couzo-verified-bounds-2026-10-14` | T-188 | 3, 132,930, 69.01 | every job equal, exit 0 | 45 s, 05:28:10Z to 05:28:55Z |
| `couzo-certificates-2026-10-14` | T-189 | 69, 31,386,744, 14,795.58; at 237, 3, 167,796, 48.51 | `--n 237`: every job equal, exit 0; the other 66 jobs priced, not run | 36 s, 05:29:37Z to 05:30:13Z |
| `couzo-n237-2026-10-15` | T-190 | 3, 167,796, 65.48 | every job equal, exit 0 | 43 s, 05:28:55Z to 05:29:37Z |

`check-claims` rebuilt all six frozen claim records equal, 1.7 to 16.5 seconds each
(05:53:01Z to 05:53:36Z). The receipts’ own totals, recomputed by the third route, are
the numbers each entry’s notes print.

The #607 packet’s other 22 counts, its fifteen beyond-horizon rows and Fang’s seven
composites, hold 66 jobs, 31,218,948 pair decisions and 12,382.15 route CPU seconds (3.4
CPU-hours) in the receipt.
The import lane decided every one of them twice, by `certify` and by a fresh serial
`check --replay` on 15 October (the packet’s README,
[Exact Replay](../../../packing/resources/web/couzo-certificates-2026-10-14/README.md#exact-replay)),
no entry reviewed here cites them, and the owner’s word for this pass was no compute
taking many hours. They are priced here, not run, as the PR #574 review priced its 64
receipts ([What Was Run](review-2026-10-14-upper-bound-imports-574.md#what-was-run)).

The #506 packet’s other 14 counts, T-152’s 304 and 305, the unrecorded 308 and eleven
beyond-horizon rows, hold 42 jobs, 5,142,756 pair decisions and 2,484.89 route CPU
seconds in the receipt.
Their replay here began at 06:12:20Z and was stopped unfinished at 06:28:24Z, when the
host’s load average reached 17 on four cores and the process had about a quarter of one;
no job had been found unequal by then, which a replay reports at once, but that is no
reproduction.
The import lane decided all of them twice on 11 October, by `certify` and a
complete `check --replay` (RY-8 of the
[12 October review](review-2026-10-11-upper-bound-imports-506.md)), and no entry
reviewed here cites them, so they too are priced, not run.

## The Third Route

`devtools.check_half_angle_area` at `e2e018f32`, unchanged since `e1fc548d9`, the
revision the 14 October review ran, decides each certificate again: every rotation on
the unit circle, containment by each square’s half-extent with no corner formed, and
pairs by the circumscribed-disc rule, else by the exact area of one square clipped by
the other’s closed half-planes.
Its tables name five of these packets not at all and #506’s only at its eleven requested
counts, so a driver written for this review ([Programs Run Here](#programs-run-here))
adds them in process: six keys, the counts the entries cite, and the packings each
certificate is measured against.
It then runs the route’s own `decide-imports` unchanged, with the route’s readers,
decisions, controls, comparisons, upstream checks and credit measurements; it adds no
reader and changes no decision.
The formats are ones the route already reads: Evan Daniel’s text, for all six, and the
center-basis Witness/v2 facts of T-186.

| Command | Outcome | Wall |
| --- | --- | --- |
| `python -I third_route_1016.py --workers 1 --json …`, which runs `decide-imports --workers 1 --imports '#506-n175' '70a033f' '#606' '487b058' '#607' '4e4c8ce'` with `--upstream` for each packet | 17 certificates, 422,712 pairs (8,138 clipped), 102 of 102 controls at their required outcome, 32 upstream checks, no disagreement, exit 0 | 179.76 s, 05:53:37Z to 05:56:37Z |

Per certificate: least wall clearance; least Euclidean distance between squares; pairs
decided (clipped); seconds for the positive and its six controls.

| Entry | n: wall; distance; pairs (clipped); time |
| --- | --- |
| T-185 | 175: $5 \times 10^{-21}$; $1 \times 10^{-20}$; 15,225 (414); 4.64 s |
| T-186 | 129: $5 \times 10^{-41}$; $1 \times 10^{-40}$; 8,256 (270); 2.63 s<br>154: $5 \times 10^{-41}$; $1 \times 10^{-40}$; 11,781 (342); 4.12 s<br>156: $5 \times 10^{-41}$; $1 \times 10^{-40}$; 12,090 (364); 5.51 s<br>175: $3.633 \times 10^{-78}$; $7.265 \times 10^{-78}$; 15,225 (366); 6.96 s<br>176: $3.624 \times 10^{-98}$; $7.249 \times 10^{-98}$; 15,400 (392); 12.35 s<br>204: $5 \times 10^{-101}$; $1 \times 10^{-100}$; 20,706 (452); 13.0 s<br>232: $5 \times 10^{-101}$; $1 \times 10^{-100}$; 26,796 (481); 13.88 s<br>264: $5 \times 10^{-101}$; $1 \times 10^{-100}$; 34,716 (580); 17.73 s<br>271: $5 \times 10^{-101}$; $1 \times 10^{-100}$; 36,585 (592); 14.81 s<br>302: $5 \times 10^{-41}$; $1 \times 10^{-40}$; 45,451 (695); 7.23 s<br>303: $5 \times 10^{-101}$; $1 \times 10^{-100}$; 45,753 (666); 12.92 s<br>304: $5 \times 10^{-41}$; $1 \times 10^{-40}$; 46,056 (695); 7.02 s |
| T-187 | 146: $5 \times 10^{-21}$; $1 \times 10^{-20}$; 10,585 (336); 1.92 s |
| T-188 | 211: $5 \times 10^{-21}$; $1 \times 10^{-20}$; 22,155 (489); 3.08 s |
| T-189 | 237: $1 \times 10^{-15}$; $1.602 \times 10^{-12}$; 27,966 (502); 3.19 s |
| T-190 | 237: $5 \times 10^{-21}$; $1 \times 10^{-20}$; 27,966 (502); 2.89 s |

Every positive passes, all 102 controls reach their required outcome, and the route
disagrees with nothing: every side, centre and rotation equals the maintained routes’
retained input, every least wall clearance equals theirs to the digit, every least
Euclidean distance is at least their separating-axis gap, and every side is the side its
frozen claim record and citing entry state, exactly.
Its 32 upstream checks held each of the five retained certificates to its fetched bytes,
each of T-186’s twelve derived facts to the packing its pinned `.cert` states, each of
those twelve sides to the `side_fraction` of `certificates/census.json` at `70a033f`,
and the 175, the 211 and the `4e4c8ce` 237 to the side the source’s
`certificates/README.md` prints at its pin.

The six controls are the precedent’s: two gross ones the kernel shares (a square
duplicated, a square moved by $S + 2$), the side at far-wall contact (accepted, the box
being closed) and $10^{-40}$ past it (refused), and the closest pair translated into
contact (accepted) and $10^{-30}$ of the centre distance further (refused).
No certificate here touches a wall or has two squares in contact, so every contact
control starts from a positive clearance.

## From Certificate to Bound

The argument is the one the
[#528/#529 review](review-2026-10-12-upper-bound-imports-528-529.md#from-certificate-to-bound)
gives: each certificate states a rational side $S$ and, per square, a rational centre in
$[0, S]^2$ and a rotation, either $t = \tan(\theta/2)$, in Evan Daniel’s format, or, in
T-186’s derived facts, a stated basis held to $c^2 + s^2 = 1$; exactly $n$ unit squares
lie in the closed box with pairwise disjoint interiors, so $s(n) \le S$. Every route
decides in exact `Fraction` arithmetic and none rounds, dilates or tolerates.
Guards are in the certificates and were believed by nothing: Couzo’s exact optima at
$1 + 10^{-20}$ (175, 211 and the `4e4c8ce` 237) and his #607 rational witness at 237,
whose least wall clearance is $10^{-15}$; Daniel’s 80-digit KKT point scaled by
$1 + 10^{-20}$ about the origin corner (146); and Polkovskyi’s KKT endpoints, cleared by
$5 \times 10^{-101}$ to $5 \times 10^{-41}$. Every certificate clears every wall and
every pair by a positive amount; the bound needs only the closed box.

## Custody

All six pinned scopes were fetched over HTTPS at their pins on 16 October between
05:37:13Z and 05:37:23Z, as blobless Git clones read at the pinned commits, into scratch
space outside the repository, and read as data; this host’s proxy refuses the codeload
tarballs the 14 October review fetched.
Each pinned commit’s tree is the `git_tree` its packet’s acquisition record states.
All 802 manifest lines have their pinned SHA-256, every one of the 752 `pinned_only`
entries its digest and byte count, and the 50 retained files of the five packets that
retain bytes (#506, #606, `487b058`, #607 and `4e4c8ce`) are byte for byte their
upstream blobs.
For the derived facts, the third route read each of T-186’s twelve pinned
`.cert` files with its own reader and found it to state the fact’s packing, side and
every pose, and the census to print each side.
That binds each fact to its pinned source as of this date (RX-7 of the #528/#529 review,
RQ-7 of 14 October, unchanged).

Two derived statements were re-read from the pinned files.
The seed certificate that `certificates/n211.json` names at `487b058` has SHA-256
`7d35edaa…`, which is Daniil Ostashev’s #575 `records/n0211.sqcert` byte for byte as the
#575 packet retains it, and not his #501 file of that name (`4b2275ab…`); and the seed
that `certificates/n237.json` names at `58a7833` has SHA-256 `b825369b…`, Polkovskyi’s
#593 `certificates/n237.cert` as the #593 packet pins it.
The census at `70a033f` credits all twelve recorded counts to “Mykhailo Polkovskyi
(ultra-precision KKT dual-verified optimum)”.

## Trust Boundaries

| Route | Decides | Shares with the others |
| --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, pairs by exact separating axes | the importer’s adapters, the parse and half-angle map of `evand_exact_certificates`; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same on rational corners | the same adapters, parse and map; `Fraction`; the separating-axis method |
| third route (V-check-half-angle-area) | unit circle, half-extent containment, disc rule then exact intersection area; its own readers | `Fraction` and the formats’ meaning only |

No source program ran.
The sources report their own checkers: Couzo’s runs of this repository’s `sqpack.verify`
(#506 and `487b058`, and at `37e6757` #607 and `4e4c8ce`), of Evan Daniel’s
`verify_cert.py` (#506, `487b058`, #607) and of his own `verify_bound_certificate.py`
(`4e4c8ce`); Daniel’s `verify_cert.py` and `verify_cert2.py` (#606); and the `70a033f`
README’s dual run of Daniel’s two, which the pinned tree does not contain.
Where a source ran this repository’s own checker, as Couzo reports, that run is the
producer’s and confirms nothing here; the replay ran the current routes from this
repository on the packet’s own bytes.
The third route’s author read both maintained routes and their adapters before writing
its readers, so it is not clean-room; it imports none of their parsing or deciding code,
and it is a second pair-deciding procedure within one method, `exact-algebraic`. The
review lane, the import lanes and the assistants of two sources are one AI system
family: #506 states that its search code and request were written with Claude (Claude
Code), and #606 that its search, checks and request were done with it; #607 states
OpenAI Codex, and Claude Code for earlier search; the #593 draft states Gemini.

## Credit and Lineage

`arrangement_gap` pairs each square with the nearest centre of the named packing under
the box symmetry whose one-to-one matching moves its farthest square least; `unmoved`
finds the symmetry that keeps most squares within $10^{-9}$. Each decides nothing.
The record’s sense of a refinement is a one-to-one pairing in which no square moves
beyond a tenth (T-150, T-152).

| Certificate | Against | Pairing | Moved beyond $10^{-3}$ / $10^{-2}$ / $10^{-1}$ | Largest move, turn | What it says |
| --- | --- | --- | --- | --- | --- |
| T-185 175 | T-140, Couzo | one to one, identity | 38 / 2 / 0 | 0.0112, 0.93° | his #488 packing refined, as stated |
| T-185 175 | T-125, Xu; T-130; T-158 | none; 86, 86 and 95 within 0.1 | — | — | not Xu’s packing by pose (RT-2), nor T-158’s |
| T-186 129 | T-174; T-162, Ostashev | one to one, identity | 0 / 0 / 0; 2 / 2 / 2 | $1.4 \times 10^{-4}$; 0.139 | PR #574’s packing re-solved, which is Ostashev’s with two squares moved |
| T-186 154 | T-182; T-172 | one to one, identity | 0 / 0 / 0; 153 / 61 / 19 | $6.4 \times 10^{-4}$; 0.29, 23.3° | T-182’s packing re-solved, which moves #583’s design well beyond a refinement |
| T-186 156 | T-174 and T-161; T-149, Ostashev | one to one, identity | 0 / 0 / 0; 30 / 8 / 1 | $7.6 \times 10^{-16}$; 0.20, 0.98° | Couzo’s continuation of Ostashev’s packing, padded |
| T-186 175 | T-174; T-158, Ostashev | one to one, identity | 0 / 0 / 0; 4 / 2 / 2 | $9.2 \times 10^{-16}$; 0.45 | PR #574’s packing padded, Ostashev’s with four squares moved |
| T-186 176 | T-174; #575’s 176, Ostashev | one to one, identity | 0 / 0 / 0 at both | $1.4 \times 10^{-4}$ | Ostashev’s #575 packing re-solved (RP-4 of the #574 review) |
| T-186 204 | T-174; T-162 | one to one, identity; a reflection | 2 / 0 / 0; 10 / 3 / 1 | $1.02 \times 10^{-3}$; 0.81 | PR #574’s packing re-solved |
| T-186 232 | T-174; T-158 | one to one, identity | 0 / 0 / 0; 5 / 4 / 4 | $2.8 \times 10^{-4}$; 0.45 | the same |
| T-186 264 | T-174; T-158 | one to one, identity | 0 / 0 / 0; 2 / 2 / 1 | $1.2 \times 10^{-15}$; 0.44 | PR #574’s packing padded |
| T-186 271 | T-174 and T-161; T-151, SQUISH | one to one, identity; a quarter turn | 0 / 0 / 0; 73 / 29 / 0 | $9.9 \times 10^{-16}$; 0.086, 5.4° | Couzo’s refinement of SQUISH’s packing, padded (RT-4) |
| T-186 302 | T-181; T-164, PingYou | one to one, identity | 0 / 0 / 0; 172 / 38 / 1 | $7.8 \times 10^{-16}$; 0.15, 12.3° | Couzo’s continuation of PingYou’s #564 arrangement, padded |
| T-186 303 | T-174; T-162 | one to one, identity; none, 297 in place | 0 / 0 / 0; — | $9.5 \times 10^{-16}$ | PR #574’s packing padded, Ostashev’s with one square moved across the box |
| T-186 304 | T-175, Ostashev | one to one, identity | 0 / 0 / 0 | $9.4 \times 10^{-16}$ | Ostashev’s #575 packing padded |
| T-187 146 | T-150, Barnett; T-168; T-174 | one to one, identity | 57 / 40 / 9 at each | 0.453, 1.8° | another arrangement of the same design (RT-5) |
| T-187 146 | T-125, Xu; T-146 | one to one, identity | 55 / 30 / 9; 52 / 35 / 9 | 0.478, 2.8° | Xu’s arrangement, nine squares moved beyond a tenth |
| T-188 211 | T-182 and T-181, Couzo | one to one, a reflection | 70 / 16 / 5 | 0.353, 2.6° | Couzo’s #583 and #586 packing moved, five squares beyond a tenth (RT-1) |
| T-188 211 | T-175, Ostashev | one to one, identity | 99 / 23 / 5 | 0.445, 1.9° | Ostashev’s #575 arrangement continued |
| T-188 211 | T-149, Ostashev’s #501 | none; 80 within 0.1 | — | — | not the packing the metadata’s seed label names (RT-11) |
| T-189 237 | T-183, Polkovskyi | one to one, a reflection | 41 / 21 / 0 | 0.033, 4.6° | a refinement of #593’s packing, as stated |
| T-189 237 | T-161; T-140 | one to one, a reflection | 62 / 27 / 7; 116 / 30 / 7 | 0.42; 0.21 | through #593, Couzo’s #561 design |
| T-190 237 | T-183 | one to one, identity | 42 / 21 / 0 | 0.066, 4.6° | a refinement of #593’s packing, as its metadata says |
| T-190 237 | T-189 | one to one, a reflection | 12 / 4 / 0 | 0.076, 1.5° | the #607 packing refined: 198 squares within $10^{-9}$ (RT-6) |

Each of T-186’s twelve regularization items states the identity measured here exactly:
`moved`, the squares beyond $10^{-3}$, is 2 at 204 and 0 elsewhere, and every `max_move`
is the largest displacement above.
T-185’s and T-190’s items do too; T-188’s and T-189’s state 72 and 42 squares beyond
$10^{-3}$ where the nearest-centre pairing here finds 70 and 41, the import lane’s
greedy matching pairing a few squares differently (RT-7). Measured against #593’s
certificate at each count, as the 14 October review did, T-186 equals #593 within
$3.2 \times 10^{-12}$ at 156, 176, 271, 303 and 304 (#593 restating PR #574’s packings
there, RP-2 of the #574 review), and at 146 and 211 the measures against #593 equal
those against T-150 and T-182; nothing there bears on these entries’ credit.

## Findings

Graded blocking, major, minor or note, each with the file and line it concerns.
None is blocking or major.

**RT-1, minor: T-188’s regularization is no refinement in the record’s sense.**
`packing/frontier/results.yaml` lines 25631 to 25643 list T-188’s 211 as a
regularization of T-182 with 72 squares moved and `max_move` 0.3535. Under the best
one-to-one pairing five squares move beyond a tenth, at most 0.353, against T-182 and
five against Ostashev’s T-175, at most 0.445. The 14 October review recorded the like
cases as another arrangement of the earlier design, with no regularization: T-182’s 154
and T-173’s 153. The records lane should do the same here, keeping the credit sentence
(Couzo, continuing Ostashev’s #575 arrangement as his #583 and #586 certificates did)
and stating the measurement in the notes, citing this review, or keep the item with the
measured fields and say that it is not a refinement.
Either way the credit is Couzo’s after Ostashev’s; the records lane should check that
the case record `adopt_houses` drafts at 211 says so.

**RT-2, minor: T-185’s claim calls T-140 a refinement of Ryan Xu’s packing.**
`packing/frontier/results.yaml` lines 24971 to 24974: “the arrangement of his T-140
certificate, itself a refinement of Ryan Xu’s packing, moved”.
By pose, no symmetry pairs T-140’s 175 with Xu’s (T-125) one to one, and at most 86 of
its 175 squares lie within a tenth of Xu’s; T-185 measures the same.
T-140’s own claim says it started from Xu’s packing and was moved by Evan Daniel’s `fq`,
the author’s basin hopping and David Ellsworth’s `refine_packing`. The sentence should
read “the arrangement of his T-140 certificate, which started from Ryan Xu’s packing,
refined”; “after Ryan Xu” stays the author’s statement (the source’s table: “seeded from
Ryan Xu”).

**RT-3, minor: T-186’s and T-187’s notes name the houses of `9b32da04d`.**
`packing/frontier/results.yaml` lines 25153 to 25255 call T-146, T-160, T-149, T-151,
T-101, T-151, T-146, T-146 and T-152 the case’s ceiling at 129, 154, 156, 176, 204, 271,
302, 303 and 304, and lines 25482 and 25509 call T-150 the ceiling at 146; their
packets’ claim records froze the record at `9b32da04d`, before #614 moved those houses.
On `main` the houses are T-162, T-182, T-161, T-165, T-162, T-161, T-181, T-162 and
T-175, and T-168 at 146. Each current house is among the reports each claim record
compares, and each certificate is below it, decided exactly here
([Adoption per Count](#adoption-per-count)), so no relation changes.
The rewritten notes should name the current houses, or say that the case’s ceiling is
the one of `9b32da04d`.

**RT-4, minor: T-186 names Couzo as the first finder at 154, 156, 271 and 302.**
`packing/frontier/results.yaml` lines 25094 to 25100, and the “Packing first found by”
column of the
[packet’s README](../../../packing/resources/web/mishapolk-kkt-refinements-2026-10-14/README.md#report-order-and-lineage)
(lines 151, 152, 158 and 159), credit each certificate after “that packing’s finder”,
Francisco Couzo, at these four counts.
The entries it chains through say more: T-161 continues Ostashev’s arrangement at 156
and SQUISH’s at 271, T-181’s 302 continues PingYou Ltd’s #564 arrangement, and T-182’s
154 continues Evan Daniel’s #552 arrangement; the poses here agree.
The credit sentence should follow each chain: at 156 Ostashev’s arrangement as Couzo
continued it, at 271 Nate Chaoweeraprasit’s SQUISH packing as Couzo refined it, at 302
PingYou Ltd’s arrangement as Couzo continued it, and at 154 Couzo’s arrangement after
Daniel’s. At 271 the record’s own rule would leave the packing with SQUISH, since
T-161’s 271 is a refinement of T-151 by pose (no square beyond 0.087, here and on 14
October), but T-161 lists no `regularizations`; adding that item is a change to an entry
outside this review, for the records lane or the owner.

**RT-5, note: T-187’s lineage can now be stated as measured.**
`packing/frontier/results.yaml` lines 25495 to 25501 leave “that it continues Ryan Xu’s
arrangement” in the author’s voice.
Pose for pose it pairs one to one with Xu’s T-125 under the identity, nine squares
beyond a tenth (at most 0.478) and 137 within one, and the same with Barnett’s T-150 (at
most 0.453): no refinement of either, and another arrangement of Xu’s design, which
supports both the author’s start and his “different local minimum”.
The record can say so in its own voice, with this review as `measured_in`, and keep
recording the 146 as a new packing.

**RT-6, note: T-190 refines T-189’s packing as well as T-183’s.** Under a reflection,
198 of its 237 squares lie within $10^{-9}$ of T-189’s and twelve move beyond $10^{-3}$,
at most 0.076; under the identity it is T-183’s with 42 moved, at most 0.066. Its
`regularizations` item (lines 25999 to 26011) names T-183, the seed its metadata states
by digest, and the credit is the same either way: Couzo after Polkovskyi.
Identity of poses establishes no derivation; two exact solves of nearly one contact
graph from one seed agree at most squares.

**RT-7, note: two `moved` counts differ by method.** T-188’s and T-189’s items (lines
25642 and 25888) state 72 and 42 squares beyond $10^{-3}$, from the import lane’s greedy
nearest-first matching; the nearest-centre one-to-one pairing here, under the same
symmetry, counts 70 and 41. Both are measurements and `max_move` agrees; the records
lane can keep either, naming the method.

**RT-8, minor: this review’s third-route run and custody check are not retained.** The
lane brief keeps this review to its document, so the driver, the report it wrote and the
custody program stay in scratch space ([Programs Run Here](#programs-run-here)); like
the 12 October review’s scratch decision of the 175, which T-185’s notes call not
retained, they confirm nothing on the record until kept.
The records lane can keep the third route’s decision by adding the six keys, rosters and
credit lines to `devtools.check_half_angle_area` (the driver’s tables, with tests as the
14 October roster has) and running it with `--receipts third-route-2026-10-16.json.xz`,
three minutes here; until then the confirming evidence should not list
V-check-half-angle-area.
The maintained replay, which `V3`/`C3` rest on, is the import lanes’ retained receipts,
reproduced here.

**RT-9, note: the lane’s compute was priced low.** The bead priced this review at under
one CPU-hour; the six packets’ receipts hold 17,256 route CPU seconds (4.8 CPU-hours),
12,382 of them at #607’s 22 counts and 2,485 at #506’s 14 that no entry here cites,
priced above and not run.
The runs here took about an hour of one niced process’s wall (3,634 s: 2,454 s of
completed replays, 964 s of the stopped one, 34 s of `check-claims` and 181 s of the
third route).

**RT-10, note: T-185’s next rung.** Lines 25032 to 25036 ask for a retained third-route
decision before the rungs rise.
A second route is recorded beside the rung and is not a condition of `C3`
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)): with
this review and its confirming evidence entry the rungs can rise on the maintained
replay already retained, and the bound stays superseded, by T-158 and now T-186.

**RT-11, note: T-188’s seed label.** `certificates/n211.json` at `487b058` labels its
seed issue #501 (line 15), but the seed’s SHA-256 on line 14 is Ostashev’s #575
certificate’s (Custody), and the poses agree: T-188 pairs with #575’s 211 one to one and
with #501’s not at all.
The entry’s statement by side (lines 25526 to 25529) holds by digest; the label is a
question for the author.

**RT-12, note: #639’s exact sides bear at 175, 204, 232 and 302.** Evan Daniel’s exact
algebraic sides of the record’s packings there agree with T-186’s to the 25 digits #639
prints (13.76417431748659662929018, 14.80866323438695656632290,
15.76417431748659662929018 and 17.87001385040446434446015); the print cannot order them
with T-186’s, and an algebraic certificate is no house candidate until the owner decides
RP-3 of the #574 review.
#639’s triage (PR #642) is another session’s; nothing is decided for it here.

**RT-13, note: a re-housed count may owe a regularization run.** PR #641, open and not
on `main`, would make the pull request that adopts a house regularize each count it
re-houses, at 5 to 15 CPU-minutes a count, or defer it with its bead; if it merges
first, the fifteen moves below owe that.

## Rungs

**`V3`/`C3` for all six entries.** Machine-replayed here: every certificate the entries
cite and its two kernel controls on both maintained routes, and every one of them with
its six controls on the third route, with certificates, replay commands, passing replays
and retained controls; each retained file held to its upstream bytes and each derived
fact to its pinned source; reviewed adversarially here.
`V` is the strongest verification anywhere, the record’s replay being `V3`’s predicate
for exact-algebraic evidence of any origin.
Not `V4`/`C4`: one AI review, no human oversight record.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

| Entry | Verdict | Blocking findings | Confirming evidence entry to write | Adoption |
| --- | --- | --- | --- | --- |
| T-185 | accepted; `V3`/`C3` supported | no | `E-couzo-506-n175-exact-feasibility`, scope 175 | none: above the case by $2.94 \times 10^{-3}$, superseded |
| T-186 | accepted; `V3`/`C3` supported | no | `E-mishapolk-70a033f-exact-feasibility`, the twelve counts | the house at all twelve counts |
| T-187 | accepted; `V3`/`C3` supported | no | `E-evand-606-n146-exact-feasibility` | the house at 146 |
| T-188 | accepted; `V3`/`C3` supported | no | `E-couzo-487b058-exact-feasibility` | the house at 211 |
| T-189 | accepted; `V3`/`C3` supported | no | `E-couzo-607-exact-feasibility`, scope 237 | none: T-190 is smaller; kept as history |
| T-190 | accepted; `V3`/`C3` supported | no | `E-couzo-4e4c8ce-n237-exact-feasibility` | the house at 237 |

**Verdict lines for the records lane.** For each entry, a confirming evidence entry as
tabled, with `assurance: verified`, `method: exact-algebraic`,
`performed_by: repository`, `origin: replayed-here`,
`relationship_to_generator: independent-implementation`, the packet’s certificate or
facts, the `check --replay` command with its `--n` where this review used one,
`replay_status: passed`, the verifiers V-sqpack-verify,
V-check-rational-witness-independent, V-evand-arrangement-receipts,
V-upper-bound-reports and V-evand-exact-certificates (and V-check-half-angle-area once
its decision is kept, RT-8), an `independence` record with `coverage: full` over the
certificates the entry cites, its `overlaps_producer` note naming the Claude assistance
#506 and #606 state, and this review as `independence_record` and `external_review`
(`informally-verified`); on each reported entry, `external_review` naming this review;
on each register entry, the evidence, the rungs, a `reviews` item (`kind: adversarial`,
`reviewer_kind: ai`, `relation: project`, `verdict: accepted`), the controls
(`test_check_half_angle_area.py` beside `test_upper_bound_reports.py` once the third
route’s roster lands with its tests), and claim, notes and `next_rung` rewritten
together. `E-couzo-506-exact-feasibility` covers #506’s eleven requested counts and not
175, which T-185 cites under its own source key, so 175 takes an entry of its own.
T-189’s may also cover the fifteen beyond-horizon rows its claim states, on the import
lane’s two replays, which this review did not repeat.

## Significance

| Entry | Draft | Here | Why |
| --- | --- | --- | --- |
| T-185 | `S1` | `S2` | a refinement of the author’s T-140 packing to a new smallest side $1.70 \times 10^{-6}$ below it, as T-165 ($2.5 \times 10^{-10}$) and T-167 (`S2`); not padding, and not a step of T-172’s $6.7 \times 10^{-5}$ (`S3`); T-158 superseding it does not lower it |
| T-186 | `S1` | `S1` | padding and exact re-solves of credited packings, $1.25 \times 10^{-94}$ to $1.79 \times 10^{-19}$ below the nearest report, as T-174 and T-170 |
| T-187 | `S2` | `S2` | another arrangement of Xu’s design $1.38 \times 10^{-8}$ below the case, as T-167 |
| T-188 | `S1` | `S2` | a further arrangement of Ostashev’s design $9.29 \times 10^{-6}$ below the case, five squares moved beyond a tenth: more than the re-solves of T-168 and T-169 (`S2`), less than T-172’s $6.7 \times 10^{-5}$ (`S3`); “routine” fits padding, as T-166’s (`S1`) |
| T-189 | `S2` | `S3` | a refinement of #593’s packing $1.01 \times 10^{-4}$ below the case, as T-172 ($6.7 \times 10^{-5}$) and T-183 (`S3`); the draft calls it routine “as T-188 and T-190 are”, citing a later result (RQ-2 of 14 October) |
| T-190 | `S1` | `S2` | a refinement of the #607 packing $2.40 \times 10^{-11}$ below it, as T-165 ($2.5 \times 10^{-10}$, `S2`), above the padding of T-166 and T-170 (`S1`) |

`by` should name this review.

## Adoption per Count

Each comparison exact, sides rounded up at sixteen places, decided by `import_side` from
each packet; the case is its verified ceiling on `main` at `e2e018f32`. Each recommended
house is the smallest exact certificate at its count among the reviewed entries,
replayed on both maintained routes and the third route with no blocking defect, and
below the case. T-174 (PR #574) is held for the owner (`devtools.select_houses.HELD`),
and a hold skips only the held entry; T-174 is shown where it is smaller than the case,
and T-186 is below it at every count they share, so the hold decides none of these
houses.
No other open report is smaller at these counts: #639’s algebraic sides are named
where they bear (RT-12), and Couzo’s `4e4c8ce` index holds, inside the corpus, T-188’s
and T-190’s certificates and otherwise other reports’ certificates or none smaller than
the smallest earlier report (its packet’s
[README](../../../packing/resources/web/couzo-n237-2026-10-15/README.md#what-the-commits-change)).

| n | Case ceiling, house | Reviewed and pending certificates, smallest first | House |
| --- | --- | --- | --- |
| 129 | 11.8700138504044644, T-162 | T-186 below the case by $1.19 \times 10^{-19}$; T-174 (held), $1.10 \times 10^{-21}$ above T-186 | T-186, Polkovskyi after PingYou after Ostashev |
| 146 | 12.5837822039508343, T-168 | T-187 12.5837821901518604, below by $1.38 \times 10^{-8}$; T-174 (held), $1.3 \times 10^{-79}$ below the case | T-187, Daniel after Xu |
| 154 | 12.9212065771326311, T-182 | T-186, below by $1.29 \times 10^{-19}$ | T-186, Polkovskyi after Couzo |
| 156 | 12.9791658538342765, T-161 | T-186, below by $1.30 \times 10^{-19}$; T-174 (held), $1.19 \times 10^{-34}$ above T-186 | T-186, Polkovskyi after PingYou after Couzo after Ostashev |
| 175 | 13.7641743174865967, T-158 | T-186, below by $1.38 \times 10^{-19}$; T-174 (held), $7.23 \times 10^{-75}$ above T-186; T-185 13.7671190241983643, above the case by $2.94 \times 10^{-3}$; #639 (RT-12) | T-186, Polkovskyi after PingYou after Ostashev |
| 176 | 13.8076372268022796, T-165 | T-186 13.7958723184364073, below by $1.18 \times 10^{-2}$; T-174 (held), $1.25 \times 10^{-94}$ above T-186 | T-186, Polkovskyi after PingYou, on Ostashev’s #575 packing |
| 204 | 14.8086632343869566, T-162 | T-186, below by $1.48 \times 10^{-19}$; T-174 (held), $1.83 \times 10^{-21}$ above T-186; #639 (RT-12) | T-186, Polkovskyi after PingYou after Ostashev |
| 211 | 14.9935589139740062, T-182 | T-188 14.9935496262994211, below by $9.29 \times 10^{-6}$ | T-188, Couzo after Ostashev (RT-1) |
| 232 | 15.7641743174865967, T-158 | T-186, below by $1.58 \times 10^{-19}$; T-174 (held), $1.45 \times 10^{-74}$ above T-186; #639 (RT-12) | T-186, Polkovskyi after PingYou after Ostashev |
| 237 | 15.9027050578663668, T-183 | T-190 15.9026036382595969, below by $1.01 \times 10^{-4}$; T-189 15.9026036382835755, $2.40 \times 10^{-11}$ above T-190 | T-190, Couzo after Polkovskyi |
| 264 | 16.7747351323878329, T-158 | T-186, below by $1.68 \times 10^{-19}$; T-174 (held), $1.75 \times 10^{-74}$ above T-186 | T-186, Polkovskyi after PingYou after Ostashev |
| 271 | 16.9489923564512057, T-161 | T-186, below by $1.69 \times 10^{-19}$; T-174 (held), $2.09 \times 10^{-34}$ above T-186 | T-186, Polkovskyi after PingYou after Couzo after Chaoweeraprasit (RT-4) |
| 302 | 17.8700138504044644, T-181 | T-186, below by $1.79 \times 10^{-19}$; #639 (RT-12) | T-186, Polkovskyi after Couzo after PingYou |
| 303 | 17.9099582910699080, T-162 | T-186, below by $1.79 \times 10^{-19}$; T-174 (held), $2.43 \times 10^{-74}$ above T-186 | T-186, Polkovskyi after PingYou after Ostashev |
| 304 | 17.9294277580751750, T-175 | T-186, below by $1.79 \times 10^{-19}$ | T-186, Polkovskyi after Ostashev |

Where a side is not printed it equals the case’s at sixteen places.
T-185 and T-189 are recorded and superseded, kept as history.
The earlier houses stay retained as history, and the reported and verified ceilings move
together. Credit follows each entry and its `regularizations`, as the column says: the
twelve of T-186 after the packing each tightens, T-187 Daniel’s after Xu’s start, T-188
Couzo’s after Ostashev’s arrangement, and T-190 Couzo’s refinement of Polkovskyi’s
packing.

The witnesses at T-186’s twelve counts total 1.56 MB on `main`, and T-186’s facts 1.73
MB uncompressed: on that estimate these houses replace witnesses with ones of about the
same size, far from the 18.5 MB that holds PR #574’s; the records lane measures it.
By the coordinator’s rule of 15 October, T-186 takes the house at the nine counts it
shares with T-174 once confirmed, which also leaves the hold on T-174 deciding nothing
at them; the owner may want to know that, and nothing waits on it.

## Proposed Record Changes

For the records lane; this review writes none of them.

- The confirming evidence and register fields under [Rungs](#rungs), for all six.
- Claims, notes and `next_rung`: RT-1 on T-188’s regularization; RT-2 on T-185’s
  sentence; RT-3’s houses in T-186’s and T-187’s notes; RT-4’s credit chains in T-186’s
  claim; RT-5’s measured lineage on T-187 and RT-6’s on T-190, with this review as
  `measured_in`; RT-10’s next rung for T-185.
- Significance as tabled, `by` naming this review.
- Houses at the fifteen counts of [Adoption per Count](#adoption-per-count), with
  `source-coverage.yaml` overrides and `priority_notes` for the earlier houses, and the
  regularization each re-housed count owes if PR #641 has merged (RT-13).
- The third route’s roster and receipts, if the record is to cite it (RT-8), and then
  `verifiers.yaml`: V-check-half-angle-area’s note gains this review’s roster.
- For the owner: RT-4’s question whether T-161’s 271 is listed as a regularization of
  SQUISH’s packing.
- For the authors, in the replies drafted at stage 7: the questions under
  [For the Authors](#for-the-authors).

## Programs Run Here

The lane brief keeps this review to its document, so the programs it wrote stay in the
session’s scratch space and are described here; they run only this repository’s
maintained tools and code written for this review, read the sources as data, and write
nothing in the repository.

- **`custody.py`** made one blobless clone per source repository over HTTPS, checked out
  each packet’s manifest paths at its pin, and held the tree, every manifest line, every
  `pinned_only` entry and every retained file to the packet’s acquisition record,
  writing the pinned files where the third route’s `--upstream` reads them.
  It printed, per packet, the pin, the tree, 13, 13, 40, 52, 599 and 85 manifest lines,
  the `pinned_only` and retained counts, and no problem.
- **`third_route_1016.py`** added the six keys to `devtools.check_half_angle_area`’s
  tables (`ALL_IMPORTS`, `IMPORTS_1014` and `REGISTERED`, `ROSTERS`, `CREDITED`,
  `CREDITED_READERS` for T-182, T-183 and T-189, `ALSO_MEASURED` with #593) and ran its
  `main` with `decide-imports`; it printed the route’s own report, summarized in
  [The Third Route](#the-third-route), and wrote its JSON report.
  The credit lines it adds are the pairs in [Credit and Lineage](#credit-and-lineage).
- **`adoption_table.py`** read each case record’s verified ceiling and each packet’s
  exact side through `upper_bound_reports.import_side`, and printed the exact
  comparisons of [Adoption per Count](#adoption-per-count).
- **`receipt_totals.py`** and **`receipt_subsets.py`** summed each receipt, whole and
  over the counts named here, with `receipt_summary`; **`summarize_third_route.py`**
  printed the third route’s JSON report as these tables.
  None of the three decides anything.
- **`run_serial.sh`** ran each heavy command niced under one lock file, so that one
  process of this review ran at a time, and logged its UTC start, end, wall and exit
  status.

## The Earlier Review of the 175

One earlier review touched a certificate reviewed here: the
[12 October review of #506](review-2026-10-11-upper-bound-imports-506.md), whose RY-10
decided the 175 on the third route in scratch, with its six controls, and kept no
decision.
Before its findings were written, this review saw of it only what T-185’s notes
say of RY-10 and its title and opening lines; it read the rest afterwards.

The two agree. Each finds the side 13.7671190241983643 rounded up at sixteen places, a
pass with all six controls, a least wall clearance of exactly $1/(2 \cdot 10^{20})$ and
a least distance of $10^{-20}$, equal to the retained positive job’s inputs and margins,
and the side printed in the pinned `certificates/README.md`. They differ where the
record has moved since: the 12 October review found the 175 the smallest side known at
its count, before Ostashev’s #528 (T-158) was reported, while here T-158 and T-186 are
smaller and T-185 is recorded as superseded.
That review measured no lineage for the 175, so RT-2’s measurement against T-140 and
Ryan Xu’s T-125 is new.
Neither review’s third-route decision of the 175 is retained (RT-8), and both note that
the reviewer and the source’s assistant are one model family (RY-9 there).

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty or priority; no run of any
source’s checker, solver or search; no replay here of #607’s 22 counts or #506’s 14 that
no entry here cites; no decision of the beyond-horizon rows or of the certificates no
entry cites; no identification of derivation beyond the measurements above; no retained
third-route receipt (RT-8); no `derive --check` from a Git checkout; no house adoption
or case-record change; nothing for #639, whose triage is another session’s.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
