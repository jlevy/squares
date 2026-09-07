# GitHub Certificates for s(17), Retrieved 2026-09-07

Three public GitHub repositories, each claiming a lower bound on `s(17)`, the least side
of a square holding 17 unit squares.
All three were published in August 2026 and none was in the record until now: the
literature refresh of 2026-09-05 searched arXiv, Crossref, OpenAlex, and Zenodo, not
GitHub, so a code-hosting repository with no paper indexed anywhere else was invisible
to it. These were found afterward and are retained here.

This repository’s own bound, `s(17) >= 459/100 = 4.59` (`T-019`, 2026-09-04), remains
the strongest and is not displaced by anything in this packet.
The strongest archived bound, anabologyco-maker’s `4.5705` of 16 August, predates
`T-019` by three weeks and is above the `4.5058` (Massaccesi, 21 August) the record had
believed was the best public value as of the 5 September refresh.
That belief was already stale when the refresh ran; the refresh’s gap was GitHub
coverage, not the calendar.

## Chronology of 2026 lower-bound claims for `s(17)`

| Date | Author | Type | Value |
| --- | --- | --- | --- |
| 2026-07-18 | Kim Brandwijk | exact 16-point pose-space certificate (Zenodo) | `89/20 = 4.45` |
| 2026-08-06 | Sam Burns | weighted atomic-measure certificate, 268 atoms (blog) | `44811/10000 = 4.4811` |
| 2026-08-10 | Mira | exact 16-point pose-space certificate (GitHub; not retained here) | `4.450837` |
| 2026-08-11 | Stanislav Fort | exact 16-point pose-space certificate (GitHub; retained) | `4456575/1000000 = 4.456575` |
| 2026-08-11 | Mira | exact 16-point certificate with triangle-piercing leaves (GitHub; retained) | `4468292/1000000 = 4.468292` |
| 2026-08-13 | anabologyco-maker | weighted atomic-measure certificate, non-strict, v0.1.1 (GitHub; legacy, not retained) | `4.57` |
| 2026-08-16 | anabologyco-maker | weighted atomic-measure certificate, non-strict, v0.2.0 (GitHub; retained) | `9141/2000 = 4.5705` |
| 2026-08-21 | Gustavo Massaccesi | weighted atomic-measure certificate (blog) | `22529/5000 = 4.5058` |
| 2026-09-04 | this repository | weighted atomic-measure certificate (`T-019`) | `459/100 = 4.59` |

The three exact 16-point certificates (Mira’s `4.450837`, Fort’s `4.456575`, and Mira’s
`4.468292`) are the strongest unweighted-point, integral bounds on record for this case:
each is above Brandwijk’s `4.45` and above this repository’s own sixteen-point
certificate, `cases/green17`, at `s(17) >= 4.426213` (`T-001`). None of the three
approaches the weighted bounds; Mira’s own README states this directly, noting Fort’s
certificate as its immediate predecessor.

## Mira-acc/17squares: `s(17) > 4.468292`

Full tree of <https://github.com/Mira-acc/17squares> at commit
`0872d3ac9a95bb4f8f628c8ee255d76eb27d6c2f` (11 August 2026), minus `.git`.

The claim is 16 rational points, denominator `10^7`, plus 18 triangles
(`certificates/lower_bound_4p468292/points.json`), certified against a 122,626,747-node
exact pose-space subdivision: every unit square contained in `[0,4.468292]^2`, at every
orientation, strictly contains a point or has its center rectangle strictly inside a
triangle whose three sides are all strictly shorter than 1 (a strict triangle-piercing
lemma forces a vertex into the square in that case).
Node counts: split `61,313,373`; point `33,762,069`; triangle `483,875`; infeasible
`27,067,430`; max depth `74`. Seventeen interior-disjoint squares would need 17 distinct
witnesses from a 16-point set, so no packing exists at that side; compactness makes the
bound strict.

The raw certificate is above GitHub’s ordinary 100 MB file limit, so the source ships
only its deterministic XZ archive, `square17_lb_4p468292.cert.xz` (374,096 bytes).
Three checkers accompany it: `verify_certificate.cpp` (fast, shares
`lower_bound_common.hpp` with the generator, needs Boost),
`verify_certificate_bigint.cpp` (independent Boost `cpp_int` implementation), and
`verify_certificate.py` (independent pure-Python arbitrary-integer implementation).
The paper (`paper/main.tex`, `paper/17squares-lower-bound.pdf`), “An Exact
Computer-Assisted Lower Bound for Packing 17 Unit Squares in a Square,” is dated August
2026 and cites Friedman’s survey, Stromquist 2003, Ellsworth’s catalogue, and Fort,
giving Green’s value `(40*sqrt(2)+19)/17 = 4.4452` as the survey’s lower bound; it does
not mention Brandwijk, Burns, or Massaccesi.
`CITATION.cff` gives version `1.1.0`, dated 2026-08-11: the metadata already reflects
this second result, not the first.

