"""Decide direction r = 0 of the certificate completely: F_0(c) >= 1 on the quadrant.

Usage: dm_axis.py CERTIFICATE.json.gz OUT.json [CENSUS_CAPTURE.jsonl.gz]

At r = 0 the core is axis-parallel, and F_0(x, y) = sum_k rho_k o_k(x) p_k(y) with
o_k(x) = |[x - h, x + h] ∩ [x1_k, x2_k]|, h = B/2, and p_k the same in y. Each o_k is
affine between consecutive points of {x1_k ± h, x2_k ± h}, so on each cell of the grid
of all such points in [L/2, U_0] (with both ends), F_0 is bilinear and its least value
on the cell is at a corner. The least value of F_0 on the quadrant [L/2, U_0]^2,
U_0 = L - rho(0) = L - 1/2 (format M's per-bin domain), is therefore its least value
on the grid's vertices, and by the quarter turn (lemma C1) that is its least value on
the whole domain.

The event sets are built in exact rationals. Every vertex is then evaluated in binary64
as one matrix product, F = (O_x diag(rho)) O_y^T, and the least value is reduced by a
rigorous bound on the rounding error, derived in `main`'s comments: each input is
correctly rounded (|error| <= e_in, measured exactly), each overlap is within
e_o = 4 e_in + 3 u V of the exact one (V bounds every magnitude, u = 2^-53), each term
rho o p is then within rho (4u + 3 e_o) of the exact term, and a sum of K nonnegative
products in any order and with or without fused multiply-adds is within gamma_K times
the sum of their magnitudes (Higham, Accuracy and Stability, 2nd ed., section 3.1),
which is at most M plus the terms' error. The direction is decided when the least
computed value minus that bound is at least 1. The vertices of least computed value are
then evaluated exactly with dmlib's clipping evaluator. With the census capture given,
its r = 0 row's least vertex and certified bound are compared with these.

This decides nothing for r >= 1, and shares no code with the crate's axis sweep.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dmlib  # noqa: E402

U = Fraction(1, 2**53)


def events(images: list[dmlib.Image], lower: Fraction, upper: Fraction, h: Fraction, axis: str) -> list[Fraction]:
    found = {lower, upper}
    for image in images:
        edges = (image.x1, image.x2) if axis == "x" else (image.y1, image.y2)
        for edge in edges:
            for point in (edge - h, edge + h):
                if lower <= point <= upper:
                    found.add(point)
    return sorted(found)


def main() -> None:
    cert_path, out_path = Path(sys.argv[1]), Path(sys.argv[2])
    census_path = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    block = 512
    started = time.process_time()
    cert = dmlib.certificate(dmlib.read_gzip_json(cert_path).data)
    images = dmlib.expand(cert)
    h = cert.core / 2
    lower = cert.side / 2
    _, upper = dmlib.domain(cert, 0)
    xs = events(images, lower, upper, h, "x")
    ys = events(images, lower, upper, h, "y")
    crate_like_counts = (len(xs), len(ys))
    # Hosono's domain end at r = 0, in these coordinates: lambda (L0 - 1/2). Adding it to
    # both event sets refines the grid without changing the least value over the
    # quadrant, and makes [L/2, old_end]^2 a union of cells, so the least value over it is
    # the least over its vertices: the region the base certificate's own run covered.
    lam = Fraction(1993, 1990)
    old_end = lam * (Fraction(199, 20) - Fraction(1, 2))
    xs = sorted({*xs, old_end})
    ys = sorted({*ys, old_end})
    old_x = sum(1 for v in xs if v <= old_end)
    old_y = sum(1 for v in ys if v <= old_end)
    # Images that can meet a core centred in the quadrant.
    active = [
        i
        for i in images
        if i.x2 > lower - h and i.x1 < upper + h and i.y2 > lower - h and i.y1 < upper + h
    ]
    # The exact rounding error of every binary64 input, and the largest magnitude.
    inputs = [*xs, *ys, h]
    for i in active:
        inputs += [i.x1, i.x2, i.y1, i.y2]
    e_in = max(abs(Fraction(float(v)) - v) for v in inputs)
    big = max(abs(v) for v in inputs) + h + 1
    e_o = 4 * e_in + 3 * U * big
    density_sum = sum((i.density for i in active), Fraction(0))
    k = len(active)
    gamma = k * U / (1 - k * U)
    # Every capture is at most the total mass, so the sum of the computed products is at
    # most M + density_sum * (per-term error); per-term error <= rho (4u + 3 e_o).
    per_term = 4 * U + 3 * e_o
    bound = density_sum * per_term + gamma * (cert.mass + density_sum * per_term)

    hf = float(h)
    xf = np.array([float(v) for v in xs])
    yf = np.array([float(v) for v in ys])
    x1 = np.array([float(i.x1) for i in active])
    x2 = np.array([float(i.x2) for i in active])
    y1 = np.array([float(i.y1) for i in active])
    y2 = np.array([float(i.y2) for i in active])
    rho = np.array([float(i.density) for i in active])

    def overlaps(points: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        top = np.minimum(points[:, None] + hf, b[None, :])
        bottom = np.maximum(points[:, None] - hf, a[None, :])
        return np.maximum(top - bottom, 0.0)

    oy = overlaps(yf, y1, y2)  # (ny, k)
    least = np.inf
    least_at = (-1, -1)
    least_old = np.inf
    least_old_at = (-1, -1)
    lowest: list[tuple[float, int, int]] = []
    for start in range(0, len(xf), block):
        ox = overlaps(xf[start : start + block], x1, x2)  # (b, k)
        values = (ox * rho[None, :]) @ oy.T  # (b, ny)
        flat = np.argpartition(values, 8, axis=None)[:8]
        for f in flat:
            i, j = divmod(int(f), values.shape[1])
            lowest.append((float(values[i, j]), start + i, j))
        index = int(np.argmin(values))
        i, j = divmod(index, values.shape[1])
        if values[i, j] < least:
            least = float(values[i, j])
            least_at = (start + i, j)
        rows_old = max(0, min(block, old_x - start))
        if rows_old:
            part = values[:rows_old, :old_y]
            index = int(np.argmin(part))
            i, j = divmod(index, part.shape[1])
            if part[i, j] < least_old:
                least_old = float(part[i, j])
                least_old_at = (start + i, j)
    lowest.sort()
    lowest = lowest[:12]

    exact = dmlib.ExactMeasure.of(cert, images)
    checked = []
    for value, i, j in lowest:
        cap, _ = dmlib.capture_exact(exact, 0, dmlib.q(xs[i]), dmlib.q(ys[j]))
        checked.append(
            {
                "x": str(xs[i]),
                "y": str(ys[j]),
                "binary64": value,
                "exact": dmlib.short(cap, 17),
                "exact_minus_binary64": float(dmlib.fraction_of(cap) - Fraction(value)),
                "within_bound": abs(dmlib.fraction_of(cap) - Fraction(value)) <= bound,
            }
        )
    i, j = least_at
    decided = Fraction(least) - bound >= 1
    oi, oj = least_old_at
    old_cap, _ = dmlib.capture_exact(exact, 0, dmlib.q(xs[oi]), dmlib.q(ys[oj]))
    report = {
        "program": "dm_axis.py",
        "program_sha256": dmlib.sha256_file(Path(__file__)),
        "dmlib_sha256": dmlib.sha256_file(Path(dmlib.__file__)),
        "certificate_file_sha256": dmlib.sha256_file(cert_path),
        "r": 0,
        "quadrant": [str(lower), str(upper)],
        "x_events_without_old_end": crate_like_counts[0],
        "y_events_without_old_end": crate_like_counts[1],
        "x_events": len(xs),
        "y_events": len(ys),
        "vertices": len(xs) * len(ys),
        "active_images": k,
        "max_input_rounding_error": float(e_in),
        "overlap_error_bound": float(e_o),
        "sum_of_active_densities": float(density_sum),
        "rigorous_error_bound": float(bound),
        "least_binary64": least,
        "least_at": [str(xs[i]), str(ys[j])],
        "least_minus_bound": float(Fraction(least) - bound),
        "decided_at_least_1": decided,
        "lowest_vertices_exact": checked,
        "hosono_domain_end_in_these_coordinates": str(old_end),
        "least_vertex_in_the_strip_the_dilation_adds": Fraction(xs[i]) > old_end or Fraction(ys[j]) > old_end,
        "least_on_hosono_domain_binary64": least_old,
        "least_on_hosono_domain_at": [str(xs[oi]), str(ys[oj])],
        "least_on_hosono_domain_exact": dmlib.short(old_cap, 17),
    }
    if census_path is not None:
        import gzip

        with gzip.open(census_path, "rt") as stream:
            row = next(r for r in map(json.loads, stream) if r.get("r") == 0)
        crate_at = sorted(Fraction(v) for v in row["argmin"])
        least_cap, _ = dmlib.capture_exact(exact, 0, dmlib.q(xs[i]), dmlib.q(ys[j]))
        crate_bound = Fraction(row["min_certified_lower_bound"])
        report["census_r0"] = {
            "census_capture_sha256": dmlib.sha256_file(census_path),
            "crate_x_events": row.get("x_events"),
            "crate_y_events": row.get("y_events"),
            "crate_vertices": row.get("vertices"),
            "event_counts_equal": (row.get("x_events"), row.get("y_events")) == crate_like_counts,
            "crate_argmin": row["argmin"],
            "same_vertex_up_to_the_diagonal": crate_at == sorted([xs[i], ys[j]]),
            "crate_certified_bound": float(crate_bound),
            "exact_capture_there": dmlib.short(least_cap, 17),
            "exact_minus_crate_bound": float(dmlib.fraction_of(least_cap) - crate_bound),
        }
    report["cpu_seconds"] = round(time.process_time() - started, 2)
    out_path.write_text(dmlib.dumps(report) + "\n")
    print(json.dumps({key: report[key] for key in ("x_events", "y_events", "vertices", "active_images", "rigorous_error_bound", "least_binary64", "least_at", "decided_at_least_1", "cpu_seconds")}, indent=1))


if __name__ == "__main__":
    main()
