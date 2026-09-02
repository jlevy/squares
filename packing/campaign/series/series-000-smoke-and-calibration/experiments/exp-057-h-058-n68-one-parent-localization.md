---
title: exp-057 — H-058 n = 68 one-parent localization
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-057
  series: series-000
  title: Bind the reported n = 68 side token to admissible exact and directional semantics
  date: '2026-09-02'
  hypotheses:
  - H-058
  tier: exploratory
  known_defects:
  - D-419
  subject:
    label: preregistered side-semantics binding for one n = 68 parent source
    engine: sqpack UnitSquare one-parent production adapter 0.1.0-side-bound
    engine_commit: 11ce70ee
    assurance: verified
    method: exact-algebraic
    host_system: linux x86_64 container, Python 3.14
    selftest_passed: true
  instance:
    axis: n
    point: 68
    role: calibration
  method:
    control: >-
      Byte-identical canonical receipts under normal and optimized Python over named
      guards run against injected in-memory SVG bytes and a temporary output root only:
      the four new binding mutations `unbound-token`, `wrong-direction`, `wrong-quantum`
      and `changed-released-gain`, the frozen-parent contract refusal
      `unfrozen-parent-contract`, and the twenty already admitted exp-054 mutations,
      which stay reachable through the unchanged `run.py` selftest. No target, source or
      network channel is opened by any control.
    candidate: >-
      A frozen side-semantics module and a bound entry point that compose the unchanged
      exp-054 adapter, runner and verifier with an exact or directional side value per
      declared model, so `production_model_factory` receives a bound `Fraction` instead
      of `None` and the three models can terminate in a geometry outcome rather than
      three typed `serialization-refusal` outcomes.
    runs_per_condition: 1
    interleaved: false
    operator: claude-opus-5
    commit: 11ce70ee
    dirty: true
    entry_point: cases/unitsquare_precision/production/bound_run.py
    command: >-
      uv run --frozen python -m cases.unitsquare_precision.production.bound_run --record
      campaign/series/series-000-smoke-and-calibration/results/exp-057-h-058-n68-one-parent-localization.json
    budget: >-
      Agenda-015 BC-138 gives this binding 150 minutes through 2026-09-02T06:43:00Z, of
      which 0--25 preregisters this record before any network access, 25--75 implements
      the binding without editing a frozen file, and 75--100 stops at the different-lane
      W2 readmission gate. The declared parent is retrieved only under BC-139, and only
      if BC-143 routes it.
    record: campaign/series/series-000-smoke-and-calibration/results/exp-057-h-058-n68-one-parent-localization.json
  effort:
    timebox: >-
      One 150-minute BC-138 wall through 2026-09-02T06:43:00Z, of which the lane's own
      writing stops at the 100-minute W2 gate; the coordinator owns readmission.
    wall_seconds: 1000
    agent_minutes: 16.666666666666668
    stopped_by: guard
  results:
  - shape: determination
    question: >-
      Were all three side models derived from source evidence under their own declared
      quantization rules, as the conjunctive BC-138 admission criterion requires?
    role: guard
    outcome: invalid
    checked_by: >-
      Independent Max-level review traced `_source_interval` to exactly six-digit SVG
      coordinate tokens and found no source declaration that applies nearest-six or
      truncate-six semantics to the fourteen-digit release-text side token. The literal
      printed-rational point model remains mechanically valid but cannot satisfy the
      three-model criterion alone.
  verdict:
    decision: unresolved
    needs_review: true
    primary_criterion: >-
      The binding is admissible only if every declared model receives an exact or
      directional side value derived from the reported token by the model's own declared
      quantization rule, every directional threshold is at most one quarter of the
      released 7.68618004216131e-5 gain, the four named binding mutations and the
      frozen-parent contract refusal all fire, the normal and optimized receipts are
      byte-identical, and the frozen adapter, runner, verifier and refusal bytes are
      unchanged.
    reason: >-
      The release supports the literal printed-rational point model but supplies no
      provenance for applying either six-decimal coordinate rule to its fourteen-digit
      side token, so the conjunctive binding stops before BC-139 and H-058 remains
      unmeasured.
    commit: 11ce70ee
    resume_from: >-
      The frozen exp-054 instrument at adapter.py SHA-256
      9b503050115a5a48b01ec9f4d348b869495fbe4ee4847dc83188b05a3352f539, run.py
      8cef0f9cd4f473e594ed55e650be2fe7b286a798d2a94e5edb0a35efb7b12d54, verify.py
      e39a6a725e7af01a2e1796e1a218576f76b8a2ec2cecf7fbde3f38aeb9630a7a and focused test
      17f4be0611fb02419d9007222f07b3f585b290c03866403a1d2bd5da954f01df, plus the bound
      side semantics registered here. A future literal-only localization requires a new
      prospectively frozen hypothesis and experiment; exp-057 cannot narrow its
      three-model criterion after review.
