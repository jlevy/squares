# BC-378 / H-240 receipt: n=21, L = 122/25, B = 9977/10000

Status: **the confirm half of the criterion is met by set C and awaits the Fable max W2
review H-240 requires before any register entry.** `decide_certificate` printed
RETAINABLE on a frozen point certificate of mass `5036431/250000 = 20.145724 < 21`.
Nothing here is a register entry or a retained result until the coordinator admits the
bytes and the review passes.

Instrument commit: `69dac09a029de16ecb86c2072c1f18a67bd42794` (worktree `w3-review`,
branch `claude/w3-overnight-2026-09-23`). No tracked `packing/devtools` or `packing/src`
file differed from HEAD at launch.
Every run was single-process, under `OMP/OPENBLAS/MKL/VECLIB_MAXIMUM_THREADS=1`. The
gate ran with `PACK_JOBS=3`. The machine was shared, with load averages between 16 and
158 over the session.

## Common Command Shape

From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_colgen \
  --n 21 --side 122/25 --shrink 9977/10000 --direction-steps 181 \
  --grid-counts auto --scale 4000000 --support-cap 32 \
  --column-rounds 1 --max-rounds 80 --deadline-seconds <D> <SITE FLAGS> \
  --freeze <X>-covering.json --freeze-family <X>-family.json \
  --json <X>-run.json --row-log <X>-rows.jsonl --log <X>.log
```

Auto grids resolved to `(34, 46, 56)` at inset `1/2` for all three sets.

| Set | Site flags | D (s) | Seed sites | Orbits / sites / rows | LP rounds | Wall | Stop | Objective |
| --- | --- | ---: | ---: | --- | ---: | ---: | --- | --- |
| A | `--seed-certificate cases/n20_fractional_certificate/certificate.json --seed-map scale --seed-windows 6` | 3600 | 2256 | 1106 / 8472 / 13227 | 54 | 3814.2 s (real 63m35s) | deadline, unconverged; least covered 0.993953, 144 violated | 20.040960 (float LP on an incomplete row set; not a value) |
| B | `--seed-windows 5` | 3600 | 400 | 861 / 6616 / 12376 | 61 | 1908.8 s (real 31m50s) | converged | 20.131946; frozen mass `20132143/1000000`, 1460 atoms |
| C | `--seed-windows 0` | 2700 | 0 | 806 / 6216 / 8895 | 36 | 690.9 s (real 11m32s) | converged | 20.145556; frozen mass `5036431/250000`, 1228 atoms |

Set C’s first launch (09:04:49Z) was killed by an external SIGTERM at 09:17:27Z. The
same SIGTERM ended the n12 leg-2 run and a ceiling reader in the same second.
The system load average was 148 at the time.
The partial run is kept in `C-killed-1/`, and nothing from it was used.
C was relaunched unchanged from `exp-229-n21-run-C.command.txt`.

## Gate

For each converged freeze, a copy was declared with a one-worker sweep, then decided:

```bash
cp X-covering.json X-covering-declared.json
PACK_JOBS=1 uv run ... python -m devtools.declare_least_cell_mass X-covering-declared.json
PACK_JOBS=3 uv run ... python -m devtools.decide_certificate [--dump-stalls X-stalls.json] X-covering-declared.json
```

**Set C: RETAINABLE.**

```text
n = 21, L = 122/25 = 4.880000, 1228 atoms, mass 5036431/250000 = 20.145724
  ceiling 4.988500, certifies every n >= 21
  interval accepted=True enclosure=(Fraction(250001, 250000), Fraction(250001, 250000)) boxes=4289657 stalled=0 (67s)
  exact    accepted=True least=250001/250000 (15s)
  RETAINABLE: both routes accept and agree at 250001/250000; sha256 b230f7cd6806343f115331caf53f02019cc634a8959359684581835a0cc7fb0f
```

The declared file differs from the raw freeze only in `least_cell_mass`, checked with a
`jq -S` diff. It declares no `variant`, so the gate decided it as `unconditional`. Its
header reads `id C-n021-fractional-122-25`, `claim "s(21) >= 122/25"`,
`direction_steps 181`, `angle_limit 207107/500000`, `symmetry D4`. The declaration sweep
took 65 s and reported least cell mass `250001/250000`.

**Set B: REFUSED by a stalled interval route, not by a counterexample.** The sweep
accepted it with least cell mass `2000013/2000000`. The interval route then gave:

```text
interval accepted=False enclosure=(Fraction(3756841, 4000000), Fraction(2000013, 2000000)) boxes=4894465 stalled=1608 (206s)
REFUSED: the interval route refused it: ('Condition 5 every admissible centre covers mass 1',)
REFUSED: 1608 boxes stalled; the interval route decided nothing there
REFUSED: the enclosure has width: ...
```

The stall dump (`B-stalls.json`) puts 1608 of the 1612 stalled boxes in direction 0, the
upright squares, with zero width across centre lines such as y = 3.4015333 and y =
1.4784667 and their D4 images.
That much is measured.
The cause below is inferred:

- The freeze has 15 distinct atom rows with a partner exactly `B = 9977/10000` above.
  One example is `58777/60000` and `58777/60000 + B`, both carrying weight.
- A stalled centre line is exactly where an upright placement has both closed edges on
  two such rows. The pitch-B window lattice (`--seed-windows 5`) is the likely source.
- Set C has no windows and no row pair exactly B apart, and it decided with 0 stalls.

The enclosure’s lower end, 0.939, bounds the stalled boxes only.
It is not a covering failure.

## Determination Against the Frozen Criterion

- **Confirm:** RETAINABLE with mass below 21 is met by set C (sha256 `b230f7cd…0fb0f`).
  The W2 review is the remaining condition and belongs to the coordinator.
- **Reject:** not met.
  No site set converged at 21 or above, and none returned the grid.
- Set A’s deadline decides nothing.
  B’s refusal is an instrument stall on a degenerate seam, and it neither confirms nor
  rejects.

## Artifacts (Bytes)

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `C-covering.json` (raw freeze) | 71995 | `734765c26a91cf2a34865a7dae37bf4f6b3d0d6f21864278e90cc1ffb7d0111d` |
| `C-covering-declared.json` (decided) | 72006 | `b230f7cd6806343f115331caf53f02019cc634a8959359684581835a0cc7fb0f` |
| `C-family.json` | 33404 |  |
| `C-run.json` / `C-rows.jsonl` / `C.log` / `C.stdout` | 7931 / 2627 / 486 / 1228 |  |
| `C-decide.stdout` / `C-declare.stdout` / `C-stalls.json` | 520 / 172 / 17221 |  |
| `B-covering.json` (raw freeze) | 86509 | `b2d75e9ce503e2037d3a68110578f0de4bab4ff796ff4fa353b45affa803dca6` |
| `B-covering-declared.json` | 86522 | `787c9aca18ae67be8c6a56fb0df18da46bc47ebd233d4970fd4c8e30bb3f2b95` |
| `B-family.json` / `B-run.json` / `B-rows.jsonl` / `B.log` / `B.stdout` | 33037 / 12417 / 4402 / 486 / 1232 |  |
| `B-decide.stdout` / `B-decide-stalls.stdout` / `B-declare.stdout` / `B-stalls.json` | 768 / 622 / 175 / 193948 |  |
| `A-run.json` / `A-rows.jsonl` / `A.log` / `A.stdout` | 10836 / 3905 / 174 / 1019 | no freeze written |

The in-run `check_ceiling` screens on the priced duals report nothing near 21: B
`feasible total 9.998728` and C `feasible total 11.881470`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