`PROVENANCE.md` places this package third in its own line: Mira’s own first exact
certificate, `s(17) > 4.450837` (commit `3d5fc2c`, 10 August 2026), then Fort’s
`4.456575`, then this `4.468292` instance adding the triangle leaves.
The point search, generator, and exposition were developed “with substantial assistance
from OpenAI’s GPT-5.6 Pro under human direction”; the package has not undergone
independent peer review.

Replayed here with `replay_mira_python.py`, run as `uv run --frozen python
resources/web/n17-github-certificates-2026/replay_mira_python.py` from `packing/`: it
decompresses the archive with Python’s own `lzma` module, checks both the archive
SHA-256 (`a349b81e630ccf7292ae0afe6ed954591f7e88fe6289847f67883204a7ed60ac`) and the
decompressed SHA-256
(`2838f315302d67da131745925e9ec7dd2a602bb299d1335ce25e4e13a7b7b6d2`) against the
source’s published values, then runs the source’s own `verify_certificate.py` as a
subprocess and requires its `PYTHON_INTEGER_CERTIFICATE_VALID_4P468292` marker.
Both hashes matched and the marker printed, over all 122,626,747 nodes, in about 3 min
(2 min 36 s wall, measured here).
No Boost headers were available in this container and installing them was declined, so
the two C++ checkers did not run here.

## stanislavfort/17squares: `s(17) > 4.456575`

Full tree of <https://github.com/stanislavfort/17squares> at commit
`853f7ee61e7d37c8284a3fe130d79831140ad507` (three commits, 11 August 2026, author
Stanislav Fort), minus `.git` and `.DS_Store`.

The claim is 16 rational points, denominator `10^6`
(`certificates/lower_bound_4p456575/points.json`), with no triangle leaves: a pure
point-witness certificate of 21,696,657 nodes (split `10,848,328`; covered `10,594,408`;
infeasible `253,921`; max depth `68`), using the same pose-space subdivision
architecture and the same three-checker protocol as Mira’s repository.
`PROVENANCE.md` states plainly that it is a response to Mira’s `4.450837`, preserving
that proof idea and certificate protocol while substituting a stronger point set, and
notes that several files here intentionally adapt Mira’s upstream architecture.

The repository’s own README opens with the author’s warning: “everything here has been
done by GPT-5.6-Sol with high reasoning settings.
I, Stanislav Fort, don’t really understand it => can’t vouch for its correctness.
But it should be checkable by other AIs and/or knowledgeable humans.”
A GitHub Action (`.github/workflows/verify.yml`, not part of this packet) installs Boost
and runs the three checkers on push.
The README also links a `CHANGELOG_FROM_4p452625.md` that is not present in the source
tree; the source’s own `MANIFEST.sha256` (retained here) lists it and four other
maintainer-facing files, `.gitignore`, `MESSAGE_TO_MAINTAINER.md`,
`UPLOAD_TO_GITHUB.md`, and `UPSTREAM_INTEGRATION.md`, that this packet also does not
retain, since none of the five bear on the certificate or its verification.

Unlike Mira’s repository, this source ships the raw 21,696,657-byte certificate directly
(SHA-256 `5fbee90dc6fedc1851e4b8b9866f8ffa41c38cb09ebb6a9f748096217f078550`, also in
`MANIFEST.sha256`); this packet recompressed it to `square17_lb_4p456575.cert.xz`
(SHA-256 `629f6407142147493a34a8e2a9f63dcc743aa773547d7b5a39384ca5f9307d4f`) to save
space, and the raw hash is checked on decompression by the replay script rather than
assumed.

Replayed here with `replay_fort_python.py` (same invocation pattern as Mira’s script,
decompress via `lzma`, check the published SHA-256, run `verify_certificate.py` as a
subprocess and require its marker): the decompressed certificate matched the published
raw SHA-256, and the source’s `verify_certificate.py` printed
`PYTHON_INTEGER_CERTIFICATE_VALID` over all 21,696,657 nodes, in about 20 s wall (22 s,
measured here). As with Mira’s package, no Boost headers were available, so the two C++
checkers did not run.

