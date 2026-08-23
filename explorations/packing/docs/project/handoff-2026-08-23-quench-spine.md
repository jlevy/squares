# Handoff: Where the Square-Packing Loop Stands

**Date:** 2026-08-23

**Author:** Claude (agent)

**Status:** Current

This is the short, dated view: where the work stands and what to pick up.
It is written to be thrown away when it stops being true, so it states positions rather
than results — [`SYNOPSIS.md`](../../SYNOPSIS.md) is the durable technical account, and
where the two ever disagree the synopsis is right, because it is reconciled against the
artifacts in the gate and this is not.

Read this, then [`SYNOPSIS.md`](../../SYNOPSIS.md) for what the numbers actually are,
then [`conventions.md`](../../conventions.md), then the one or two things you are about
to work on.

## The one-paragraph state

The experiment loop has run **ten rounds** and produced a real result: the LP-in-cell
quench refines annealer output to the analytic optimum **to machine precision** at
`n = 5` and `n = 10`, and does essentially nothing at `n = 11`. That separates two
failures the campaign could not previously tell apart — `n = 10` was a *polish* failure,
now fixed; `n = 11` is an *exploration* failure, untouched by fixing polish.
**The bottleneck has moved from the refiner to the proposer.** Three registered
hypotheses are `blocked`, all on the same two missing tools, and building them is the
critical path.

## What exists and works

| Piece | State |
| --- | --- |
| `sqpack` exact verifier over `ℚ(α)` | works; reproduces all 33 published digits of `s(11)` |
| `sqsearch` f64 annealer (Rust) | works; selftest of 13 checks gates every run |
| `sqpack.quench` — LP-in-cell + cell fixed point + class bracketing | **built this session**; reaches the analytic optimum to `1e-15` at `n = 5, 10` |
| Soundness perimeter | every component that emits a packing is checked by `sqpack` through code it does not share |
| Campaign record | 11 rounds, 9 hypotheses, generated ledger, negative controls, effort tracking |
| Lint floor | ruff + basedpyright clean; clippy pedantic + rustfmt clean; enforced in `test.sh` |

`./explorations/packing/test.sh` runs all of it and passes.
It takes a few minutes and needs `uv` and `cargo`; both are skipped gracefully if
absent.

## What is missing, and why it is the critical path

The plan spec’s **Phase 1 (the quench spine)** has six blocks.
Two are done, four are not:

| Block | Bead | State | What it unblocks |
| --- | --- | --- | --- |
| `quench` | `think-imot` | **done** | — |
| `verify` | — | **done** (`sqpack`) | — |
| `canonicalize` | `think-t1s9` | open | **H-011, H-012** — without a canonical basin key, “basin” is undefined and basin statistics are not statistics |
| `atlas` | `think-eq6l` | open | **H-011, H-012** — the deliverable itself |
| `descriptors` | `think-hhon` | open | H-015 steering, H-003 retention |
| `meter` | `think-b4jc` | open | any comparison between proposers, in machine-independent units |

**Resolving the bead ids.** The `think-*` ids above are *local* `tbd` ids.
They are not stored in the repository and not in the synced bead data either, which keys
every issue by a ULID (`is-01...`) — so `think-eq6l` cannot be looked up from a fresh
clone. Restore the database from the [`tbd-sync`](../../../../.tbd/config.yml) branch
first (`tbd sync`), after which `tbd show think-eq6l` and `tbd list --spec <the plan>`
resolve. Until then, the durable handle for each row is the **block name in the first
column**: every one is a checklist item under *Phase 1: The quench spine* in
[the plan spec](specs/active/plan-2026-08-22-minimal-packing-toolkit.md), which needs no
tooling to read.

Three hypotheses are `blocked` in the registry — `H-001` (angle-class reduction),
`H-011` (small-`n` census), `H-012` (the rarity premise) — and all three wait on
`canonicalize` + `atlas`. Nothing else in the loop is blocked on anything.

**Recommended order: `canonicalize` → `atlas` → run H-011 → read H-012 off it.** That is
the smallest amount of building that unblocks the most, and H-012 is the premise the
whole cartography programme rests on, deliberately made cheap to kill.

