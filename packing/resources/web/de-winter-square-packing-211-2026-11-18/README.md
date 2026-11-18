# Joost de Winter’s `square-packing-211` at 43e15330, Retrieved 2026-11-18

This packet retains the README of
[JoostdeWinter/square-packing-211](https://github.com/JoostdeWinter/square-packing-211/tree/43e15330bab7dd11588067167a2dd370137ef2b7)
at `43e15330bab7dd11588067167a2dd370137ef2b7`, the revision that names the sources of
the author’s packing of 211 squares (T-057).
The author pushed it in answer to the record’s question on
[jlevy/squares#1008](https://github.com/jlevy/squares/issues/1008) and named it in
[his comment of 18 November 2026](https://github.com/jlevy/squares/issues/1008#issuecomment-6971284605).
Its Frontier key is **[de Winter n211 2026-11-18]**, which carries T-057’s credit.
The packing is unchanged: the earlier
[2026-09-16 packet](../de-winter-square-packing-211-2026-09-16/README.md), under
**[de Winter n211 2026-09-16]**, keeps it as derived facts with its certificate and
replays.

## Source and Pin

| Field | Value |
| --- | --- |
| Revision | `43e15330bab7dd11588067167a2dd370137ef2b7`, tree `8f85d93ce0c2a6607d40ecab01a5028200e981d6`, the third commit; its parent is `702df9bb`, the revision T-057 cites |
| Committed | 2026-11-18T06:36:16+01:00, which is 2026-11-18T05:36:16Z; author and committer clocks agree. The message is “Name the construction and the sources of the 211 packing in the README” |
| Author | Joost de Winter, by the commit metadata and the README (“under the direction of Joost de Winter”) |
| Licence | None published: no LICENSE, and the README states no reuse terms |
| Retrieved | 2026-11-18T08:02:46Z, a full clone; `main`, the only branch, was at the pin |
| Retained here | [`source/README.md`](source/README.md), 1,413 bytes, byte-identical to the upstream file |
| Not retained | `n211__record.json` and `n211__record.svg`, pinned by digest only. Both have the same Git blobs and SHA-256 as at `702df9bb`, which the 2026-09-16 packet pins |

The commit changes `README.md` alone, from 84 bytes to 1,413.
[`acquisition/declaration.json`](acquisition/declaration.json) is what
`devtools.acquire_source` read, and it wrote
[`acquisition/sources.json`](acquisition/sources.json) and
[`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256), the
SHA-256 of all three files.
From `packing/`, this command re-derives the packet from its manifest:

```bash
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  de-winter-square-packing-211-2026-11-18 --check
```

**Why the README is retained.** The repository states no licence.
The author submitted this revision to the repository on #1008, and the owner’s ruling of
24 October 2026 (think-cnn7) presumes permission to retain an author’s own submitted
material. The README is his own statement of his sources.
The licence follow-up is think-zx9y, which does not hold this import.
The packing is not retained here; the earlier packet keeps it as derived facts.

## What the README Says

The README says the packing combines a 64-square rectangular component from Arslanov,
Mustafin and Shangitbayev (2021), a computationally found 30-square component, and two
aligned grids of 99 and 18 squares; 64 + 30 + 99 + 18 = 211.

“The numerical search and refinement were performed with GPT-6 Astra under the direction
of Joost de Winter. Earlier solutions and optimization scripts supplied to the model had
been developed with Claude Opus and previous GPT models.”

Its Sources section names three sources:

- M. Z. Arslanov, S. A. Mustafin and Z. K. Shangitbayev (2021), *Improved packings of
  n(n − 1) unit squares in a square*, The Electronic Journal of Combinatorics 28(4),
  P4.22, [doi:10.37236/8586](https://doi.org/10.37236/8586), as the source of the
  construction with tilted components combined with grids, and of the 64-square
  rectangular component. The record holds the paper as **[Arslanov et al.]**.
- Erich Friedman’s collection of square packings (Packing Center, “Squares in Squares”)
  and his survey, E. Friedman (2009), *Packing unit squares in squares: A survey and new
  results*, Dynamic Survey DS7, [doi:10.37236/28](https://doi.org/10.37236/28), as the
  source of the known packings used as starting points and for comparison. The record
  holds the survey as **[Friedman DS7]**.
- David Ellsworth’s records of square packings, used as starting points and for
  comparison.

## Credit

Credit is read from the source’s own files at the pinned revision (epistemics.md,
Parallel Projects and Their Credit), and this revision is the first whose files name
prior work. So T-057’s credit line is read from this key:
*de Winter after Arslanov, Mustafin, Shangitbayev, Friedman, Ellsworth*, the README’s
three sources in its order. The short form is *de Winter after Arslanov et al.*.

By attribution.md’s chain rule, every line that runs through T-057 keeps those names
too. The chain is the one the 2026-09-16 packet’s
[Lineage Request](../de-winter-square-packing-211-2026-09-16/README.md#lineage-request-17-november-2026)
checks link by link:

- T-098, Evan Daniel’s exact optimum of this packing;
- T-175, Daniil Ostashev’s design re-hardened from T-098;
- T-181, T-182 and T-188, Francisco Couzo’s continuations of that design;
- T-253, Mykhailo Polkovskyi’s re-certification of the 211 house (T-188), among others;
- T-243 at `n = 182`, Evan Daniel’s L-cut of T-188;
- T-287 at `n = 156`, Doğa Özden’s strip cut of that 182.

Each line places the five names directly after de Winter, and names Ellsworth once.
The 30-square component and the two grids are the author’s and name no one.

The AI assistance is the README’s own statement now: GPT-6 Astra for the search and
refinement, and Claude Opus and earlier GPT models for the earlier solutions and
scripts. Until this revision it rested on the issue alone.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
