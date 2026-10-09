# Session 184: n11 First-Round Readiness Objects

These three objects retain exp268’s complete first certified round and fresh replay.
The [manifest](../../../hosted/n11-session-184-readiness.yaml) names release
`data/n11-session-184-readiness-v1` in `jlevy/squares` and verifies original compressed
bytes. All object paths are under this directory.
The
[experiment record](../../series/series-000-smoke-and-calibration/experiments/exp-268-h281-n11-first-round-relaunch.md)
and
[production/fresh receipts](../../series/series-000-smoke-and-calibration/results/exp-268-n11-first-round-control/)
retain source, inputs, endpoint checks and measured work.

| Object | Bytes | Compressed SHA-256 |
| --- | ---: | --- |
| `checkpoint-round-001.json.gz` | 25,275,233 | `48a574be6fdb483d40f6adaa9dab5133dc298233e909baa8e46f24953c1dbd42` |
| `node-7034ab8f816f7c851878a06d9b8bfd3996ecf1b31b7f06df0bde59eaedb39a09.json.gz` | 23,254,765 | `682f9a33f9ae6ee07ad5c0f31edf1a46f7c99b7ec70d6e9b99145ccfa8db4a05` |
| `seed-b07e4f328e87ff5a00b1125cb29b70b7d18742e575abcc00c3120672b06ac56c.json.gz` | 41,563 | `60668edbdf975dcc48501f03db8c8e50a1f3fec5cf7df7a583ab2d59354c1f13` |

The node’s canonical content identity is
`7034ab8f816f7c851878a06d9b8bfd3996ecf1b31b7f06df0bde59eaedb39a09`; the seed’s is
`b07e4f328e87ff5a00b1125cb29b70b7d18742e575abcc00c3120672b06ac56c`. These identify
decoded content; the manifest hashes identify compressed custody.
Production and fresh replay retain the same content identities and complete final state.
The checkpoint includes the saved seed, node, settings, round/update records and writer
provenance; it supports replay without relying on an old result-directory path.

Run recovery from `packing/`, using the project’s Python 3.14 environment and mounted,
writable external scratch.
Set `TMPDIR`, `UV_CACHE_DIR`, `CARGO_TARGET_DIR` and `UV_PROJECT_ENVIRONMENT` there
before running commands so caches and the Python environment stay on that volume.
Fetch downloads and verifies all three objects; an absent release asset leaves recovery
blocked rather than establishing a clean-fetch replay.
Publication and clean-fetch success must be recorded separately.

```bash
uv run --frozen --all-extras --group dev python -m devtools.hosted_data fetch \
  --manifest hosted/n11-session-184-readiness.yaml
uv run --frozen --all-extras --group dev python -m devtools.hosted_data check \
  --manifest hosted/n11-session-184-readiness.yaml
```

For a fresh first-round replay, keep `--max-rounds 1`. Resuming the complete round-1
checkpoint then executes zero new producer updates.
Write new replay evidence to a separate external `REPLAY_DIR`; preserve the retained
objects. The registered replay ceiling was 300 seconds with a 4,096 MiB current-RSS
guard; on macOS, GNU `gtimeout` supplies the owned-process wall ceiling and ten-second
cleanup allowance.

```bash
gtimeout -k 10s 300s uv run --frozen --all-extras --group dev python \
  -m devtools.pilot_n17_capture --system n11 --cap capture --bins 32 \
  --max-rounds 1 --max-live 64 --min-width-log2 22 --hull-limit 48 \
  --core octagon --seed-grid 0 --max-seconds 300 --replay-share 0.5 \
  --max-memory-mib 4096 \
  --resume campaign/retained/session-184-n11-readiness/checkpoint-round-001.json.gz \
  --save-objects "$REPLAY_DIR/objects" --output "$REPLAY_DIR/fresh-replay.json"
```

Require `PASS_REPLAYED`, eleven checked steps, `final_state_agrees=true`, identical
canonical seed/node content, unchanged round/update records and no new production.
Record source drift explicitly; the accepted exp268 replay had none.
Top-level producer success alone is insufficient.
The exact endpoint survived seed admission and every certified update, giving twelve
checks.

This evidence establishes one complete eleven-owner round, endpoint retention and
first-round readiness/cost.
It proves neither the separate fifteen-round contraction criterion nor n17 capture, a
new side bound or a global exclusion.
The RSS guard samples checked boundaries rather than every allocation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
