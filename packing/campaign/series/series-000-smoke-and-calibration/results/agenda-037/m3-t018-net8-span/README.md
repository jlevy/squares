# M3 T-018 9-Direction Search After Span-Sweep Encoding

Status: **unresolved**. Not a kill. Not an eleven-candidate.

Session-139 re-ran `devtools.pierce_t018_sites --search --direction-steps 8`
with a 45 s limit after the frozenset encoder landed. The 9-direction net
encoded 25,223,634 reachable cells to 31,940 unique covering rows. HiGHS
returned an integral incumbent of 9 sites. The row set is truncated, so nine
is a lower bound on this net only.

The 5-direction selftest also returned piercing 9. Extra directions did not
raise the truncated optimum. A float LP was not used.

## Command

From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.pierce_t018_sites \
  --search --direction-steps 8 --time-limit-s 45 \
  --output-dir campaign/series/series-000-smoke-and-calibration/results/agenda-037/m3-t018-net8-span
```

## Outcome

| Quantity | Value |
| --- | --- |
| Unique sites | 1121 |
| Directions | 9 |
| `search_status` | `feasible` |
| `piercing` | 9 |
| `cover_rows` | 31940 |
| `truncated_rows` | true |
| `m3_verdict` | `unresolved` |
| `optimizer_ran` | true |
| `float_lp_used` | false |
| Wall cap | 45 s |

Machine JSON: `pierce-t018-receipt.json` beside this file.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
