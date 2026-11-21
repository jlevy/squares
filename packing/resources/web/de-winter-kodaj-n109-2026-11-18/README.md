# Tomáš Kodaj’s 109 as Joost de Winter Transcribed It, at aae089c

This packet retains part of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/aae089c37a2d3fb91b161a1b3a45f06a41277d18),
a watched repository, at `aae089c37a2d3fb91b161a1b3a45f06a41277d18` (committed
2026-11-18T07:30:49Z, “Add Tomáš Kodaj’s public coordinates for n = 109 (issue #1012)”).
That commit adds the folder `n109_kaggle/` and nothing else; its child `7232328`
(07:31:33Z) deletes the folder again, and
[the comment of 18 November on issue #1012](https://github.com/jlevy/squares/issues/1012#issuecomment-6972165182)
(07:33:46Z) attaches the same files as `Issue_1012_n109_Kodaj_Coordinates.zip`.

The attachment is not readable from this session: the session proxy answers GitHub’s
`user-attachments` addresses with HTTP 403, and the lane did not route around it.
Lane w10-1118 read the zip on 18 November (42,790 bytes, SHA-256 `b0134067…4db1`) and
recorded its members’ digests on think-wvr8.
`n109_tomkodaj.csv`, `n109_tomkodaj.yaml` and `verification.txt` here have exactly those
digests. The zip’s `README.txt` (3,298 bytes) is not this folder’s `README.md` (2,038
bytes), and is not retained.

Intake lane c7-pointers (think-wvr8) retained it, replayed it and measured it on 20
November 2026.

## What the Source Claims

- `n109_kaggle/n109_tomkodaj.yaml` is a corner Witness/v2 of 109 unit squares at side
  547464479047171949843/(5 × 10¹⁹) = 10.94928958094343899686, so s(109) ≤
  10.949289580944 rounded up. The issue’s first print, 10.949289580943, was rounded to
  nearest and lies below the exact side, so it bounds nothing; the comment says so.
- **Provenance.** The folder README and the comment say the witness is an exact
  transcription of `n109_tomkodaj.csv`: the 109 rows for n = 109, unchanged, of Tomáš
  Kodaj’s Kaggle dataset “Squares in Squares: strips and bands (coordinates)”, version
  2, 13 November 2026, under CC0. Each orientation is a rational tan(angle/2), so every
  square has exactly unit sides, and the centres are translated into the first
  quadrant. They give the SHA-256 of the full `submission.csv` as `7700b20d…489b`.
  Kaggle is not readable from this session, so that digest, the dataset’s date and its
  licence are the source’s word.
- **Checker.** `verification.txt` is this repository’s independent rational-corner
  checker at `f9ddfeeef`: “VERIFIED: 109 squares, 5886 pairs”, least pair gap about
  2.0 × 10⁻¹⁵.
- **Credit.** Kodaj publishes the coordinates and refers readers to his source notebooks
  for the original credits. Navneet Prabhat’s public compilation contains the same
  packing, at about 10.94928958094337. Guilherme Dias da Fonseca published a 109-square
  pinwheel earlier, on 6 November 2026, at 10.949392392. Issue #958 documents
  Samanyu-dev’s pinwheel in `best_fit_101_500.csv` at 10.94928958094538. Who made the last
  numerical refinement is unconfirmed, and the comment asks for credit as this
  repository’s sources support. The transcription was made with GPT-6.2 Sol (OpenAI) and
  checked again with Claude (Anthropic), under Joost de Winter’s direction; the README
  says the packing is not his work.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is the licence and the whole of `n109_kaggle/`: five
files retained under [source/](source/) and `LICENSE` pinned against the byte-identical
copy the
[de-winter-upper-bounds-227-229-260-2026-10-17](../de-winter-upper-bounds-227-229-260-2026-10-17/README.md)
packet retains. Every line of the folder’s `SHA256SUMS` matches its file.

The witness numbers its squares `square-0` to `square-108`, as the Kaggle rows do, so
the declaration reads it with `witness-corners` and the option `first_id: 0`, added for
it. Read so, each square’s corners are a unit square’s in the order the reader expects.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison, read from
`main` `06754afe6`.
The certificate lies 4.57887 × 10⁻⁴ below the house at 109: the Kingbird catalogue’s
6 + (7/2)√2, verified by T-101’s rational ceiling 10.949747468305832670915408009418.
No register bound is pending adoption at 109; T-327’s 10.630037940829 is a lower bound.
The
[ledger of 20 November for this lane](../../../campaign/issue-intake/upper-bounds-1012-20261120/README.md)
records the comment’s claim as a new packing relative to the record.

## Pose by Pose

`devtools.measure_identity` wrote [measure/identity.json](measure/identity.json).
It is a measurement for credit and decides nothing.

- **Against the house**, T-101’s exact view: no symmetry pairs them one to one by
  nearest centres; the optimal assignment moves 64 squares beyond 10⁻³ and 56 beyond
  0.1 (largest 0.824348). 45 squares are tilted beyond a degree, at 23.23 to 29.50
  degrees, all one way, against the house’s 49 at 45 degrees. A new arrangement relative
  to the record’s packing.
- **Against Samanyu-dev’s public 109**, the rows of count 109 in `best_fit_101_500.csv`
  at Samanyu-dev/squares_in_squares `53551d7` (committed 2026-11-07T20:20:31Z), read by
  the `kaggle-csv` reader added for this import. That file was read from a blobless
  clone in scratch space and is not retained (5,577,150 bytes, SHA-256 `377b9177…6c04`,
  the blob of that commit). Nearest centres pair the squares one to one (symmetry 1),
  with the same 45 tilted squares at 23.23 to 29.50 degrees. 37 squares sit more than
  10⁻³ apart, and 5 more than 10⁻² (largest 0.0256).
  The file’s two earlier versions, `1d95296` (30 October) and `942db6d` (7 November),
  hold the 45-degree packing at 10.949747468316 instead.
- **Against Kodaj’s rows**, `n109_tomkodaj.csv` read by the same reader: the witness
  states them to within 1.8 × 10⁻¹⁵, so the transcription is of those rows.

## Exact Replay

The checks below were planned before any of them ran, in
[receipts/controls-plan-1012-n109.md](receipts/controls-plan-1012-n109.md) (SHA-256
`323a526f…d49b`), hashed on think-wvr8 at 09:29:30Z, before the first route decided the
certificate.

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes: 3 jobs, 35,316 pair decisions,
8.22 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)).
The positive passed and both controls were refused on both routes.
Squares touch the box, a least wall clearance of exactly 0, and every pair clears by at
least 2.0 × 10⁻¹⁵ (squares 60 and 70), the gap `verification.txt` reports.
`check --replay` decided the three jobs again.

`sharp-controls` took the certificate to exact contact and 10⁻³⁰ past it on both routes
([receipts/sharp-controls.json](receipts/sharp-controls.json)), and all 11 came out as
the plan states, the branch for a square touching the wall taken. The box lowered to the
packing’s extent, the tightest pair closed (square 70 toward 60) and every square moved
toward its near wall by 0 were accepted at contact and refused 10⁻³⁰ past it. Square 70
enlarged to its partner was refused at contact for its shape alone and past it for the
overlap as well. Square 39, at its wall, grown by 0 was accepted, and 10⁻³⁰ past it was
refused. A duplicated square was refused.
The two routes, the sqpack rational witness verifier and the independent rational corner
checker, share certificate parsing, half-angle conversion, Fraction arithmetic and the
separating-axis method. The second is the checker `verification.txt` reports running.

## The Gain Against Padding (Option D)

`devtools.contraction_margin`, each contracted packing decided on both routes:

- **The house**, T-101’s ceiling, lies 1.1 × 10⁻¹⁹ above 6 + (7/2)√2, so the gain on it,
  4.5789 × 10⁻⁴, lies wholly outside its padding.
- **Samanyu-dev’s public 109**, read exactly by the `kaggle-csv` reader and boxed at its
  own exact extent, 10.9492895809453792966: both routes accept it as a packing there.
  Contracted uniformly to first contact (squares 17 and 73), its margin is
  1.9960 × 10⁻¹² and its contracted side 10.9492895809433833, which both routes accept
  at contact
  ([measure/contraction-n109-samanyu.json](measure/contraction-n109-samanyu.json)).
  This certificate’s gain on it is 1.9403 × 10⁻¹², 0.9721 of the margin, so the
  predecessor shrunk to first contact lies 5.57 × 10⁻¹⁴ below this certificate.
  By the owner’s option D (think-b0w5), the certificate is a restatement of that
  packing, not a new result.
- **This certificate’s own margin** is 1.9898 × 10⁻¹⁴ (squares 60 and 70;
  [measure/contraction-n109-own.json](measure/contraction-n109-own.json)).

The L-step scan, `devtools.l_step_scan` with this side stood in for 109’s ceiling
([measure/l-step-scan.json](measure/l-step-scan.json)), finds exactly `main`’s
consequences: the bound carries to no other count.

The later comparison uses the canonical Samanyu-dev fact registered as T-335.
The [canonical contraction receipt](measure/contraction-canonical-samanyu-vs-kodaj.json)
puts this certificate’s gain at 0.9723 of that packing’s margin. The
[canonical pose comparison](measure/identity-canonical-samanyu.json) pairs their
centres one to one. Under Option D, the later certificate remains a restatement
of the earlier arrangement.

## Credit

- The certificate is de Winter’s exact transcription of Kodaj’s 13 November rows.
- Those rows restate Samanyu-dev’s 7 November pinwheel under option D. The pairing is
  one to one, and the gain is within that packing’s padding.
- Samanyu-dev’s README credits its submission to per-puzzle merges of public notebooks.
  For 109 it names its own stretch-and-quench chains (“n=109 beats a leader”) and a
  `kmmmvs` merge (score step 15). It names no source for its 109.

The owner credited Samanyu-dev as finder of the construction registered as T-335.
The source credit for the later certificate is “de Winter after Kodaj, Samanyu-dev.”
The similarities to Fonseca’s 6 November pinwheel and the priority of the Prabhat and
`kmmmvs` compilations remain unresolved. The intake could inspect Samanyu-dev’s public
GitHub CSV, while the linked Kaggle notebooks were inaccessible.

## Commands

From `packing/`, with the project interpreter. `SAMANYU` is a local copy of
`best_fit_101_500.csv` at Samanyu-dev/squares_in_squares `53551d7`, held to its SHA-256
above:

```bash
P=de-winter-kodaj-n109-2026-11-18
M=resources/web/$P/measure
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 109 "KODAJ=packet:$P" \
  'T-101=witness-center-basis:cases/regularized_bounds/views/n-109.yaml.gz' \
  "SAMANYU-53551d7=kaggle-csv:$SAMANYU" \
  "KODAJ-ROWS=kaggle-csv:resources/web/$P/source/n109_kaggle/n109_tomkodaj.csv" \
  --out $M/identity.json
python -m devtools.contraction_margin --n 109 "SAMANYU-53551d7=kaggle-csv:$SAMANYU" \
  --against "KODAJ=packet:$P" --out $M/contraction-n109-samanyu.json
python -m devtools.contraction_margin --n 109 "KODAJ=packet:$P" \
  --out $M/contraction-n109-own.json
python -m devtools.l_step_scan --with 109=547464479047171949843/50000000000000000000 \
  --out $M/l-step-scan.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