## anabologyco-square17-lower-bound: `s(17) >= 4.5705`

Tree of <https://github.com/anabologyco-maker/square17-lower-bound> at commit
`396da6f7c112f49b50b5f4563ad2486ef38ac909` (17 August 2026), minus `.git` and minus
`legacy/` (the frozen v0.1.1 release, tagged `v0.1.1` and `4p57-final`, 13 August 2026,
still retrievable at that tag).
The repository’s tags run `v0.1.1` (13 August, `s(17) >= 4.57`, 52 orbits, 408 atoms)
and `v0.2.0` (16 August, `4.5705`, retained here).

The claim is `s(17) >= 9141/2000 = 4.5705`, deliberately not a strict inequality, and it
is a different proof architecture than the two point-certificate repositories above: a
nonnegative atomic measure on the container, 71 dihedral orbits expanding to 560 atoms
(`data/atoms.csv`), coordinates on the `1/4000` grid, weights with denominator `10^12`.
Exact total mass is `16994734834452/10^12 = 16.994734834452`, slack `0.005265165548`
below 17. The weighted obstruction lemma (`docs/PROOF.md`) is standard for this
architecture: if every closed unit square in the container captures mass at least 1 and
the total mass is under 17, no 17 interior-disjoint unit squares fit.

The verification chain regenerates 1,344,862 geometric event polynomials, exactly
discards 1,194,331 of them by an integer Bernstein sign test on `t = tan(theta/2)` in
`[0, 83/200]`, and runs exact Sturm chains on the remaining 150,531 to produce 148,936
distinct interior roots and 148,937 open orientation cells.
One exact rational `t` is sampled per cell; all 278,950,150 maximal subthreshold runs
across those cells are proved outside the feasible-center diamond by exact
separating-axis inequalities.
The two endpoints, `theta = 0` and `theta = pi/4`, are checked separately (the latter in
`Z[sqrt(2)]`, 700 subthreshold runs), reporting a minimum open-cell coverage at
`theta = 0` of `1.000300000011`. The design target used when the candidate was built
(`scripts/make_candidate.py`) was a safety factor of `10003/10000 = 1.0003`, the same
per-cell margin convention Burns and Massaccesi use; the audited value lands just above
that target. `lean/` is a Lean 4.33.0 formalization of the finite computation layer:
`native_decide` theorems `certificate_ok`, `theta0_coverage_ok`,
`quarter_turn_coverage_ok`, and `sample_subset_coverage_ok` build in the default target,
and `sample_full_coverage_ok` (`FullTheorem.lean`) replays the full 148,937-orientation
audit in an 8.5-hour build.
Not formalized: the event-completeness and partition layer, and the measure argument
itself (both documented as open in `lean/README.md`).

Four files over 1 MB were XZ-compressed for this packet, with their raw SHA-256 recorded
in `raw-hashes-of-compressed-files.sha256`: `data/event_polys.npy`,
`data/event_polys_filtered.tsv`, `data/orientation_samples.tsv`, and
`lean/Square17/SampleDataFull.lean`. The source’s own `SHA256SUMS` (76 entries) verified
against the uncompressed originals before compression.

Provenance, per the repository’s own README: certificate and pipeline built with “GPT
5.6 Sol Pro (OpenAI),” the same optimization pipeline as the frozen `4.57` release;
audit, reproduction, and the Lean formalization credited to “Claude Fable 5
(Anthropic)”; external human peer review pending.

Replayed here with `replay_anabologyco_python_stages.py`, which needs Python 3 with
NumPy and so is run with the project interpreter.
It copies the retained package to a temporary directory, restores the four XZ-compressed
files above and checks their raw SHA-256 against
`raw-hashes-of-compressed-files.sha256`, checks the source’s own `SHA256SUMS`, then runs
`scripts/check_certificate.py` and `scripts/verify_filter.py` as subprocesses and
requires their PASS markers, the only two stages that need no Boost.
All 76 `SHA256SUMS` entries verified; `check_certificate.py` printed
`exact_mass=4248683708613/250000000000` and `EXACT CERTIFICATE ARITHMETIC PASS`;
`verify_filter.py` printed `raw_polynomials=1344862`, `exactly_discarded=1194331`,
`filtered_polynomials=150531`, and `EXACT BERNSTEIN FILTER PASS`. The whole script ran
in about 2 s here. The Sturm partition (`src/verify_event_partition.cpp`), the endpoint
audit (`src/verify_endpoints.cpp`), and the 148,937-cell coverage audit
(`src/verify_coverage_segment.cpp`, via `scripts/run_coverage_ranges.sh`) all need
Boost.Multiprecision and were not run here; the Lean layer needs a Lean 4.33 toolchain,
also unavailable, so none of the `native_decide` theorems were rebuilt.