## Everything is tracked, and where

- **The plan**:
  [`plan-2026-08-22-minimal-packing-toolkit.md`](specs/active/plan-2026-08-22-minimal-packing-toolkit.md),
  Phases 1–7, each with a bead epic.
  `tbd list --spec <that path>` is the work list; `tbd ready` is the unblocked subset.
  The tree is now checked by the gate — `tools/check_beads.py` refuses an open bead
  under a closed parent and two open siblings with one title, which are the two shapes
  D-025 left behind. It reads the beads out of the `tbd-sync` branch, so it needs no
  `tbd` binary.
- **The science**: `campaign/` — the runbook, the idea board, the hypothesis registry,
  one artifact per round, and a generated `ledger.md`. Never hand-edit the ledger.
- **What has gone wrong**: [`defects.md`](../../defects.md), generated from
  `defects.yaml` — every defect with what caught it and what stops it recurring.
  The counts live there and in [the synopsis](../../SYNOPSIS.md#the-defect-record),
  which is reconciled against the same source; do not retype them here.
- **Known tooling debt**:
  [the tooling-layout review](reviews/review-2026-08-23-tooling-layout.md) maps what is
  scattered or misnamed under `explorations/packing/` — including a `pytest` config that
  collects nothing and exits 0. Nothing there blocks research; it is a map, not a plan.
- **The strategy**:
  [the search-philosophy report](research/research-2026-08-23-search-philosophy-and-landscape-cartography.md)
  says where search effort should point and why; the
  [standing review](reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md)
  boils it into hypotheses with kill criteria.

## Six things that will save you a day

1. **Nothing below the `exact` tier may claim a record.** The `polished` tier has a
   measured floor of about `1e-11`; several recorded rounds sit on it with small
   *negative* gaps to the analytic value.
   That is solver noise, not a discovery ([D-021](../../defects.md), open on purpose).
2. **A screen-tier run below the standing best is a promotion trigger, not a record.**
   Treat it as a defect candidate until an independent verifier agrees, but do not
   assume it must be a bug when the standing best is unproved.
   D-042 records why `n=12` cannot serve as a known-answer negative control.
3. **The tested class-angle slice has a corner at the optimum**, not a smooth minimum —
   one-sided slopes `0.175` and `0.384`. That invalidates smooth derivative models on
   the slice. Bracketing worked here; tested Powell and Nelder–Mead runs did worse, which
   is empirical evidence rather than a general impossibility theorem.
   ([`exp-010`](../../campaign/series/series-000-smoke-and-calibration/experiments/exp-010-angle-kink-n11.md).)
4. **Tolerances must be compared to the scale of what they govern.** Two
   unrelated-looking defects — a false record claim and a non-terminating loop — were
   the same mistake, once too loose and once unreachably tight.
   See rule R2 in
   [the postmortem](postmortems/postmortem-2026-08-23-soundness-class.md).
5. **A new component joins the perimeter in the same change that introduces it**
   (`tools/perimeter_test.py`). The quench did not, which is how D-014 happened.
6. **Do not verify things in throwaway snippets.** `tools/negctl.py` runs negative
   controls from a file; `tools/regression_test.py` holds checks labelled by the defect
   each one guards. Adding to those is cheaper than rewriting a probe for the fourth time
   ([D-023](../../defects.md)).

## Open questions a fresh pair of eyes should weigh

- **Is the atlas worth building before a better proposer?** The premise (`H-012`) says
  record basins are rare, which is the argument for cartography — but it is *untested*,
  and `exp-009` already showed the proposer is the bottleneck at `n = 11`. The register
  orders premise-first deliberately, and it is cheap; but a reasonable person could
  argue for going straight at δ-continuation (`think-v2m1`) instead.
- **`class_tol` still shapes the search path**, even though a free-angle pass now
  certifies the endpoint.
  Whether two different tolerances can route the same start to two different basins is
  unmeasured, and it matters for what “basin” means in the atlas.
- **`exp-001`’s engine commit is orphaned** by a rebase; the round is annotated and the
  gate reports it every run.
  It cannot be repaired, only carried.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
