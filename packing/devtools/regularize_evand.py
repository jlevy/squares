#!/usr/bin/env python3
"""Drive Evan Daniel's vendored regularizer over known-best witnesses and classify its views.

Usage, from `packing/`, each after
`uv run --frozen --all-extras --group dev python -m devtools.regularize_evand`:

    run --run-dir DIR --n 10 26 70 [--workers K] [--timeout S] [--from-stage STAGE]
        [--frame kkt|witness] [--variant conservative|fewest] [--orient 0|best|K]
    input --n N --output FILE
    reclassify --run-dir DIR [--n N ...] [--refresh-bounds]
    layer --run-dir DIR [DIR ...] --repo-root TREE [--select admitted|preview]
        [--exclude N ...] [--grid-run DIR --grid-counts N ...]
    rungs --run-dir DIR [DIR ...] --repo-root TREE
    rename-run --from ID --to ID --note TEXT --repo-root TREE
    provenance --repo-root TREE [--check]
    report --run-dir DIR [--json]

This is the automated pass of the regularization policy
(`docs/project/policies/regularization-policy.md`, section 4). The vendored code under
`vendor/evand-regularize/` (evand/square-packing at the pin `vendored.yaml` records) is
the generator; it decides nothing. Every view it yields is converted exactly, decided
here on this project's exact routes, measured against its source witness, and classified
by the policy's decision table. Per count, in order:

1. **Input.** The witness `packing/witnesses/known-best/n-NNN.yaml` becomes upstream's text
   input (`n S`, then `x y degrees` per square, in the witness's own order and frame) at
   full precision: a rational witness's exact centres and side to 50 significant digits,
   its angles from the exact edge direction by `mpmath.atan2` at 60 digits; a decimal
   witness from its own decimal strings, an angle in radians converted at 60 digits; the
   algebraic witness (n = 51) from its field values evaluated at 60 digits. Upstream's own
   batch inputs reduced every witness to binary64; these do not.
2. **Replica.** A scratch copy, under the run directory, of only the seven vendored
   modules the pipeline runs, with a generated `search/exact/batch/results.json` (one row
   per count: `n`, `from_: witness`, the solve's `status`, the finder as `by`, the
   record's printed side as `register`) and `batch/work/n-N` linked to the count's solve
   directory, which is where `reg.load` reads its 80-digit input. A solve the retry
   ladder runs with a replica patch runs from a copy of `search/exact` with the patch
   applied, under `replica/patched/NAME/`; the replica's own copies stay the pinned
   bytes. Nothing is written under `vendor/`, and the run directory must lie outside the
   checkout.
3. **Exact solve.** `exactsolve.py witness.txt --out solve -q` with `python -I`, one
   thread, a timeout, and the count's directory as working directory. An attempt that
   gives no view climbs the retry ladder below (`solve_with_retries`). A count that still
   does not reach the regularizer (not jammed, not converged, an invalid certificate at a
   point that is not a local minimum, a timeout) is reported and stops there; it is never
   polished.
4. **Regularize.** `regularize_evand_shim.py`, beside this file, runs upstream's
   `reg.regularize` with `coincide` placement, the `conservative` angle policy and the
   source orientation, upstream's `atlas.level_of`, and `reg.write_cert`, and writes
   `regularize.json` with the result's poses at 50 digits. It starts from the solve's KKT
   point (`--frame kkt`, the default, upstream's own input) or, with `--frame witness`,
   from the witness's own exact pose at `s_W` to 80 digits beside the solve's free-square
   list, so that the regularizer keeps the witness's side and rotations. At a rational
   witness whose side has slack the KKT point lowers the side by about `10^-10` and can
   turn a tilted band by hundredths of a degree (0.0115 degrees at n = 70), which no
   exact rotation of the witness matches. Elsewhere it leaves rotations within `10^-10`
   degrees of the witness's (7.5e-11 at n = 146, 2e-11 at 206), which the same-side
   re-solve matches within a sine of `10^-9`. In the pilot of 11 October 2026 the
   witness frame did not rescue 70, 129 and 146: upstream's 80-digit verification finds
   overlaps of about `10^-10` at `s_W` and its certificate is invalid.
5. **Import.** The dilated certificate becomes `view-solved.yaml`, a rational
   centre-basis Witness/v2, through `devtools.evand_exact_certificates` (`parse`,
   `basis_witness`), decided by `sqpack.witness.exact_verify`, the independent checker and
   the half-angle route of `devtools.check_half_angle_area`. Its side is upstream's `S'`,
   so its relation to the witness is `bound` where `S'` is the verified upper bound `U`
   exactly, and `solved` otherwise.
6. **Same side.** `devtools.regularize_same_side.resolve` re-solves the view's tight
   contacts over Q at the witness's side `s_W`; when it succeeds, `view-same.yaml` is
   decided here again on the two maintained routes and its side compared with `s_W`
   exactly, so the relation `same` is computed, not taken from the resolver.
7. **Measure.** Identity by `check_half_angle_area.arrangement_gap` between the chosen
   view (the same-side view when there is one, else the solved one) and the witness's
   exact frame, with the squares it turns beyond a sine of `10^-6`; house and stage
   full-side contact counts per square, before and after, by the census's replicas
   (`census_atlas_contact_shades.edge_rule_contacts` and `centre_rule_contacts` on
   `packings_from_witness`), as histograms and per-square regressions against the witness
   and against the project's current regularized view of the count, if it has one.
8. **Classify.** `classify` applies rows 1 to 10 of the decision table to each output on
   its own; the first row that matches decides. The count's decision is the same-side
   view's where stage 6 produced one, else the solved view's. Row 1's "no output" is a
   solve that did not certify or timed out, or a regularization that raised, timed out,
   found its placement infeasible, or wrote no certificate upstream's own checker accepts.
   A placement LP that merely stalled (`place: stalled`) still yields an output and is not
   row 1, and neither is a failed 80-digit verification (`verify_ok: false`) beside a
   certificate upstream accepted: upstream's checks are evidence and never decide, so that
   certificate goes to this project's routes like any other.
   The decision is reported in the words the policy gives (owner, 11 October 2026):
   `no-view` for row 1; `no-change` wherever the view would draw the same picture, whatever
   row matched (nothing moved beyond `10^-3` or turned, the pairing one to one, the house
   counts the source's), so nothing is refused or held that would not change; `held` for a
   visible view at rows 3 and 4; `refuse` for row 2 and for row 7 where a house or stage
   total falls. The owner's answers of 12 October 2026 admit a view at the bound as a
   same-side one is admitted, and send what the rules cannot settle to review: row 7 where
   per-square counts fall but no total does. Those of 13 October 2026 retire rows 6 and 9,
   so a changed pose is named in the admission's reason and stops nothing, and draw the
   view at the bound where the witness's side is above it (`yield_to_bound`). A row 3
   candidate is listed in the receipt whatever it is reported as, for registration
   first. `reclassify` decides a finished run again from its reports, for a change to the
   table, without re-running a stage; with `--refresh-bounds` it first reads each count's
   `U` again from the case record, for a run decided before a register result moved the
   bound.

Every count writes `RUN/n-NNN/report.json`, and the run writes `RUN/receipt.json`: the
generator (name, pin, local patches, interpreter), the parameters, one row per count with
its sides, decision, own parameters and seconds per stage, the register-result candidates
of row 3, the review queue, the solve's input and outputs by digest (kept for rows an
earlier run into the same directory decided), and the run's CPU and wall seconds,
children included. A count's report is removed when its run starts and written once it is
decided, so a verdict is never read beside views a re-run was remaking. Each view's block
records the view's bytes by their Git blob id, as provenance only: nothing compares it
(OR-18). `layer` decides the file it is about to write again instead, on both maintained
exact routes, and takes it only with the side, relation and id its report decided, and
only from a report whose settings are the ones its stored regularization ran with.

**Stage reuse.** `--from-stage` reuses what the earlier stages left in the count's
directory, and their settings and source with it. Reuse is refused, naming the stage to
run from, where the witness's input today is not the stored `input.txt` (`input.json`
records the witness it was written from), or where `--from-stage import` is asked for a
variant, orientation or frame other than the stored regularization ran with.

**What the measurements are.** Upstream's level, symmetry and moves are its own report,
recorded as upstream's. The exact routes decide validity over Q and nothing else. The
identity measure is a nearest-centre matching under the box's eight symmetries; it says
how far squares moved and whether the pairing is one to one, not that two packings are
the same in any stronger sense. Per-square regressions pair squares by index, which the
generator preserves in the source orientation. The witness's frame for a decimal witness
is its 36-digit rational promotion at centre dilation 1, whose exact side is `s_W`; the
algebraic witness has no rational frame, so its identity is measured against a 55-digit
rational approximation and no view of it can be `same`. `U` is the case record's
`verified_upper_bound`, held exactly (`verified_bound`): its exact form where that is a
fraction, its printed decimal where it has no exact form, and a closed form as the one
root of its minimal polynomial in a rational interval. A view is `bound` only at a
rational `U`; row 3 compares a side with a closed form exactly; and a form the driver
cannot read (n = 11's `root(P_trump11, ...)`) decides nothing, so a view there goes to
review rather than being compared with a printed decimal.

**Credit and dates.** A view's `regularization.provenance` is the credit of the packing
it redraws (`packing_credit`): the case record's credit for its reported bound at the
bound, and at the witness's own side the witness's packing, which is the one before the
improvement the record credits where the two differ. `provenance --repo-root TREE`
restates the drawn views' credit by that rule, in each index entry and its view
together, without the run directories; `--check` writes nothing and fails where it
would. A receipt records the time it was written (`finished`), which dates the run in
the layer's index, and the directory the run spent its cost in (`run_directory`). A run
reclassified on a copy of that directory under another name is marked so in its receipt
(`reclassified.from`), and records no cost of its own in the layer
(`regularize_axis_components.costed_once`); a cost repeated unmarked is refused.

**The retry ladder** (the no-view study of 12 October 2026; rungs 3 and 5a under the
owner's overnight instruction of the same day). These are policy-visible behaviours: each
decides whether a count gets a view at all, and none of them decides a view, which is
decided on this project's exact routes as every view is. Every attempt is listed in the
report's `solve.attempts` with its rungs, arguments, replica patches, status, gate and
seconds. Each rung adds to the attempt before it, none is climbed twice, and the first
attempt that reaches the regularizer is kept under `solve/`, the first attempt moved to
`solve-first/` and the others left in `solve-retry-RUNG/`.

- *The gate* (`solve_gate`). A solve reaches the regularizer when it certifies (`KKT
  local min`, `bound only`), or, the relaxed gate of rung 3, when Newton converged and
  upstream's second-order status is a local minimum but upstream refused its own dilated
  certificate (`certificate invalid`). The regularizer writes and checks a certificate of
  its own output, so upstream's refusal of the solve's certificate decides nothing about
  the view. A point upstream finds is not a local minimum (155, with a first-order
  descent of 0.084) still stops.
- *Rung 1, `dps-100`.* A solve that failed in its first pass is solved again at 100
  digits (n = 18, where an exactly degenerate input sends Newton off at 80).
- *Rung 2, `force-kkt`.* A witness found not jammed only at noise level, its jam
  residual below `1e-6` and the MILP's descent below `1e-5`, is solved with upstream's
  `--force-kkt` (152, 269), and the result is kept only where its exact side is at most
  `10^-10` below the witness's, so the solve removed noise and polished nothing. The
  eight rational witnesses with slack the solver rightly finds not jammed (jam residual
  2.4e-7 to 1.5e-2, descent 2.2e-5 to 1.0) stay out.
- *Rung 3, `first-pass`.* A solve that failed in an active-set step, where upstream
  re-solves with the pairs that closed during the solve as equations (258: the contact
  equations became inconsistent), is solved again by `regularize_evand_first_pass.py`,
  which stops upstream's recursion, so the converged first pass's outputs are what the
  solve leaves; they reach the regularizer through the relaxed gate or not at all. A
  solve that still times out after rung 5a climbs this rung too.
- *Rung 5a, `stall-stop`.* A solve that timed out is solved again, never with a longer
  timeout, from a copy of `search/exact` with the replica patch `probe-flat-stall-stop`
  applied (`vendor/evand-regularize/vendored.yaml`, kind `replica`, and its README's Local
  Changes): upstream's zero-mode probe also stops at its stall floor, which leaves the
  KKT point and the certificate unchanged. In the run of 12 October 2026, 290 certified
  in 282 s with the outputs the study's patched solve gave, and 302's whole solve, two
  active-set steps included, certified in 819 s, where the pristine first pass alone took
  1,641 s and its active-set step did not finish in 1,800. A count solved so lists the
  patch in its report's `generator.patches` and its views' `certificate.generator.patches`,
  its `method` names it, and the receipt lists it with the counts that used it.

Rung 4 of the study, a solve of the load-bearing sub-packing where upstream's promotion
of wedged force-free squares sends Newton off (150), is not part of the ladder.

**Workers.** Counts run in a process pool of `sqpack.workers.worker_count` workers,
capped at two when `--workers` is not given; each count's solve and regularization are
further child processes with one BLAS thread.
"""

from __future__ import annotations

import argparse
import fcntl
import functools
import gzip
import hashlib
import importlib
import json
import math
import os
import platform
import resource
import shutil
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable, Collection, Iterable, Iterator, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor, as_completed
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field, replace
from decimal import ROUND_HALF_EVEN, Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Literal

import mpmath
from strif import atomic_output_file

from devtools import census_atlas_contact_shades as shades
from devtools import check_half_angle_area as area
from devtools import check_rational_witness_independent as independent
from devtools import evand_exact_certificates as evand
from devtools import regularize_axis_components as axis
from devtools.check_vendored_evand import apply_patch
from devtools.retained_data import git_blob
from devtools.upper_bound_packets import RATIONAL_DIGITS
from sqpack.witness import (
    # The 36-digit rational pose at dilation 1 is the decimal witness's exact frame, as
    # `regularize_axis_components.exact_frame` takes it; this builds it the same way.
    _promoted_candidate,  # pyright: ignore[reportPrivateUsage]
    exact_verify,
    load_witness,
    materialize_exact_witness,
    materialize_witness,
    validate_witness_document,
    witness_document,
)
from sqpack.workers import worker_count
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
VENDOR = REPO / "vendor/evand-regularize"
VENDORED_MANIFEST = VENDOR / "vendored.yaml"
UPSTREAM_INPUTS = VENDOR / "search/exact/batch/inputs"
KNOWN_BEST = ROOT / "witnesses/known-best"
WITNESS_SCHEMA = ROOT / "witnesses/witness.schema.yaml"
FRONTIER = ROOT / "frontier"
LAYER_INDEX = ROOT / "atlas/known-best/regularized/index.json"
SHIM = Path(__file__).with_name("regularize_evand_shim.py")
#: Runs upstream's solve without its active-set recursion: the ladder's `first-pass` rung.
FIRST_PASS_SHIM = Path(__file__).with_name("regularize_evand_first_pass.py")
POLICY = "docs/project/policies/regularization-policy.md"

GENERATOR = "evand-regularize"
GENERATED_BY = "python -m devtools.regularize_evand run"
RECEIPT_FORMAT = "evand-regularization-receipt-v1"
RUN_MEASURED_BY = (
    "resource.getrusage: each count's worker RUSAGE_SELF plus RUSAGE_CHILDREN (its "
    "solve and shim), summed, plus the driver's RUSAGE_SELF"
)
"""How `run` measures a run's cost, in its receipt's `cost.measured_by`."""
REPORT_FORMAT = "evand-regularization-report-v1"
#: The vendored modules the pipeline runs, by their upstream directory.
REPLICA_FILES: dict[str, tuple[str, ...]] = {
    "search/exact": ("exactsolve.py", "geom.py", "verify_cert.py", "verify_cert2.py"),
    "search/regularize": ("reg.py", "atlas.py", "samepacking.py"),
}
BATCH = Path("search/exact/batch")
#: Significant digits of a written input value and of the evaluation behind it.
INPUT_DIGITS = 50
EVALUATION_DIGITS = 60
STYLE = "coincide"
VARIANTS = ("conservative", "fewest")
#: What the regularizer starts from: the exact solve's KKT point, or the witness's own pose
#: at its side `s_W` with the solve's free squares (`regularizer_frame`).
FRAMES = ("kkt", "witness")
#: Significant digits of the witness frame handed to the regularizer, which reads at 80.
FRAME_DIGITS = 80
DEFAULT_TIMEOUT = 600.0
#: The pool's size when `--workers` is not given: the host is shared with other work.
DEFAULT_WORKER_CAP = 2
#: The stages a run can start from; the later stages always run after the first chosen.
STAGES = ("input", "solve", "regularize", "import")
#: A move over this is named in the reason a view is admitted with (`pose_changes`): a
#: measurement since the owner's answers of 13 October 2026, not a gate (policy section 3).
#: The turn is obligation 3's: a square turned by more than it, as a sine, is turned.
MOVE_BOUND = Fraction(1, 2)
TURN_BOUND = Fraction(1, 10**6)
SOLVE_CERTIFIED = ("KKT local min", "bound only")
#: The second-order statuses upstream gives a local minimum of S.
LOCAL_MINIMUM = ("rigid", "PD", "PSD", "local minimum")
SINGLE_THREAD = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS")
HOUSE, STAGE = shades.RULES[0], shades.RULES[1]
RULE_NAMES = ("house", "stage")

Placed = tuple[Fraction, Fraction, Fraction, Fraction]
Output = Literal["solved", "same"]
Corners = list[tuple[Fraction, Fraction]]


class EvandRunError(ValueError):
    """A request this driver refuses, or an input it cannot write."""


# --------------------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------------------


def sha256_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def relative(path: Path) -> str:
    """A repository-relative path for a file in the checkout, else the absolute one."""
    resolved = path.resolve()
    return str(resolved.relative_to(REPO)) if resolved.is_relative_to(REPO) else str(resolved)


def decimal_text(value: Fraction, digits: int = INPUT_DIGITS) -> str:
    """`value` to `digits` significant digits, rounded to nearest, in fixed notation."""
    with localcontext() as context:
        context.prec = digits
        context.rounding = ROUND_HALF_EVEN
        number = Decimal(value.numerator) / Decimal(value.denominator)
    return format(number, "f")


def mp_text(value: Any, digits: int = INPUT_DIGITS) -> str:
    """An mpmath value to `digits` significant digits in fixed notation."""
    return str(mpmath.nstr(value, digits, min_fixed=-mpmath.inf, max_fixed=mpmath.inf))


def literal(value: Fraction) -> str:
    return evand.literal(value)


def write_json(path: Path, document: Any) -> None:
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text(
            json.dumps(document, indent=1, default=str) + "\n", encoding="utf-8"
        )


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def count_dir(run_dir: Path, n: int) -> Path:
    return run_dir / f"n-{n:03d}"


def witness_path(n: int) -> Path:
    return KNOWN_BEST / f"n-{n:03d}.yaml"


def outside_checkout(path: Path) -> Path:
    """`path`, resolved, refused when it lies inside this repository."""
    resolved = path.resolve()
    if resolved.is_relative_to(REPO):
        raise EvandRunError(
            f"{path} is inside the checkout; the replica and the solve outputs belong in a "
            "scratch directory outside it (vendor/evand-regularize/README.md, OR-18)"
        )
    return resolved


# --------------------------------------------------------------------------------------
# The source witness: its input text, its exact frame and its side
# --------------------------------------------------------------------------------------


def _degrees(dy: Any, dx: Any) -> Any:
    with mpmath.workdps(EVALUATION_DIGITS):
        return mpmath.atan2(dy, dx) * 180 / mpmath.pi