---
# Exp-057 — H-058 `n = 68` One-Parent Localization

Exp-054 admitted a target-blind production adapter whose reported side token is
deliberately unbound: `_exact_side()` refuses a `None` side, so
`production_model_factory(expected_polygon_count=68, side=None)` returns three typed
`serialization-refusal` outcomes and no geometry.
This round binds the side, and only the side.
It edits no frozen file, opens no network, source or target channel, and produces no
result.

## Frozen Bindings

| Binding | Value |
| --- | --- |
| Reported side token | `8.80345993651653` (`adapter.REPORTED_SIDE_TOKEN`) |
| Parent URL | `https://kingbird.myphotos.cc/packing/square-68.svg` |
| Parent SHA-256 | `558fbdddfeb0b2f8752b88e172d2776544beb4d2a7122189ef77c1e1c5ebdc6d` |
| Released gain | `7.68618004216131e-5` = `768618004216131/10000000000000000000` |
| One-quarter threshold | `192154501054032.75/10000000000000000000` ≈ `1.9215450105403275e-5` |
| Six-decimal quantum | `1/1000000` |
| Frozen `adapter.py` SHA-256 | `9b503050115a5a48b01ec9f4d348b869495fbe4ee4847dc83188b05a3352f539` |
| Frozen `run.py` SHA-256 | `8cef0f9cd4f473e594ed55e650be2fe7b286a798d2a94e5edb0a35efb7b12d54` |
| Frozen `verify.py` SHA-256 | `e39a6a725e7af01a2e1796e1a218576f76b8a2ec2cecf7fbde3f38aeb9630a7a` |

The parent URL and digest are declarations here, not access authority.
This round retrieves nothing.

## The Binding

The reported side token is one printed decimal string.
Each declared model reads it by that model’s own quantization rule, which is the rule
`adapter._source_interval` already applies to a source coordinate token: the literal
model keeps a degenerate point interval, and the two six-decimal models keep a closed
interval of one quantum, placed symmetrically for nearest rounding and away from zero
for truncation.
Let `v = 880345993651653/100000000000000`, the exact decimal rational the
token prints, already in lowest terms because its numerator ends in 3 and the
denominator is `2^14 * 5^14`.

| Model | Side interval | Width | Direction | Scalar admitted |
| --- | --- | ---: | --- | --- |
| `declared:svg-literal` | `[v, v]` | `0` | exact | `v` |
| `nearest-6` | `[v - 1/2000000, v + 1/2000000]` | `1/1000000` | symmetric about `v` | `v` |
| `truncate-6` | `[v, v + 1/1000000]` | `1/1000000` | away from zero, `v` is the lower endpoint | `v` |

Both interval widths and both half-widths are at most one quarter of the released gain:
`1/1000000 <= 192154501054032.75/10000000000000000000`, and the literal model’s
threshold is exactly `0`. The comparison is exact rational arithmetic, never a float.

The token has fourteen fractional decimals rather than six, so it is not itself a
six-decimal serialization and `adapter._source_interval` would refuse it as a coordinate
token. That refusal is about coordinate tokens, and the side is not one: it is the
reported container side, published in the release text and not in the SVG. The binding
therefore states, for each model, the interval that the same quantum and the same
direction produce when applied to the printed side token, and the six-decimal models
keep the six-decimal interval semantics they already declare for the coordinates they do
read.

## Why a Scalar Side Is Sound

`production_model_factory` accepts `side: Fraction | None`, a scalar, and this round may
not change that signature.
The binding therefore admits the single representative `v`, which lies in all three
declared intervals: it is the only point of the literal interval, the center of the
`nearest-6` interval and the lower endpoint of the `truncate-6` interval.

That is sound in the direction this round needs.
Every normalized cell in `adapter._normalized_cells` is `side` times a nonnegative
container-relative ratio, so for a side interval `[s_lo, s_hi]` and any fixed coordinate
interval `[a, b]` with `0 <= a <= b`, the cell at the scalar `v` is
`[v*a, v*b] ⊆ [s_lo*a, s_hi*b]`, the cell under the full interval semantics.
The sought outcome is existential — a compatible rigid unit-square pose whose
inverse-mapped corners lie inside their matched cells — and the unit square’s side stays
exactly 1 under any container normalization.
Shrinking the cells can only make that existence harder.
So a `compatible` outcome at `v` transfers to the full interval semantics, while a
refusal at `v` transfers to nothing: it stays `unresolved` or a typed refusal and can
never reject an interval model.
An interval-valued side would need a different factory signature, which would mean
editing a frozen file; the under-approximation is the admissible binding available
without one, and it is recorded as an under-approximation rather than as the interval
semantics themselves.

