# Session 184: TailA Dependency Reports

The [manifest](../../../hosted/n17-session-184-tail-a-dependencies.yaml) retains both
complete dependency reports from
[exp273](../../series/series-000-smoke-and-calibration/experiments/exp-273-h282-tail-a-dependency-inventory.md)
as deterministic gzip assets.
The original raw reports remain intact and ignored in the experiment result directory,
outside disposable scratch.
Decompression reproduces their bytes exactly; the small tracked
[summary](../../series/series-000-smoke-and-calibration/results/exp-273-tail-a-dependency-inventory/summary.json)
records raw byte identities, inputs and the common deterministic inventory identity.

| Report | Raw bytes | Compressed bytes |
| --- | ---: | ---: |
| `inventory.json` | 14,921,634 | 393,099 |
| `fresh-inventory.json` | 14,921,640 | 393,103 |

Both complete reports have identical deterministic cores, excluding invocation and
source metadata. The geometric and validation dependency channels both retain all 17
owners. This conservative inventory supplies no smaller admission, owner necessity or
minimality proof.
Geometry, exclusion, smaller-mask admission and minimality flags remain
false.

From `packing/`, use the project Python 3.14 environment with mounted writable external
scratch and explicit `TMPDIR`, `UV_CACHE_DIR` and `CARGO_TARGET_DIR`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.hosted_data fetch \
  --manifest hosted/n17-session-184-tail-a-dependencies.yaml
uv run --frozen --all-extras --group dev python -m devtools.hosted_data check \
  --manifest hosted/n17-session-184-tail-a-dependencies.yaml
```

Offline compressed-object checks passed.
Release publication and a clean fetch have not been verified; staging does not establish
either. These two objects are separate from the original saved TailA proof objects and
the older missing hosted inventory.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
