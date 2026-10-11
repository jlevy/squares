# Numeric-Cap First-Round Readiness

[H-289](../../hypotheses/H-289-n17-numeric-cap-first-round-readiness.md) completed a new
full17 cell seed at the checked cap `935106018721/200000000000`, followed by 16
contracting-owner updates.
Square6 retained its coarse rows.
All17 exact endpoint poses survived the seed and every update.

Production took175.86083s. Fresh resume took66.47918s and replayed the complete original
seed and16 saved steps, with1024 checked rows and143498 events.
Canonical identities, round/update records and final state agreed.
Fresh resume produced no new update and made one final full17 endpoint check.
The retained `checked_after:17` field is inherited production evidence.

The
[experiment record](../../series/series-000-smoke-and-calibration/experiments/exp-276-h289-numeric-cap-first-round.md)
retains the input join, phase receipts, supervision and object custody.
These results establish readiness and measured cost; they establish no terminal result
or exclusion.

Three unique native objects are retained through
[the hosted-data manifest](../../../hosted/n17-session-184-numeric-cap-readiness.yaml):
the original seed,16-step node and complete round001 checkpoint,
totaling23,883,806bytes. Production and fresh saved seed/node gzip bytes agree.
Original copies remain intact.
The manifest is staged; publication and clean-fetch recovery are pending.

Run these commands from `packing/`, with project Python3.14.7 and task-specific external
scratch variables:

```bash
uv run --frozen --all-extras --group dev python -m devtools.hosted_data fetch \
  --manifest hosted/n17-session-184-numeric-cap-readiness.yaml
uv run --frozen --all-extras --group dev python -m devtools.hosted_data check \
  --manifest hosted/n17-session-184-numeric-cap-readiness.yaml
```

The original scientific replay settings and300-second ceiling are frozen in exp276’s
execution manifest. Its checkpoint resume uses `--max-rounds 1`; continuing to another
round requires a new selection and registration.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