def _exact_rows(witness: Mapping[str, Any]) -> tuple[list[tuple[str, str, str]], str]:
    """A rational witness: exact centres and side to 50 digits, angles from exact edges."""
    squares, side = materialize_exact_witness(witness)
    rows: list[tuple[str, str, str]] = []
    for corners in squares:
        xs = [Fraction(x) for x, _ in corners]
        ys = [Fraction(y) for _, y in corners]
        dx, dy = xs[1] - xs[0], ys[1] - ys[0]
        with mpmath.workdps(EVALUATION_DIGITS):
            angle = _degrees(
                mpmath.mpf(dy.numerator) / dy.denominator,
                mpmath.mpf(dx.numerator) / dx.denominator,
            )
            angle_text = mp_text(angle)
        rows.append(
            (
                decimal_text(sum(xs, Fraction(0)) / 4),
                decimal_text(sum(ys, Fraction(0)) / 4),
                angle_text,
            )
        )
    return rows, decimal_text(Fraction(side))


def _decimal_rows(witness: Mapping[str, Any]) -> tuple[list[tuple[str, str, str]], str]:
    """A decimal witness from its own strings; an angle in radians converted at 60 digits."""
    if witness["representation"] != "center-angle":
        raise EvandRunError("a decimal witness must be centre-angle")
    if witness["coordinates"]["origin"] != "lower-left":
        raise EvandRunError("a decimal witness must have a lower-left origin")
    unit = witness["coordinates"]["angle_unit"]
    rows: list[tuple[str, str, str]] = []
    for square in witness["squares"]:
        x, y = (str(value) for value in square["center"])
        angle = str(square["angle"])
        if unit == "radians":
            with mpmath.workdps(EVALUATION_DIGITS):
                angle = mp_text(mpmath.mpf(angle) * 180 / mpmath.pi)
        elif unit != "degrees":
            raise EvandRunError(f"angle unit {unit!r} is not degrees or radians")
        rows.append((x, y, angle))
    return rows, str(witness["side"])


def _field_rows(witness: Mapping[str, Any]) -> tuple[list[tuple[str, str, str]], str]:
    """An algebraic witness: its field values evaluated at 60 digits."""
    squares, side = materialize_witness(witness, digits=EVALUATION_DIGITS)
    rows: list[tuple[str, str, str]] = []
    with mpmath.workdps(EVALUATION_DIGITS):
        for corners in squares:
            xs = [mpmath.mpf(x) for x, _ in corners]
            ys = [mpmath.mpf(y) for _, y in corners]
            angle = _degrees(ys[1] - ys[0], xs[1] - xs[0])
            rows.append((mp_text(sum(xs) / 4), mp_text(sum(ys) / 4), mp_text(angle)))
        side_text = mp_text(mpmath.mpf(side))
    return rows, side_text


def input_text(witness: Mapping[str, Any]) -> str:
    """Upstream's text input for a witness: `n S`, then `x y degrees` per square."""
    kind = witness["scalar"]["kind"]
    if kind == "rational":
        rows, side = _exact_rows(witness)
    elif kind == "decimal":
        rows, side = _decimal_rows(witness)
    elif kind == "algebraic-number-field":
        rows, side = _field_rows(witness)
    else:
        raise EvandRunError(f"scalar kind {kind!r} has no input form here")
    lines = [f"{witness['n']} {side}", *(f"{x} {y} {angle}" for x, y, angle in rows)]
    return "\n".join(lines) + "\n"


def read_input(text: str) -> tuple[int, str, list[tuple[str, str, str]]]:
    """Upstream's text format read back: the count, the side and each square's row."""
    rows = [line.split() for line in text.splitlines() if line.strip()]
    n, side = int(rows[0][0]), rows[0][1]
    squares = [(row[0], row[1], row[2]) for row in rows[1 : n + 1]]
    return n, side, squares


#: Beside `input.txt`: the witness it was written from, by path and digest, as recorded.
INPUT_RECORD = "input.json"


def reused_input(
    directory: Path, witness: Mapping[str, Any], reused_frame: SourceFrame | None = None
) -> None:
    """Refuse to reuse a stage whose input is not what the witness gives today.

    `--from-stage solve`, `regularize` and `import` reuse outputs made from `input.txt`.
    Where the witness has changed since (#518 re-housed 42 counts), they describe another
    input, and the report would name a witness the generator never read (review B of
    #511, B2). The stored input is compared with the witness's input as text, so a change
    that leaves the input as it was (a note, a credit) reuses the stage. Where the stored
    regularization is reused (`reused_frame`, the witness's frame today) and started from
    the witness's own pose, that pose is compared with today's too.
    """
    stored = directory / "input.txt"
    if not stored.is_file():
        raise EvandRunError(
            f"{stored} is missing: run this count again from --from-stage input"
        )
    if stored.read_text(encoding="utf-8") != input_text(witness):
        raise EvandRunError(
            "the witness has changed since this count's input was written, so its later "
            "stages describe another input: run this count again from --from-stage input"
        )
    regularized = directory / "regularize.json"
    if reused_frame is None or not regularized.is_file():
        return
    if read_json(regularized).get("frame") != "witness":
        return
    framed = directory / "frame-witness/witness.exact.txt"
    if not framed.is_file() or framed.read_text(encoding="utf-8") != frame_text(
        witness, reused_frame
    ):
        raise EvandRunError(
            "the witness's pose the regularizer started from is not the witness's today: "
            "run this count again from --from-stage regularize"
        )


def input_record(directory: Path) -> dict[str, Any]:
    """The exact solve's input by digest, and the witness it was written from as recorded
    when it was written (obligation 6: inputs by digest)."""
    stored = directory / "input.txt"
    written = directory / INPUT_RECORD
    return {
        "path": stored.name,
        "sha256": sha256_of(stored.read_bytes()),
        "written_from": read_json(written).get("witness") if written.is_file() else None,
    }


def _placed(corners: Sequence[tuple[Any, Any]]) -> Placed:
    """Centre and `(cos, sin)` of a square from its corners, the first edge's direction."""
    xs = [Fraction(x) for x, _ in corners]
    ys = [Fraction(y) for _, y in corners]
    return sum(xs, Fraction(0)) / 4, sum(ys, Fraction(0)) / 4, xs[1] - xs[0], ys[1] - ys[0]


@dataclass(frozen=True)
class SourceFrame:
    """The source witness's exact frame, its side `s_W` and how both were obtained."""

    kind: str
    side: Fraction | None
    side_text: str
    corners: list[Corners] | None
    placements: list[Placed]
    derivation: str


def source_frame(witness: Mapping[str, Any]) -> SourceFrame:
    kind = witness["scalar"]["kind"]
    if kind == "rational":
        squares, side = materialize_exact_witness(witness)
        corners = [[(Fraction(x), Fraction(y)) for x, y in square] for square in squares]
        exact = Fraction(side)
        return SourceFrame(
            kind,
            exact,
            decimal_text(exact, 40),
            corners,
            [_placed(square) for square in corners],
            "the witness's own exact geometry",
        )
    if kind == "decimal":
        squares, exact = _promoted_candidate(
            witness, rational_digits=RATIONAL_DIGITS, dilation=Fraction(1)
        )
        corners = [[(Fraction(x), Fraction(y)) for x, y in square] for square in squares]
        return SourceFrame(
            kind,
            exact,
            decimal_text(exact, 40),
            corners,
            [_placed(square) for square in corners],
            f"the {RATIONAL_DIGITS}-digit rational promotion at centre dilation 1",
        )
    squares, side = materialize_witness(witness, digits=EVALUATION_DIGITS)
    approximate = [
        [(Fraction(mp_text(x, 55)), Fraction(mp_text(y, 55))) for x, y in square]
        for square in squares
    ]
    return SourceFrame(
        kind,
        None,
        mp_text(side, 40),
        None,
        [_placed(square) for square in approximate],
        "a 55-digit rational approximation of the field values, for measurement only",
    )


def case_facts(n: int) -> dict[str, Any]:
    """The case record's verified upper bound, printed side and finders, read only."""
    path = FRONTIER / f"n-{n:03d}.md"
    if not path.is_file():
        return {
            "verified_upper_bound": None,
            "exact_form": None,
            "reported": None,
            "found_by": [],
            "improved_by": [],
            "source_key": None,
        }
    front = load_yaml(path.read_text(encoding="utf-8").split("---\n", 2)[1])["packing"]
    verified = front.get("verified_upper_bound") or {}
    reported = front.get("reported_upper_bound") or {}
    return {
        "verified_upper_bound": verified.get("value"),
        "exact_form": verified.get("exact_form"),
        "reported": reported.get("value"),
        "found_by": list(reported.get("found_by") or []),
        "improved_by": list(reported.get("improved_by") or []),
        "source_key": reported.get("source_key"),
    }


@dataclass(frozen=True)
class VerifiedBound:
    """The case record's verified upper bound `U`, held exactly.

    `rational` is `U` where it is a rational number: its exact form a fraction, or no
    exact form beside the printed decimal, which is then the bound. A closed form is an
    algebraic number, held as the one root of its minimal polynomial (`polynomial`,
    integer coefficients, highest degree first) in the rational interval `interval`; a
    rational side is compared with it exactly and is never equal to it. A form this
    driver cannot read is `unread`, with the reason, and nothing is decided against it:
    a printed decimal or a 60-digit evaluation stands above or below `U` by its rounding,
    and would decide `bound` and row 3 by that rounding (review B of #511, B3).
    """

    form: str | None
    rational: Fraction | None = None
    polynomial: tuple[int, ...] = ()
    interval: tuple[Fraction, Fraction] | None = None
    unread: str | None = None

    def compare(self, side: Fraction) -> int | None:
        """-1, 0 or 1 as `side` is below, at or above `U`, decided exactly; None unread."""
        if self.rational is not None:
            return (side > self.rational) - (side < self.rational)
        if self.interval is None:
            return None
        low, high = self.interval
        if side <= low:
            return -1
        if side >= high:
            return 1
        # `U` is the polynomial's only root in (low, high), and a rational side is no
        # root of an irreducible polynomial of degree two or more: the polynomial keeps
        # its sign at `low` up to `U` and changes it there.
        same_sign = (_evaluate(self.polynomial, side) > 0) == (
            _evaluate(self.polynomial, low) > 0
        )
        return -1 if same_sign else 1

    def difference(self, side: Fraction) -> float:
        """`side - U` in binary64, for reports only; it decides nothing."""
        if self.rational is not None:
            return float(side - self.rational)
        if self.interval is None:
            return math.nan
        low, high = self.interval
        return float(side - (low + high) / 2)

    def record(self) -> dict[str, Any]:
        """How `U` was read, for the report."""
        if self.rational is not None:
            return {"kind": "rational", "value": literal(self.rational)}
        if self.interval is not None:
            return {
                "kind": "algebraic",
                "minimal_polynomial": list(self.polynomial),
                "interval": [literal(end) for end in self.interval],
            }
        return {"kind": "unread", "form": self.form, "reason": self.unread}


#: How narrow a closed form's isolating interval is made, so that a report's `minus_U`
#: is accurate far below any side a generator writes; the comparison never needs it.
BOUND_INTERVAL_WIDTH = Fraction(1, 10**60)


def _evaluate(coefficients: Sequence[int], value: Fraction) -> Fraction:
    total = Fraction(0)
    for coefficient in coefficients:
        total = total * value + coefficient
    return total


@functools.cache
def _closed_form_bound(form: str) -> VerifiedBound:
    """A closed form as the root of its minimal polynomial, isolated exactly."""
    import sympy as sp  # noqa: PLC0415 -- the optional dependency, where it is used
    from sympy.parsing.sympy_parser import (  # noqa: PLC0415
        implicit_multiplication_application,
        parse_expr,
        standard_transformations,
    )

    transformations = (*standard_transformations, implicit_multiplication_application)
    try:
        value = parse_expr(form, transformations=transformations)
    except (SyntaxError, TypeError, ValueError, sp.SympifyError) as error:
        return VerifiedBound(form, unread=f"the form does not parse: {error}")
    if value.free_symbols or value.atoms(sp.Float):
        return VerifiedBound(
            form,
            unread="the form names a symbol or a decimal, not an exact number this driver "
            "reads; its printed decimal is not used in its place",
        )
    x = sp.Symbol("x")
    polynomial = sp.minimal_polynomial(value, x, polys=True)
    coefficients = tuple(int(c) for c in polynomial.all_coeffs())
    if polynomial.degree() == 1:
        return VerifiedBound(form, rational=Fraction(-coefficients[1], coefficients[0]))
    approximate = sp.N(value, 80)
    width = sp.Rational(BOUND_INTERVAL_WIDTH.numerator, BOUND_INTERVAL_WIDTH.denominator)
    # Real root isolation over Q: each interval holds exactly one root; the 80-digit value
    # only picks which. It lies within `reach` of the root, and SymPy may refine an interval
    # far below `width`, past that error (to 1.6e-82 for sqrt(16 + 10^-40)), so a root is
    # matched within that reach rather than strictly inside.
    reach = sp.Rational(1, 10**70)
    isolated: Any = polynomial.intervals(eps=width)
    found = [
        (Fraction(str(low)), Fraction(str(high)))
        for (low, high), _multiplicity in isolated
        if low - reach <= approximate <= high + reach
    ]
    if len(found) != 1:
        return VerifiedBound(form, unread="no single root of its minimal polynomial is it")
    return VerifiedBound(form, polynomial=coefficients, interval=found[0])


def verified_bound(facts: Mapping[str, Any]) -> VerifiedBound | None:
    """The record's verified upper bound held exactly (`VerifiedBound`), None without one."""
    value, form = facts["verified_upper_bound"], facts["exact_form"]
    if value is None:
        return None
    if form is None:
        return VerifiedBound(None, rational=Fraction(str(value)))
    try:
        return VerifiedBound(str(form), rational=Fraction(str(form).replace(" ", "")))
    except ValueError:
        return _closed_form_bound(str(form))


def upper_bound(facts: Mapping[str, Any]) -> Fraction | None:
    """`U` where it is a rational number exactly, else None.

    Its exact form where that is a fraction, or its printed decimal where the record has
    no exact form, which is then the bound. A closed form is not rational, so no side
    equals it and no frame is built at it; `verified_bound` holds it exactly, for
    comparison. A 60-digit evaluation of it (`apply_exact_ceilings.bound_value`) lies
    above or below it by its rounding, so it is never read as `U` here. Neither is the
    printed decimal of a form: at n = 51 it is the exact side rounded up at sixteen
    digits, below which every dilated certificate of the optimum falls.
    """
    bound = verified_bound(facts)
    return None if bound is None else bound.rational


# --------------------------------------------------------------------------------------
# The replica
# --------------------------------------------------------------------------------------


def vendored_pin() -> dict[str, Any]:
    """The generator: its pin, and the local changes every solve and regularization run.

    A replica patch is not among them: it runs only where the retry ladder applies it,
    and is added to a count's patches there (`applied_patches`) and to the receipt's with
    the counts that used it (`run_generator`).
    """
    manifest = load_yaml(VENDORED_MANIFEST.read_text(encoding="utf-8"))
    commit = str(manifest["source_commit"])
    return {
        "name": GENERATOR,
        "source_url": manifest["source_url"],
        "pin": commit[:7],
        "source_commit": commit,
        "patches": [
            dict(change)
            for change in manifest["local_changes"]
            if change.get("kind") != "replica"
        ],
        "interpreter": f"{platform.python_implementation()} {platform.python_version()}",
    }


def replica_patches() -> dict[str, dict[str, Any]]:
    """The manifest's replica patches by name, the stem of the patch file."""
    manifest = load_yaml(VENDORED_MANIFEST.read_text(encoding="utf-8"))
    found: dict[str, dict[str, Any]] = {}
    for change in manifest["local_changes"]:
        if change.get("kind") == "replica":
            name = Path(str(change["patch"])).stem
            found[name] = {"name": name, **change}
    return found


def applied_patches(names: Iterable[str]) -> list[dict[str, Any]]:
    """The manifest's records of the replica patches a solve ran with."""
    recorded = replica_patches()
    return [recorded.get(name, {"name": name}) for name in names]


def patch_name(patch: Mapping[str, Any]) -> str:
    """How a `method` names a patch: a replica patch by its name, a local change by path."""
    return str(patch.get("name") or patch.get("path"))


def build_replica(run_dir: Path, rows: Sequence[Mapping[str, Any]]) -> Path:
    """Copy the pipeline's vendored modules under `run_dir` and write their batch inputs.

    `rows` are the batch rows for the counts of this run; rows already in the replica for
    other counts are kept. Each count's `batch/work/n-N` links to its solve directory.
    """
    replica = outside_checkout(run_dir) / "replica"
    for directory, names in REPLICA_FILES.items():
        target = replica / directory
        target.mkdir(parents=True, exist_ok=True)
        for name in names:
            shutil.copyfile(VENDOR / directory / name, target / name)
    batch = replica / BATCH
    (batch / "work").mkdir(parents=True, exist_ok=True)
    results = batch / "results.json"
    kept = {int(row["n"]): row for row in read_json(results)} if results.is_file() else {}
    for row in rows:
        kept[int(row["n"])] = dict(row)
        solve = count_dir(run_dir.resolve(), int(row["n"])) / "solve"
        solve.mkdir(parents=True, exist_ok=True)
        point_work(replica, int(row["n"]), solve)
    write_json(results, [kept[n] for n in sorted(kept)])
    return replica


def solver_tree(replica: Path, patches: Sequence[str]) -> Path:
    """The `search/exact` a solve runs from: the replica's own, or a patched copy.

    With replica patches, a copy of the replica's `search/exact` modules with each patch
    applied (`check_vendored_evand.apply_patch`, exact context, refused rather than fuzzed)
    under `replica/patched/NAME-KEY/`, built once: in a staging directory renamed into
    place, so the pool's workers never run a half-written copy. `KEY` names what the copy
    is built from, the pinned modules' bytes and each patch's, so a re-pin or an edited
    patch builds a new copy rather than running the old one under the new name (review B
    of #511, B7). It is a cache key: nothing compares it.
    """
    exact = Path("search/exact")
    if not patches:
        return replica / exact
    recorded = replica_patches()
    diffs: dict[str, str] = {}
    for name in patches:
        record = recorded.get(name)
        if record is None:
            raise EvandRunError(f"replica patch {name!r} is not recorded in vendored.yaml")
        if Path(str(record["path"])).parent != exact:
            raise EvandRunError(f"replica patch {name!r} patches outside {exact}")
        diffs[name] = (REPO / str(record["patch"])).read_text(encoding="utf-8")
    key = hashlib.sha256()
    for name in REPLICA_FILES[str(exact)]:
        key.update((VENDOR / exact / name).read_bytes())
    for diff in diffs.values():
        key.update(diff.encode("utf-8"))
    target = replica / "patched" / f"{'+'.join(patches)}-{key.hexdigest()[:12]}"
    if (target / exact).is_dir():
        return target / exact
    (replica / "patched").mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".staging-", dir=replica / "patched"))
    try:
        (staging / exact).mkdir(parents=True)
        for name in REPLICA_FILES[str(exact)]:
            shutil.copyfile(VENDOR / exact / name, staging / exact / name)
        for name, diff in diffs.items():
            patched = staging / str(recorded[name]["path"])
            write_text(patched, apply_patch(patched.read_text(encoding="utf-8"), diff))
        try:
            staging.rename(target)
        except OSError:
            if not (target / exact).is_dir():  # not another worker's copy: a real failure
                raise
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    return target / exact


def point_work(replica: Path, n: int, target: Path) -> None:
    """Link the replica's `batch/work/n-N`, where `reg.load` reads, to `target`."""
    link = replica / BATCH / "work" / f"n-{n}"
    if link.is_symlink() or link.exists():
        link.unlink()
    link.symlink_to(target.resolve(), target_is_directory=True)


def record_solve_status(replica: Path, n: int, status: str) -> None:
    """Set one count's batch status, under a lock: the pool's workers share the file."""
    results = replica / BATCH / "results.json"
    with (replica / BATCH / "results.lock").open("a", encoding="utf-8") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        rows = read_json(results)
        for row in rows:
            if int(row["n"]) == n:
                row["status"] = status
        write_json(results, rows)


def batch_row(n: int, facts: Mapping[str, Any], witness: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "n": n,
        "from_": "witness",
        "status": "pending",
        "by": facts["found_by"],
        "register": facts["reported"] or str(witness["side"]),
        "input": "devtools.regularize_evand input (full precision)",
    }