## Why the repository’s own verifier cannot decide the anabologyco certificate

The 560 atoms were re-encoded into `sqpack.fractional` at side `9141/2000` over the
181-direction net and checked against a shrunken test square, first at side
`B = 9977/10000` and again at `B = 9973/10000`. Both runs are refused by the exact
sweep, with least cell mass `6119404457/250000000000` (about `0.0245`) at direction 0.
This is a refusal, not evidence against the source: the source’s argument relies on
closed unit squares at exact orientations, and it places atoms on the lines exactly one
unit from the container walls (`X` or `Y` equal to `4000/4000` or to
`L - 1 = 7141/2000`, in the `1/4000` grid).
A closed unit square touching a container wall captures such an atom on its own
boundary; the repository’s shrunken `B`-square, built smaller than a full unit square
precisely to give the sweep a rounding margin, cannot reach that boundary.
The artifact is in the verifier’s shrink reduction, not in the certificate.

A read-only check of `data/atoms.csv` with the project’s `venv` Python and exact
`fractions`, no third-party libraries, quantifies this.
Of the 560 atoms, `108` have `x` or `y` exactly equal to `1` or to `L - 1 = 7141/2000`,
i.e. `X` or `Y` equal to `4000` or `14282` on the `1/4000` grid.
The total mass captured by the closed unit square `[0,1]^2` at `theta = 0` is exactly

```text
1000300000011/1000000000000 = 1.000300000011,
```

which is at least 1, as the weighted obstruction lemma requires, and matches the
source’s own claimed `theta = 0` minimum open-cell coverage (`docs/AUDIT.md`,
`run_summary.json`) digit for digit.
That agreement is consistent with the source’s endpoint audit being correct; it does not
by itself confirm the unformalized event-completeness argument that carries the result
from 148,937 sampled orientations to all of them.

## What is retained, and what is not

- Mira’s repository: the source itself ships only the XZ archive (GitHub’s 100 MB file
  limit already forces that); this packet keeps it unchanged.
  Mira’s first exact certificate, `s(17) > 4.450837` (commit `3d5fc2c`, 10 August 2026),
  is not extracted into this packet; it remains retrievable at that commit.
- Fort’s repository: the source ships the raw 21.7 MB certificate; this packet
  recompresses it to XZ and records both hashes (above).
- anabologyco’s repository: four data/Lean files over 1 MB are XZ-compressed here, with
  raw hashes in `raw-hashes-of-compressed-files.sha256`; `legacy/4p57/` (the frozen
  `v0.1.1` release and its own Lean layer) is omitted and retrievable at the `v0.1.1` /
  `4p57-final` tag.
- Five maintainer-facing files from Fort’s repository (`.gitignore`,
  `CHANGELOG_FROM_4p452625.md`, `MESSAGE_TO_MAINTAINER.md`, `UPLOAD_TO_GITHUB.md`,
  `UPSTREAM_INTEGRATION.md`) are in the source’s own `MANIFEST.sha256` but not retained
  here, since none bear on the certificate.

## Trust notes

All three repositories disclose model-generated code, and in two cases model-generated
proof exposition: Mira credits “GPT-5.6 Pro”; Fort’s README credits “GPT-5.6-Sol” and
states the author cannot personally vouch for the result; anabologyco credits “GPT 5.6
Sol Pro” for the certificate and pipeline and “Claude Fable 5” for the audit,
reproduction, and Lean formalization.
None of the three has undergone external peer review; all three say so explicitly.

The two 16-point certificate lines, Mira’s and Fort’s, share a code architecture by
design: Fort’s own `PROVENANCE.md` states that the package preserves Mira’s proof idea
and certificate protocol and that several files intentionally adapt Mira’s upstream
code, and Mira’s `4.468292` package in turn names Fort’s `4.456575` repository as its
immediate predecessor.
anabologyco’s weighted-measure architecture is unrelated to either point-certificate
line; its own provenance note ties its `4.5705` release to the same optimization
pipeline as its own earlier `4.57` release rather than to Mira’s or Fort’s code.

## Retrieval hashes

