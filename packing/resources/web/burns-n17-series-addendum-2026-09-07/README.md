# Burns n = 17 Series Addendum, 2026-09-07

The rest of Sam Burns’s three-part `n = 17` series, retrieved on 7 September 2026: the
items the adjacent [`n17-lower-bounds-2026/`](../n17-lower-bounds-2026/README.md)
snapshot of 31 August does not hold, plus a replay receipt for the verifier it does
hold.

That directory’s README is a frozen input of the resumable `n = 17` certificate replay
(its SHA-256 is pinned in
[`literature-refresh-2026-09-05/`](../literature-refresh-2026-09-05/README.md)), so the
additions live here rather than in an edit to it.
Nothing here changes a bound.
The lower-bound post, its proof note and its verifier were re-fetched on the same day
and are byte-identical to the retained copies.

## What is new here

| File | What it is | SHA-256 |
| --- | --- | --- |
| `burns-n17-problem-intro.html` | Part 1 of the series, *The n=17 Square Packing Problem — Introduction*, 5 August 2026 | `d26b7ce8913ae0e47b9dd58554547392a02adc4e25c1c30b13d5072ceca9e61b` |
| `burns-alternative-packing-rounded-coordinates.json` | The coordinates file Part 2 links for its six-tilted-square arrangement | `40622c8b03e1f15d4a9c2ea083745bbe9094d8a7a9ff00b72f8851292383ca03` |
| `burns-near-record-01-alternative-packing.svg` | Part 2, figure 1: the arrangement at its topology-constrained limit | `68e7e4f5115affea9b141573f0aab8dce124d65143fc80fff974dbf5c85f5d00` |
| `burns-near-record-02-record-vs-alternative.svg` | Part 2, figure 2: Bidwell’s record beside the alternative | `297fde8414c943d21222d507b3fa3ab5c70a6677cc5c442d9b4aab1af576f7d5` |
| `burns-near-record-03-four-searches-one-topology.svg` | Part 2, figure 3: four raw search outputs collapsing onto one arrangement | `3a6dd9114b2d7105b4b2de4be23653cd78832caa6b59629f2ba3ddc1bab3c1b2` |
| `burns-near-record-04-contact-certificates.svg` | Part 2, figure 4: the contacts used by the two width certificates | `6744ac052d0933c28f32c3c5811c8a6f76c0b1247a2c6aa91f9dace245a92a4e` |
| `burns-near-record-05-angle-balance.svg` | Part 2, figure 5: the two certificate widths against the common tilt | `7c499769b6284de27211553c95829df0467cc5843d784e20bbc5af7d58d2a60b` |
| `burns-lower-bound-post-image.png` | The header image of Part 3, the lower-bound post | `6de7aecf2db71fdca5c8623eda987eab6b591e82ebbcfac59c0bf04a06f6279b` |
| `burns-intro-post-image.png` | The header image of Part 1, Bidwell’s packing | `370c0cf297867443fc06bea9e4bac566ae75406125c227fd608dd443b8a27230` |
| `burns-verifier-replay-2026-09-07.log` | Transcript of the retained 4.4811 verifier run here | `2d277c3af1fd35b1dfbc0b386222d46bc01292f875aec6ac86f61b8827856580` |

Source URLs:

- <https://sam-burns.com/posts/n17-square-packing-problem-intro/>
- <https://sam-burns.com/posts/n17-square-packing-near-record-arrangement/> (the post
  itself is retained in the adjacent directory; the figures and data file are here)
- <https://sam-burns.com/downloads/n17-square-packing/alternative-packing-rounded-coordinates.json>

The five SVG figures are Matplotlib 3.10.8 renderings dated 5 August 2026. They carry
the drawn square polygons in figure coordinates and are illustration, not a certificate;
the JSON is the data behind them.

## The introduction post

Part 1 states the problem, names Bidwell’s 1998 packing at about `4.675530` as the
unbeaten record, and describes it as ten axis-aligned squares, six at about `39.8°` and
one at about `53.4°` — the last being the complement of the `-36.62°` tilt this
repository records, so the two descriptions agree.
It gives the best proven lower bound as `(40√2 + 19)/17 ≈ 4.4452`, Green’s value from
Friedman’s survey, and does not mention Brandwijk’s `s(17) > 89/20 = 4.45` capsule of 18
July 2026 (retained in `literature-refresh-2026-09-05/`), so the series’ baseline was
already superseded when it was written.
The search method is a learned model that takes a random arrangement and packs it
tighter by small adjustments, with code, data and trained weights in the Squarl
repository. Its outcome, in the author’s words: “The world record was not broken.”

## The coordinates file, checked

The JSON declares format `squarl_n17_blog_rounded_coordinates_v1`, container width
`W = 4.677648294965133`, a common core angle of `0.6917068161801347` radians, the six
core indices, and the defining equations.
The author marks it “for illustration, not as a rigorous non-overlap certificate.”

