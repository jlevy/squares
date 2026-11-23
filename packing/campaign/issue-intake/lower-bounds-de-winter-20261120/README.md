# Lower Bounds of Issues 1039, 1041 and 1042: Report Order

Joost de Winter’s reports and follow-ups of 19 November 2026 state 294 lower bounds at
156 counts from 18 to 313. This directory walks their exact endpoints in report order
against both lower lanes and the monotone floor, following the owner’s rule of 14
October 2026.

The first reports are retained in the
[19 November packet](../../../resources/web/de-winter-lower-bounds-2026-11-19/README.md).
The last follow-up’s four archive members are retained in the
[155-count packet](../../../resources/web/de-winter-1042-public-replay-2026-11-20/README.md).

| File | What it is |
| --- | --- |
| `claims.yaml` | Every claim, exactly, in report order, transcribed from the retained files |
| `classification.json` | The receipt of `devtools.lower_bound_claims` |

From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.lower_bound_claims \
  campaign/issue-intake/lower-bounds-de-winter-20261120/claims.yaml \
  --check campaign/issue-intake/lower-bounds-de-winter-20261120/classification.json
```

`--table FILE` writes the receipt as one Markdown table, a row per claim.

## Sources and Order

| Report | Reported | Claims | Read from |
| --- | --- | ---: | --- |
| #1039 | 2026-11-19T04:49:37Z | 56 | `exact_claims.csv` in the #1039 zip, SHA-256 `9641ca15…` |
| #1041 | 2026-11-19T12:05:56Z | 34 | `lower_bounds.csv` at 21d944c |
| #1042 | 2026-11-19T18:45:38Z | 48 | `followup/best_by_count.csv` at 21d944c |
| #1042, comment 7020627554 | 2026-11-19T19:59:12Z | 1 | the comment: $s(161) \ge 8036307/625000$ |
| #1042, comment 7022143149 | 2026-11-19T21:02:44Z | 155 | `certificate.json` in the retained base85 archive |

The case baseline is `main` at `ad02e1650b1c`. The walk reads both lower lanes from 1 to
313\. The last comment was edited at 02:02:32 UTC on 20 November and the packet retains
that revision.

## The Walk

| Report | Current within this walk | Superseded within this walk | Consequence | Below or equal to the floor |
| --- | ---: | ---: | ---: | ---: |
| #1039 | 1 | 48 | 7 | 0 |
| #1041 | 0 | 34 | 0 | 0 |
| #1042 | 0 | 48 | 0 | 0 |
| #1042, comment 7020627554 | 0 | 1 | 0 | 0 |
| #1042, comment 7022143149 | 148 | 0 | 7 | 0 |

The #1039 claim at 19 is the one earlier row still current within this walk.
Each of the two sets of seven monotonicity rows inherits its report’s own 101, 122 and
145 endpoints at 102, 123–125 and 146–148.

Issue #1060 later raises all 153 endpoints it shares with the final #1042 comment.
Its table has no rows at 18 or 20. The 61 corner-family rows in the 155-count archive
depend on T-180’s unchanged-region coverage.
Numerical standing here leaves proof coverage and registration open under think-fv42 and
think-4iec.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
