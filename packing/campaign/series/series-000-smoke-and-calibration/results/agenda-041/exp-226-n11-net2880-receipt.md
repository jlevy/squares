# Exp-226 The `n = 11` Threshold Atoms at the 2880-Step Net

Status: **`RETAINABLE`, and the dilation-limit theorem moves the bound.** Both routes of
the retention gate accept the frozen bytes and agree at exactly 1. Nothing is registered
by this receipt; the register entry is a separate decision.

**Reconciliation note, 2026-09-22.** This receipt records the first-party move from
T-026 to T-033. Session 152 subsequently verified Kleddamag’s stronger
`s(11) > 31/8 = 3.875` certificate, which is the current Frontier lower bound.
The unchanged fixed-core family’s refinement ceiling `955000/249507 ≈ 3.82755` is below
`3.875`; this run remains auditable method and calibration evidence and does not support
a current public-bound advance.

This is `X-042`’s slate row A6 and the `H-G` of the `n = 11` review lane, which `X-041`
called a rung to be run in an idle CPU slot and never as a block.
It was run that way, beside the review lanes, and it is the one bound movement of the
session.

## What was asked

`T-026` re-certifies the frozen `T-025` threshold atoms at the 1440-step net and takes
its bound from the dilation-limit corollary, whose value rises as the net gap `D` falls.
The open question was whether the crossing shrink `B*` **rises** under refinement, which
would mean the remaining `0.0011` of the series is not all available.

`H-G`’s kill was explicit: least charge below `M/11` at `B*` on the new directions.

## The refinement run

```
uv run --frozen --all-extras --group dev python -m devtools.measure_threshold_net_refinement \
  --certificate cases/n11_threshold_certificate/certificate-191-50-net1440.json \
  --nets 1440 2880 --workers 2 --work <work-dir>
```

89 m 36 s of wall on a contended four-core box.

| Net | `D` | `B` | least charge | verdict |
| --- | --- | --- | --- | --- |
| 1440 (control) | `207107/720000000` | `249507/250000` | `1.000000000` at direction 914 | PASS, +0 directions |
| 1440 | — | `2499281/2500000` | `1.002639737` | PASS |
| **2880** | `207107/1440000000` | `249507/250000` | `1.000000000` | **PASS, +1440 directions** |
| 2880 | — | `2499281/2500000` | `1.002639737` | PASS |

The 1440 row is a control and it reproduces the registered record exactly: its dilation
supremum is `955000*sqrt(518400042893309449)/179696714646249 = 3.826447410572939744`,
which is `T-026`’s registered surd **exactly** — the stronger statement, and the one to
make; the retained `decimal_20` carries 21 significant digits, so an earlier draft’s
“twenty-two digits” was both weaker and wrong.

**`B*` does not rise.** The 1,440 directions the finer net adds do not break the frozen
atoms, so `H-G` is confirmed and its kill did not fire.
The threshold `M/11` is `5483661432/5485530809 = 0.999659216753`, and the least charge
is exactly 1.

## The gate

```
PACK_JOBS=3 uv run --frozen --all-extras --group dev python -m devtools.decide_threshold_certificate \
  --workers 3 exp-226-n11-threshold-191-50-net2880-certificate.json
```

40 m 15 s of wall.
584 point atoms of mass `4336840816/498684619`, 320 threshold atoms of
budget `1146820616/498684619`, total `5483661432/498684619 = 10.996251384`, below 11.

Conditions 1, 1', 2', 3 and 4 hold in closed form.
Condition 5' is decided twice:

- **interval route**: `accepted=True`, enclosure `(1, 1)` — zero width — over 5,761
  directions and 23,785,079 boxes, **0 stalled**, 0 budget-exhausted, 588.1 s;
- **exact route**: least cell charge `1` at direction 1828, re-evaluated at its witness
  `(1.8583992664183653, 0.4665738637756622)` in the rotated frame by membership counting
  and agreeing, with 0 dense/slab disagreements.

```
RETAINABLE: both routes accept and agree at 1
sha256 fefcf8ac23456442f855b5bb9188fc16db3b2bf5380e0e0bd1f472ba17665219
```

## What it is worth

`devtools.dilation_corollary` on the accepted bytes:

```
sharp factor supremum = 250000*sqrt(2073600042893309449)/359341754646249
side supremum = 955000*sqrt(2073600042893309449)/359341754646249 = 3.826997548829544
the dilation-limit theorem establishes s(11) >= 955000*sqrt(2073600042893309449)/359341754646249
```

|  | exact | decimal |
| --- | --- | --- |
| `T-026`, registered | `955000*sqrt(518400042893309449)/179696714646249` | `3.826447410572939744` |
| **this certificate** | `955000*sqrt(2073600042893309449)/359341754646249` | **`3.826997548829543624`** |
| movement | — | **`+0.000550138257`** |

It sits below `L/B* = 3.827547924507` and below the point-certificate ceiling
`L* = 38200/9977 = 3.828806254385`, and neither comparison is an independent check of
the run. `S < L/B*` is an algebraic identity, since `sqrt(1 + D^2) < 1 + D` for `D > 0`,
so a value above it would have meant an arithmetic defect.
`L*` is the ceiling on *point* certificates, and `T-025`’s own rationale is that
threshold atoms carry budget the point method cannot have, so `L*` is exactly the bound
that does not bind this language: `S < L*` holds here because `B* > 9977/10000`, which
the refinement measurement forces, not because of a theorem about threshold
certificates.

## What this does not establish

The theorem gives `s(11) >=` the supremum and **supplies no individual certificate at
that side**; it does not establish a strict inequality there.
The tool says so in its own output and the claim must not be quoted without it.

At the time of this first-party run, it left a `0.050086` gap to Trump’s `3.877084`. The
later external certificate narrows the current gap to about `0.0020836`. Nothing here
bears on global optimality, and nothing here is a new mechanism: this is the same frozen
measure on a finer net, which is why `X-041` called it a rung.
The remaining series headroom, `L/B* - 3.826998 = 0.000550`, is now half what it was.

The register entry is not written by this receipt.

## The limit record was re-derived once, and only its label moved

The record this run first wrote named its source by the bare experiment label
`exp-226-n11-threshold-191-50-net2880`. That is not a path, and
`tests/test_rung_figures.py` reads a limit record’s `source.certificate` as
repository-relative and opens it, so registering `T-033` failed on a `FileNotFoundError`
that named the label.
`T-022`’s, `T-024`’s and `T-026`’s records all name the case copy’s path there.

Re-derived with
`--source-name packing/cases/n11_threshold_certificate/certificate-191-50-net2880.json`,
31 m 51 s of wall on a contended four-core box.
**Exactly one field differs between the two records**, `source.certificate`; the surd,
the factor supremum and its squared form, the sharpened-containment identity, the six
accepted conditions and the source digest are identical, which is what says the
re-derivation reproduced the same mathematics rather than a new measurement.
The copy under `cases/` and the copy here are byte-identical again, at `sha256
e891b3b1e47cb328a8a53e16ed3b72985633ff04034343467038383dcd948fa2`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