SHA-256 hashes of key retained files.
Certificate and archive hashes are the source’s own published values, checked against
the retained bytes; the rest are hashes of this packet’s own copies.

| File | SHA-256 |
| --- | --- |
| `mira-17squares/README.md` | `0cab51693ae7cd9e5fc3af574da8c2e431487e0e65d83a6f0a7e13f9d761deb2` |
| `mira-17squares/CITATION.cff` | `d3b0381ce345d30f283de4f1ae327b5aaea39a33defd6c9791bfd931e9ad6fd7` |
| `mira-17squares/paper/main.tex` | `f5c9caa75449cba00dc8b20138bd3f45ca8c15106a65391c174fa7b9414715d8` |
| `mira-17squares/paper/17squares-lower-bound.pdf` | `64820a1328aac3fb7a89ad1139b4dc051e38a82e184112943cdb8c41964574fe` |
| `mira-17squares/certificates/lower_bound_4p468292/README.md` | `190f72bd5191d271e082af6438d93053eae110472335d9de966f08179d235ec1` |
| `mira-17squares/certificates/lower_bound_4p468292/PROVENANCE.md` | `44574c61973629d67027d22fb70fdd3071eaaef87181d59f3b79b6ecb1e4fe9a` |
| `mira-17squares/certificates/lower_bound_4p468292/points.json` | `71d33dabc3311961e83949a72dd82358fa0ed6de6db39132434edbc5152ce179` |
| `mira-17squares/.../square17_lb_4p468292.cert.xz` | `a349b81e630ccf7292ae0afe6ed954591f7e88fe6289847f67883204a7ed60ac` |
| `mira-17squares/.../square17_lb_4p468292.cert` (decompressed) | `2838f315302d67da131745925e9ec7dd2a602bb299d1335ce25e4e13a7b7b6d2` |
| `stanislavfort-17squares/README.md` | `621b3d025b243f1f6648e76c5ee8e708d64b34b0c875e7ea35bd5f8251476d05` |
| `stanislavfort-17squares/PROVENANCE.md` | `02ee612040e923e6714b4d350154de2361fea9019a01308b8c051108cbb03dc1` |
| `stanislavfort-17squares/MANIFEST.sha256` | source’s own manifest, retained unmodified |
| `stanislavfort-17squares/certificates/lower_bound_4p456575/points.json` | `726f5bac3bd69e7273fe8857938f2a124d92b42f8dfad539805519b2445a72d8` |
| `stanislavfort-17squares/.../square17_lb_4p456575.cert.xz` | `629f6407142147493a34a8e2a9f63dcc743aa773547d7b5a39384ca5f9307d4f` |
| `stanislavfort-17squares/.../square17_lb_4p456575.cert` (decompressed) | `5fbee90dc6fedc1851e4b8b9866f8ffa41c38cb09ebb6a9f748096217f078550` |
| `anabologyco-square17-lower-bound/README.md` | `98f484d93ccf24eb2ff45da854379d36722f62282be8c6278210925ad7a3fb38` |
| `anabologyco-square17-lower-bound/SHA256SUMS` | `d3b75c6eae74456d20d8f1b14e8811d34bdd4abc7ab3cd500a3e2837f8e0752d` |
| `anabologyco-square17-lower-bound/data/atoms.csv` | `8f518d9463efea3923545349d22e2f2788ac95a62d91deb621b1ce6186012aa8` |
| `anabologyco-square17-lower-bound/run_summary.json` | `befca9413f973ed3288e350b233fd36908dc15f61385087ac361ae3cebfff477` |
| `anabologyco-square17-lower-bound/AUDIT_RESULTS.txt` | `9885ebd30eb4bdf4f93ea3d3b25577f9959eebe5d51cbe6e83c4d5b0c54a9667` |
| `raw-hashes-of-compressed-files.sha256` | `651023b6773cd2f8e1d3c58e060a970169c9c70a651b0276ea8ecc4233bd8801` |
| `replay_mira_python.py` | `ba8af295ea57ea17dd6deb15c62c7a58c8a10beefaac4835a6e0f4fc5b39f7c5` |
| `replay_fort_python.py` | `f40dce78215f6fecb7f8c96155b0bce27cb355387e9216727a7cc7ebdd9a2377` |
| `replay_anabologyco_python_stages.py` | `b56c93d93a6dd119a6de0bd7da731dfec8e781789bbfe8d083804af8b1d5c4a9` |

Retained for private research use.
Consult the authors before redistribution.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
