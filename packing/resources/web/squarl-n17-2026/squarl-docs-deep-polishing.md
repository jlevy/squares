# Deep polishing

Squarl has two deliberately separate polishing paths:

- **Fast polish** is the batched CUDA wall-pressure solver used during every
  rollout. It discovers useful contact basins at high throughput.
- **Deep polish** is a sparse float64 topology optimiser for provisional
  records, topology representatives and final evaluation. It never replaces
  the rollout solver.

Deep polishing infers one directed SAT branch for each of the 136 square
pairs. A separator is

```text
sign * axis(owner_square, local_axis) dot (centre_second - centre_first)
    >= projected_radius(first) + projected_radius(second)
```

where `local_axis` is 0 or 1 and `sign` is `-1` or `+1`. The branch with the
largest current SAT margin is selected. A pair is ambiguous when the two best
margins differ by at most `5e-5` square widths; only these pairs may enter the
bounded alternative-branch beam.

Boundary emitters may add a temporary positive entry margin to a replacement
axis while constructing a legal seed on the far side of that boundary.
Ordinary inferred production separators keep this margin at zero.

For fixed angles, Gonum's float64 simplex LP solves all 34 centre coordinates
and container width together under 68 wall constraints and 136 directed pair
constraints. A verified feasible simplex basis is reused between nearby angle
proposals; an infeasible or ill-conditioned cached basis falls back to Gonum's
normal phase-I solve. Near-axis angles within `0.002` radians are snapped to an
exact multiple of `pi/2`. Other angles within `0.01` radians are tied initially,
optimised by a bounded Nelder–Mead search, then released as independent angle
variables. Default budgets are 96 clustered and 32 released evaluations. The
ambiguous-branch beam considers at most two pairs, keeps four states and fully
refines at most one alternative.

The LP result is retained in float64. Two float32 candidates are then made: a
direct rounded candidate and one with square size reduced by an initial
`2e-7` container-width padding (up to `1e-4` if needed). Both run twice through
the ordinary deterministic CUDA `Finish` path. An improvement is accepted only
when both replays agree within `5e-7`, pass independent wall/SAT verification
within `2e-7`, and improve the legal fast-polished input. Record polishing has
a five-minute outer deadline, checked between complete LP solves. A timeout,
infeasible branch, numerical failure or failed replay leaves that input
unchanged. Production callers retain every atomic stage snapshot and can use
`ReplayCompletedSolution` to replay a verified float64 stage directly, without
restarting the remaining angle search.

Use fast polishing during ordinary training:

```text
make train POLISH_MODE=fast
```

To deep-polish only provisional run records:

```text
make train POLISH_MODE=deep
```

For a saved arrangement:

```text
make deep-polish \
  DEEP_POLISH_INPUT=/workspace/data/best-ever.json \
  DEEP_POLISH_OUTPUT=/workspace/data/experiments/deep-polish.json
```

`make validate-deep-polish` runs the gated CUDA reference validation. It checks
the `4.676313884573993` input's centre-only result, full record-basin
convergence, ten nearby starts, the `4.677648294965133` older topology, and
double replay legality. The generated JSON report includes exact widths, LP
attempts and per-stage runtimes. The demonstrated primary pass took 30.6
seconds on the development GPU: 0.38 seconds for the centre LP, 22.3 for
clustered search, 6.8 for release, and 1.1 for two CUDA replay batches. The
complete default path also examined four bounded ambiguous branches; that
added 29.6 seconds for a 60.5-second total on the same input.
