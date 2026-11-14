# Roberto Ono’s s(147) Certificate at b5636fd

This packet retains part of
[RobertoOno/squares-in-square](https://github.com/RobertoOno/squares-in-square/tree/b5636fd6694d2cc7aa5811ae33f441268b81b714)
at `b5636fd6694d2cc7aa5811ae33f441268b81b714` (committed 2026-11-14T20:26:58Z), the
repository’s `main` when it was fetched at 21:07Z on 14 November 2026, for
[issue #985](https://github.com/jlevy/squares/issues/985), as
[ono-issue984-2026-11-14](../ono-issue984-2026-11-14/README.md) does for #984 at 228.
That packet’s README says how the pin relates to `fce076f`, the commit both issues name,
55 seconds before #985 was posted at 20:11:26Z: every n = 147 file retained here has the
same Git blob at both.
The certificate was first committed in `be713b7` (2026-11-11T22:15:40Z). This is the
account’s first contribution to this repository, with #984.

## What the Source Claims

- `runs/2026-11-11_fable-5.2/certificates/n147_S65104355.json`, an exact rational
  certificate of 147 unit squares, each its centre `(cx, cy)` in [0, S]² and
  `t = tan(θ/2)`, bounds s(147) by its rational side, whose 12-place ceiling #985
  prints, 12.651043556588. The issue also prints the side to 30 places before an
  ellipsis, 12.651043556587694471904370629016, the side’s floor there.
  It states the gain on the registry’s 12.65685424949238 (7 + 4√2, read at `main`
  `fa980f8e`) as 0.005810692904685, the exact gap’s floor at 15 places, and that no
  request is open for this count.
  It claims an upper bound only: no optimality, KKT or rigidity claim.
- `evidence/registration/n147.cert` is the same packing as text.
  `n147.strict.cert` and `n147.strict.json` are the packing moved by (10⁻¹⁵, 10⁻¹⁵) in a
  square of side S + 2 × 10⁻¹⁵; the issue says the packing touches the four walls.
- The issue reports the author’s runs of `verify.py` (all 10,731 pairs) VALID,
  `indep_check.py` (328 close pairs) PASSED and `fu_strict_check.py` on the strict copy
  STRICT VALID, least pair margin 3.003 × 10⁻¹⁰ and least wall margin 10⁻¹⁵, with the
  same statement of what the checkers share as #984’s. Those statements are the
  author’s; no source program ran here.
- **The leaderboard, disclosed first.** The issue opens by saying the packing does not
  beat the Kaggle per-puzzle leaderboard’s side-only entry at 147,
  12.651043553172632772258400… (team Nevska, 7 November), 3.415 × 10⁻⁹ below the side,
  which supplies no packing.
- **Lineage.** The registry’s n = 229 record (Evan Daniel, 20 October 2026, side
  15.6501615138764…, `W-known-best-n229`), a three-wide diagonal band of tilted squares
  between two corner-anchored grids, with every square of 13 ≤ x + y < 19 deleted and
  the squares beyond moved by (−3, −3), which removes one period of the band; the 147
  squares that remain overlap by at most 0.010, and a penalty step and an
  exact-constraint sequential-LP polish (`search/opt.py`) remove the overlaps at a cost
  of 0.00088 in side. The issue says other cut positions and seven other published copies
  or versions of the n = 229 packing give sides from 12.651043557 to 12.651056453, that
  the registry’s n = 147 packing, the 45-degree arrangement shared with n = 148, is a
  different arrangement, and asks that Daniel’s n = 229 packing be credited as the
  start.
- `REPORT.md`, retained in the 228 packet, ranked n = 147 first among the run’s targets
  before any attack, since its record was the n = 148 packing less a square, and records
  the same withdrawal of the word improvement as at 228.
- **AI assistance.** As at #984: an AI coding agent (Claude, by Anthropic) working in
  the repository’s harness, directed by a person who read the request before it was
  posted.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
The scope is 24 files: 11 retained under [source/](source/), 12 pinned against their
byte-identical copies in the 228 packet, and one raster pinned by digest.

| File | Bytes |
| --- | --- |
| `certificates/n147_S65104355.json` | 45,156, the claim |
| `evidence/registration/n147.cert` | 38,818, the same packing as text, which the reader holds equal to the JSON |
| `evidence/registration/n147.strict.cert`, `n147.strict.json` | 45,585 and 49,948: the copy moved off the walls |
| `evidence/registration/` check outputs and `issue_n147.md` | the author’s verifier, clipping and strict-check outputs, and the issue as posted |
| `search/opt.py` | 11,330, the polish the issue names, never executed here |
| `LICENSE`, `README.md`, `VERIFIER.sha256`, `verify.py`, the run’s `REPORT.md`, `RUN.md` and `FOLLOWUP.md`, its two notes, `search/README.md`, `indep_check.py` and `fu_strict_check.py` | pinned against the identical copies the 228 packet retains from the same pin |
| `evidence/cand147.png` | 143,158, pinned by digest: a picture that decides nothing |

The SHA-256 the issue states for the JSON (`fce8c8c2…d2038135`), the text copy
(`0e092607…cc11af`) and the strict copy (`cfe00796…a7a6ce`) are the files’.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `473577f42` on 14
November 2026), through the `ono-json` reader:

- **147:** exact side 12.6510435565876945 rounded up at 16 places, below the case’s
  house, the Kingbird catalogue’s 7 + 4√2, by 5.8107 × 10⁻³, the 0.005810692904685 the
  issue states. The comparison reads the house at the exact ceiling T-155 verifies, its
  retained view’s side, 12.65685424949238019520675489684, which the gap to 7 + 4√2
  itself differs from by about 1.2 × 10⁻³⁰. No register bound is pending adoption at
  147\.

## Report Order

The
[ledger of 14 November for this lane](../../../campaign/issue-intake/upper-bounds-984-985-20261114/README.md)
records this claim at 147 as a new packing, the only report at that count; the side-only
leaderboard entry the issue states first is unpublished and states no packing, so it is
no report and is recorded as context only.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-155’s exact view of the
house’s packing, the 45-degree arrangement 147 shares with 148, and wrote
[measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.
No symmetry of the box pairs the two one to one by nearest centres.
The optimal assignment, best under symmetry 1, moves 140 squares beyond 10⁻³, 116 beyond
0.01 and 92 beyond 0.1 (largest 1.13164), and turns 78 squares by more than 10⁻⁶
radians.
Tilted beyond a degree: 44 here, at 25.84 to 27.72 degrees, all one way, against
the house’s 64, all at 45 degrees.
So it is a new arrangement relative to the house’s packing, as the issue says; its band
is Daniel’s 229’s, cut.
The 229 packing it starts from is at another count, which the measurement cannot pair.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 64,386 pair decisions, 10.6 seconds of job wall time
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 3.003 × 10⁻¹⁰, squares 101 and 108, the margin the author’s strict check reports,
exactly. `check --replay` decided the three jobs again.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
10⁻³⁰ past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)), with the
expected verdicts stated in a plan hashed before any run of either certificate (SHA-256
`a2ed80d123eab30d33f701c2636dfa77220924242f4ffd9a6ebce8c8d5f89212`, 21:12:34Z on 14
November, recorded on the bead).
The side lowered by the least far-wall clearance, 0, the least-gap pair closed (square
108 toward 101) and every square moved toward the nearer near wall by 0 were each
accepted at contact with margin 0 and refused past it.
Square 108 enlarged to its partner was refused at contact for its shape alone; square 3,
which touches its wall, grew by 0 and was accepted at contact; both were refused 10⁻³⁰
past it for the overlap or the wall as well.
Both routes refused a duplicated square.
All 11 were as stated in advance.
The two routes share what the 228 packet’s README says they share.

