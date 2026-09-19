# M3 T-018 9-Direction Search Receipt

Status: **unresolved**. Not a kill. Not an eleven-candidate.

Session-139 ran `devtools.pierce_t018_sites --search --direction-steps 8`
(`9` net directions) with a 180 s limit on T-018's 1121 unique sites at
`19/5` with closed unit squares. Event-cell encoding hit the time limit
before HiGHS ran, same as the 5-direction 20 s selftest. Timeout is unresolved.
A float LP was not used.

Encoding, not the MIP, is the cost. A 36-net scientific search needs a cheaper
event-cell encoding, not only a larger wall.

## Command

From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.pierce_t018_sites \
  --search --direction-steps 8 --time-limit-s 180 \
  --output-dir campaign/series/series-000-smoke-and-calibration/results/agenda-037/m3-t018-net8
```

## Outcome

| Quantity | Value |
| --- | --- |
| Unique sites | 1121 |
| Directions | 9 |
| `search_status` | `timeout` |
| `m3_verdict` | `unresolved` |
| `optimizer_ran` | false |
| `float_lp_used` | false |
| Wall | 180.6 s |

Machine JSON: `pierce-t018-receipt.json` beside this file.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