def child_environment() -> dict[str, str]:
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("PYTHON")
    }
    environment.update(dict.fromkeys(SINGLE_THREAD, "1"))
    environment["REG_REFRESH"] = "0"
    return environment


# --------------------------------------------------------------------------------------
# Stages 3 and 4: the exact solve and the regularization, as child processes
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Options:
    run_dir: Path
    timeout: float = DEFAULT_TIMEOUT
    regularize_timeout: float = DEFAULT_TIMEOUT
    variant: str = "conservative"
    orient: str = "0"
    from_stage: str = "input"
    same_mode: str = "relax"
    frame: str = "kkt"


def local_minimum(second: object) -> bool:
    """Whether upstream's second-order status is a local minimum of S."""
    return str(second or "").startswith(LOCAL_MINIMUM)


def solve_status(meta: Mapping[str, Any]) -> str:
    """The batch's status vocabulary from one `witness.json`."""
    if meta.get("status") in {"not jammed", "solve failed"}:
        return str(meta["status"])
    if not meta.get("newton_converged"):
        return "not converged"
    if not meta.get("cert_valid"):
        return "certificate invalid"
    if local_minimum((meta.get("second_order") or {}).get("status")):
        return "KKT local min"
    return "bound only"


def solve_gate(block: Mapping[str, Any]) -> Literal["certified", "relaxed"] | None:
    """How a solve reaches the regularizer, or None when it does not (module docstring).

    `certified`: upstream certified it. `relaxed`, rung 3: Newton converged to a point
    upstream's second-order analysis finds a local minimum, and only upstream's own dilated
    certificate of that point was refused.
    """
    status = block.get("status")
    if status in SOLVE_CERTIFIED:
        return "certified"
    if (
        status == "certificate invalid"
        and block.get("newton_converged")
        and local_minimum(block.get("second_order"))
    ):
        return "relaxed"
    return None


