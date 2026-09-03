# Proposed 2026 Lower Bounds for 17 Unit Squares

Primary-source snapshot of two August 2026 proposals for improving the lower bound on
the side length needed to pack 17 unit squares in a square.

These sources were retrieved on 31 August 2026. They are retained because they contain
replayable, exact-rational certificates and because neither proposal was present in the
repository's frontier record when found. Neither result is peer reviewed or independently
implemented here yet.

## Burns: 4.4811

Sam Burns proposes `s(17) >= 4.4811` using 268 rationally weighted atoms whose total
mass is 16.9476. A rational angle net and an exact event-cell enumeration are used to
check that every unit square contains mass at least 1.0003.

- `burns-proposing-lower-bound.html` is the first-party explanatory post.
- `burns-n17-lower-bound-4.4811.md` is the downloadable proof note, retained byte for
  byte.
- `burns-verify-n17-lower-bound-4_4811.py` is the downloadable verifier, retained byte
  for byte.
- `burns-near-record-arrangement.html` is a separate first-party post in which Burns
  describes a near-record `n = 17` arrangement as having a topology distinct from the
  known record; this repository has not reconstructed that contact graph independently.

Source URLs:

- <https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/>
- <https://sam-burns.com/downloads/n17-square-packing/n17-lower-bound-4.4811.md>
- <https://sam-burns.com/downloads/n17-square-packing/verify_n17_lower_bound_4_4811.py>
- <https://sam-burns.com/posts/n17-square-packing-near-record-arrangement/>

## Massaccesi: 4.5058

Gustavo Massaccesi proposes `s(17) >= 4.5058` by applying linear programming to the
same certificate architecture. The published certificate has 168 atoms on a 29 by 29
grid, total mass `9744 / 576 = 16.91666...`, and claimed minimum checked mass
`576 / 576 = 1`.

- `massaccesi-lower-bound-4_5058.html` is the first-party result post and contains the
  verifier in a code block.
- `massaccesi-linear-programming.html` describes the grid and linear-programming search.
- `massaccesi-verify-n17-lower-bound-4_5058.py` is the verifier extracted from the result
  post for replay. HTML entities were decoded and the final non-breaking space after
  `main()` was replaced by an ASCII newline; the executable text is otherwise unchanged.

Source URLs:

- <https://gus-massa.blogspot.com/2026/08/another-better-lower-bound-for-n17.html>
- <https://gus-massa.blogspot.com/2026/08/linear-programing-for-square-packing.html>

The extracted verifier was replayed on 31 August 2026 with the repository's Python 3.14
environment. It completed in under five seconds and reported 168 atoms, total mass
`9744 / 576`, a minimum score of `576 / 576` over 181 sampled rational directions, and
`CERTIFICATE CONDITIONS VERIFIED`. A manual read-only review reported no issue in the
angle cover, shrunken-square containment, event-cell sweep, or strict-scaling argument,
but no replayable audit checklist was retained at that time.
Both of those gaps closed on 2026-09-03: `H-052` completed an independent implementation
that agrees with this certificate on all 181 exact direction cells (`exp-059`), the
`BC-150` packet audited the eleven lemmas, and `BC-151` reviewed both and adopted the
bound at source-backed scope.
The result stays externally proposed rather than first-party, and one method family
carries it: Massaccesi's verifier is derived from Burns's, and every implementation on
the record sweeps event cells over the same reduction.

The audit also found source defects that matter when reusing the work:

- The separate floating-point LP generator excludes an inclusive endpoint with
  `range(j0, j1)`. The final exact verifier correctly uses `j0:j1 + 1`, so the published
  certificate survives even though the candidate generator can omit constraints.
- The blog drawing spaces 29 grid points by `/29`; the verifier uses the correct 28
  intervals. The picture is not the certified geometry.
- The prose transposes `4.5058` once and gives the internal grid side as `3.9545` rather
  than the code's exact `L - M = 2.9545`.
- The source's claim of a consequential transfer to `n = 20` is stale relative to the
  stronger Nagamochi lower bound already in this repository. Monotonicity does improve
  the current `n = 18` and `n = 19` lower bounds if the certificate is adopted.

## Retrieval hashes

SHA-256 hashes of the retained source snapshots:

| File | SHA-256 |
| --- | --- |
| `burns-n17-lower-bound-4.4811.md` | `a7ddd7642b2a35064506978afc78b48460904bedb7f387481b248b4d3d42db85` |
| `burns-near-record-arrangement.html` | `3ae24f8da0c1ca068afb923a11229468307dedeba6a35925002aba58eef85c42` |
| `burns-proposing-lower-bound.html` | `9033d31c4ea3c49b3a2f77d6683df39b2552497dc5cb8a26e9da91f39fa38015` |
| `burns-verify-n17-lower-bound-4_4811.py` | `6d83c28634d42074a19df9e34572b0cba2ce203031004aa84a29aed76fbb2d7e` |
| `massaccesi-linear-programming.html` | `cdd27897f4f6c3b83835d59a317b3248b4f94b888f8568b740c778524a11f177` |
| `massaccesi-lower-bound-4_5058.html` | `7dffb6e6e6cbff0ac2e887ca445b45f46c95055718219f7229d1c8cb06f84514` |

The normalized extracted verifier has SHA-256
`04531a54da9a654f2318401aff43222daf721bd99e948b2491f91c05bd0b5d3f`.

Retained for private research use. Consult the authors before redistribution.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