A read-only check on 7 September 2026, in binary64 with a separating-axis overlap test:

- 17 squares; 11 at angle `0` and 6 at `39.6318812275°`, as the post says.
- Every corner lies in `[0, W]^2`; the largest coordinate is exactly `W` and the
  smallest exactly `0`, so the arrangement needs exactly the declared side.
- The largest pairwise penetration is `8.9e-16`, rounding noise; 25 pairs and 26
  corner-to-wall incidences are within `1e-6` of contact.
- The angle quintic `5q^5 + 5q^4 + 3q^3 - 3q^2 - 3q + 1` has two real roots in `(0, 1)`:
  `q = 0.63785262957341249` gives `θ = 39.6318812275532°`,
  `W = 4 + 2/q - 1/q^2 = 4.677648294965135`, and Burns’s two certificate widths
  `A(θ) = B(θ) = 4.677648294965133`, with the side quintic
  `W^5 - 11W^4 + 41W^3 - 37W^2 - 81W + 19` vanishing to `5.7e-14`; the other root gives
  a negative `W` and is spurious.
- The JSON’s `W` and `θ` agree with the algebraic values to `2e-15` and `2e-14`.
- The side exceeds Bidwell’s `4.675530093604551` by `0.0021182013605818`.

This confirms the file describes what the post describes.
It does not reconstruct the contact graph, verify the arrangement exactly, or decide
whether the topology differs from Bidwell’s; those are `think-t5va`’s.

## The 4.4811 verifier, replayed here

The retained `burns-verify-n17-lower-bound-4_4811.py` was run unchanged on 7 September
2026 with the project’s `uv` environment (CPython 3.14.0rc2, the 3.14 build `uv` could
provision in the session’s container; NumPy 2.5.2). The transcript is retained in
`burns-verifier-replay-2026-09-07.log` and reads, in full:

```text
atoms = 268
total_weight = 169476/10000 = 16.9476
angle_net_size = 181
b*(1+d) = 899635478111/900000000000 = 0.999594975679 < 1
orientation   0/180: min=10003/10000, global=10003/10000
...
orientation 180/180: min=10003/10000, global=10003/10000
minimum_score = 10003/10000 = 1.0003 at k=0
CERTIFICATE CONDITIONS VERIFIED.
By the scaling argument: s(17) >= 44811/10000 = 4.4811.
```

Wall time was 5.9 s. Every line matches the expected transcript printed in the proof
note’s Section 7. This is the first replay of Burns’s own certificate in this
repository; the 31 August snapshot replayed Massaccesi’s derived verifier only.
The three decisive checks are `assert` statements, so as with Massaccesi’s copy the run
proves nothing under `python -O`.

The same 268 atoms were also rebuilt in the repository’s own certificate schema
(`cases/n17_fractional_certificate/control-burns-4-4811.json`, from the note’s
constants) and handed to the repository’s two decision procedures.
The exact event-cell sweep accepts it, all five conditions holding, with least cell mass
`10003/10000` at direction 0, in 6.9 s. The interval branch and bound does not decide
it: 360 of the 361 doubled-net directions certify, and the least point mass it samples
is the same `10003/10000`, but direction 0 returns 5,820 stalled boxes as undecided.
The cause is a seam: the grid’s fifth column sits at exactly `1/2 + (L - 1)/7 = B`, so a
centre on the domain boundary `h = B/2` has that column exactly on the far edge of its
square. Closed membership counts it in the sweep; no outward-rounded enclosure can close
a region edge that lies on the domain edge.
That is a refusal, not an acceptance, and Massaccesi’s grid, which carries a margin, has
no column at `B` and is decided whole.

## The Squarl repository

The proof note credits the certificate to Burns’s *Squarl* project at
<https://github.com/sam-bee/squarl>. Inspected on 7 September 2026 at its single
squashed commit `016dff982938c69f0b7b2d63edd90d2e7e839dcc` (5 August 2026, MIT licence):
a 3.4 MB Go and CUDA reinforcement-learning library for the `n = 17` search, with a
GoMLX policy over contact-group actions and a CUDA wall-pressure polisher.
Two files bear on the record and neither is retained:

- `docs/final-search-closeout.md` reports the final nine-hour non-learning search (1162
  centre-LP candidates, 143 deep attempts) reached a best strict width of
  `4.675530095599908`, above the published reference by `2.0e-9`, and concludes the
  reference “was not beaten under the required strict validation rule.”
- `data/world-record.json` is Bidwell’s packing normalised into Squarl’s `float32`
  container, reconstructed from Ellsworth’s exact SVG; it is reference data, not a new
  arrangement.

The repository is the provenance of the near-record basin, not a source of bounds.

Retained for private research use.
Consult the author before redistribution.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
