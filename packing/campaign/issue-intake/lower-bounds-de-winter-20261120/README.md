# Lower Bounds of Issues 1039, 1041 and 1042: Report Order

Joost de Winter’s three reports of 19 November 2026 claim raised lower bounds at 80
distinct counts from 19 to 218, 139 claims in all with #1042’s follow-up comment at 161.
This directory transcribes them and walks them against the case records in report order,
by the owner’s rule of 14 October 2026: each report is recorded as long as it is
stronger than the last.
The certificates are retained in the
[`de-winter-lower-bounds-2026-11-19`](../../../resources/web/de-winter-lower-bounds-2026-11-19/README.md)
packet; nothing here reads them.

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

The start is the case records on `main` at `7a3b186a2e`, both lower lanes at every count
from 1 to 218, and the monotone floor, the stronger lane at any smaller count.

## The Walk

Every one of the 139 claims is above both lower lanes of its case and above the monotone
floor, and no later report is weaker than an earlier one at any count.

| Report | Current | Superseded by a later report | Consequence | Not an improvement |
| --- | ---: | ---: | ---: | ---: |
| #1039 | 23 | 26 | 7 | 0 |
| #1041 | 2 | 32 | 0 | 0 |
| #1042 | 47 | 1 | 0 | 0 |
| #1042, comment at 161 | 1 | 0 | 0 | 0 |

- **Current**, the strongest report at its count: #1039 at 19, 20, 26, 27, 29, 30, 31,
  37–41, 43, 51, 66, 82, 83, 90, 92, 101, 110, 122 and 145; #1041 at 105 and 111; #1042
  at its 47 other counts; the comment at 161.
- **Superseded**, recorded in order and passed by a later report: #1039’s other 26
  direct counts, all but 105 and 111 of #1041’s, and #1042’s 161.
- **Consequences**, #1039’s seven monotonicity rows at 102, 123–125 and 146–148, equal
  to its own 101, 122 and 145; they go in the parent’s scope.
  #1041’s 115, a certificate of its own at 87/8, equals its 114 and is superseded by
  #1042’s 115.

## What This Does Not Decide

Whether any certificate is sound.
The walk compares numbers only; the replays and reviews of bead think-fv42 decide the
bounds.

A fourth report, #1042’s comment 7022143149 (21:02:44Z on 19 November, edited 02:02:32Z
on 20 November), claims 155 counts from 18 to 313 in a base85 archive, many of them
above the claims here; it is not walked here and is an import of its own.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