## The Gain Against Padding

`devtools.contraction_margin` contracted each certificate uniformly about the origin to
first contact and boxed it, each contracted packing decided on both maintained routes:

- **The house**, T-155’s exact view at 147: margin 0, squares 1 and 2 of its grid
  touching ([measure/contraction-n147-t155.json](measure/contraction-n147-t155.json)),
  so the whole gain, 5.8107 × 10⁻³, lies outside the house’s padding and RV-3
  (think-ruu2) does not reach it.
- **This certificate**: margin 2.934 × 10⁻⁹ (1 − λ\* about 2.557 × 10⁻¹⁰, squares 145
  and 147) ([measure/contraction-n147-own.json](measure/contraction-n147-own.json));
  contracted, it would be a square about 2.93 × 10⁻⁹ smaller, still about 4.8 × 10⁻¹⁰
  above the side-only leaderboard entry.
  Nobody reported that side, and it is not registered (RV-3).

## The L Step

`devtools.l_step_scan`, with this side stood in for 147’s ceiling
([measure/l-step-scan.json](measure/l-step-scan.json)), finds the same L-step
improvements and monotonicity consequences as on `main`, and one fewer L extension: the
house at 147, 7 + 4√2, was the L step from 124’s 6 + 4√2, and this side is below it.
The L step from this side lands at 172 above its house, so the bound carries to no other
count.

## Stage 4 Review

