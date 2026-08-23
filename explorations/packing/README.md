# Square Packing

A self-contained project directory: the research reports, the local archive of the
literature they cite, and the exact verifier written alongside them.

`s(n)` is the side of the smallest square holding `n` non-overlapping unit squares.
The motivating case is `n = 11` — the smallest instance of this problem that is still
open. Its best known packing dates from 1979 and its best proved lower bound from 2003,
and a gap of roughly 0.088 in the side length separates them.

Two documents get you oriented, and they have different jobs.

**[`SYNOPSIS.md`](SYNOPSIS.md) is the technical root** — the single account of what this
project knows, how it knows it, and what it is doing next: the problem, the results
established here and their evidential status, the per-`n` lay of the land, the
hypothesis registry, and a roll-up of every experiment run so far.
It is kept current, reconciled against the artifacts in the gate, and points at the
artifact behind each claim rather than restating it.
Read it to understand the project.

**[The current handoff](docs/project/handoff-2026-08-23-quench-spine.md) is where the
work stands today** — what is built, what is missing, which few things are the critical
path, and the half-dozen facts that would otherwise cost an arriving agent a day.
It is dated and written to be thrown away when it stops being true.
Read it to know what to do next.

## Layout

```
explorations/packing/
├── SYNOPSIS.md             The technical root: results, status, and the experiment
│                           roll-up. Read this first.
├── docs/project/           Reports, reviews, specs, postmortems, and the dated
│                           handoff that says where the work stands today
├── docs/project/research/  The six research reports (see below)
├── campaign/               The experiment record: hypothesis registry, series, rounds,
│                           and a generated ledger. See campaign/README.md.
├── frontier/               What is known about s(n) for every n <= 100: one
│                           schema-validated artifact per case, plus editorial.
│                           See frontier/README.md.
├── resources/              Local archive of the primary literature: papers + web
│                           sources, each kept as original, cleaned .md, and raw
│                           extraction. See resources/README.md.
├── sqpack/
│   ├── field.py            exact arithmetic in Q(alpha): +, -, *, /, exact zero test,
│   │                       exact sign by rational interval arithmetic with bisection
│   ├── verify.py           separating-axis validity check, generic over the scalar
│   │                       type; exact or float backend, optional grid bucketing
│   ├── quench.py           LP-in-cell quench: solve the cell, search the angles,
│   │                       land on a named basin at solver precision
│   └── packings/trump11.py Walter Trump's 1979 packing of 11 unit squares, exactly
├── derive_field.py         derives the number field from the published polynomial
├── verify_trump11.py       verify the packing and report what it took
├── negative_control.py     show the verifier rejects bad packings, and where float64
│                           fails
├── bench.py                exact vs approximate cost, and scaling with algebraic degree
├── lp_cell.py              rebuild the fixed-angle cell as a linear program, through
│                           constraint rows sqpack/quench.py does not share
├── run_quench.py           quench annealer output, both angle methods
├── run_basin_entry.sh      perturb a known packing and measure the return
├── defects.md              generated logbook of everything that has gone wrong here,
│                           from defects.yaml
├── tools/                  checkers and generators: the soundness perimeter, the
│                           negative controls, the generated views and their drift gates
├── sqsearch/               tier-1 screening annealer (Rust)
├── test.sh                 run everything and check the expected results
└── frankensim-probe/       two experiments run against Jeffrey Emanuel's FrankenSim,
                            asking whether its certified-arithmetic and RNG layers help
                            here (see that directory's README)
```

## What has gone wrong here

[`defects.md`](defects.md) is the logbook: every bug, inefficiency and record defect
found in this toolchain, what caught it, and what now stops it recurring.
It is generated from [`defects.yaml`](defects.yaml) and checked in the gate.

