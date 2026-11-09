# Kaelan Yim’s First s(303) Certificate at 78eb9ea

This packet retains the first `n303.cert` of
[vitamoon/vitamoon](https://github.com/vitamoon/vitamoon/tree/78eb9ea5da43230686941289b9de3ce0f8e34899),
Kaelan Yim’s GitHub profile repository, at `78eb9ea5da43230686941289b9de3ce0f8e34899`
(committed 2026-11-09T07:13:34Z), the commit that first holds it.
The file is unchanged through `e4209f6` and `c10e094`. Then `546928a` (09:36:10Z)
overwrites it with a second certificate, which the
[yim-certificates-2026-11-09](../yim-certificates-2026-11-09/README.md) packet retains at
the later head `ac14112` with the author’s other 13 certificates.
No issue reports either. Each is a report of its own from its first commit (the owner,
14 October 2026), so this packet keeps the first, which no later tree holds.

GitHub’s activity log was not readable from this session, so no push time is recorded;
`78eb9ea` was public by 07:56:30Z, when the intake pass’s bead think-h96r named it.
`sha256sum -c SHA256SUMS` passes on all 13 lines at the pin.

## What the Source Claims

- `n303.cert` states s(303) ≤
  `1259726429694979000000000000001259726429694979/70368744177664000000000000000000000000000000`
  $= 17.9017892732954777\ldots$, which `PACKINGS.md` prints rounded up at 12 places as
  17.901789273296. Its comment line reads “Resumed L40S n303 candidate; tiny improvement,
  no structural discovery claim.”
- `PACKINGS.md` at the pin: “n303 is not a new-best submission: the pending public
  submission #930 reports a smaller side than the certificate in this snapshot.”
  `packing-certificates.json` calls it a “Computational refinement of Evan Daniel’s
  issue914 packing, after Chris Deotte’s multi-gadget fault-DP method”, with search
  tooling including griffcass/square-packing, and makes “No current public/global record
  or optimality claim.”
- It says five local exact checks accepted the certificate, two of them this
  repository’s maintained routes at `f30d6405`.
  Those statements are the author’s; no source program ran here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json).
It retains `n303.cert` (62,142 bytes, blob `0e28ca53`, SHA-256 `b8318f81…ab9b`) under
[source/](source/) as factual data. `PACKINGS.md`, `SHA256SUMS` and
`packing-certificates.json` at this revision are pinned by digest; their later revisions
are retained by the yim-certificates-2026-11-09 packet.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the
manifest and [acquisition/sources.json](acquisition/sources.json) the record.

## Against the Record

[acquisition/claims.json](acquisition/claims.json), read from `main` `adca8d352`: the
certificate is 1.39e-10 above the house, T-278 (Doğa Özden’s #930, 17.901789273157,
reported at 06:03:47Z, an hour before this commit), and 4.35e-5 below T-272 (Evan Daniel’s
#914 packing, after Chris Deotte), the house it replaced. The
[ledger of 9 November](../../../campaign/issue-intake/upper-bounds-yim-certificates-20261109/README.md)
does not record it, since #930 came first and is lower, and the source says so itself. It
stays in this packet.

## Pose by Pose

[measure/identity-n303.json](measure/identity-n303.json): the certificate pairs one to
one with T-272’s packing under the identity by nearest centres; 5 squares move beyond
0.1 (largest 0.145), 83 beyond 0.01, and turns reach 19.0 degrees. It is a further
arrangement of T-272’s packing, one to one with it. Against T-278’s packing, and the house
witness that is now T-278’s, it is a sibling: one to one, 9 squares beyond 0.1.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes: 3 jobs, 274,518 pair
decisions, 47.6 route CPU seconds
([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)). The
positive passed and both controls were refused on both routes.
`sharp-controls` took it to exact contact and $10^{-30}$ past it, with 11 controls and
181.9 CPU seconds ([receipts/sharp-controls.json](receipts/sharp-controls.json)). Every
control was as expected on both routes.
The least wall clearance is $7.3 \times 10^{-25}$ and the least pair gap
$1.8 \times 10^{-16}$. The routes are the ones the author reports running himself, at
`f30d6405`, and are unchanged since.

## Credit and Licence

Kaelan Yim’s computational refinement of Evan Daniel’s #914 packing, after Chris
Deotte’s method, by his account; AI-assisted (Hermes Agent).
The repository carries no licence file, and nothing was submitted here, so the
certificate is retained as factual data under the owner’s decision of 9 October 2026
([Retained Factual Data](../known-best-packings/README.md#retained-factual-data)).
Retaining it grants no licence and relicenses nothing.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source yim-n303-2026-11-09 --checkout CHECKOUT
python -m devtools.acquire_source yim-n303-2026-11-09 --check
python -m devtools.upper_bound_reports yim-n303-2026-11-09 check-claims --write
python -m devtools.upper_bound_reports yim-n303-2026-11-09 certify --jobs-dir "$TMPDIR/jobs" --workers 1
python -m devtools.upper_bound_reports yim-n303-2026-11-09 check --replay
python -m devtools.upper_bound_reports yim-n303-2026-11-09 sharp-controls
python -m devtools.measure_identity --n 303 'YIM-78eb9ea=packet:yim-n303-2026-11-09' \
  'T-272=packet:evand-issue914-2026-11-05' \
  'T-278=packet:ozden-s303-upper-bound-2026-11-09' \
  'house-witness=witness-center-basis:witnesses/known-best/n-303.yaml' \
  --out resources/web/yim-n303-2026-11-09/measure/identity-n303.json
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
