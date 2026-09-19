# M3 T-018 Selftest Receipt

Status: **unresolved**. Not a kill. Not an eleven-candidate.

Session-139 ran `devtools.pierce_t018_sites --selftest` on T-018's 1121 unique
sites at side `19/5` with closed unit squares (not the fractional shrink).
The 5-direction net's event-cell encoding hit the 20 s time limit before HiGHS
ran. Timeout is unresolved. A float LP was not used.

A 36-direction scientific search needs a larger encoding budget than 20 s.

## Command

From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.pierce_t018_sites \
  --selftest \
  --output-dir campaign/series/series-000-smoke-and-calibration/results/agenda-037/m3-t018-selftest
```

## Outcome

| Quantity | Value |
| --- | --- |
| Unique sites | 1121 |
| Directions | 5 |
| `search_status` | `timeout` |
| `m3_verdict` | `unresolved` |
| `optimizer_ran` | false |
| `float_lp_used` | false |
| Wall | 20.4 s |

Machine JSON: `pierce-t018-receipt.json` beside this file.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