It is kept because the aggregate says things no individual bug report can.
Of 28 defects, 6 were **soundness** failures — the system asserting something false
about the mathematics — and 4 of those pointed in the *flattering* direction, where the
error looks like a success.
The automated gate has caught **one** of the 28 and **none** of the 6: every soundness
failure was found by a control cell whose answer was known in advance, a rule written
down before the measurement, a generated view contradicting its source, or someone
reading carefully. And 8 fixes left no regression check behind, which is why one of them
([D-017](defects.md)) is a verbatim repeat of an earlier one.
(Counts as of 2026-08-23; [`defects.md`](defects.md) is the live tally, and
[the synopsis](SYNOPSIS.md#the-defect-record) carries the per-class breakdown,
reconciled against `defects.yaml` in the gate.)

## Conventions

[`conventions.md`](conventions.md) consolidates every convention this directory runs on
— the id scheme across all layers, file naming, artifact discipline, the evidence tiers
and what each may claim, provenance, corrections, and which rules are machine-checked
versus which rest on care.
Read it before adding an artifact, a round, or a tool.

## Reports

Written to be read in this order.
They move from what is known, to how it is computed and checked, to what to build, to
where a proof assistant fits, and finally to how to search — the strategy the tooling
exists to serve.

| Report | Scope |
| --- | --- |
| [Packing 11 Unit Squares in a Square](docs/project/research/research-2026-08-22-packing-11-unit-squares.md) | The mathematics of `s(11)`: what is proved, what is only conjectured, and why the available proof technique cannot close the gap |
| [Algorithms and Tooling for Square Packing](docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md) | How packings are searched for, refined from numerical to exact algebraic form, and verified; who holds the records and with what |
| [FrankenSim as a Rust Toolkit for Square Packing](docs/project/research/research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md) | First-hand study of a large Rust simulation framework as a source of certified-arithmetic and determinism building blocks |
| [Infrastructure for Square-Packing Exploration](docs/project/research/research-2026-08-22-infrastructure-for-packing-exploration.md) | Synthesis of the two above into a build order: three latency tiers, the language boundary, which symbolic layer to use where, and what to deliberately not build |
| [Lean for Square-Packing Proofs and Validation](docs/project/research/research-2026-08-22-lean-for-packing-proofs-and-validation.md) | Where a proof assistant fits: the upper bound is formalisable today and unclaimed, the lemma layer is the diagnostic first target, and certificates make a result checkable by someone who does not trust our code |
| [A Search Philosophy for Square Packing](docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md) | The strategy layer: why volume-weighted search fails precisely at records, the basin atlas over the LP-quench map as the deliverable, diversity over structural descriptors instead of loss-shaping, the LLM at the structural layer, and relaxation ladders into the hard instances |

The structured record of the problem’s frontier — best known packing and best proved
lower bound for every `n ≤ 100`, with provenance and per-case editorial — lives in
[`frontier/`](frontier/README.md) as soft-schema artifacts rather than as a table inside
a report, so it can be validated and queried.

Claims in the reports are separated by evidential status — proved, computationally
verified, best known, or asserted-but-unverified — and every citation resolves both to a
full reference and to a local copy in [`resources/`](resources/README.md).

The reports have been through a full technical review (2026-08-22): every substantive
claim re-checked against the archived primary sources, the central algebra re-derived
independently at 50-digit precision, and the findings applied to the documents
themselves. Corrections this produced are recorded in the `n = 11` report’s
[Corrections to Common Summaries](docs/project/research/research-2026-08-22-packing-11-unit-squares.md#corrections-to-common-summaries),
its remaining gaps in
[Open Questions](docs/project/research/research-2026-08-22-packing-11-unit-squares.md#open-questions),
and the prioritized path forward in
[A Research Program](docs/project/research/research-2026-08-22-packing-11-unit-squares.md#a-research-program).

## Plan

The implementation plan for the first experiments — search, verify, iterate on `n = 11`
and `n = 12` — is
[plan-2026-08-22-minimal-packing-toolkit.md](docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md).
It turns the six reports into seven phases and a bead tree, one epic per phase;
`tbd list --spec docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md`
shows the work items and `tbd ready` the unblocked subset.

The current standing review —
[review-2026-08-23-toolkit-docs-and-first-experiments.md](docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md)
— audits the toolkit documents, supplies the experiment method they lacked (a hypothesis
register with kill criteria, a run protocol, a series plan starting from an `n = 11`
smoke), and contributes one verified theoretical result: for fixed angles the whole
problem is a linear program, checked numerically against Trump’s packing.
Its register carries the search-philosophy report’s boil-down as hypotheses H-11–H-15
and series S6 (landscape cartography).

## Exact verification

Record packings are published as high-precision decimals, and there is no public tool
that checks one **exactly**. `sqpack` is that check.

### Why exactness needs more than precision

A valid packing has squares with disjoint *interiors*, so touching is allowed — and in a
record packing many squares touch exactly.
The separation on those pairs is exactly zero.

Floating point and interval arithmetic can prove a strict inequality; neither can prove
an equality. So a float check needs a slack tolerance to accept the true contacts, and
that tolerance is then a blind spot that accepts small overlaps.
Setting the tolerance to zero rejects the true packing instead.
`negative_control.py` demonstrates both failure modes.

The fix is representational, not numerical: put the configuration in the real algebraic
number field it actually lives in, where equality is decidable.

### Use

```bash
python3 verify_trump11.py     # exact verification of s(11) <= 3.877083590022814...
python3 negative_control.py   # exact rejects any overlap; float64 has a blind spot
python3 bench.py              # timings
python3 derive_field.py       # re-derive the field (needs sympy)
./test.sh                     # all of the above, with assertions
```

Only `derive_field.py` needs a third-party package (SymPy).
The verifier itself is standard library only.

`verify_trump11.py` output:

```
VALID: 11 squares, 55 pairs tested
  container: 20 corner coordinates exactly on the boundary
  pairs:     14 separated with zero gap, 41 strictly
  field:     Q(u), degree 8, u = tan(a/2)
  P(s) == 0 for the published degree-8 polynomial: True
  s = 3.87708359002281417730789706010096270637645566846
```

The 14 zero-gap pairs are the ones no floating-point verifier can certify.
The 33 leading digits match the value published on the
[Squares in Squares](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
record page, so this is also an independent check of that record.

### Verifying another packing

Supply the corners in an exact field and call `verify_packing`:

```python
from sqpack.field import NumberField
from sqpack.verify import verify_packing, exact_sign

field = NumberField(min_poly, isolating_interval)  # coefficients high degree first
squares = [...]  # 11 x 4 corners of FieldElements
print(verify_packing(squares, side, sign=exact_sign))
```

The work is in the first line.
Record packings are published as SVG transforms with 33-digit decimal entities and, for
the analytically solved ones, Mathematica source in an XML comment; recovering the field
means reading that by hand, once per packing.
`sqpack/packings/trump11.py` is the worked example.

For a quick, non-certifying check, swap in the float backend:

```python
from sqpack.verify import float_sign

verify_packing(squares, side, sign=float_sign(1e-9), bucket=True)
```

`bucket=True` grid-buckets the squares so pair enumeration is linear rather than
quadratic — at `n = 1000` that is 15,936 candidate pairs instead of 499,500.

### Scope

This checks that a *proposed* packing is valid, which is a different and far easier
question than whether it is optimal.
The only rigorous computer-assisted optimality proof for rotatable unit squares in any
container covers three squares in a circle (Montanher et al.
2018); nothing comparable exists for squares in a square.
