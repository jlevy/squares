# Kaelan Yim’s s(260) Certificate at d11a8a1

This packet retains `n260.cert` from
[vitamoon/vitamoon](https://github.com/vitamoon/vitamoon/tree/d11a8a1ce798f7c0b4f801e922e242d22cedcd73),
Kaelan Yim’s GitHub profile repository, at `d11a8a1ce798f7c0b4f801e922e242d22cedcd73`
(committed 2026-11-05T05:44:44Z), the head of `main` when it was read at 05:57Z on 5
November 2026. [Issue #895](https://github.com/jlevy/squares/issues/895), opened at
02:15:02Z on 4 November, reports the bound and attached the certificate as a GitHub user
attachment, `n260.cert.txt`, which this environment cannot fetch.
The acknowledgement of 4 November asked for the file at a public commit and its SHA-256.
The author’s
[reply of 5 November](https://github.com/jlevy/squares/issues/895#issuecomment-6650567350)
(05:31:32Z, edited once at 05:31:52Z) links
`github.com/vitamoon/vitamoon/blob/main/n260.cert`, which names a branch, not a commit,
and states no digest.
So the packet is pinned by commit, at the head that branch named when it was read.

The file was added at `e7cab3ac67e6d7c22970e7b8ffb121c1d96016a5` (committed
2026-11-05T05:27:47Z, “n260 square packing cert 895”), four minutes before the reply.
The four later commits up to the pin each change `README.md` only, so the file at the
pin is the file first committed.
Whether it is byte-identical to the 4 November attachment is not established, since the
attachment was never fetched; the reply offers this file as that certificate.

## What the Source Claims

- `n260.cert` is Evan Daniel’s certificate format: a comment line, the header `260 S`,
  then 260 rows `x y t`, each a rational centre in $[0, S]^2$ and the rational tangent
  of the square’s half-angle.
  Its header side is
  `1045817814143413714427921537528704162855767253933/62872364692131569638734867237718772414897487626`,
  which is $16.63398250192261413979\ldots$, 16.6339825019226142 rounded up at 16 places
  and 16.633982501923 at 12. The issue states this fraction exactly, with the
  approximation 16.6339825019226141, and says it is about $1.99 \times 10^{-10}$ below
  the record’s 16.6339825021218840, Evan Daniel’s #845 certificate (T-257).
- The issue says the author converted the certificate to this repository’s Witness/v2
  corner form and ran `devtools.check_rational_witness_independent` from a local
  checkout at `e6e8d577` (#888’s merge), which reported VERIFIED: 260 unit squares and
  all 33,670 pairs in exact rational arithmetic at the stated side.
  It says that was the only checker run.
  The conversion is not published, and the statement is the author’s.
- **Lineage.** “The search started from a publicly available packing attributed to Evan
  Daniel and Kirill Tymchishin.
  I independently carried out the computational refinement that produced this
  candidate.” The certificate’s comment line reads “by Kaelan Yim, derived from Evan
  Daniel and Kirill Tymchishin packing method using CUDA/SLP numeric tightening”.
- **AI assistance.** “I used AI to study and set up an environment similar to the one
  used by Daniel and Tymchishin.”
- It claims an upper bound only: no KKT, local-optimality, rigidity or global-optimality
  claim.

## Retained Here

`devtools.acquire_source` wrote the packet from a full clone of the repository, from
[acquisition/declaration.json](acquisition/declaration.json); the file is bound to its
Git blob at the pin.
The scope is that one file.
The repository’s other file, `README.md`, is the author’s profile page, which says
nothing about packing, and is not retained.

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `n260.cert` | `82ecdeccd504618180df3ea99d5b80f9a7c76e0f` | 67,514 | `c9e83969169f2ceec6014bc7fcd18418067209d485816c9b899b2e8b2a86ccbb` |

The SHA-256 is measured here, on the clone; the author stated none.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the
manifest and [acquisition/sources.json](acquisition/sources.json) the record.
The file has 262 lines, so it is stored as written, and the packet is well under a
megabyte, so it is kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `a7db9aad3` on 5 November
2026):

- **260:** exact side 16.6339825019226142… rounded up, below the case’s house (T-257,
  Evan Daniel, from a search started from Kirill Tymchishin’s Kaggle notebook packing)
  by $1.99 \times 10^{-10}$; no register bound pending adoption below the house.

## Report Order

The
[ledger of 4 November for this pass](../../../campaign/issue-intake/upper-bounds-893-895-20261104/README.md)
walks every report at 204, 260 and 299 in the order it reached this repository, from
starts frozen at `main` `ca3a171bb`, and records #895 at 260, the first report below
T-257 there. It first walked the claim by the side the issue states; from 5 November it
reads this packet’s claim record, with the same side and verdict.
T-257 still holds 260 on `main` `a7db9aad3`.

## Pose by Pose

`devtools.measure_identity` measured the certificate against T-257’s packing and wrote
[measure/identity.json](measure/identity.json).
A measurement for credit; it decides nothing.

- **260:** one to one with T-257’s packing under the identity by nearest centres; the
  optimal assignment moves 26 squares beyond 0.1, 64 beyond 0.01 and 96 beyond 0.001
  (largest 0.382307), and turns 14 squares by more than $10^{-6}$ radians, by up to
  1.498 degrees. Tilted beyond 1 degree: this packing 105, T-257 104, all but five turned
  one way in each; one of this packing’s tilted squares pairs with one T-257 has
  upright.
- **The upright squares.** Every one of the 260 squares carries a nonzero half-angle
  tangent: 146 of the 155 near-upright squares are turned by $-1.34 \times 10^{-10}$ to
  $-1.40 \times 10^{-10}$ degrees, with 64 distinct tangents, the commonest
  $-1/850217033674$. T-257 has 112 squares exactly upright.
- **The word.** The issue calls the work a computational refinement.
  The record keeps “refinement” for a pairing in which no square moves beyond a tenth,
  and 26 do here, so the register drafts it as a further arrangement of T-257’s packing,
  one to one with it, and lists no regularization, as T-239 at 303 does.
  T-257’s packing is not rigid (103 of its 260 squares admit a translation, by the case
  record), which leaves room for large moves at almost no change of side; the stage 4
  review is asked to say what moved.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 202,020 pair decisions, 41.04 route CPU seconds and 41.35 job wall
seconds, the longest job 14.08 seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes, and `check --replay`
decided the receipt again.
Squares touch the box, a least wall clearance of exactly 0 (the far walls), and the
least pair gap is about $1.336 \times 10^{-15}$.

`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
$10^{-30}$ past it ([receipts/sharp-controls.json](receipts/sharp-controls.json), 11
controls, 157 CPU seconds):

- It lowered the side by the least far-wall clearance, which is 0, closed the least-gap
  pair by its gap, and moved every square toward the nearer near wall by its least
  clearance, about $7.22 \times 10^{-16}$: both routes accepted each at contact with
  margin 0 and refused each past it.
- It enlarged one square to its pair: both routes refused it at contact for its shape
  alone and $10^{-30}$ past it for the overlap as well.
  The square it enlarged to its wall already touches it, so both accepted it at contact
  and refused it $10^{-30}$ past it for the wall and its shape.
- Both refused a duplicated square.

The two routes, the `sqpack` exact witness verifier and the independent rational corner
checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic and the
separating-axis method, and read the certificate through the `evand-cert` reader, whose
line filter and corner construction are transcribed from Evan Daniel’s checkers.
The second route is `devtools.check_rational_witness_independent`, the program the
author reports running on his own Witness/v2 conversion, so on that route the replay
runs the producer’s check on this repository’s conversion; the first route is not the
code he ran. No source program ran here.

## What Is Not Established

- **The stage 4 review.** No independent review has read the certificate yet; the brief
  for it is on think-o7ly.
- **Human oversight.** No human oversight record is retained.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing
  more.
- **The lineage** the source states, beyond what the measurement above shows, and the
  identity of this file with the attachment of 4 November.

## Credit and Licence

The packing is Kaelan Yim’s refinement, by his account, of a public packing he
attributes to Evan Daniel and Kirill Tymchishin, which is T-257’s at 260: Evan Daniel’s
packing from a search started from Kirill Tymchishin’s Kaggle notebook packing.
The bibliography key is **[Yim s260 upper bound 2026-11-05]**, credited “Yim after
Daniel, Tymchishin”.
The author used AI to study and set up his search environment.

The author releases `n260.cert` under CC BY 4.0: “I release n260.cert under the Creative
Commons Attribution 4.0 International (CC BY 4.0) license … You may retain and use it in
the project with attribution to Kaelan Yim” (the reply of 5 November).
The repository carries no licence file.
The certificate is in Evan Daniel’s MIT-licensed format, and its packing starts from
T-257’s certificate, whose notice the
[evand-issue845-2026-10-29](../evand-issue845-2026-10-29/README.md) packet retains; the
file carries no copy of that notice.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source yim-s260-upper-bound-2026-11-05 --checkout CHECKOUT
python -m devtools.acquire_source yim-s260-upper-bound-2026-11-05 --check
python -m devtools.upper_bound_reports yim-s260-upper-bound-2026-11-05 check-claims --write
python -m devtools.upper_bound_reports yim-s260-upper-bound-2026-11-05 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports yim-s260-upper-bound-2026-11-05 check --replay
python -m devtools.upper_bound_reports yim-s260-upper-bound-2026-11-05 sharp-controls
python -m devtools.measure_identity --n 260 'YIM=packet:yim-s260-upper-bound-2026-11-05' \
  'T-257=packet:evand-issue845-2026-10-29' \
  --out resources/web/yim-s260-upper-bound-2026-11-05/measure/identity.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
