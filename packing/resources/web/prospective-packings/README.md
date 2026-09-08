# Prospective Packing Sources

This directory retains the four UnitSquare Release 1 SVGs selected by the frozen
`n = 101..324` source-availability policy: `n = 103`, `105`, `110`, and `131`. The files
were retrieved from [UnitSquare Results](https://www.hmbelvedere.com/) on 26 August 2026
and matched the SHA-256 values declared in its public
[`results.json`](../unitsquare-release1-2026/results.json).

The UnitSquare results page identifies the dataset as
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), and its creator is the
UnitSquare Project. This file is where that attribution is stated; the known-best source
index [`sources.json`](../known-best-packings/sources.json) and each derived witness keep
the source URLs, retrieval date, and upstream-declared SVG digests beside the geometry.
Git and deterministic full-content replay remain the integrity boundary for co-committed
outputs.
That statement is provenance metadata, not a repository claim about the license of the
separate Kingbird catalogue.
No Kingbird SVG above 100 is retained here.

These four files stayed here when the prospective seed was retired on 2026-09-07.
[`devtools/build_known_best_atlas.py`](../../../devtools/build_known_best_atlas.py) reads
them at this path — it resolves a UnitSquare case by looking in both retention roots
rather than by range — and its `--fetch` re-acquires them against the same
upstream-declared digests, so the known-best rebuild is what exercises them now:

```shell
uv run --frozen python -m devtools.build_known_best_atlas --fetch
uv run --frozen python -m devtools.build_known_best_atlas --check
```

The witnesses and house renderings derived from them carry no contact, chunk, rigidity,
or grammar annotations and are not a hypothesis verdict.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