## Model Order

The parent model order is X-011’s fixed order, unchanged: `declared:<stable-id>`
lexicographically, then `nearest-6`, then `truncate-6`. In this adapter that is
`declared:svg-literal`, `nearest-6`, `truncate-6`, which is also `verify._MODELS` and
the `model_order` field of every published result.
A later model never rescues an earlier one, and the models are never collapsed into one
apparent contact graph.

## Named Mutations

The binding is refusable.
Each of these fires a typed, named guard:

1. **`unbound-token`.** A `None`, empty or whitespace token yields no side; the binding
   refuses instead of inventing one, preserving exp-054’s `serialization-refusal`
   boundary.
2. **`wrong-direction`.** Declaring `truncate-6` as reaching downward from a positive
   token, or `nearest-6` as one-sided, contradicts `adapter._source_interval` and is
   refused.
3. **`wrong-quantum`.** Any quantum other than `1/1000000` for a six-decimal model is
   refused, including a quantum that would still satisfy the one-quarter rule.
4. **`changed-released-gain`.** A released gain other than `7.68618004216131e-5` is
   refused, so the one-quarter threshold cannot be widened by restating the gain.
5. **`unfrozen-parent-contract`.** A bound dependency set whose contract does not name
   the frozen URL and digest is refused before any opener is constructed, exactly as
   `run.production_dependencies` refuses it.

A malformed token — one that is not a finite exact decimal, or that carries an exponent
or stray syntax — is refused by the same typed error as `unbound-token`’s family.
No guard is a bare `assert`, so the receipts are byte-identical under `python -O`.

## Claim Boundary

This round binds semantics.
It measures nothing.

- It concerns **one parent source only**, and one selected polygon of it at a time.
- It **neither decides H-053** — whose registered criterion needs two successes among
  six parent-child pairs — **nor opens H-051 surgery calibration**.
- **`n = 69` is excluded**: its released improvement is about a twelfth of this one and
  it remains a later, harder control.
- **No raw source is retained.** Bytes are bounded, hashed before parse and discarded;
  the published result carries no markup and no forbidden channel.
- Instrument admission is not an H-058 sample.
  H-058 stays unmeasured until a separately routed BC-139 retrieves the one declared
  parent.

## Stopped-By Rules

The round stops and records why when any of these holds:

1. **Provenance drift.** The retrieved parent’s digest, byte size or final URL differs
   from the frozen declaration; nothing is parsed and nothing is written.
2. **Network refusal.** The policy refuses the one declared URL. That is a typed
   retrieval refusal and never a reason to fetch the source anywhere else.
3. **Mutation silence.** Any named mutation above does not fire its guard, or the normal
   and optimized receipts differ by one byte.
4. **Frozen-byte drift.** `adapter.py`, `run.py`, `verify.py`, the exp-054 focused test
   or anything under `cases/unitsquare_precision/refusal/` no longer matches its frozen
   SHA-256.
5. **Binding refusal.** The binding cannot be expressed without editing a frozen file,
   in which case the typed refusal is retained and the adapter stays unchanged.

## Result Path

`campaign/series/series-000-smoke-and-calibration/results/exp-057-h-058-n68-one-parent-localization.json`
was absent at preregistration and stays absent through BC-138. The `--record` mode of
the bound entry point runs only the literal target-blind selftest path against a
synthetic SVG under a temporary root, exactly as `run.py` does; it publishes nothing to
the canonical path.

## Independent Readmission Refusal

The author-side controls prove that the implementation is internally consistent with the
three declared intervals.
They do not prove that the retained source used those interval semantics for its side
token.

The source adapter’s six-decimal rule accepts coordinate tokens with exactly six
fractional digits.
The published side token has fourteen fractional digits and appears in
release text rather than as an SVG coordinate.
Reusing the coordinate quantum and direction therefore invents provenance for
`nearest-6` and `truncate-6`; named mutations of those invented rules cannot supply the
missing source evidence.

The literal model remains a defensible point interpretation: it reads `8.80345993651653`
as the exact rational the release prints, without asserting that the token is the
parent’s true algebraic side.
The registered acceptance rule is conjunctive across all three models, so that one model
cannot readmit exp-057. BC-139 stops before network access, the canonical result remains
absent, and H-058 is unresolved.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
