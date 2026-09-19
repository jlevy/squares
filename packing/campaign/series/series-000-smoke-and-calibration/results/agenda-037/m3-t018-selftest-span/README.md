# M3 T-018 Selftest After Span-Sweep Encoding

Status: **unresolved**. Not a kill. Not an eleven-candidate.

Session-139 re-ran `devtools.pierce_t018_sites --selftest` after the event-cell
encoder stopped expanding every cell into an `O(cells × sites)` boolean chunk.
The 5-direction net encoded 12,702,392 reachable cells to 19,072 unique covering
rows in under the 20 s limit and HiGHS returned an integral incumbent of 9
sites. The row set is truncated, so nine is a lower bound on this net only: it
cannot nominate an eleven-candidate and it is not a kill (`piercing >= 12`).

A float LP was not used. T-018's shrink was not the ownership object.

## Command

From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.pierce_t018_sites \
  --selftest \
  --output-dir campaign/series/series-000-smoke-and-calibration/results/agenda-037/m3-t018-selftest-span
```

## Outcome

| Quantity | Value |
| --- | --- |
| Unique sites | 1121 |
| Directions | 5 |
| `search_status` | `feasible` |
| `piercing` | 9 |
| `cover_rows` | 19072 |
| `truncated_rows` | true |
| `m3_verdict` | `unresolved` |
| `optimizer_ran` | true |
| `float_lp_used` | false |
| Wall | 14.6 s |

Machine JSON: `pierce-t018-receipt.json` beside this file.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
