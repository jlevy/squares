# Prospective Packing Sources

This directory retains the four UnitSquare Release 1 SVGs selected by the frozen
`n = 101..324` source-availability policy: `n = 103`, `105`, `110`, and `131`. The files
were retrieved from [UnitSquare Results](https://www.hmbelvedere.com/) on 26 August 2026
and matched the SHA-256 values declared in its public
[`results.json`](../unitsquare-release1-2026/results.json).

The UnitSquare results page identifies the dataset as
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The retained manifest keeps
the creator, source URLs, retrieval date, and upstream-declared SVG digests with the
derived witnesses. Git and deterministic full-content replay remain the integrity
boundary for co-committed outputs.
That statement is provenance metadata, not a repository claim about the license of the
separate Kingbird catalogue.
No Kingbird SVG above 100 is retained here.

Run the offline rebuild after acquisition:

```shell
uv run --frozen python -m devtools.build_prospective_atlas --update
uv run --frozen python -m devtools.build_prospective_atlas --check
```

The generated witnesses and house renderings contain no contact, chunk, rigidity, or
grammar annotations and are not a hypothesis verdict.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