def run_child(
    command: Sequence[str], cwd: Path, timeout: float, log: Path
) -> tuple[int | None, float]:
    """Run one child with `python -I`'s isolation; the return code is None on a timeout."""
    started = time.perf_counter()
    with log.open("w", encoding="utf-8") as handle:
        try:
            completed = subprocess.run(
                command,
                cwd=cwd,
                env=child_environment(),
                stdout=handle,
                stderr=subprocess.STDOUT,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return None, time.perf_counter() - started
    return completed.returncode, time.perf_counter() - started


@dataclass(frozen=True)
class Rung:
    """One rung of the retry ladder: what it adds to the attempt it follows."""

    name: str
    arguments: tuple[str, ...] = ()
    #: Replica patches (`vendored.yaml`, kind `replica`) the solve runs with, by name.
    patches: tuple[str, ...] = ()
    #: Whether upstream's active-set recursion is stopped after the first pass.
    first_pass: bool = False


@dataclass(frozen=True)
class Attempt:
    """A solve's configuration: the rungs climbed to it, each adding to the one before."""

    rungs: tuple[Rung, ...] = ()

    @property
    def arguments(self) -> list[str]:
        return [argument for rung in self.rungs for argument in rung.arguments]

    @property
    def patches(self) -> list[str]:
        return list(dict.fromkeys(name for rung in self.rungs for name in rung.patches))

    @property
    def first_pass(self) -> bool:
        return any(rung.first_pass for rung in self.rungs)

    def climb(self, rung: Rung) -> Attempt:
        return Attempt((*self.rungs, rung))

    def record(self) -> dict[str, Any]:
        return {
            "rungs": [rung.name for rung in self.rungs],
            "arguments": self.arguments,
            "patches": self.patches,
            "first_pass": self.first_pass,
        }


#: The rungs of the retry ladder (module docstring). Thresholds are the study's.
RETRY_DIGITS = Rung("dps-100", ("--dps", "100"))
FORCE_KKT = Rung("force-kkt", ("--force-kkt",))
FIRST_PASS = Rung("first-pass", first_pass=True)
STALL_STOP = Rung("stall-stop", patches=("probe-flat-stall-stop",))
PLAIN = Attempt()
NOISE_JAM_RESIDUAL = 1e-6
NOISE_DESCENT = 1e-5
POLISH_ALLOWANCE = Fraction(1, 10**10)
#: Where an attempt's configuration is written beside its outputs, for `--from-stage`.
ATTEMPT_FILE = "attempt.json"


def solve(
    directory: Path,
    replica: Path,
    timeout: float,
    attempt: Attempt = PLAIN,
    name: str = "solve",
) -> dict[str, Any]:
    """One attempt at the exact solve, its outputs under `directory / name`."""
    solve_dir = directory / name
    solve_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(directory / "input.txt", solve_dir / "witness.txt")
    for stale in solve_dir.glob("witness.*"):
        if stale.name != "witness.txt":
            stale.unlink()
    write_json(solve_dir / ATTEMPT_FILE, attempt.record())
    exact = solver_tree(replica, attempt.patches)
    program = (
        [str(FIRST_PASS_SHIM), "--exact", str(exact)]
        if attempt.first_pass
        else [str(exact / "exactsolve.py")]
    )
    code, seconds = run_child(
        [
            sys.executable,
            "-I",
            *program,
            str(solve_dir / "witness.txt"),
            "--out",
            str(solve_dir),
            "-q",
            *attempt.arguments,
        ],
        directory,
        timeout,
        directory / f"{name}.log",
    )
    if code is None:
        return {
            "status": "timeout",
            "gate": None,
            "seconds": round(seconds, 2),
            "timeout": timeout,
            **attempt.record(),
        }
    meta_path = solve_dir / "witness.json"
    if not meta_path.is_file():
        return {
            "status": "error",
            "gate": None,
            "returncode": code,
            "seconds": round(seconds, 2),
            **attempt.record(),
        }
    block = solve_block(read_json(meta_path))
    block.update(returncode=code, seconds=round(seconds, 2), **attempt.record())
    return block


def attempt_of(solve_dir: Path) -> dict[str, Any]:
    """The configuration a kept solve ran with, as `solve` wrote it beside its outputs."""
    path = solve_dir / ATTEMPT_FILE
    return read_json(path) if path.is_file() else PLAIN.record()


def solve_block(meta: Mapping[str, Any]) -> dict[str, Any]:
    block = {
        "status": solve_status(meta),
        "S_exact": meta.get("S_exact"),
        "S_cert": meta.get("S_cert"),
        "cert_valid": meta.get("cert_valid"),
        "newton_converged": meta.get("newton_converged"),
        "free": meta.get("free_squares") or [],
        "second_order": (meta.get("second_order") or {}).get("status"),
        "why": meta.get("why"),
        "jam_residual": meta.get("jam_residual"),
        "vv_milp_dS": meta.get("vv_milp_dS"),
        # An active-set step's pairs, present where the last pass upstream ran was one.
        "forced_pairs": meta.get("forced_pairs"),
        "promoted": meta.get("promoted"),
        "solver_seconds": meta.get("seconds"),
    }
    block["gate"] = solve_gate(block)
    return block


def noise_level(block: Mapping[str, Any]) -> bool:
    """Whether a solve found not jammed was so only at noise level (rung 2)."""
    residual, descent = block.get("jam_residual"), block.get("vv_milp_dS")
    return (
        residual is not None
        and descent is not None
        and float(residual) < NOISE_JAM_RESIDUAL
        and abs(float(descent)) < NOISE_DESCENT
    )


def retry_rung(latest: Mapping[str, Any], climbed: Sequence[Rung] = ()) -> Rung | None:
    """The ladder's next rung after an attempt that gives no view, or None where it ends."""
    status = latest.get("status")
    candidates: tuple[Rung, ...] = ()
    if status == "timeout":
        candidates = (STALL_STOP, FIRST_PASS)
    elif status == "solve failed" and latest.get("forced_pairs"):
        candidates = (FIRST_PASS, RETRY_DIGITS)
    elif status == "solve failed":
        candidates = (RETRY_DIGITS,)
    elif status == "not jammed" and noise_level(latest):
        candidates = (FORCE_KKT,)
    return next((rung for rung in candidates if rung not in climbed), None)


def polished(block: Mapping[str, Any], printed: Fraction | None) -> bool:
    """Whether a forced solve moved the side more than noise below the witness's."""
    if printed is None or not block.get("S_exact"):
        return True
    return Fraction(str(block["S_exact"])) < printed - POLISH_ALLOWANCE


def _attempt_row(rung: Rung | None, block: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "rung": rung.name if rung is not None else None,
        "rungs": block.get("rungs") or [],
        "arguments": block.get("arguments") or [],
        "patches": block.get("patches") or [],
        "first_pass": bool(block.get("first_pass")),
        "status": block["status"],
        "gate": block.get("gate"),
        "seconds": block.get("seconds"),
    }


def solve_with_retries(
    directory: Path, replica: Path, timeout: float, printed: Fraction | None
) -> dict[str, Any]:
    """The solve, and the retry ladder's climb while an attempt gives no view.

    Every attempt is listed in `attempts`. The first to reach the regularizer
    (`solve_gate`) is kept: a retry's outputs replace the first attempt's under `solve/`,
    the first kept as `solve-first/`. A retry that does not is left in its own
    `solve-retry-RUNG/` and the climb goes on from it. A forced solve that lowered the side
    by more than noise ends the climb, as does a status no rung is left for; the first
    attempt's result then stands.
    """
    attempt = PLAIN
    first = solve(directory, replica, timeout, attempt)
    attempts = [_attempt_row(None, first)]
    latest = first
    while latest.get("gate") is None:
        rung = retry_rung(latest, attempt.rungs)
        if rung is None:
            break
        attempt = attempt.climb(rung)
        name = f"solve-retry-{rung.name}"
        latest = solve(directory, replica, timeout, attempt, name=name)
        polish = (
            FORCE_KKT in attempt.rungs
            and latest.get("gate") is not None
            and polished(latest, printed)
        )
        row = _attempt_row(rung, latest)
        row["accepted"] = latest.get("gate") is not None and not polish
        if polish:
            row["polished"] = True
        attempts.append(row)
        if row["accepted"]:
            shutil.rmtree(directory / "solve-first", ignore_errors=True)
            (directory / "solve").rename(directory / "solve-first")
            (directory / name).rename(directory / "solve")
            return {**latest, "attempts": attempts}
        if polish:
            break
    return {**first, "attempts": attempts}


def frame_text(witness: Mapping[str, Any], frame: SourceFrame) -> str:
    """The witness's own pose in `reg.load`'s format, at `s_W`, to 80 digits.

    The policy's frame: a rational witness's exact geometry or a decimal witness's 36-digit
    promotion, centres and side to 80 significant digits and each angle from its exact
    rotation at 90. The algebraic witness has no rational frame and is written as its
    input is, its field values at 60 digits.
    """
    if frame.side is None:
        return input_text(witness)
    lines = [f"{witness['n']} {decimal_text(frame.side, FRAME_DIGITS)}"]
    with mpmath.workdps(FRAME_DIGITS + 10):
        for x, y, c, s in frame.placements:
            angle = mpmath.atan2(
                mpmath.mpf(s.numerator) / s.denominator, mpmath.mpf(c.numerator) / c.denominator
            )
            degrees = mp_text(angle * 180 / mpmath.pi, FRAME_DIGITS)
            lines.append(
                f"{decimal_text(x, FRAME_DIGITS)} {decimal_text(y, FRAME_DIGITS)} {degrees}"
            )
    return "\n".join(lines) + "\n"


def regularizer_frame(
    directory: Path, witness: Mapping[str, Any], frame: SourceFrame, kind: str
) -> Path:
    """The directory the regularizer reads its 80-digit input from.

    `kkt` is the solve's own output. `witness` is a sibling directory holding the
    witness's pose at `s_W` as `witness.exact.txt` beside the solve's `witness.json`, whose
    status and free squares `reg.load` still reads; the solve's outputs are left as they
    were, since the receipt names them by digest.
    """
    solve_dir = directory / "solve"
    if kind == "kkt":
        return solve_dir
    if kind != "witness":
        raise EvandRunError(f"frame {kind!r} is not one of {FRAMES}")
    target = directory / "frame-witness"
    target.mkdir(parents=True, exist_ok=True)
    write_text(target / "witness.exact.txt", frame_text(witness, frame))
    shutil.copyfile(solve_dir / "witness.json", target / "witness.json")
    return target


def regularize(directory: Path, replica: Path, n: int, options: Options) -> dict[str, Any]:
    output, certificate = directory / "regularize.json", directory / "regularize.cert"
    for stale in (output, certificate):
        stale.unlink(missing_ok=True)
    code, seconds = run_child(
        [
            sys.executable,
            "-I",
            str(SHIM),
            "--replica",
            str(replica),
            "--n",
            str(n),
            "--output",
            str(output),
            "--certificate",
            str(certificate),
            "--variant",
            options.variant,
            "--style",
            STYLE,
            "--orient",
            options.orient,
        ],
        directory,
        options.regularize_timeout,
        directory / "regularize.log",
    )
    if code is None:
        return {"status": "timeout", "seconds": round(seconds, 2)}
    if not output.is_file():
        return {"status": "error", "error": f"no output, exit status {code}"}
    document = read_json(output)
    document["wall_seconds"] = round(seconds, 2)
    document["frame"] = options.frame
    write_json(output, document)
    return document


def regularize_block(document: Mapping[str, Any]) -> dict[str, Any]:
    verify = document.get("verify") or {}
    return {
        "level": document.get("level"),
        "level_text": document.get("level_text"),
        "moved": document.get("moved"),
        "max_move": document.get("max_move"),
        "symmetry": document.get("symmetry"),
        "symmetry_dropped": document.get("symmetry_dropped"),
        "groups_before": document.get("groups_before"),
        "groups_after": document.get("groups_after"),
        "merged": document.get("merged"),
        "angle_changes": document.get("angle_changes"),
        "changed_angles": [row["square"] for row in document.get("changed_angles") or []],
        "place": document.get("place"),
        "refine": document.get("refine"),
        "verify_ok": verify.get("ok"),
        "min_gap": verify.get("min_gap"),
        "cert_ok": document.get("cert_ok"),
        "S_exact": document.get("S_exact"),
        "S_cert": document.get("S_cert"),
        "g": document.get("g"),
        "seconds": document.get("seconds"),
    }


def regularize_failure(document: Mapping[str, Any]) -> str | None:
    """Why a regularization yields no output (row 1), or None when it yields one."""
    if document.get("status") == "timeout":
        return "regularize timeout"
    if document.get("error"):
        return f"regularize error: {document['error']}"
    if document.get("place") == "infeasible":
        return "regularize: infeasible placement"
    if not document.get("cert_ok"):
        return "regularize: upstream's checker refused the certificate"
    return None


def stored_settings(regularized: Mapping[str, Any], options: Options) -> Options:
    """The settings a reused regularization ran with, refused where they are not asked for.

    `--from-stage import` reuses `regularize.json`, which records the variant, style and
    orientation the shim ran and the frame it started from. A stored output is decided
    and labelled by those, never by the command line's, which may differ: a `fewest`
    regularization re-imported under the default would otherwise be admitted at row 10
    as `conservative` (review B of #511, B1). An output written before the frame was
    recorded started from the KKT point, the only frame there was.
    """
    asked = {"variant": options.variant, "orient": options.orient, "frame": options.frame}
    differ = settings_differ(regularized, asked, "asked")
    if differ:
        raise EvandRunError(
            f"the stored regularization ran with {', '.join(differ)}: run this count again "
            "from --from-stage regularize, or ask for the settings it ran with"
        )
    stored = _stored(regularized)
    return replace(options, **{name: str(value) for name, value in stored.items() if value})


def _stored(regularized: Mapping[str, Any]) -> dict[str, Any]:
    """The variant, orientation and frame a regularization ran with, as it recorded them;
    one written before the frame was recorded started from the KKT point."""
    return {
        "variant": regularized.get("variant"),
        "orient": regularized.get("orient"),
        "frame": regularized.get("frame", "kkt"),
    }


def settings_differ(
    regularized: Mapping[str, Any], stated: Mapping[str, str], word: str
) -> list[str]:
    """Each setting a stored regularization ran with that is not the one `stated`, in the
    command line's terms, with the stated value after `word`; and a style not this
    driver's."""
    differ = [
        f"--{name} {value} ({word}: {stated[name]})"
        for name, value in _stored(regularized).items()
        if value is not None and str(value) != stated[name]
    ]
    style = regularized.get("style")
    if style is not None and style != STYLE:
        differ.append(f"style {style} (this driver runs {STYLE})")
    return differ


def settings_disagreement(directory: Path, report: Mapping[str, Any]) -> str | None:
    """Why a count's report is not labelled with the settings its stored regularization
    ran with, or None; None too where there is no stored regularization to hold it to.

    A report written before review B's B1 fix of #511 could call a `fewest` regularization
    `conservative`, and a decision read from its labels is then the wrong variant's row.
    `reclassify` and `layer` hold each report to the `regularize.json` beside it (review
    C of #511, C1 and C3).
    """
    path = directory / "regularize.json"
    if not path.is_file():
        return None
    generator = report.get("generator") or {}
    stated = {
        "variant": str(generator.get("variant", "conservative")),
        "orient": str(generator.get("orient", "0")),
        "frame": str(generator.get("frame", "kkt")),
    }
    differ = settings_differ(read_json(path), stated, "its report says")
    if not differ:
        return None
    return (
        f"its stored regularization ran with {', '.join(differ)}: run this count again "
        "from --from-stage import, asking for the settings it ran with"
    )


# --------------------------------------------------------------------------------------
# Stages 5 and 6: the solved view and the same-side view, decided here
# --------------------------------------------------------------------------------------


def square_corners(x: Fraction, y: Fraction, c: Fraction, s: Fraction) -> Corners:
    """A unit square's corners, counter-clockwise, from its centre and rotation."""
    half = Fraction(1, 2)
    return [
        (x + c * a - s * b, y + s * a + c * b)
        for a, b in ((half, half), (-half, half), (-half, -half), (half, -half))
    ]


def view_geometry(witness: Mapping[str, Any]) -> tuple[Fraction, list[Placed], list[Corners]]:
    """A rational view's side, placements and corners, read from its stated fields."""
    side = Fraction(str(witness["side"]))
    placements: list[Placed] = []
    corners: list[Corners] = []
    for square in witness["squares"]:
        if witness["representation"] == "corners":
            points = [(Fraction(str(x)), Fraction(str(y))) for x, y in square["corners"]]
            corners.append(points)
            placements.append(_placed(points))
            continue
        x, y = (Fraction(str(value)) for value in square["center"])
        c, s = (Fraction(str(value)) for value in square["basis"])
        placements.append((x, y, c, s))
        corners.append(square_corners(x, y, c, s))
    return side, placements, corners


def certificate_block(
    source: Mapping[str, Any], relation: str, options: Options, pin: Mapping[str, Any]
) -> dict[str, Any]:
    return {
        "kind": "evand-regularized-view",
        "relation": relation,
        "derived_from": {"path": source["path"], "sha256": source["sha256"]},
        "generator": {
            "name": pin["name"],
            "pin": pin["pin"],
            "source_commit": pin["source_commit"],
            "patches": pin["patches"],
        },
        "variant": options.variant,
        "style": STYLE,
        "orient": options.orient,
        "frame": options.frame,
        "driver": GENERATED_BY,
        "policy": POLICY,
    }


def solved_view(
    directory: Path, n: int, source: Mapping[str, Any], options: Options, pin: Mapping[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """`view-solved.yaml` from `regularize.cert`, and its three exact decisions."""
    text = (directory / "regularize.cert").read_text(encoding="utf-8")
    certificate = evand.parse(text, expected_n=n)
    document = evand.basis_witness(certificate)
    document["id"] = f"W-known-best-n{n:03d}-regularized"
    document["claim"]["limitations"] = (
        "A regularized display view: Evan Daniel's regularizer's dilated certificate "
        "(the solved point scaled by 1 + 10^-20 about the origin corner, the side rounded "
        "up), converted exactly. Its side is not the source witness's; it proves only "
        "s(n) <= side, and is a drawing only as the regularization policy decides."
    )
    document["source"] = {"path": source["path"]}
    document["certificate"] = certificate_block(source, "solved", options, pin)
    started = time.perf_counter()
    decided = evand.decide(certificate)
    side, poses = area.parse_certificate(text, n)
    half_angle = area.decide(side, poses)
    # Decided here before it is written: a view both maintained routes accept is an
    # exactly verified packing at its own side, which is what the house renderer's
    # `verified` provenance says. It never says so of the source's side.
    if decided["exact_verify"]["passed"] and decided["independent"]["passed"]:
        document["claim"]["coordinate_provenance"] = "verified"
    path = directory / "view-solved.yaml"
    blob = write_view(path, document)
    block = {
        "path": path.name,
        "git_blob": blob,
        "id": document["id"],
        "side": decimal_text(certificate.side, 40),
        "side_exact": literal(certificate.side),
        "routes": {
            "exact_verify": bool(decided["exact_verify"]["passed"]),
            "independent": bool(decided["independent"]["passed"]),
            "half_angle": bool(half_angle.passed),
        },
        "decide_seconds": round(time.perf_counter() - started, 2),
    }
    return block, document


def write_text(path: Path, text: str) -> None:
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text(text, encoding="utf-8")


def write_view(path: Path, document: Mapping[str, Any]) -> str:
    """A view as a Witness/v2 file, held to the witness schema before it is written.

    Returns the Git blob id of the bytes written, which the report keeps beside the
    view's verdict as provenance: it says which bytes were decided, and nothing compares
    it (OR-18). `layer` decides the file it takes again (`layer_refusal`).
    """
    text = witness_document(document)
    validate_witness_document(load_yaml(text), path=path, fallback_schema=WITNESS_SCHEMA)
    write_text(path, text)
    return git_blob(text.encode("utf-8"))


def same_side_module() -> tuple[Any | None, str | None]:
    """Lane A's resolver, imported when first needed, or why it is unavailable."""
    try:
        return importlib.import_module("devtools.regularize_same_side"), None
    except ImportError as error:
        return None, f"same-side-unavailable: {error}"


def same_view(
    *,
    directory: Path,
    n: int,
    witness: Mapping[str, Any],
    regularized: Mapping[str, Any],
    source: Mapping[str, Any],
    options: Options,
    pin: Mapping[str, Any],
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, str | None]:
    """`view-same.yaml` from the resolver, decided here; or why there is none."""
    (directory / "view-same.yaml").unlink(missing_ok=True)
    module, unavailable = same_side_module()
    if module is None:
        return None, None, unavailable
    poses = [
        module.GeneratorPose(x, y, degrees) for x, y, degrees in regularized["packing"]["sq"]
    ]
    started = time.perf_counter()
    try:
        outcome = module.resolve(
            dict(witness),
            poses,
            mode=options.same_mode,
            view_id=f"W-known-best-n{n:03d}-regularized",
        )
    except Exception as error:  # noqa: BLE001 -- a resolver failure is recorded, not fatal
        return None, None, f"same-side-error: {type(error).__name__}: {error}"
    seconds = time.perf_counter() - started
    if outcome.status != "same" or outcome.witness is None:
        return None, None, f"same-side-refused: {outcome.reason or 'no reason given'}"
    document = dict(outcome.witness)
    # The driver's provenance wins where the resolver's certificate names the same field:
    # the source by path and digest rather than by id alone, and this generator's kind
    # (review B of #511, B8). The resolver's own words for those fields are kept under
    # `resolver`, and its other fields stay as it wrote them.
    resolver = dict(document.get("certificate") or {})
    provenance = certificate_block(source, "same", options, pin)
    stated = {**resolver, **provenance}
    replaced = {
        key: resolver[key]
        for key in provenance
        if key in resolver and resolver[key] != provenance[key]
    }
    if replaced:
        stated["resolver"] = replaced
    document["certificate"] = stated
    path = directory / "view-same.yaml"
    blob = write_view(path, document)
    side, _placements, corners = view_geometry(document)
    result, _report = exact_verify(document)
    second = independent.check_squares(corners, side)
    block = {
        "path": path.name,
        "git_blob": blob,
        "id": document.get("id"),
        "side": decimal_text(side, 40),
        "side_exact": literal(side),
        "routes": {
            "exact_verify": bool(result["verification_passed"]),
            "independent": bool(second["verification_passed"]),
        },
        "resolve": outcome.report,
        "resolve_seconds": round(seconds, 2),
    }
    return block, document, None


# --------------------------------------------------------------------------------------
# Stage 7: identity and contact shades
# --------------------------------------------------------------------------------------


def turned_squares(
    view: tuple[Fraction, Sequence[Placed]], source: tuple[Fraction, Sequence[Placed]], k: int
) -> list[int]:
    """The view's squares turned beyond `TURN_BOUND` from their match under symmetry `k`.

    The match is `arrangement_gap`'s, nearest centre to the symmetric image; the nearest
    is found in binary64, which agrees with the exact nearest wherever no two of the
    source's centres are within rounding of each other, and the turn is exact.
    """
    other_side = source[0]
    mapped = [area.symmetric(other_side, square, k) for square in source[1]]
    floats = [(float(u), float(v)) for u, v, _a, _b in mapped]
    turned: list[int] = []
    for index, (x, y, c, s) in enumerate(view[1]):
        fx, fy = float(x), float(y)
        j = min(
            range(len(floats)),
            key=lambda m: (fx - floats[m][0]) ** 2 + (fy - floats[m][1]) ** 2,
        )
        a, b = mapped[j][2], mapped[j][3]
        if min(abs(c * b - s * a), abs(c * a + s * b)) > TURN_BOUND:
            turned.append(index)
    return turned


@contextmanager
def long_integer_text() -> Iterator[None]:
    """Lift Python's 4300-digit limit on writing integers as text, for one measurement.

    The limit guards parsing untrusted text. `arrangement_gap` writes the exact squared
    largest move, whose terms multiply a view's and a witness's coordinates and can pass
    it where every coordinate is well within it (n = 110 in the re-run of 12 October 2026);
    the driver reads only the move's decimal root.
    """
    previous = sys.get_int_max_str_digits()
    sys.set_int_max_str_digits(0)
    try:
        yield
    finally:
        sys.set_int_max_str_digits(previous)


def identity(
    view: tuple[Fraction, Sequence[Placed]],
    source: tuple[Fraction, Sequence[Placed]],
    named: Iterable[int],
    of: str,
) -> dict[str, Any]:
    """Obligation 3's measurement of a view against the source witness."""
    record: dict[str, Any] = {
        "basis": "measured",
        "measured_in": "devtools.check_half_angle_area.arrangement_gap",
        "of": of,
    }
    try:
        with long_integer_text():
            gap = area.arrangement_gap(view, source)
    except area.AreaRouteError as error:
        record.update(one_to_one=False, unmatched=str(error), unnamed_turns=[])
        return record
    turned = turned_squares(view, source, int(gap["symmetry"]))
    sine = min(1.0, float(gap["largest_orientation_sine"]))
    record.update(
        one_to_one=True,
        moved=gap["moved_beyond"]["1e-3"],
        moved_beyond=gap["moved_beyond"],
        max_move=gap["largest_displacement"],
        max_turn_deg=f"{math.degrees(math.asin(sine)):.6g}",
        turned=turned,
        unnamed_turns=sorted(set(turned) - set(named)),
        symmetry=gap["symmetry"],
        side_difference=gap["side_difference"],
    )
    return record


def contact_partners(witness: Mapping[str, Any]) -> dict[str, list[list[str]]]:
    """Each square's full-side contacts under the house and stage rules, by the census."""
    exact, frame, _degrees = shades.packings_from_witness(dict(witness))
    return {
        "house": [
            [c.other for c in found] for found in shades.edge_rule_contacts(exact, HOUSE)
        ],
        "stage": [
            [c.other for c in found] for found in shades.centre_rule_contacts(frame, STAGE)
        ],
    }


def histogram(partners: Sequence[Sequence[str]]) -> list[int]:
    counts = [min(4, len(found)) for found in partners]
    return [counts.count(k) for k in range(5)]


def regressions(
    before: Mapping[str, Sequence[Sequence[str]]],
    after: Mapping[str, Sequence[Sequence[str]]],
    ids: Sequence[Any],
) -> list[dict[str, Any]]:
    """Squares whose count under a rule fell, paired by index."""
    found: list[dict[str, Any]] = []
    for rule in RULE_NAMES:
        for index, (was, now) in enumerate(zip(before[rule], after[rule], strict=True)):
            if min(4, len(now)) < min(4, len(was)):
                found.append(
                    {
                        "square": index,
                        "id": ids[index],
                        "rule": rule,
                        "before": min(4, len(was)),
                        "after": min(4, len(now)),
                    }
                )
    return found


def current_view(n: int) -> tuple[str, dict[str, Any]] | None:
    """The project's regularized view of `n` that a new view would replace, if any."""
    if not LAYER_INDEX.is_file():
        return None
    entries = read_json(LAYER_INDEX)["entries"]
    entry = next((row for row in entries if row["n"] == n), None)
    if entry is None or entry.get("status") != "regularized" or not entry.get("view"):
        return None
    path = REPO / entry["view"]["path"]
    text = gzip.decompress(path.read_bytes()).decode("utf-8")
    return entry["view"]["path"], load_yaml(text)["witness"]


def contact_shades(
    n: int, witness: Mapping[str, Any], view: Mapping[str, Any], of: str
) -> dict[str, Any]:
    before, after = contact_partners(witness), contact_partners(view)
    ids = [square["id"] for square in witness["squares"]]
    record: dict[str, Any] = {
        "of": of,
        "measured_in": (
            "devtools.census_atlas_contact_shades: edge_rule_contacts (house) and "
            "centre_rule_contacts (stage) on packings_from_witness"
        ),
        **{
            rule: {"before": histogram(before[rule]), "after": histogram(after[rule])}
            for rule in RULE_NAMES
        },
        "regressions": regressions(before, after, ids),
        "against_current": None,
    }
    current = current_view(n)
    if current is not None:
        path, document = current
        partners = contact_partners(document)
        record["against_current"] = {
            "view": path,
            "regressions": regressions(partners, after, ids),
            "histograms": {rule: histogram(partners[rule]) for rule in RULE_NAMES},
        }
    return record


def totals_fall(shaded: Mapping[str, Any]) -> bool:
    """Whether a house or stage total of shared sides falls, against the witness or the
    current view the new one would replace (policy row 7, owner, 12 October 2026)."""
    current = (shaded.get("against_current") or {}).get("histograms") or {}
    for rule in RULE_NAMES:
        counts = shaded.get(rule) or {}
        after = total_contacts(counts.get("after") or [])
        if after < total_contacts(counts.get("before") or []):
            return True
        if rule in current and after < total_contacts(current[rule]):
            return True
    return False


def poses_equal(view_corners: Sequence[Corners], frame: SourceFrame) -> bool:
    """Whether every square of the view is exactly the source frame's square at its index."""
    if frame.corners is None or len(frame.corners) != len(view_corners):
        return False
    return all(
        set(mine) == set(theirs)
        for mine, theirs in zip(view_corners, frame.corners, strict=True)
    )


# --------------------------------------------------------------------------------------
# Stage 8: the decision table
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Measured:
    """What the decision table reads of one output of one count."""

    output: Output
    produced: bool
    status: str = "ok"
    routes: Mapping[str, bool] = field(default_factory=dict)
    relation: Literal["same", "bound", "solved"] | None = None
    side: Fraction | None = None
    #: `U` where it is rational (`upper_bound`); `bound` holds it exactly in every case,
    #: and decides where it is given (`below_bound`).
    upper: Fraction | None = None
    bound: VerifiedBound | None = None
    pose_equals_witness: bool = False
    one_to_one: bool = True
    unnamed_turns: tuple[int, ...] = ()
    regressions: int = 0
    variant: str = "conservative"
    determined_merge: bool = False
    level: int | None = None
    max_move: Fraction | None = None
    #: Whether the view draws a different picture from the source: a square moved beyond
    #: `10^-3` or turned, a house contact count changed, or no one-to-one pairing to say
    #: otherwise. Unmeasured outputs count as changed.
    visible_change: bool = True
    #: Whether a house or stage total of shared sides falls (`totals_fall`).
    totals_fall: bool = False
    #: False for a drawable output whose identity and shades were never measured: a
    #: report written before `bound` existed measured only the output it chose.
    measured: bool = True


@dataclass(frozen=True)
class Decision:
    row: int | None
    decision: str
    index_record: str | None
    refusal: str | None
    reason: str


def classify(measured: Measured) -> Decision:
    """The policy's decision table, reported in the owner's words of 11 October 2026.

    The rows decide; the word reports. A view that would draw the same picture is "no
    change" whatever row matched, since there is nothing to refuse or hold; a register
    candidate under it is still row 3, and the receipt still lists it. Row 1 is "no
    view"; a visible view held by rows 3 or 4 is "held"; "refuse" is left for an exact
    route's refusal (row 2) and a falling total (row 7), and row 7 otherwise sends the
    view to review (owner, 12 October 2026). Rows 6 and 9 are retired (owner, 13 October
    2026): a changed pose is named in the reason and decides nothing.
    """
    decided = table_row(measured)
    if decided.row in {1, 2} or measured.visible_change:
        return decided
    return Decision(
        decided.row,
        "no-change",
        "unchanged",
        None,
        f"nothing visible changes ({decided.reason})",
    )


def visible_change(ident: Mapping[str, Any], shaded: Mapping[str, Any]) -> bool:
    """Whether a measured view draws a different picture from its source (see `Measured`)."""
    house = shaded.get("house") or {}
    return bool(
        ident.get("moved")
        or ident.get("turned")
        or not ident.get("one_to_one", False)
        or house.get("before") != house.get("after")
    )


def below_bound(m: Measured) -> bool | None:
    """Whether the view's side is below `U`, decided exactly (row 3).

    Against `m.bound` where it is given, a closed form included (`VerifiedBound`), else
    against `m.upper`; None where the record's bound could not be read, so that nothing
    is decided against it.
    """
    if m.side is None:
        return False
    if m.bound is not None:
        order = m.bound.compare(m.side)
        return None if order is None else order < 0
    return m.upper is not None and m.side < m.upper


def table_row(measured: Measured) -> Decision:  # noqa: PLR0911 -- one return per table row
    """Rows 1 to 10 of the policy's decision table; the first that matches decides."""
    m = measured
    if not m.produced:
        return Decision(1, "no-view", None, "generator-failed", f"no view: {m.status}")
    refused = sorted(name for name, passed in m.routes.items() if not passed)
    if refused or not m.routes:
        names = ", ".join(refused) or "no route ran"
        return Decision(
            2, "refuse", "refused", "invalid", f"refused by {names}; open a defect bead"
        )
    below = below_bound(m)
    if below is None:
        unread = m.bound.unread if m.bound is not None else None
        return Decision(
            None,
            "review",
            None,
            None,
            f"the verified upper bound could not be read exactly ({unread}), so row 3 "
            "was not decided and nothing is compared with its printed decimal",
        )
    if below and m.side is not None:
        gap = (
            -m.bound.difference(m.side)
            if m.bound is not None
            else float(m.upper - m.side)
            if m.upper is not None
            else math.nan
        )
        return Decision(
            3,
            "held",
            None,
            None,
            f"register first: the {m.relation} side is below the verified upper bound by "
            f"{gap:.3e}, a register-result candidate",
        )
    # A view at exactly the verified bound (`bound`) is a drawing frame, as a same-side
    # view is (owner, 12 October 2026); only another side stops here.
    if m.relation == "solved":
        if m.upper is None and m.bound is None:
            where = "not the witness's; U unknown, so row 3 was not decided"
        else:
            where = "not the witness's and above the verified upper bound"
        return Decision(4, "held", None, "dilated-side", f"the view's side is {where}")
    if not m.measured:
        return Decision(None, "review", None, None, "the view was not measured")
    if m.pose_equals_witness:
        return Decision(5, "no-change", "unchanged", None, "the view is the witness's pose")
    # Rows 6 and 9, a changed pose, no longer stop a view (owner, 13 October 2026: "the
    # pose doesn't matter if it changes as long as it's optimal and conforms with our
    # regularization guidelines"). Every row above has held it to both exact routes at
    # the witness's side or the bound; the change is named in the reason it is admitted
    # with, and the rows below still decide it.
    pose = pose_changes(m)
    if m.regressions and m.totals_fall:
        return Decision(
            7, "refuse", "refused", "regression", "a house or stage total of shared sides falls"
        )
    if m.regressions:
        return Decision(
            7,
            "review",
            None,
            "regression",
            f"{m.regressions} per-square counts fell while no total did: for review",
        )
    if (m.variant == "fewest" and m.determined_merge) or m.level == 3:
        return Decision(8, "alternate", None, None, "review only, never drawn as the packing")
    if m.variant == "conservative" and (m.level is None or m.level <= 2):
        reason = "every admission condition holds"
        if pose:
            reason = f"{reason}; the pose changes: {'; '.join(pose)}"
        return Decision(10, "admit", "regularized", None, reason)
    return Decision(None, "review", None, None, "no row of the table matches")


def pose_changes(m: Measured) -> list[str]:
    """What rows 6 and 9 once sent to review, named for the reason a view is admitted
    with: no one-to-one pairing, turns no recorded angle change names, a move over 1/2."""
    changes = []
    if not m.one_to_one:
        changes.append("no one-to-one pairing")
    if m.unnamed_turns:
        changes.append(
            f"squares {list(m.unnamed_turns)} turned without a recorded angle change"
        )
    if m.max_move is not None and m.max_move > MOVE_BOUND:
        changes.append(f"a square moved {float(m.max_move):.4g} > 1/2")
    return changes


# --------------------------------------------------------------------------------------
# One count
# --------------------------------------------------------------------------------------


def _measure_view(
    *,
    n: int,
    witness: Mapping[str, Any],
    frame: SourceFrame,
    document: Mapping[str, Any],
    named: Sequence[int],
    of: str,
) -> tuple[dict[str, Any], dict[str, Any], Fraction | None, bool]:
    side, placements, corners = view_geometry(document)
    reference = frame.side if frame.side is not None else Fraction(frame.side_text)
    measured = identity((side, placements), (reference, frame.placements), named, of)
    shaded = contact_shades(n, witness, document, of)
    move = Fraction(measured["max_move"]) if measured.get("max_move") is not None else None
    return measured, shaded, move, poses_equal(corners, frame)


def side_relation(
    side: Fraction, printed: Fraction | None, upper: Fraction | None
) -> Literal["same", "bound", "solved"]:
    """A view's side against the record: the witness's own (`same`), exactly the verified
    upper bound (`bound`, admissible since 12 October 2026), or another (`solved`)."""
    if printed is not None and side == printed:
        return "same"
    if upper is not None and side == upper:
        return "bound"
    return "solved"


ABOVE_BOUND = (
    "same-side-above-bound: the witness's side is above the verified upper bound, and the "
    "view at the bound is drawn (owner, 13 October 2026)"
)


def yield_to_bound(report: dict[str, Any]) -> bool:
    """Set a same-side view aside when the solved view sits at the bound below it.

    The owner, 13 October 2026: a valid view has "equal or smaller side", and the drawing
    is "optimal as best as known". Where the witness's side is above the verified bound
    and the solve reached the bound exactly, the same-side view would draw the packing
    at a side worse than the record's, so the view at the bound is the one decided and
    drawn. The same-side view stays in the report under `same_above_bound`, with the
    measurements it was taken with, so nothing measured is lost. Returns whether it moved.
    """
    outputs = report.get("outputs") or {}
    same, solved = outputs.get("same"), outputs.get("solved")
    if not same or not solved:
        return False
    # The bound the report stored, held exactly: a rational side is at a closed form
    # never, so only a rational `U` is reached exactly.
    bound = report_bound(report)
    side = Fraction(solved["side_exact"])
    if bound is None or bound.compare(side) != 0 or Fraction(same["side_exact"]) <= side:
        return False
    ident, shaded = report.get("identity"), report.get("shades")
    if (ident or {}).get("of") == "same":
        if not (solved.get("identity") and solved.get("shades")):
            # A run written before views at the bound were measured: nothing to decide on.
            return False
        # The run measured the same-side view as the drawing; the solved view's own
        # measurements, taken because it was at the bound, become the report's.
        same = {**same, "identity": ident, "shades": shaded}
        report["identity"], report["shades"] = solved.pop("identity"), solved.pop("shades")
    outputs["same_above_bound"] = same
    outputs["same"] = None
    outputs["same_refusal"] = ABOVE_BOUND
    return True


def _regression_count(shaded: Mapping[str, Any]) -> int:
    current = shaded.get("against_current") or {}
    return len(shaded["regressions"]) + len(current.get("regressions") or [])


def _previous_report(path: Path) -> dict[str, Any] | None:
    """The count's report from the run before, if there is one that reads."""
    try:
        previous = read_json(path)
    except FileNotFoundError, json.JSONDecodeError:
        return None
    return previous if isinstance(previous, dict) else None


def run_count(n: int, options: Options) -> dict[str, Any]:
    """Every stage for one count; the report is written and returned, never raised.

    The earlier run's report is removed first and written again only once the count is
    decided, so a re-run that is interrupted leaves no verdict beside the views it was
    remaking (review B of #511, B5); its solve record is kept in memory for `kept_solve`.
    """
    directory = count_dir(options.run_dir, n)
    directory.mkdir(parents=True, exist_ok=True)
    previous = _previous_report(directory / "report.json")
    (directory / "report.json").unlink(missing_ok=True)
    report: dict[str, Any] = {"format": REPORT_FORMAT, "n": n, "status": "ok", "error": None}
    wall, cpu = time.perf_counter(), _self_cpu() + _children_cpu()
    try:
        _run_stages(n, options, directory, report, previous)
    except Exception as error:  # noqa: BLE001 -- one count's failure must not stop the run
        report["status"] = "error"
        report["error"] = f"{type(error).__name__}: {error}"
    # This worker's own time and its waited-for children's (the solve and the shim): the
    # pool's workers are not the parent's children under the forkserver start method.
    report["cost"] = {
        "cpu_seconds": round(_self_cpu() + _children_cpu() - cpu, 2),
        "wall_seconds": round(time.perf_counter() - wall, 2),
    }
    write_json(directory / "report.json", report)
    return report


def kept_solve(directory: Path, previous: Mapping[str, Any] | None) -> dict[str, Any]:
    """The kept solve, read back for `--from-stage regularize` or `import`.

    A solve that wrote no `witness.json` (a timeout) stands as the count's previous report
    recorded it, attempts and all, so a later stage's re-run keeps its decision; without
    that record the count is run again from the solve."""
    meta = directory / "solve/witness.json"
    if meta.is_file():
        solved = solve_block(read_json(meta))
        solved["seconds"] = solved.get("solver_seconds")
        solved.update(attempt_of(directory / "solve"))
        return solved
    stored = (previous or {}).get("solve")
    if not isinstance(stored, dict) or stored.get("gate") is not None:
        raise EvandRunError(f"{meta} is missing: run this count again from --from-stage solve")
    return dict(stored)


def _run_stages(
    n: int,
    options: Options,
    directory: Path,
    report: dict[str, Any],
    previous: Mapping[str, Any] | None = None,
) -> None:
    pin = vendored_pin()
    path = witness_path(n)
    witness = load_witness(path, fallback_schema=WITNESS_SCHEMA)
    frame = source_frame(witness)
    facts = case_facts(n)
    bound = verified_bound(facts)
    upper = bound.rational if bound is not None else None
    source = {
        "id": witness.get("id"),
        "path": relative(path),
        "sha256": sha256_of(path.read_bytes()),
        "kind": frame.kind,
        "s_W": frame.side_text,
        "s_W_exact": literal(frame.side) if frame.side is not None else None,
        "frame": frame.derivation,
    }
    source["provenance"] = {
        "source_key": facts.get("source_key"),
        "found_by": facts.get("found_by") or [],
        "improved_by": facts.get("improved_by") or [],
    }
    source["witness_source_key"] = (witness.get("source") or {}).get("key")
    report["source"] = source
    report["verified_upper_bound"] = facts["verified_upper_bound"]
    report["verified_upper_bound_exact_form"] = facts["exact_form"]
    report["verified_upper_bound_as_read"] = bound.record() if bound is not None else None
    report["generator"] = {
        "name": pin["name"],
        "pin": pin["pin"],
        "patches": pin["patches"],
        "variant": options.variant,
        "style": STYLE,
        "orient": options.orient,
        "frame": options.frame,
    }
    report["parameters"] = run_parameters(options)
    seconds: dict[str, float | None] = {}
    report["seconds"] = seconds
    first = STAGES.index(options.from_stage)
    # An earlier run's outputs must not outlive a re-run that stops sooner: the receipt
    # digests `regularize.cert` and the gallery draws a view on disk. Every run makes its
    # views again at the import stage, and the regularizer's outputs at its own stage.
    stale = ["view-solved.yaml", "view-same.yaml"]
    if first <= STAGES.index("regularize"):
        stale += ["regularize.json", "regularize.cert"]
    for name in stale:
        (directory / name).unlink(missing_ok=True)
    replica = options.run_dir.resolve() / "replica"

    started = time.perf_counter()
    if first <= STAGES.index("input"):
        write_text(directory / "input.txt", input_text(witness))
        write_json(
            directory / INPUT_RECORD,
            {"witness": {"path": source["path"], "sha256": source["sha256"]}},
        )
    else:
        reused = frame if first > STAGES.index("regularize") else None
        reused_input(directory, witness, reused)
    report["input"] = input_record(directory)
    seconds["input"] = round(time.perf_counter() - started, 3)

    if first <= STAGES.index("solve"):
        solved = solve_with_retries(directory, replica, options.timeout, frame.side)
    else:
        solved = kept_solve(directory, previous)
    # The replica patches the kept solve ran with are this count's, and its views' too.
    pin = {**pin, "patches": [*pin["patches"], *applied_patches(solved.get("patches") or [])]}
    report["generator"]["patches"] = pin["patches"]
    # The stage's cost is every attempt the ladder made, not only the one it kept.
    attempted = [row.get("seconds") or 0 for row in solved.get("attempts") or []]
    seconds["solve"] = round(sum(attempted), 2) if attempted else solved.get("seconds")
    report["solve"] = solved
    record_solve_status(replica, n, str(solved["status"]))
    no_output = {"solved": None, "same": None, "same_refusal": None}
    if solved.get("gate") is None:
        report["status"] = "timeout" if solved["status"] == "timeout" else "generator-failed"
        report["outputs"] = no_output
        decide(report, Measured("solved", produced=False, status=f"solve {solved['status']}"))
        return

    if first <= STAGES.index("regularize"):
        point_work(replica, n, regularizer_frame(directory, witness, frame, options.frame))
        regularized = regularize(directory, replica, n, options)
    else:
        regularized = read_json(directory / "regularize.json")
        # The stored regularization is decided and labelled by what it ran with (B1).
        options = stored_settings(regularized, options)
    seconds["regularize"] = regularized.get("wall_seconds", regularized.get("seconds"))
    report["generator"].update(
        variant=options.variant, orient=options.orient, frame=options.frame
    )
    report["regularize"] = regularize_block(regularized)
    report["parameters"] = run_parameters(options)
    failure = regularize_failure(regularized)
    if failure is not None:
        report["status"] = "timeout" if "timeout" in failure else "generator-failed"
        report["outputs"] = no_output
        decide(report, Measured("solved", produced=False, status=failure))
        return

    started = time.perf_counter()
    solved_block, solved_document = solved_view(directory, n, source, options, pin)
    seconds["import"] = round(time.perf_counter() - started, 3)
    started = time.perf_counter()
    same_block, same_document, same_refusal = same_view(
        directory=directory,
        n=n,
        witness=witness,
        regularized=regularized,
        source=source,
        options=options,
        pin=pin,
    )
    seconds["same"] = round(time.perf_counter() - started, 3)
    report["outputs"] = {
        "solved": solved_block,
        "same": same_block,
        "same_refusal": same_refusal,
    }

    started = time.perf_counter()
    named = [row["square"] for row in regularized.get("changed_angles") or []]
    determined = any(
        isinstance(change, list) and change and change[0] == "determined-merge"
        for change in regularized.get("angle_changes") or []
    )
    common = {
        "upper": upper,
        "bound": bound,
        "variant": options.variant,
        "determined_merge": determined,
        "level": regularized.get("level"),
    }
    outputs: dict[Output, tuple[dict[str, Any], dict[str, Any]]] = {
        "solved": (solved_block, solved_document)
    }
    if same_block is not None and same_document is not None:
        outputs["same"] = (same_block, same_document)
    chosen: Output = "same" if "same" in outputs else "solved"
    measured: dict[Output, Measured] = {}
    for name, (block, document) in outputs.items():
        side = Fraction(block["side_exact"])
        relation = side_relation(side, frame.side, upper)
        block["relation"] = relation
        block["minus_s_W"] = (
            f"{float(side - frame.side):.3e}" if frame.side is not None else None
        )
        block["minus_U"] = f"{bound.difference(side):.3e}" if bound is not None else None
        fields: dict[str, Any] = {}
        if name == chosen or relation != "solved":
            ident, shaded, move, equal = _measure_view(
                n=n, witness=witness, frame=frame, document=document, named=named, of=name
            )
            if name == chosen:
                report["identity"], report["shades"] = ident, shaded
            else:
                block["identity"], block["shades"] = ident, shaded
            ident["pose_equals_witness"] = equal
            fields = {
                "visible_change": visible_change(ident, shaded),
                "pose_equals_witness": equal,
                "one_to_one": bool(ident["one_to_one"]),
                "unnamed_turns": tuple(ident.get("unnamed_turns") or ()),
                "regressions": _regression_count(shaded),
                "totals_fall": totals_fall(shaded),
                "max_move": move,
            }
        measured[name] = Measured(
            name, produced=True, routes=block["routes"], relation=relation, side=side,
            **common, **fields,
        )  # fmt: skip
    seconds["measure"] = round(time.perf_counter() - started, 3)
    if yield_to_bound(report):
        measured.pop("same")
        same_refusal = ABOVE_BOUND
    decide(report, measured["solved"], measured.get("same"), same_refusal)
    report["regularization"] = regularization_record(report)


def decide(
    report: dict[str, Any],
    solved: Measured,
    same: Measured | None = None,
    same_refusal: str | None = None,
) -> None:
    decisions = {"solved": asdict(classify(solved)), "same": None}
    if same is not None:
        decisions["same"] = asdict(classify(same))
    governing = dict(decisions["same"] or decisions["solved"])
    if same is None and same_refusal:
        governing["reason"] = f"{governing['reason']}; same side: {same_refusal}"
    chosen = same if same is not None else solved
    if governing["row"] == 3 and chosen.side is not None:
        # Registering the view makes its side the verified bound, so the row it reaches
        # then is what deciding "register first" leads to (owner, 12 October 2026).
        relation = "bound" if chosen.relation == "solved" else chosen.relation
        after = replace(chosen, upper=chosen.side, bound=None, relation=relation)
        governing["after_registration"] = asdict(classify(after))
    report["decision"] = governing
    report["decisions"] = decisions


# --------------------------------------------------------------------------------------
# The run and its receipt
# --------------------------------------------------------------------------------------


def run_parameters(options: Options) -> dict[str, Any]:
    """The settings one count ran with, for its report and its receipt row: a receipt
    gathers rows from runs made with other settings (review B of #511, B6)."""
    return {
        "variant": options.variant,
        "style": STYLE,
        "orient": options.orient,
        "frame": options.frame,
        "same_mode": options.same_mode,
        "timeout": options.timeout,
        "regularize_timeout": options.regularize_timeout,
        "from_stage": options.from_stage,
    }


def receipt_row(report: Mapping[str, Any]) -> dict[str, Any]:
    outputs = report.get("outputs") or {}
    chosen = outputs.get("same") or outputs.get("solved") or {}
    regularized = report.get("regularize") or {}
    identity_record = report.get("identity") or {}
    shaded = report.get("shades") or {}
    decision = report.get("decision") or {}
    solved_decision = (report.get("decisions") or {}).get("solved") or {}
    solve_record = report.get("solve") or {}
    return {
        "n": report["n"],
        "status": report.get("status"),
        "error": report.get("error"),
        "kind": (report.get("source") or {}).get("kind"),
        "solve_status": solve_record.get("status"),
        "solve_gate": solve_record.get("gate"),
        "solve_rungs": solve_record.get("rungs") or [],
        "replica_patches": solve_record.get("patches") or [],
        "S_exact": solve_record.get("S_exact"),
        "s_W": (report.get("source") or {}).get("s_W"),
        "U": report.get("verified_upper_bound"),
        "level": regularized.get("level"),
        "moved": len(regularized.get("moved") or []),
        "groups": [regularized.get("groups_before"), regularized.get("groups_after")],
        "symmetry": regularized.get("symmetry"),
        "view": identity_record.get("of"),
        "s_V": chosen.get("side"),
        "relation": chosen.get("relation"),
        "same_refusal": outputs.get("same_refusal"),
        "one_to_one": identity_record.get("one_to_one"),
        "max_move": identity_record.get("max_move"),
        "house": [shaded.get("house", {}).get("before"), shaded.get("house", {}).get("after")],
        "stage": [shaded.get("stage", {}).get("before"), shaded.get("stage", {}).get("after")],
        "row": decision.get("row"),
        "decision": decision.get("decision"),
        "index_record": decision.get("index_record"),
        "refusal": decision.get("refusal"),
        "after_registration": (decision.get("after_registration") or {}).get("decision"),
        "solved_row": solved_decision.get("row"),
        "seconds": report.get("seconds"),
        "cost": report.get("cost"),
        "parameters": report.get("parameters"),
    }


def run_generator(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """The receipt's generator: the pin, its local changes, and each replica patch a count
    of the run was solved with, with those counts."""
    pin = vendored_pin()
    used: dict[str, list[int]] = {}
    for row in rows:
        for name in row.get("replica_patches") or []:
            used.setdefault(str(name), []).append(int(row["n"]))
    pin["patches"] = [
        *pin["patches"],
        *(
            {**patch, "counts": used[patch_name(patch)]}
            for patch in applied_patches(sorted(used))
        ),
    ]
    return pin


def _children_cpu() -> float:
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    return usage.ru_utime + usage.ru_stime


def _self_cpu() -> float:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_utime + usage.ru_stime


def run(counts: Sequence[int], options: Options, workers: int) -> dict[str, Any]:
    """Every stage for every count in a process pool, then the receipt."""
    if options.orient != "0":
        # The dilated certificate is imported in the generator's frame, which is the
        # source's only at orientation 0; another would draw the packing turned or
        # mirrored against its witness.
        raise EvandRunError(
            f"--orient {options.orient}: the solved view is imported in the generator's "
            "frame, which is the source's only at --orient 0"
        )
    run_dir = outside_checkout(options.run_dir)
    options = Options(**{**asdict(options), "run_dir": run_dir})
    wall, cpu_self = time.perf_counter(), _self_cpu()
    rows = []
    for n in counts:
        witness = load_witness(witness_path(n), fallback_schema=WITNESS_SCHEMA)
        rows.append(batch_row(n, case_facts(n), witness))
    build_replica(run_dir, rows)
    reports: dict[int, dict[str, Any]] = {}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(run_count, n, options): n for n in counts}
        for future in as_completed(futures):
            report = future.result()
            reports[report["n"]] = report
            decision = report.get("decision") or {}
            print(
                f"n={report['n']}: {report['status']}, row {decision.get('row')} "
                f"{decision.get('decision')}",
                flush=True,
            )
    counted = sum(report["cost"]["cpu_seconds"] for report in reports.values())
    driver = _self_cpu() - cpu_self
    cost = {
        "wall_seconds": round(time.perf_counter() - wall, 2),
        "cpu_seconds": round(driver + counted, 2),
        "driver_cpu_seconds": round(driver, 2),
        "count_cpu_seconds": round(counted, 2),
        "workers": workers,
        "counts": len(counts),
        "measured_by": RUN_MEASURED_BY,
    }
    receipt = write_receipt(run_dir, reports, options, workers, cost)
    print(f"receipt: {run_dir / 'receipt.json'} ({cost['wall_seconds']} s wall)")
    return receipt


#: How this project names the vendored method in a regularization's `method`: the pin in
#: the vendored README's form for structured fields, then the variant and placement.
METHOD = (
    "Evan Daniel's search/regularize (MIT), evand/square-packing@{pin}{patches}, "
    "{variant}, {style}, through devtools.regularize_evand"
)
#: Where a regularization's identity measurements come from.
MEASURED_IN = "devtools.check_half_angle_area.arrangement_gap, in devtools.regularize_evand"


WITNESS_SOURCE_KEYS = {"Kingbird derived numerical facts": "[Kingbird]"}
"""Witness source labels that name a bibliography key in other words: a witness derived
from the Kingbird catalogue (`sqpack.known_best`) is labelled so, and is the packing the
case record credits to `[Kingbird]`."""


def packing_credit(
    credit: Mapping[str, Any] | None, witness_key: str | None, relation: str | None
) -> dict[str, Any] | None:
    """The credit of the packing a view redraws, from the case record's credit for its
    reported upper bound (`credit`), the source witness's own source key, and the view's
    side relation.

    A view at the verified upper bound (`bound`) redraws the packing solved to it, which
    the record's reported bound credits. A view at the witness's own side redraws the
    witness's packing: the reported one where the witness names the record's source or
    the record credits no improvement, and otherwise the packing before the improvement
    the record credits. At 182, 206, 241, 268 and 297 the record credits Evan Daniel's
    exact optimum (T-098) and the witness is Francisco Couzo's packing at his printed
    side (T-056), so a view at that side is credited to the witness's source, by the
    record's finders, improved by no one (#548 review B1). A witness labelled from the
    Kingbird catalogue names `[Kingbird]` (`WITNESS_SOURCE_KEYS`), and at 29, 54 and 87 is
    the packing the record credits with its improvers.
    """
    if credit is None:
        return None
    witness_key = WITNESS_SOURCE_KEYS.get(witness_key or "", witness_key)
    reported = {
        "source_key": credit.get("source_key"),
        "found_by": list(credit.get("found_by") or []),
        "improved_by": list(credit.get("improved_by") or []),
    }
    if (
        relation == "bound"
        or not reported["improved_by"]
        or witness_key in (None, reported["source_key"])
    ):
        return reported
    return {"source_key": witness_key, "found_by": reported["found_by"], "improved_by": []}


def regularization_record(report: Mapping[str, Any]) -> dict[str, Any] | None:
    """The count's regularization in the register's own terms, or None without a view.

    The fields are `results.schema.yaml`'s `regularizations` item (owner, 11 October
    2026: the regularizations this project makes are tracked with the provenance of the
    packings they redraw), so admitting a view copies the record into its index entry,
    or into a register result's `regularizations`, unchanged. Two fields stand in for
    the register's `of` until admission resolves it to a result: `of_witness`, the source
    witness the view redraws, and `provenance`, the credit of the packing it redraws
    (`packing_credit`: its `source_key`, finders and improvers), which a regularization
    never changes.
    `changes` counts the free squares the regularizer turned onto the axis
    (`straightened`) or to another angle (`re_angled`), and the largest determined-group
    merge in degrees; `identity` is measured here, on the view the decision is about.
    """
    outputs = report.get("outputs") or {}
    chosen = outputs.get("same") or outputs.get("solved")
    ident = report.get("identity")
    if not chosen or not ident:
        return None
    generator = report.get("generator") or {}
    patches = generator.get("patches") or []
    regularized = report.get("regularize") or {}
    turned = [entry for entry in regularized.get("merged") or [] if len(entry) == 3]
    axis = sum(1 for _square, _before, after in turned if abs(fold_degrees(after)) < 1e-9)
    merges = [
        abs(float(entry[2]) - float(entry[1]))
        for entry in regularized.get("angle_changes") or []
        if isinstance(entry, list) and len(entry) >= 3 and entry[0] == "determined-merge"
    ]
    changes: dict[str, Any] = {}
    if merges:
        changes["merged_rotation_groups_deg"] = round(max(merges), 6)
    if axis:
        changes["straightened"] = axis
    if len(turned) - axis:
        changes["re_angled"] = len(turned) - axis
    identity: dict[str, Any] = {"basis": "measured", "measured_in": MEASURED_IN}
    identity["one_to_one"] = bool(ident.get("one_to_one"))
    if ident.get("moved") is not None:
        identity["moved"] = int(ident["moved"])
    if ident.get("max_move") is not None:
        identity["max_move"] = float(ident["max_move"])
    if ident.get("max_turn_deg") is not None:
        identity["max_turn_deg"] = float(ident["max_turn_deg"])
    source = report.get("source") or {}
    record: dict[str, Any] = {
        "n": report["n"],
        "of_witness": source.get("id") or f"W-known-best-n{int(report['n']):03d}",
        "provenance": packing_credit(
            source.get("provenance"), source.get("witness_source_key"), chosen.get("relation")
        ),
        "by": "project",
        "method": METHOD.format(
            pin=generator.get("pin"),
            patches="".join(f"+{patch_name(patch)}" for patch in patches),
            variant=generator.get("variant"),
            style=generator.get("style"),
        ),
        # The register knows `same` and `solved`; a view at the bound was solved to it.
        "side": "same" if chosen.get("relation") == "same" else "solved",
    }
    if changes:
        record["changes"] = changes
    record["identity"] = identity
    return record


def fold_degrees(degrees: float) -> float:
    """An angle in degrees modulo 90, into (-45, 45]."""
    folded = (float(degrees) + 45.0) % 90.0 - 45.0
    return 45.0 if folded == -45.0 else folded


def receipt_lists(ordered: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """The receipt's lists: register candidates (row 3 on either output, whatever the
    decision is reported as), the review queue, and the counts by index record."""
    return {
        "candidates": [
            row["n"] for row in ordered if row.get("solved_row") == 3 or row["row"] == 3
        ],
        "review_queue": [
            row["n"] for row in ordered if row.get("decision") in {"review", "alternate"}
        ],
        "index_records": {
            record: [row["n"] for row in ordered if row.get("index_record") == record]
            for record in ("regularized", "refused", "unchanged")
        },
    }


def report_bound(report: Mapping[str, Any]) -> VerifiedBound | None:
    """The verified upper bound a report stored when its count ran, held exactly."""
    return verified_bound(
        {
            "verified_upper_bound": report.get("verified_upper_bound"),
            "exact_form": report.get("verified_upper_bound_exact_form"),
        }
    )


def report_relation(
    report: Mapping[str, Any], side: Fraction
) -> Literal["same", "bound", "solved"]:
    """`side_relation` of `side` against the witness side and the bound a report stored."""
    bound = report_bound(report)
    printed = (report.get("source") or {}).get("s_W_exact")
    return side_relation(
        side,
        Fraction(printed) if printed else None,
        bound.rational if bound is not None else None,
    )


def measured_from_report(report: Mapping[str, Any], name: Output) -> Measured:
    """What the decision table reads of one output, from a written report.

    Reports written before the pose comparison was stored lack `pose_equals_witness`; for
    them it is taken as a same-side view whose largest move is zero with nothing turned.
    """
    outputs = report.get("outputs") or {}
    block = outputs.get(name)
    if not block:
        # The stage that stopped the count says why: a regularizer's refusal after a
        # certified solve is not the solve's status (n = 303 in the full run).
        reason = str((report.get("decision") or {}).get("reason") or "")
        if reason.startswith("no view: ") and not reason.startswith("no view: solve "):
            return Measured(name, produced=False, status=reason.removeprefix("no view: "))
        solve_record = report.get("solve") or {}
        status = solve_record.get("status") or report.get("status")
        regularized = report.get("regularize")
        if solve_gate({**solve_record, "status": status}) and regularized is not None:
            failure = regularize_failure(regularized) or "regularize: no output"
            return Measured(name, produced=False, status=failure)
        return Measured(name, produced=False, status=f"solve {status}")
    regularized = report.get("regularize") or {}
    bound = report_bound(report)
    upper = bound.rational if bound is not None else None
    side = Fraction(block["side_exact"])
    # Derived again rather than read, so reports written before `bound` existed decide
    # as the table now does.
    relation = report_relation(report, side)
    chosen = "same" if outputs.get("same") else "solved"
    ident: Mapping[str, Any] | None = None
    shaded: Mapping[str, Any] | None = None
    if name == chosen:
        ident, shaded = report.get("identity"), report.get("shades")
    elif relation != "solved":
        ident, shaded = block.get("identity"), block.get("shades")
    fields: dict[str, Any] = {"measured": False}
    if ident is not None and shaded is not None:
        move = Fraction(ident["max_move"]) if ident.get("max_move") is not None else None
        equal = ident.get("pose_equals_witness")
        if equal is None:
            equal = relation == "same" and move == 0 and not ident.get("turned")
        fields = {
            "visible_change": visible_change(ident, shaded),
            "pose_equals_witness": bool(equal),
            "one_to_one": bool(ident.get("one_to_one")),
            "unnamed_turns": tuple(ident.get("unnamed_turns") or ()),
            "regressions": _regression_count(shaded),
            "totals_fall": totals_fall(shaded),
            "max_move": move,
        }
    return Measured(
        name,
        produced=True,
        routes=block.get("routes") or {},
        relation=relation,
        side=side,
        upper=upper,
        bound=bound,
        variant=(report.get("generator") or {}).get("variant", "conservative"),
        determined_merge=any(
            isinstance(change, list) and change and change[0] == "determined-merge"
            for change in regularized.get("angle_changes") or []
        ),
        level=regularized.get("level"),
        **fields,
    )


def _current_histograms(n: int, report: dict[str, Any]) -> None:
    """Add the replaced view's histograms to a report measured before they were stored,
    so row 7 can tell a falling total from per-square losses; only while the layer in
    this checkout still holds the view the report was measured against."""
    blocks = [report.get("shades"), *(
        (block or {}).get("shades") for block in (report.get("outputs") or {}).values()
        if isinstance(block, dict)
    )]  # fmt: skip
    pending = [
        block["against_current"]
        for block in blocks
        if block
        and block.get("against_current")
        and "histograms" not in block["against_current"]
    ]
    found = current_view(n) if pending else None
    for current in pending:
        if found is not None and found[0] == current.get("view"):
            partners = contact_partners(found[1])
            current["histograms"] = {rule: histogram(partners[rule]) for rule in RULE_NAMES}


def refresh_bound(report: dict[str, Any], n: int) -> dict[str, Any] | None:
    """Rewrite a report's stored `U` from the case record as it stands, and each output's
    distance to it; the change, or `None` where the record still holds the same bound.

    A run stores the verified upper bound it compared with. When a register result moves
    that bound afterwards (T-155 took 59 ceilings to the exact sides of row-3 views), the
    run's decisions are stale until `U` is read again: `upper_bound` reads the exact form
    where it is rational, so a bound printed at the same decimal with a new exact form is a
    new `U`.
    """
    facts = case_facts(n)
    before = {
        "value": report.get("verified_upper_bound"),
        "exact_form": report.get("verified_upper_bound_exact_form"),
    }
    after = {"value": facts["verified_upper_bound"], "exact_form": facts["exact_form"]}
    if before == after:
        return None
    report["verified_upper_bound"] = after["value"]
    report["verified_upper_bound_exact_form"] = after["exact_form"]
    # The bound held exactly, as the run writes `minus_U` (`verified_bound`).
    bound = verified_bound(facts)
    for block in (report.get("outputs") or {}).values():
        if isinstance(block, dict) and block.get("side_exact"):
            side = Fraction(block["side_exact"])
            block["minus_U"] = f"{bound.difference(side):.3e}" if bound is not None else None
    return {"n": n, "before": before, "after": after}


def redecide(
    report: dict[str, Any],
    n: int,
    *,
    refresh_bounds: bool = False,
    directory: Path | None = None,
) -> dict[str, Any] | None:
    """Decide one written report again in place, from its stored measurements.

    What `reclassify` does to each count, and what `devtools.regularize_select` does to a
    copy to learn what `layer` will draw once a run is reclassified, so the two cannot
    decide a count differently: with `refresh_bounds`, `U` read again from the case
    record (`refresh_bound`); the replaced view's histograms added where this checkout's
    layer still holds it (`_current_histograms`); a same-side view above the bound set
    aside (`yield_to_bound`); then both outputs decided, the source's provenance filled
    in where the run predates it, and the regularization record written again. Returns
    the bound's change, or None.

    With `directory`, the count's directory in its run, a report not labelled with the
    settings its stored regularization ran with (`settings_disagreement`) is not decided
    again: it is sent to review with no regularization record, which `layer` would refuse
    it for (`layer_refusal`; review C of #511, C3).
    """
    change = refresh_bound(report, n) if refresh_bounds else None
    mislabelled = None if directory is None else settings_disagreement(directory, report)
    if mislabelled is not None:
        report["decision"] = asdict(
            Decision(None, "review", None, None, f"not decided again: {mislabelled}")
        )
        report["decisions"] = {"solved": None, "same": None}
        report["regularization"] = None
        return change
    _current_histograms(n, report)
    yield_to_bound(report)
    outputs = report.get("outputs") or {}
    solved = measured_from_report(report, "solved")
    same = measured_from_report(report, "same") if outputs.get("same") else None
    for measured in (solved, same):
        if measured is not None and measured.produced:
            outputs[measured.output]["relation"] = measured.relation
    decide(report, solved, same, outputs.get("same_refusal"))
    source = report.setdefault("source", {})
    if not source.get("provenance"):
        facts = case_facts(n)
        source["provenance"] = {
            "source_key": facts.get("source_key"),
            "found_by": facts.get("found_by") or [],
            "improved_by": facts.get("improved_by") or [],
        }
    report["regularization"] = regularization_record(report)
    return change


def reclassify(
    run_dir: Path, counts: Sequence[int] | None = None, *, refresh_bounds: bool = False
) -> dict[str, Any]:
    """Decide a finished run again from its reports, without re-running any stage.

    For a change to the decision table or to how decisions are reported: every count's
    `decision` and `decisions` are rewritten from its stored measurements (`redecide`),
    and the receipt's rows and lists follow; its cost and parameters are left as they
    were.

    It decides on the `U` each report stored when its count ran, not on the case record
    as it stands. A count whose record has moved `U` since (T-151 moved 60 ceilings) is
    listed in the receipt's `reclassified.stale_bounds` and printed by the command, so a
    stale row 3 or 4 is never decided again silently (review B of #511, B10). With
    `refresh_bounds`, each report's `U` is first read again from the case record
    (`refresh_bound`), for a run decided before a register result moved the bound; the
    receipt lists every count whose `U` changed, and those are then not stale. Run it on
    a copy of a run directory to keep the run as it was decided.

    It decides only a report labelled with the settings its stored regularization ran
    with (`settings_disagreement`). A report written before review B's B1 fix could call
    a `fewest` regularization `conservative`, and its row is then the wrong variant's: such
    a count is not decided again but sent to review by `redecide`, with no regularization
    record, listed in `reclassified.stale_settings` and printed, to be run again from
    `--from-stage import` (review C of #511, C3).

    Its cost is left as the run that spent it recorded it. Decided on a copy of that
    run's directory, under another name, the receipt says so: `reclassified.from` is the
    run's id (`copied_from`), and the copy's run block records no cost of its own in the
    layer (`run_block`, `regularize_axis_components.costed_once`; #548 review C, C3).
    """
    path = run_dir / "receipt.json"
    receipt = read_json(path)
    rows = {int(row["n"]): row for row in receipt.get("counts", [])}
    chosen = sorted(rows) if counts is None else list(counts)
    refreshed: list[dict[str, Any]] = []
    stale: list[int] = []
    unsettled: list[int] = []
    for n in chosen:
        directory = count_dir(run_dir, n)
        report_path = directory / "report.json"
        report = read_json(report_path)
        mislabelled = settings_disagreement(directory, report)
        change = redecide(report, n, refresh_bounds=refresh_bounds, directory=directory)
        if change is not None:
            refreshed.append(change)
        facts = case_facts(n)
        stored = (
            report.get("verified_upper_bound"),
            report.get("verified_upper_bound_exact_form"),
        )
        if stored != (facts["verified_upper_bound"], facts["exact_form"]):
            stale.append(n)
        if mislabelled is not None:
            unsettled.append(n)
        write_json(report_path, report)
        rows[n] = receipt_row(report)
    ordered = [rows[n] for n in sorted(rows)]
    receipt.update({"counts": ordered, **receipt_lists(ordered)})
    source = copied_from(run_dir, receipt)
    receipt["reclassified"] = {
        "policy": POLICY,
        "counts": chosen,
        "stale_bounds": stale,
        "stale_settings": unsettled,
        **({"from": source} if source is not None else {}),
    }
    if refresh_bounds:
        receipt["reclassified"]["refreshed_bounds"] = refreshed
    write_json(path, receipt)
    return receipt


def copied_from(run_dir: Path, receipt: Mapping[str, Any]) -> str | None:
    """The id of the run whose cost `receipt` carries, where that is not the run in
    `run_dir`: a copy decided again keeps the receipt of the run it was copied from.

    An earlier `reclassify` may already have said so, and a copy of a copy keeps that
    source. Otherwise the receipt's `run_directory`, where the run spent its cost, is
    compared with the directory's name, which is the run's id in the layer. A receipt from
    before it recorded its directory says nothing here; the layer then refuses a run that
    repeats another's cost unmarked (`regularize_axis_components.repeated_costs`), and
    `reclassified.from` can be written into the copy's receipt by hand.
    """
    held = (receipt.get("reclassified") or {}).get("from")
    if held:
        return str(held)
    ran_in = receipt.get("run_directory")
    if ran_in and ran_in != run_dir.name:
        return f"{axis.EVAND_GENERATOR}-{ran_in}"
    return None


# --------------------------------------------------------------------------------------
# The layer: a run's views written where the atlas reads them
# --------------------------------------------------------------------------------------

#: The selections `layer` knows. `admitted` is the policy's: row 10 alone, and the only
#: one that may write into this checkout. `preview` is every view that would change the
#: drawing, passes the maintained exact routes, pairs one to one, and loses no contact in
#: total under either rule, against the witness or the current view; it is for a scratch
#: tree, to see the atlas with the held and review rows drawn before anyone decides them.
SELECTIONS = ("admitted", "preview")
VIEW_KIND = "regularized-view"
DRAWING_LABEL = "regularized"
LAYER_DIR = "packing/atlas/known-best/regularized"
LAYER_INDEX_PATH = f"{LAYER_DIR}/index.json"
LAYER_GENERATED_BY = "python -m devtools.regularize_evand layer --select admitted"
IDENTITY_BY = (
    "devtools.check_half_angle_area.arrangement_gap, nearest centres under the box's "
    "eight symmetries"
)
SHADES_BY = (
    "devtools.census_atlas_contact_shades: edge_rule_contacts (house) and "
    "centre_rule_contacts (stage) on packings_from_witness"
)
#: Run parameters an index's `runs` keeps: what a reader needs to rebuild the run, not
#: the list of counts it ran, which its decisions already sum.
RUN_PARAMETERS = (
    "variant", "style", "orient", "frame", "same_mode", "from_stage", "dps", "eps",
    "timeout", "regularize_timeout", "workers",
)  # fmt: skip


def total_contacts(counts: Sequence[int]) -> int:
    """Full sides shared, over a histogram of squares with 0 to 4 of them."""
    return sum(k * count for k, count in enumerate(counts))


def layer_candidate(report: Mapping[str, Any], select: str) -> Output | None:
    """Which view of a decided count `select` takes, `same` or `solved`, or None."""
    decision = report.get("decision") or {}
    outputs = report.get("outputs") or {}
    chosen = "same" if outputs.get("same") else "solved" if outputs.get("solved") else None
    if select == "admitted":
        # Row 10 decided the chosen view: the same-side one, or the solved one at the bound.
        return chosen if decision.get("decision") == "admit" else None
    if chosen is None or decision.get("decision") in {None, "no-view", "no-change"}:
        return None
    routes = outputs[chosen].get("routes") or {}
    if not (routes.get("exact_verify") and routes.get("independent")):
        return None
    if not (report.get("identity") or {}).get("one_to_one"):
        return None
    if totals_fall(report.get("shades") or {}):
        return None
    return chosen


def source_id(report: Mapping[str, Any]) -> str:
    """The source witness's id; reports written before the driver stored it name the
    known-best witness by its count."""
    return (report.get("source") or {}).get("id") or f"W-known-best-n{int(report['n']):03d}"


@dataclass(frozen=True)
class Admitted:
    """One generator's view of one count, decided and ready to be drawn by the layer."""

    n: int
    generator: str
    run: dict[str, Any]
    source: dict[str, Any]
    side: dict[str, Any]
    view: dict[str, Any]
    """The view's Witness/v2 record, its certificate not yet the layer's."""
    provenance: dict[str, Any]
    """The generator's own certificate fields, kept under the layer's certificate."""
    routes: dict[str, bool]
    decision: dict[str, Any]
    measured: dict[str, Any]
    regularization: dict[str, Any]
    house_after: list[int]


def layer_regularization(record: Mapping[str, Any]) -> dict[str, Any]:
    """A run's regularization record as the layer keeps it: the register's terms, its
    identity's measurements retained in the layer's index (`measured_in`)."""
    kept = {key: value for key, value in record.items() if value is not None}
    kept["identity"] = {**record["identity"], "measured_in": LAYER_INDEX_PATH}
    return kept


def evand_admitted(
    report: Mapping[str, Any], directory: Path, run_id: str, *, text: str | None = None
) -> Admitted:
    """A driver report's admitted view (row 10), in the layer's terms: `text`, the view as
    `layer_refusal` decided it, or else the file as it is."""
    chosen = layer_candidate(report, "admitted")
    if chosen is None:
        raise EvandRunError(f"n={report['n']}: not admitted")
    n = int(report["n"])
    source = report.get("source") or {}
    block = (report.get("outputs") or {})[chosen]
    routes = block.get("routes") or {}
    ident = report.get("identity") or {}
    shaded = report.get("shades") or {}
    regularized = report.get("regularize") or {}
    if text is None:
        text = (directory / f"view-{chosen}.yaml").read_text(encoding="utf-8")
    document = load_yaml(text)
    run: dict[str, Any] = {"id": run_id, "output": chosen}
    solved = report.get("solve") or {}
    # Before the retry ladder a report kept the retry's arguments; since, its rungs.
    retried = solved.get("retried_with")
    if retried:
        run["retried_with"] = [str(argument) for argument in retried]
    if "rungs" in solved:
        run["rungs"] = [str(rung) for rung in solved.get("rungs") or []]
    decision = report.get("decision") or {}
    record = report.get("regularization")
    if not record:
        raise EvandRunError(f"n={n}: the report carries no regularization record")
    return Admitted(
        n=n,
        generator=axis.EVAND_GENERATOR,
        run=run,
        source={
            "witness": source.get("path"),
            "id": source_id(report),
            "scalar_kind": source.get("kind"),
            "sha256": source.get("sha256"),
        },
        side={
            "reported": source.get("s_W"),
            "view": block.get("side_exact"),
            "relation": block.get("relation"),
            "view_minus_reported": block.get("minus_s_W"),
            "view_minus_verified_upper_bound": block.get("minus_U"),
        },
        view=dict(document["witness"]),
        provenance=dict(document["witness"].get("certificate") or {}),
        routes={
            "repository_verifier": bool(routes.get("exact_verify")),
            "independent_checker": bool(routes.get("independent")),
            **({"half_angle": bool(routes["half_angle"])} if "half_angle" in routes else {}),
        },
        decision={
            "row": decision.get("row"),
            "decision": decision.get("decision"),
            "reason": decision.get("reason"),
        },
        measured={
            "identity_by": f"{IDENTITY_BY}, in devtools.regularize_evand",
            "shades_by": f"{SHADES_BY}, in devtools.regularize_evand",
            "contacts": {
                rule: {
                    "before": list((shaded.get(rule) or {}).get("before") or []),
                    "after": list((shaded.get(rule) or {}).get("after") or []),
                }
                for rule in RULE_NAMES
            },
            "symmetry": int(ident.get("symmetry") or 0),
            "regressions": _regression_count(shaded) if shaded else 0,
            "level": regularized.get("level"),
            "groups": [
                int(regularized["groups_before"]),
                int(regularized["groups_after"]),
            ]
            if regularized.get("groups_before") is not None
            else [],
        },
        regularization=layer_regularization(record),
        house_after=list((shaded.get("house") or {}).get("after") or []),
    )


def run_block(run_dir: Path, run_id: str) -> dict[str, Any]:
    """A run as the layer's index records it, from its receipt: the generator version is
    the index's `generators` block, so a run keeps its parameters, decisions and cost.

    The run is dated by the time its receipt records (`finished`, written when the run
    wrote it), never by the file's modification time, which Git does not keep and a copy
    or a restore resets (#548 review B5). A receipt from before the time was recorded
    gives `None`, which `admit_views` fills from the index's own record of the run.

    A run decided again on a copy of another's directory carries the receipt's record of
    it (`reclassified.from`) as `reclassified_from`, so the layer records that cost once,
    on the run that spent it (`costed_once`; #548 review C, C3).
    """
    receipt = read_json(run_dir / "receipt.json")
    parameters = receipt.get("parameters") or {}
    cost = receipt.get("cost") or {}
    decisions: dict[str, int] = {}
    for row in receipt.get("counts") or []:
        word = str(row.get("decision"))
        decisions[word] = decisions.get(word, 0) + 1
    recorded = receipt.get("finished")
    finished = str(recorded)[:10] if recorded else None
    measured: dict[str, Any] = {
        "cpu_seconds": float(cost.get("cpu_seconds") or 0),
        "wall_seconds": float(cost.get("wall_seconds") or 0),
        "workers": int(cost.get("workers") or parameters.get("workers") or 1),
    }
    # A receipt whose cost was not measured by the run itself -- one rebuilt after the
    # run, say -- keeps the sentence that says how, so the index does not read it as
    # measured. A run's own sentence (`RUN_MEASURED_BY`) is the default and says nothing.
    if (note := cost.get("measured_by")) and note != RUN_MEASURED_BY:
        measured["note"] = str(note)
    source = (receipt.get("reclassified") or {}).get("from")
    return {
        "id": run_id,
        "generator": axis.EVAND_GENERATOR,
        "finished": finished,
        "interpreter": (receipt.get("generator") or {}).get("interpreter"),
        "parameters": {key: parameters[key] for key in RUN_PARAMETERS if key in parameters},
        "counts": len(receipt.get("counts") or []),
        "decisions": dict(sorted(decisions.items())),
        **({"reclassified_from": str(source)} if source and source != run_id else {}),
        "cost": measured,
    }


def evand_generator_block() -> dict[str, Any]:
    """The vendored generator as the layer's index describes it: its pin and patches."""
    pin = vendored_pin()
    return {
        "tool": "packing/devtools/regularize_evand.py",
        "generated_by": LAYER_GENERATED_BY,
        "method": METHOD.format(
            pin=pin["pin"],
            patches="".join(f"+{patch}" for patch in pin["patches"]),
            variant="conservative",
            style=STYLE,
        ),
        "credit": axis.EVAND_CREDIT,
        "vendored": relative(VENDOR),
        "source_url": pin["source_url"],
        "pin": pin["pin"],
        "source_commit": pin["source_commit"],
        "patches": pin["patches"],
    }


def layer_view(admitted: Admitted) -> dict[str, Any]:
    """An admitted view as the layer holds it: the renderer's certificate fields, the
    regularization and credit its entry repeats, and the generator's own fields kept."""
    view = dict(admitted.view)
    view["certificate"] = {
        "kind": VIEW_KIND,
        "label": DRAWING_LABEL,
        "derived_from": admitted.source["id"],
        "generator": admitted.generator,
        "credit": axis.EVAND_CREDIT,
        "run": admitted.run["id"],
        "regularization": admitted.regularization,
        "decision": admitted.decision,
        "generated": admitted.provenance,
    }
    return view


def layer_entry(
    admitted: Admitted,
    view_path: str,
    text: str,
    shade_record: Mapping[str, Any],
    reference: Mapping[str, Any],
) -> dict[str, Any]:
    """The index entry for a written view (`regularized-atlas-index.schema.yaml`)."""
    return {
        "n": admitted.n,
        "status": "regularized",
        "generator": admitted.generator,
        "run": admitted.run,
        "source": admitted.source,
        "side": admitted.side,
        "view": {"path": view_path, "sha256": sha256_of(text.encode("utf-8"))},
        "shades": dict(shade_record),
        "exact_verification": {
            **admitted.routes,
            "passed": bool(
                admitted.routes.get("repository_verifier")
                and admitted.routes.get("independent_checker")
            ),
        },
        "decision": admitted.decision,
        "measured": admitted.measured,
        "regularization": admitted.regularization,
        "reference": dict(reference),
    }


def current_house_total(entry: Mapping[str, Any] | None, root: Path) -> int | None:
    """Full sides the layer's current view of a count shares under the house rule."""
    if entry is None or entry.get("status") != "regularized" or not entry.get("view"):
        return None
    text = gzip.decompress((root / entry["view"]["path"]).read_bytes()).decode("utf-8")
    return total_contacts(histogram(contact_partners(load_yaml(text)["witness"])["house"]))


def layer_refusal(
    directory: Path, report: Mapping[str, Any], chosen: Output
) -> tuple[str | None, str | None]:
    """The view `chosen` of a decided count as `layer` would write it, or why it may not.

    Returns the file's text and None, or None and the refusal. The file is decided as it
    is now, not identified (`view_refusal`), so an edit that leaves the same valid view, a
    comment say, is taken, and any other is refused. The report's settings must also be
    its stored regularization's (`settings_disagreement`), which keeps out a report
    labelled before that was checked. Nothing is compared by digest or Git blob id (OR-16,
    OR-18); `git_blob` stays in the report as provenance. An interrupted re-run leaves no
    report beside its views (`run_count`), so they are never reached here.
    """
    refusal = settings_disagreement(directory, report)
    if refusal is None and not (directory / "regularize.json").is_file():
        refusal = "no regularize.json beside the report to hold its settings to"
    if refusal is not None:
        return None, refusal
    path = directory / f"view-{chosen}.yaml"
    try:
        text = path.read_text(encoding="utf-8")
        document = load_yaml(text)
        validate_witness_document(document, path=path, fallback_schema=WITNESS_SCHEMA)
        refusal = view_refusal(report, chosen, path.name, document["witness"])
    except Exception as error:  # noqa: BLE001 -- a view that does not read is refused
        return None, f"{path.name} does not read as a rational view: {error}"
    return (None, refusal) if refusal is not None else (text, None)


def view_refusal(
    report: Mapping[str, Any], chosen: Output, name: str, witness: Mapping[str, Any]
) -> str | None:
    """Why a view's witness, as it is now, is not the view its report decided, or None.

    `exact_verify` and the independent checker must both accept it; for the solved view,
    converted from a certificate, the half-angle route must decide it as the report
    recorded; and its exact side, its relation to the witness's side and the bound the
    report stored, and its id must be the ones its report decided on (`decided_refusal`).
    """
    block = (report.get("outputs") or {})[chosen]
    _routes, refusal = decided_refusal(
        name,
        witness,
        recorded=block.get("routes") or {},
        decided={
            "side": block.get("side_exact"),
            "relation": block.get("relation"),
            "id": block.get("id"),
        },
        relation=lambda side: report_relation(report, side),
        half_angle=chosen == "solved",
    )
    return refusal


def decided_refusal(
    name: str,
    witness: Mapping[str, Any],
    *,
    recorded: Mapping[str, Any],
    decided: Mapping[str, Any],
    relation: Callable[[Fraction], str] | None = None,
    half_angle: bool = False,
) -> tuple[dict[str, bool], str | None]:
    """A view's witness decided as it is now, and why it is not the view its run decided,
    or None: what `view_refusal` holds a driver view to, and the grid-slack generator's
    admission its own (`regularize_grid_slack.admitted`, #548 review C, C1).

    The routes are run on the witness: `exact_verify` and the independent checker, and
    with `half_angle` the half-angle route. Both exact routes must accept it, and each
    route must decide it as the run `recorded` (by route name). Each field the run
    `decided` must be the witness's own: `side`, its exact side as a literal; `id`; and
    `relation`, which `relation` reads from that side. The verdicts come back with the
    refusal, so a caller records what was decided on these bytes, not what its run says.
    """
    side, placements, corners = view_geometry(witness)
    result, _report = exact_verify(witness)
    now = {
        "exact_verify": bool(result["verification_passed"]),
        "independent": bool(independent.check_squares(corners, side)["verification_passed"]),
    }
    if half_angle:
        now["half_angle"] = bool(area.decide_placed(side, placements).passed)
    own: dict[str, Any] = {"side": literal(side), "id": witness.get("id")}
    if relation is not None:
        own["relation"] = relation(side)
    failed = [route for route in ("exact_verify", "independent") if not now[route]]
    differ = [route for route, passed in now.items() if bool(recorded.get(route)) != passed]
    problems = [
        *([f"{name} as it is now fails {' and '.join(failed)}"] if failed else []),
        *(
            [f"{name} as it is now is decided otherwise by {', '.join(differ)}"]
            if differ and not failed
            else []
        ),
        *(
            f"{name}'s {field} is {own[field]}, not the {value} its report decided"
            for field, value in decided.items()
            if own[field] != value
        ),
    ]
    return now, "; ".join(problems) or None


def admit_views(
    candidates: Sequence[Admitted],
    root: Path,
    *,
    generators: Mapping[str, Any],
    runs: Sequence[Mapping[str, Any]],
    exclude: Collection[int] = (),
) -> dict[str, Any]:
    """Write admitted views into the layer under `root` and their entries into its index.

    A count in `exclude` is left out whatever was decided there (its witness is about to
    change). A view replaces the layer's current one only when it shares at least as
    many full sides in total under the house rule; the axis tool's record of the count
    stays beside it as `reference`. The index keeps the generators and runs its entries
    draw from, and its totals are summed again.
    """
    root = root.resolve()
    index_path = root / LAYER_INDEX_PATH
    index = read_json(index_path)
    if index.get("contract") != axis.ATLAS_CONTRACT:
        raise EvandRunError(f"{LAYER_INDEX_PATH} is not a {axis.ATLAS_CONTRACT} index")
    entries = {int(entry["n"]): entry for entry in index["entries"]}
    dated = dated_runs(runs, index.get("runs") or [])
    known = {run["id"]: dict(run) for run in index.get("runs") or []}
    known.update({run["id"]: run for run in dated})
    repeated = axis.repeated_costs(list(known.values()))
    if repeated:
        raise EvandRunError("; ".join(repeated))
    layout = layer_layout(root)
    written: list[int] = []
    kept: list[int] = []
    excluded: list[int] = []
    for admitted in sorted(candidates, key=lambda item: item.n):
        n = admitted.n
        if n in exclude:
            excluded.append(n)
            continue
        current = entries.get(n)
        reference = (current or {}).get("reference") or current
        if reference is None or reference.get("generator") != axis.ALGORITHM:
            raise EvandRunError(f"n={n}: the layer holds no record of the axis tool's")
        drawn = current_house_total(current, root)
        if drawn is not None and total_contacts(admitted.house_after) < drawn:
            kept.append(n)
            continue
        text = witness_document(layer_view(admitted), schema=layout.schema_reference())
        view_path = f"{LAYER_DIR}/n-{n:03d}-regularized.yaml.gz"
        target = root / view_path
        with atomic_output_file(target, make_parents=True) as temporary:
            temporary.write_bytes(gzip.compress(text.encode("utf-8"), compresslevel=9, mtime=0))
        source = root / admitted.source["witness"]
        with tempfile.TemporaryDirectory() as scratch:
            plain = Path(scratch) / "view.yaml"
            plain.write_text(text, encoding="utf-8")
            after = shades.witness_shades(plain)
        shade_record = axis.shade_record(shades.witness_shades(source), after)
        entries[n] = json.loads(
            json.dumps(layer_entry(admitted, view_path, text, shade_record, reference))
        )
        written.append(n)
    records = [entries[n] for n in sorted(entries)]
    rebuilt = axis.carried_index(
        {
            **index,
            "generators": {**(index.get("generators") or {}), **generators},
            "runs": list(known.values()),
        },
        records,
    )
    with atomic_output_file(index_path) as temporary:
        temporary.write_text(axis.index_text(rebuilt), encoding="utf-8")
    return {"written": written, "kept_current": kept, "excluded": excluded}


def dated_runs(
    runs: Sequence[Mapping[str, Any]], committed: Sequence[Mapping[str, Any]]
) -> list[dict[str, Any]]:
    """Each run block with its finish date: its receipt's, or, for a receipt from before
    the driver recorded one, the date the index already holds for the run. A run neither
    dates is refused before anything is written.

    In the same way, a run whose receipt does not mark it a reclassified copy keeps the
    mark the index already holds for it (`reclassified_from`, #548 review C, C3): a
    receipt from before `reclassify` recorded its source says nothing either way, and the
    run the index records as a copy stays one."""
    held = {str(run["id"]): run.get("finished") for run in committed}
    marked = {
        str(run["id"]): run["reclassified_from"]
        for run in committed
        if run.get("reclassified_from")
    }
    found: list[dict[str, Any]] = []
    for run in runs:
        dated = dict(run)
        if not dated.get("reclassified_from") and str(dated["id"]) in marked:
            cost = dated.pop("cost", None)
            dated["reclassified_from"] = marked[str(dated["id"])]
            if cost is not None:
                dated["cost"] = cost  # after the mark, where `run_block` puts it
        if dated.get("finished") is None:
            if not held.get(str(dated["id"])):
                message = (
                    f"{dated['id']}: its receipt records no finish time (a run from before "
                    "its generator wrote one), and the index holds no date for it: add "
                    "`finished`, the UTC time the run ended, to its receipt.json, or for a "
                    "grid-slack run to one of its reports"
                )
                raise EvandRunError(message)
            dated["finished"] = held[str(dated["id"])]
        found.append(dated)
    return found


def evand_candidates(
    run_dirs: Sequence[Path],
) -> tuple[list[Admitted], list[dict[str, Any]], dict[str, str]]:
    """Every count finished runs admitted (row 10), a later run winning at a count two
    decided, with the runs they came from, and, with the reason, each admitted view
    `layer_refusal` refused.

    Each view is decided again as it is now, on both maintained exact routes, and taken
    only with the side, relation and id its report decided, from a report whose settings
    are its stored regularization's (review C of #511, C1). A report's blob ids for its
    views (`outputs.<name>.git_blob`) are its provenance and are compared with nothing
    (OR-16, OR-18); `--verify-atlas` decides every drawn view again, its identity and
    shades measured again."""
    found: dict[int, tuple[Path, str, dict[str, Any]]] = {}
    for run_dir in run_dirs:
        run_id = f"{axis.EVAND_GENERATOR}-{Path(run_dir).name}"
        for path in sorted(Path(run_dir).glob("n-*/report.json")):
            report = read_json(path)
            found[int(report["n"])] = (path.parent, run_id, report)
    admitted, refused = decided_candidates(found)
    used = {item.run["id"] for item in admitted}
    runs = [
        run_block(Path(run_dir), run_id)
        for run_dir in run_dirs
        if (run_id := f"{axis.EVAND_GENERATOR}-{Path(run_dir).name}") in used
    ]
    return admitted, runs, refused


def decided_candidates(
    found: Mapping[int, tuple[Path, str, dict[str, Any]]],
) -> tuple[list[Admitted], dict[str, str]]:
    """Each found report's admitted view, decided again as it is now (`layer_refusal`),
    and, with the reason, each one refused, which is never admitted."""
    admitted: list[Admitted] = []
    refused: dict[str, str] = {}
    for n, (directory, run_id, report) in sorted(found.items()):
        chosen = layer_candidate(report, "admitted")
        if chosen is None:
            continue
        text, refusal = layer_refusal(directory, report, chosen)
        if text is None:
            refused[str(n)] = refusal or "refused"
            continue
        admitted.append(evand_admitted(report, directory, run_id, text=text))
    return admitted, refused


def write_preview(run_dirs: Sequence[Path], root: Path, select: str) -> dict[str, Any]:
    """Write the selected views of finished runs into a scratch tree's layer, as
    `admit_views` writes admitted ones, for a preview of what the policy would draw."""
    if root.resolve() == REPO.resolve():
        raise EvandRunError("only the admitted selection may write into this checkout")
    found: dict[int, tuple[Path, str, dict[str, Any]]] = {}
    for run_dir in run_dirs:
        run_id = f"{axis.EVAND_GENERATOR}-{Path(run_dir).name}"
        for path in sorted(Path(run_dir).glob("n-*/report.json")):
            report = read_json(path)
            chosen = layer_candidate(report, select)
            if chosen is None:
                continue
            # A preview draws what row 10 would have drawn: the record is the run's.
            report = {**report, "decision": {**report["decision"], "decision": "admit"}}
            found[int(report["n"])] = (path.parent, run_id, report)
    admitted, refused = decided_candidates(found)
    runs = [
        run_block(Path(run_dir), f"{axis.EVAND_GENERATOR}-{Path(run_dir).name}")
        for run_dir in run_dirs
    ]
    summary = admit_views(
        admitted, root, generators={axis.EVAND_GENERATOR: evand_generator_block()}, runs=runs
    )
    return {"select": select, **summary, "refused": refused}


def layer_layout(root: Path) -> Any:
    """The layer under `root` as the axis tool's check reads it, with the tree's case
    records where it keeps them, so the drawn views' sides are held to `U`."""
    root = root.resolve()
    frontier = root / "packing/frontier"
    return axis.AtlasLayout(
        root / "packing",
        root,
        root / "packing/atlas/known-best/manifest.json",
        root / LAYER_DIR,
        root / "packing/witnesses",
        frontier if frontier.is_dir() else None,
    )


def restate_provenance(root: Path, *, write: bool = True) -> list[int]:
    """Restate each drawn view's `regularization.provenance` by `packing_credit`, in its
    index entry and in its view's certificate together, and return the counts it changed.

    The recorded provenance is the case record's credit when the view was made, so the
    rule is applied to it and to the source witness's key, not to the record as it stands
    now. The view's squares are unchanged and only its certificate is rewritten, so its
    digest is recomputed; `--verify-atlas` decides it again. The run directories are not
    needed, which is why this exists: the views drawn before the rule credited the
    packing at `U` where the view is at the witness's side (#548 review B1).
    """
    root = root.resolve()
    layout = layer_layout(root)
    index = read_json(layout.index)
    changed: list[int] = []
    for entry in index["entries"]:
        record = entry.get("regularization") or {}
        if entry.get("status") != "regularized" or "provenance" not in record:
            continue
        witness = load_yaml((root / entry["source"]["witness"]).read_text(encoding="utf-8"))
        key = (witness["witness"].get("source") or {}).get("key")
        credit = packing_credit(record["provenance"], key, entry["side"]["relation"])
        if credit == record["provenance"]:
            continue
        changed.append(int(entry["n"]))
        if not write:
            continue
        path = root / entry["view"]["path"]
        document = load_yaml(gzip.decompress(path.read_bytes()).decode("utf-8"))
        view = document["witness"]
        view["certificate"]["regularization"]["provenance"] = credit
        text = witness_document(view, schema=document["softschema"]["schema"])
        with atomic_output_file(path) as temporary:
            temporary.write_bytes(gzip.compress(text.encode("utf-8"), compresslevel=9, mtime=0))
        record["provenance"] = credit
        entry["view"]["sha256"] = sha256_of(text.encode("utf-8"))
    if write and changed:
        with atomic_output_file(layout.index) as temporary:
            temporary.write_text(axis.index_text(index), encoding="utf-8")
    return changed


def write_layer_with_grid(
    run_dirs: Sequence[Path],
    root: Path,
    *,
    grid_run: Path,
    grid_counts: Collection[int],
    exclude: Collection[int] = (),
) -> dict[str, Any]:
    """Admit finished runs' views and, at `grid_counts`, the grid-slack run's view instead
    (`devtools.regularize_grid_slack.admitted_views`), in one write of the layer.

    Every view is decided again as it is now before it is written, on both exact routes
    (`decided_refusal`), with its side and id held to its report's: the driver's by
    `layer_refusal`, the grid run's by `regularize_grid_slack.admitted`, which refuses
    the whole write when one is not the view its report decided (#548 review C, C1)."""
    grid = importlib.import_module("devtools.regularize_grid_slack")
    admitted, runs, refused = evand_candidates(run_dirs)
    chosen = set(grid_counts)
    views, grid_run_block, grid_generator = grid.admitted_views(grid_run, sorted(chosen))
    candidates = [item for item in admitted if item.n not in chosen] + list(views)
    used = {item.run["id"] for item in candidates}
    summary = admit_views(
        candidates,
        root,
        generators={
            axis.EVAND_GENERATOR: evand_generator_block(),
            grid.GENERATOR: grid_generator,
        },
        runs=[run for run in [*runs, grid_run_block] if run["id"] in used],
        exclude=exclude,
    )
    refused = {n: why for n, why in refused.items() if int(n) not in chosen}
    return {"select": "admitted", "grid_counts": sorted(chosen), **summary, "refused": refused}


def write_layer(
    run_dirs: Sequence[Path], root: Path, select: str, exclude: Collection[int] = ()
) -> dict[str, Any]:
    """Write finished runs' admitted views into the layer under `root` (`admit_views`),
    or with `preview`, every drawable view into a scratch tree (`write_preview`). Each
    view is decided again as it is now first (`layer_refusal`); a refused one is never
    written, and the summary's `refused` names it with the reason."""
    if select not in SELECTIONS:
        raise EvandRunError(f"unknown selection {select!r}")
    if select != "admitted":
        return write_preview(run_dirs, root, select)
    admitted, runs, refused = evand_candidates(run_dirs)
    summary = admit_views(
        admitted,
        root,
        generators={axis.EVAND_GENERATOR: evand_generator_block()},
        runs=runs,
        exclude=exclude,
    )
    return {"select": select, **summary, "refused": refused}


def record_rungs(run_dirs: Sequence[Path], root: Path) -> dict[str, Any]:
    """Record in the layer's index the retry rungs each drawn view's solve climbed
    (`run.rungs`), from finished runs' reports, for a view admitted without them, and the
    run whose report supplied them (`run.rungs_from`).

    `evand_admitted` records them from 13 October 2026. Before the retry ladder of 12
    October a report kept only the arguments of the one retry it made, which the index
    keeps as `retried_with`; between the two, the reports kept the rungs and the index
    nothing. An entry that already records either is left as it is and listed
    (`already_recorded`): what admission or an earlier pass recorded is never written over.
    A report answers for a drawn view only when its admitted view, recorded under the
    entry's own run, renders to the drawn view byte for byte: the same solve,
    regularization and decision. The comparison is of the text itself, the stored view
    decompressed against the one rendered here, not of a digest (OR-16): the layer's check
    (`check_atlas`) already holds the stored view to its index entry. Then its rungs are
    written, so a run of the same counts again records the rungs of a solve that makes the
    very view drawn; a view that differs records nothing and is listed. A supplying run
    other than the entry's own enters the index's `runs` from its receipt, as an admitted
    one does, so `rungs_from` names a run the index records.
    """
    root = root.resolve()
    index_path = root / LAYER_INDEX_PATH
    index = read_json(index_path)
    entries = {int(entry["n"]): entry for entry in index["entries"]}
    layout = layer_layout(root)
    summary: dict[str, list[int]] = {
        "recorded": [],
        "already_recorded": [],
        "differs": [],
        "not_drawn": [],
    }
    supplying: dict[str, Path] = {}
    for run_dir in run_dirs:
        run_id = f"{axis.EVAND_GENERATOR}-{Path(run_dir).name}"
        for path in sorted(Path(run_dir).glob("n-*/report.json")):
            report = read_json(path)
            n = int(report["n"])
            entry = entries.get(n) or {}
            solved = report.get("solve") or {}
            if (
                entry.get("status") != "regularized"
                or entry.get("generator") != axis.EVAND_GENERATOR
                or layer_candidate(report, "admitted") is None
                or "rungs" not in solved
            ):
                summary["not_drawn"].append(n)
                continue
            run = entry["run"]
            if "rungs" in run or "retried_with" in run:
                summary["already_recorded"].append(n)
                continue
            admitted = evand_admitted(report, path.parent, str(run["id"]))
            text = witness_document(layer_view(admitted), schema=layout.schema_reference())
            stored = gzip.decompress((root / entry["view"]["path"]).read_bytes())
            if stored.decode("utf-8") != text:
                summary["differs"].append(n)
                continue
            run["rungs"] = [str(rung) for rung in solved.get("rungs") or []]
            run["rungs_from"] = run_id
            supplying[run_id] = Path(run_dir)
            summary["recorded"].append(n)
    known = {str(block["id"]) for block in index.get("runs") or []}
    index["runs"] = [
        *(index.get("runs") or []),
        *(
            run_block(run_dir, run_id)
            for run_id, run_dir in supplying.items()
            if run_id not in known
        ),
    ]
    with atomic_output_file(index_path) as temporary:
        temporary.write_text(axis.index_text(index), encoding="utf-8")
    return {key: sorted(set(counts)) for key, counts in summary.items()}


def rename_run(root: Path, old: str, new: str, note: str) -> dict[str, Any]:
    """Give a run the layer's index records only as a supplier of rungs another id, and
    say why on its block (`id_note`).

    A run's receipt records no id: `layer` and `rungs` name it by the driver's convention,
    `evand-regularize-<run directory>`, so two runs in directories of the same name get
    the same id. The fresh run of 13 October 2026 that supplied the rungs of the fifteen
    views drawn from the run on jlevy/squares#518's witnesses was named
    `evand-regularize-adopt518-v2` that way, the id the convention also gives the 12
    October run of 37 counts in `runs/adopt518-v2`. This renames the block and every
    entry's `run.rungs_from` that names it, and records `note` on the block, so the id
    says it was assigned afterwards. A run an entry draws from (`run.id`) is refused: its
    id is in the drawn view's text, which the layer's check holds to the index. So is a
    new id the index already records, an old one it does not, and an empty note."""
    root = root.resolve()
    index_path = root / LAYER_INDEX_PATH
    index = read_json(index_path)
    blocks = [block for block in index.get("runs") or [] if str(block["id"]) == old]
    if len(blocks) != 1:
        raise EvandRunError(f"the index records {len(blocks)} runs named {old!r}")
    if any(str(block["id"]) == new for block in index.get("runs") or []):
        raise EvandRunError(f"the index already records a run named {new!r}")
    if not note.strip():
        raise EvandRunError("a renamed run says why its id was assigned (--note)")
    drawing = sorted(
        int(entry["n"])
        for entry in index["entries"]
        if str((entry.get("run") or {}).get("id")) == old
    )
    if drawing:
        raise EvandRunError(
            f"entries {drawing} draw from {old!r}, whose id their views record; not renamed"
        )
    renamed: list[int] = []
    for entry in index["entries"]:
        run = entry.get("run") or {}
        if str(run.get("rungs_from")) == old:
            run["rungs_from"] = new
            renamed.append(int(entry["n"]))
    block = blocks[0]
    rest = {key: value for key, value in block.items() if key not in {"id", "id_note"}}
    block.clear()
    block.update({"id": new, "id_note": note.strip(), **rest})
    with atomic_output_file(index_path) as temporary:
        temporary.write_text(axis.index_text(index), encoding="utf-8")
    return {"renamed": old, "to": new, "rungs_from": sorted(renamed)}


def write_receipt(
    run_dir: Path,
    reports: Mapping[int, Mapping[str, Any]],
    options: Options,
    workers: int,
    cost: Mapping[str, Any],
) -> dict[str, Any]:
    path = run_dir / "receipt.json"
    previous = read_json(path) if path.is_file() else None
    rows = {int(row["n"]): row for row in (previous or {}).get("counts", [])}
    rows.update({n: receipt_row(report) for n, report in reports.items()})
    ordered = [rows[n] for n in sorted(rows)]
    parameters = {
        **{key: value for key, value in asdict(options).items() if key != "run_dir"},
        "style": STYLE,
        "dps": 80,
        "eps": "1e-20",
        "workers": workers,
        "counts": sorted(reports),
    }
    history = list((previous or {}).get("previous_runs", []))
    if previous is not None:
        history.append({"parameters": previous.get("parameters"), "cost": previous.get("cost")})
    # A row kept from an earlier run keeps the outputs that run named by digest; this
    # run's counts are named afresh (review B of #511, B6). Each row carries its own
    # `parameters`; the receipt's are this run's.
    kept = {
        key: value
        for key, value in ((previous or {}).get("solve_outputs") or {}).items()
        if int(key) in rows and int(key) not in reports
    }
    named = {**kept, **solve_digests(run_dir, sorted(reports))}
    receipt = {
        "format": RECEIPT_FORMAT,
        "generated_by": GENERATED_BY,
        "policy": POLICY,
        "finished": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        # The directory the run spent `cost` in, whose name is its run id's: a copy
        # `reclassify` decides again names it as the run it was copied from.
        "run_directory": run_dir.name,
        "generator": run_generator(ordered),
        "parameters": parameters,
        "counts": ordered,
        **receipt_lists(ordered),
        "solve_outputs": {key: named[key] for key in sorted(named, key=int)},
        "cost": dict(cost),
        "previous_runs": history,
    }
    write_json(path, receipt)
    return receipt


def solve_digests(run_dir: Path, counts: Sequence[int]) -> dict[str, dict[str, str]]:
    """The retained solve outputs by digest, as policy section 9's question 8 asks, and
    the exact solve's input (obligation 6)."""
    names = (
        "input.txt",
        "solve/witness.exact.txt",
        "solve/witness.contacts.json",
        "regularize.cert",
    )
    found: dict[str, dict[str, str]] = {}
    for n in counts:
        directory = count_dir(run_dir, n)
        present = {name: directory / name for name in names if (directory / name).is_file()}
        if present:
            found[str(n)] = {
                name: sha256_of(path.read_bytes()) for name, path in present.items()
            }
    return found


# --------------------------------------------------------------------------------------
# The report table
# --------------------------------------------------------------------------------------


def _cell(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, list):
        return "/".join(_cell(item) for item in value)
    return str(value)


def solve_cell(row: Mapping[str, Any]) -> str | None:
    """A count's solve status, with the rungs that reached it and a relaxed gate."""
    status = row.get("solve_status")
    if status is None:
        return None
    rungs = row.get("solve_rungs") or []
    relaxed = row.get("solve_gate") == "relaxed"
    return (
        f"{status}"
        + (f" [{'+'.join(rungs)}]" if rungs else "")
        + (" (relaxed gate)" if relaxed else "")
    )


def report_table(receipt: Mapping[str, Any]) -> str:
    """A compact table of a receipt's counts."""
    header = (
        "n", "kind", "solve", "lvl", "mv", "groups", "sym", "view", "1:1", "max_move",
        "house before>after", "row", "decision", "solve s", "reg s",
    )  # fmt: skip
    lines = ["  ".join(header)]
    for row in receipt["counts"]:
        seconds = row.get("seconds") or {}
        house = row.get("house") or [None, None]
        cells = (
            row["n"],
            row.get("kind"),
            solve_cell(row),
            row.get("level"),
            row.get("moved"),
            f"{_cell(row['groups'][0])}>{_cell(row['groups'][1])}"
            if row.get("groups")
            else None,
            row.get("symmetry"),
            row.get("view"),
            row.get("one_to_one"),
            row.get("max_move"),
            f"{_cell(house[0])}>{_cell(house[1])}",
            row.get("row"),
            row.get("decision"),
            seconds.get("solve"),
            seconds.get("regularize"),
        )
        lines.append("  ".join(_cell(cell) for cell in cells))
    cost = receipt.get("cost") or {}
    lines.append(
        f"cost: {cost.get('cpu_seconds')} CPU s, {cost.get('wall_seconds')} wall s, "
        f"{cost.get('workers')} workers; candidates {receipt.get('candidates')}; "
        f"review {receipt.get('review_queue')}"
    )
    return "\n".join(lines)


# --------------------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------------------


def parse_counts(values: Sequence[str]) -> list[int]:
    """Counts as integers or inclusive ranges `a-b`, in the order given, without repeats."""
    counts: list[int] = []
    for value in values:
        low, _, high = value.partition("-")
        span = range(int(low), int(high or low) + 1)
        counts.extend(n for n in span if n not in counts)
    for n in counts:
        if not witness_path(n).is_file():
            raise EvandRunError(f"no known-best witness for n = {n}")
    return counts


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = command.add_subparsers(dest="command", required=True)
    run_command = sub.add_parser("run", help="run the automated pass over counts")
    run_command.add_argument("--run-dir", type=Path, required=True)
    run_command.add_argument("--n", nargs="+", required=True, help="counts or ranges a-b")
    run_command.add_argument("--workers", type=int, default=None)
    run_command.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    run_command.add_argument("--regularize-timeout", type=float, default=DEFAULT_TIMEOUT)
    run_command.add_argument(
        "--variant",
        choices=VARIANTS,
        default="conservative",
        help="upstream's angle policy; the policy runs only conservative (section 9, q1)",
    )
    run_command.add_argument("--orient", default="0", help="0 (the source's), best, or 1..7")
    run_command.add_argument(
        "--from-stage",
        choices=STAGES,
        default="input",
        help="reuse the outputs, settings and source of the stages before this one",
    )
    run_command.add_argument("--same-mode", choices=("relax", "refuse"), default="relax")
    run_command.add_argument(
        "--frame",
        choices=FRAMES,
        default="kkt",
        help="regularize from the solve's KKT point, or from the witness's pose at s_W",
    )
    input_command = sub.add_parser("input", help="write one witness as upstream's input")
    input_command.add_argument("--n", type=int, required=True)
    input_command.add_argument("--output", type=Path, required=True)
    reclassify_command = sub.add_parser(
        "reclassify", help="decide a finished run again from its reports"
    )
    reclassify_command.add_argument("--run-dir", type=Path, required=True)
    reclassify_command.add_argument("--n", nargs="+", default=None, help="counts or a-b")
    reclassify_command.add_argument(
        "--refresh-bounds",
        action="store_true",
        help="read each report's verified upper bound again from the case record first",
    )
    layer_command = sub.add_parser(
        "layer", help="write finished runs' selected views into a layer under a tree"
    )
    layer_command.add_argument("--run-dir", type=Path, nargs="+", required=True)
    layer_command.add_argument("--repo-root", type=Path, required=True)
    layer_command.add_argument("--select", choices=SELECTIONS, default="admitted")
    layer_command.add_argument(
        "--exclude",
        nargs="+",
        default=[],
        help="counts or a-b left out whatever was decided (their witnesses are changing)",
    )
    layer_command.add_argument(
        "--grid-run",
        type=Path,
        default=None,
        help="a finished devtools.regularize_grid_slack run whose views to admit as well",
    )
    layer_command.add_argument(
        "--grid-counts",
        nargs="+",
        default=[],
        help="the counts at which to draw the grid-slack run's view rather than this one's",
    )
    rungs_command = sub.add_parser(
        "rungs", help="record the retry rungs of drawn views that finished runs reproduce"
    )
    rungs_command.add_argument("--run-dir", type=Path, nargs="+", required=True)
    rungs_command.add_argument("--repo-root", type=Path, required=True)
    rename_command = sub.add_parser(
        "rename-run", help="give a run that only supplied rungs another id, saying why"
    )
    rename_command.add_argument("--from", dest="old", required=True)
    rename_command.add_argument("--to", dest="new", required=True)
    rename_command.add_argument("--note", required=True, help="why the id was assigned")
    rename_command.add_argument("--repo-root", type=Path, required=True)
    provenance_command = sub.add_parser(
        "provenance", help="restate the drawn views' credit by packing_credit"
    )
    provenance_command.add_argument("--repo-root", type=Path, required=True)
    provenance_command.add_argument("--check", action="store_true", help="write nothing")
    report_command = sub.add_parser("report", help="print a run's receipt as a table")
    report_command.add_argument("--run-dir", type=Path, required=True)
    report_command.add_argument("--json", action="store_true")
    return command


def layer_command(arguments: argparse.Namespace) -> dict[str, Any]:
    """Run a command that writes the layer's index (`layer`, `rungs`, `rename-run`) and
    return its summary; `main` then runs the layer's check."""
    if arguments.command == "rungs":
        return record_rungs(arguments.run_dir, arguments.repo_root)
    if arguments.command == "rename-run":
        return rename_run(arguments.repo_root, arguments.old, arguments.new, arguments.note)
    exclude = parse_counts(arguments.exclude)
    if arguments.grid_run is None:
        return write_layer(arguments.run_dir, arguments.repo_root, arguments.select, exclude)
    return write_layer_with_grid(
        arguments.run_dir,
        arguments.repo_root,
        grid_run=arguments.grid_run,
        grid_counts=parse_counts(arguments.grid_counts),
        exclude=exclude,
    )


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    if arguments.command == "input":
        witness = load_witness(witness_path(arguments.n), fallback_schema=WITNESS_SCHEMA)
        write_text(arguments.output, input_text(witness))
        return 0
    if arguments.command == "reclassify":
        counts = None if arguments.n is None else parse_counts(arguments.n)
        receipt = reclassify(arguments.run_dir, counts, refresh_bounds=arguments.refresh_bounds)
        print(report_table(receipt))
        stale = receipt["reclassified"]["stale_bounds"]
        if stale:
            print(
                f"decided on the U each report stored; the case record has moved U since "
                f"at {stale}: run those counts again (--from-stage import) to decide them "
                "on today's U"
            )
        unsettled = receipt["reclassified"]["stale_settings"]
        if unsettled:
            print(
                f"not decided again, sent to review: at {unsettled} the report's settings "
                "are not the ones its stored regularization ran with; run those counts "
                "again (--from-stage import), asking for the settings they ran with"
            )
        return 0
    if arguments.command in {"layer", "rungs", "rename-run"}:
        print(json.dumps(layer_command(arguments)))
        problems = axis.check_atlas(layer_layout(arguments.repo_root))
        for problem in problems:
            print(problem)
        return 1 if problems else 0
    if arguments.command == "provenance":
        changed = restate_provenance(arguments.repo_root, write=not arguments.check)
        verb = "would restate" if arguments.check else "restated"
        print(f"{verb} the provenance of {len(changed)} drawn view(s): {changed}")
        return 1 if arguments.check and changed else 0
    if arguments.command == "report":
        receipt = read_json(arguments.run_dir / "receipt.json")
        print(json.dumps(receipt, indent=1) if arguments.json else report_table(receipt))
        return 0
    counts = parse_counts(arguments.n)
    workers = (
        arguments.workers
        if arguments.workers is not None
        else min(DEFAULT_WORKER_CAP, worker_count(len(counts)))
    )
    options = Options(
        run_dir=arguments.run_dir,
        timeout=arguments.timeout,
        regularize_timeout=arguments.regularize_timeout,
        variant=arguments.variant,
        orient=arguments.orient,
        from_stage=arguments.from_stage,
        same_mode=arguments.same_mode,
        frame=arguments.frame,
    )
    receipt = run(counts, options, max(1, workers))
    failed = [row["n"] for row in receipt["counts"] if row["status"] == "error"]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