The stage 4 review of 14 November 2026
([review-2026-11-14-ono-984-985.md](../../../../docs/project/reviews/review-2026-11-14-ono-984-985.md),
lane L163), written blind to this lane throughout, accepts this certificate with #984’s,
fourteen findings, all notes, none blocking, and scores it S3, as the record scored
T-196 at 260 and T-248 at 299. Its clean-room checker decides every square, wall and all
10,731 pairs twice, all 20 of its controls at this count as stated, and accepts the
squares in the box of the claim’s own side, 12.651043556588 (F4). This lane read it as
the [228 packet’s README](../ono-issue984-2026-11-14/README.md#stage-4-review) says: its
frozen findings at 21:45Z and its final head at 21:56Z, after its own replay, controls
and measurements (21:29Z) and registration (21:44Z) were committed.
Read against this packet’s receipts, the review’s least pair margin (3.00262 × 10⁻¹⁰,
squares 101 and 108) is the replay’s exactly, square 3, which the sharp controls grew at
its wall, is one of its three wall contacts (3 at the left, 65 at the bottom, 134 at the
top), and its contraction receipts for T-155 (0, squares 1 and 2) and this certificate
(2.934 × 10⁻⁹, squares 145 and 147) and its identity measurement against the house’s
packing equal [measure/](measure/)’s. No disagreement.

What the review adds:

- **Three walls, not four** (F5): no square touches the right wall, cleared by 1.92 ×
  10⁻¹³ at square 106, so the side is the packing’s extent in y.
- **The lineage reproduces exactly** (F10): the stated cut of Evan Daniel’s 229 leaves
  147 squares with deepest overlap 0.00978, and the certificate is a refinement of that
  seed, one to one with it, no square moved beyond 0.046.
- **A new arrangement** relative to T-101, T-155 and the house, which is the 148 house
  less one corner square, so s(148) is not moved; the case’s listed conjectured optimum,
  7 + 4√2, is beaten, as the catalogue’s values at 260 and 299 were (F12). No s(m) + k
  is the side within 10⁻⁹ but the old record itself, s(66) + 4 and s(124) + 1.
- T-101, the earlier exact certificate of the house’s packing, has margin 1.27 × 10⁻¹⁹,
  and RV-3 does not apply (F11).

Its questions for the author are shared with #984 and listed in the 228 packet’s README.

## What Is Not Established

- **Human oversight.** One AI review is retained; no human oversight record.
- **Optimality** of any kind.
- **The lineage** the source states, beyond what the measurement above shows; the cut
  from Daniel’s 229 was not rebuilt here.

## Credit and Licence

The packing is Roberto Ono’s, found by the AI agent his harness directs, from Evan
Daniel’s packing of 229 squares with one band period cut out, as the issue says and asks
to be credited. The record at 147 before this import was the Kingbird catalogue’s
45-degree packing at 7 + 4√2, which T-155’s exact ceiling verifies.
The harness reads its starting packings from this registry’s witnesses, so its lineage
builds on this project.
The bibliography key is **[Ono issue 985 2026-11-14]**. The repository is published
under the MIT licence, copyright (c) 2026 Roberto Ono, which the 228 packet retains as
`source/LICENSE` and this packet pins against.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source ono-issue985-2026-11-14 --checkout CHECKOUT
python -m devtools.acquire_source ono-issue985-2026-11-14 --check
python -m devtools.upper_bound_reports ono-issue985-2026-11-14 check-claims --write
python -m devtools.upper_bound_reports ono-issue985-2026-11-14 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports ono-issue985-2026-11-14 check --replay
python -m devtools.upper_bound_reports ono-issue985-2026-11-14 sharp-controls
python -m devtools.measure_identity --n 147 'ONO=packet:ono-issue985-2026-11-14' \
  'T-155=witness-center-basis:cases/regularized_bounds/views/n-147.yaml.gz' \
  --out resources/web/ono-issue985-2026-11-14/measure/identity.json
python -m devtools.contraction_margin --n 147 \
  'T-155=witness-center-basis:cases/regularized_bounds/views/n-147.yaml.gz' \
  --against 'ono-985=packet:ono-issue985-2026-11-14' \
  --out resources/web/ono-issue985-2026-11-14/measure/contraction-n147-t155.json
python -m devtools.contraction_margin --n 147 'ono-985=packet:ono-issue985-2026-11-14' \
  --out resources/web/ono-issue985-2026-11-14/measure/contraction-n147-own.json
python -m devtools.l_step_scan --with 147=S147 \
  --out resources/web/ono-issue985-2026-11-14/measure/l-step-scan.json
```

In the last command `S147` is the `exact_side` in the packet’s claim record.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
