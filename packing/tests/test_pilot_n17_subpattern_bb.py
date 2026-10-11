"""Fast checks of the P2 branch-and-bound pilot: rounding, the relaxation and verdicts."""

from __future__ import annotations

import math
import random
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath
import pytest

from devtools import pilot_n17_subpattern_bb as bb
from devtools import verify_n17_bb_certificate as verifier

Q = Fraction


def rectangle(x0: str, x1: str, y0: str, y1: str) -> tuple[tuple[Fraction, Fraction], ...]:
    a, b, c, d = Q(x0), Q(x1), Q(y0), Q(y1)
    return ((a, c), (b, c), (b, d), (a, d))


@pytest.fixture(autouse=True)
def _restore_mpmath_precision() -> Any:
    """Several tests raise `mpmath.mp.prec`; put it back so later modules on the worker
    see the default. Leaving it raised made `test_promote_krawczyk`'s enclosure check
    compare at about 30 digits and fail in suite C on PR 307 (run 37034789370)."""
    saved = mpmath.mp.prec
    yield
    mpmath.mp.prec = saved


def contains(interval: bb.Iv, value: Fraction | float) -> bool:
    return Q(interval[0]) <= Q(value) <= Q(interval[1])


def separated(pose_i: tuple[float, float, float], pose_j: tuple[float, float, float]) -> float:
    """The separating-axis gap of two unit squares (positive: interiors disjoint), mpmath."""
    mpmath.mp.prec = 100
    (xi, yi, ti), (xj, yj, tj) = pose_i, pose_j
    dx, dy = mpmath.mpf(xj) - mpmath.mpf(xi), mpmath.mpf(yj) - mpmath.mpf(yi)
    alpha = mpmath.mpf(tj) - mpmath.mpf(ti)
    g = mpmath.mpf(1) / 2 + (abs(mpmath.cos(alpha)) + abs(mpmath.sin(alpha))) / 2
    gaps = []
    for theta in (ti, tj):
        for k in range(4):
            phi = mpmath.mpf(theta) + k * mpmath.pi / 2
            gaps.append(mpmath.cos(phi) * dx + mpmath.sin(phi) * dy - g)
    return float(max(gaps))


def test_rounding_floor_encloses_exact_results() -> None:
    rng = random.Random(7)
    for _ in range(2000):
        a = sorted((rng.uniform(-3, 3), rng.uniform(-3, 3)))
        b = sorted((rng.uniform(-3, 3), rng.uniform(-3, 3)))
        ia, ib = (a[0], a[1]), (b[0], b[1])
        for x in (a[0], a[1]):
            for y in (b[0], b[1]):
                assert contains(bb.iadd(ia, ib), Q(x) + Q(y))
                assert contains(bb.isub(ia, ib), Q(x) - Q(y))
                assert contains(bb.imul(ia, ib), Q(x) * Q(y))
    for q in (Q(1169, 250), Q(1, 3), Q(-2, 7), Q(10**20 + 1, 10**20)):
        assert Q(bb.lower_float(q)) <= q <= Q(bb.upper_float(q))


def test_trig_enclosures_and_constants() -> None:
    mpmath.mp.prec = 200
    rng = random.Random(11)
    points = [0.0, 0.4, math.pi / 2, math.pi, -math.pi / 4] + [
        rng.uniform(-4, 8) for _ in range(300)
    ]
    for theta in points:
        c, s = bb.cos_sin(theta)
        assert c[0] <= mpmath.cos(mpmath.mpf(theta)) <= c[1]
        assert s[0] <= mpmath.sin(mpmath.mpf(theta)) <= s[1]
        assert c[1] - c[0] < 1e-15
        assert s[1] - s[0] < 1e-15
    for k, value in bb.HALF_PI_MULTIPLES.items():
        assert value[0] <= k * mpmath.pi / 2 <= value[1]
    root = bb.Solver(
        bb.Pattern(("a",), (rectangle("2", "2.1", "2", "2.1"),), bb.cover.U), bb.Settings()
    )
    lo, hi = root.root().angles[0]
    assert mpmath.mpf(hi) - mpmath.mpf(lo) >= mpmath.pi / 2


def test_half_width_and_gap_bounds_are_lower_bounds() -> None:
    mpmath.mp.prec = 120
    rng = random.Random(5)

    def h(value: float) -> float:
        return float((abs(mpmath.cos(value)) + abs(mpmath.sin(value))) / 2)

    for _ in range(400):
        lo = rng.uniform(-1, 2)
        hi = lo + rng.choice((1e-3, 0.05, 0.3, 1.0)) * rng.random()
        bound = bb.h_lower(lo, hi)
        samples = [lo, hi] + [rng.uniform(lo, hi) for _ in range(20)]
        assert all(bound <= h(t) + 1e-15 for t in samples)
        other = (rng.uniform(-1, 2), 0.0)
        other = (other[0], other[0] + 0.2 * rng.random())
        gap = bb.gap_lower((lo, hi), other)
        for _ in range(20):
            ti, tj = rng.uniform(lo, hi), rng.uniform(*other)
            assert gap <= 0.5 + h(tj - ti) + 1e-15


def test_disjoint_pair_poses_satisfy_every_cut() -> None:
    """Every disjoint pose in a node satisfies the hull cuts and one of the half-planes."""
    rng = random.Random(3)
    checked = 0
    for _ in range(70):
        ci = (Q(rng.randint(150, 200), 100), Q(rng.randint(150, 200), 100))
        offset = (Q(rng.randint(-150, 150), 100), Q(rng.randint(-150, 150), 100))
        cj = (ci[0] + offset[0], ci[1] + offset[1])
        size = Q(rng.randint(5, 40), 100)
        polygons = tuple(
            ((x, y), (x + size, y), (x + size, y + size), (x, y + size)) for x, y in (ci, cj)
        )
        pattern = bb.Pattern(("i", "j"), polygons, bb.cover.U)
        solver = bb.Solver(pattern, bb.Settings())
        root = solver.root()
        width = rng.choice((math.pi / 2, 0.3, 0.05))
        starts = [rng.uniform(root.angles[0][0], root.angles[0][1] - width) for _ in range(2)]
        angles = tuple((start, start + width) for start in starts)
        node = bb.Node(angles, solver.cell_boxes, (None,), 0)
        boxes = solver.contract(node)
        if boxes is None:
            continue
        term = solver.pair_term(node, boxes, 0)
        for _ in range(40):
            pose = [
                (
                    rng.uniform(box[0], box[1]),
                    rng.uniform(box[2], box[3]),
                    rng.uniform(*angle),
                )
                for box, angle in zip(boxes, angles, strict=True)
            ]
            if separated(pose[0], pose[1]) < 0:
                continue
            assert term.kind not in ("disc", "pair")
            checked += 1
            dx, dy = pose[1][0] - pose[0][0], pose[1][1] - pose[0][1]
            for ux, uy, v in term.cuts:
                assert ux * dx + uy * dy >= v - 1e-12
            if term.planes:
                assert max(nx * dx + ny * dy - r for nx, ny, r in term.planes) >= -1e-12
    assert checked > 100


def test_dual_bound_is_below_the_exact_value() -> None:
    rng = random.Random(9)
    boxes = ((1.0, 2.0, 1.5, 2.5), (2.0, 3.25, 1.0, 1.75))
    for _ in range(200):
        rows = []
        for _ in range(4):
            columns = (0, 1, 2, 3)
            values = tuple(rng.uniform(-1, 1) for _ in columns)
            rhs = rng.uniform(-2, 2)
            norm = rng.uniform(0.5, 2.0)
            rows.append(
                bb.Row(columns, values, rhs, norm, tuple((v, v) for v in values), (rhs, rhs))
            )
        weights = [rng.random() for _ in rows]
        cost = (rng.randrange(4), rng.choice((1.0, -1.0)))
        bound = bb.dual_bound(rows, weights, bb.column_spans(boxes), cost)
        combined = [Q(0)] * 4
        combined[cost[0]] = Q(cost[1])
        right = Q(0)
        for row, weight in zip(rows, weights, strict=True):
            y = Q(weight / row.norm)
            for column, value in zip(row.columns, row.values, strict=True):
                combined[column] += y * Q(value)
            right += y * Q(row.rhs)
        spans = [(b[0], b[1]) if axis == 0 else (b[2], b[3]) for b in boxes for axis in (0, 1)]
        exact = sum(
            (
                c * Q(span[0] if c > 0 else span[1])
                for c, span in zip(combined, spans, strict=True)
            ),
            start=Q(0),
        )
        assert Q(bound) <= exact - right


def three_in_a_row(right_x: tuple[str, str]) -> bb.Pattern:
    return bb.Pattern(
        ("left", "middle", "right"),
        (
            rectangle("1.00", "1.05", "2.00", "2.05"),
            rectangle("1.40", "2.40", "2.00", "2.05"),
            rectangle(*right_x, "2.00", "2.05"),
        ),
        bb.cover.U,
    )


@pytest.mark.parametrize(("right", "obbt_rounds"), [("2.80", 0), ("2.80", 3), ("2.94", 3)])
def test_a_crowded_row_is_certified(right: str, obbt_rounds: int) -> None:
    # The middle square needs a horizontal gap of at least sqrt(1 - 0.05^2) to each end
    # square, so the two end centres need 1.9975 between them; the cells allow at most
    # 1.85 or 1.94. Without bound tightening every leaf is an exact Farkas prune.
    right_x = (right, str(Q(right) + Q("0.05")))
    pattern = three_in_a_row((str(float(Q(right_x[0]))), str(float(Q(right_x[1])))))
    result = bb.search(pattern, bb.Settings(max_seconds=20, obbt_rounds=obbt_rounds))
    assert result["verdict"] == "certified-infeasible"
    assert result["farkas_failures"] == 0
    if obbt_rounds == 0:
        assert set(result["prune_reasons"]) == {"lp"}


@pytest.mark.parametrize("theta0", [0.0, bb.DEFAULT_THETA0])
def test_a_feasible_row_is_never_certified(theta0: float) -> None:
    # Axis-aligned squares at x = 1.00, 2.02 and 3.05 are disjoint.
    pattern = three_in_a_row(("3.05", "3.10"))
    result = bb.search(pattern, bb.Settings(theta0=theta0, max_seconds=1, max_nodes=300))
    assert result["verdict"] != "certified-infeasible"


@pytest.mark.parametrize("theta0", [0.0, bb.DEFAULT_THETA0])
def test_a_feasible_pose_survives_every_node_on_its_path(theta0: float) -> None:
    pattern = three_in_a_row(("3.05", "3.10"))
    pose = [(1.0, 2.0, 0.0), (2.025, 2.0, 0.0), (3.05, 2.0, 0.0)]
    result = bb.witness_path(pattern, bb.Settings(theta0=theta0), pose)
    assert result["passed"], result["failure"]
    assert result["final_max_angle_width"] < bb.DEFAULT_FLOOR


def test_the_tree_estimate_matches_a_small_exact_count() -> None:
    pattern = three_in_a_row(("2.80", "2.85"))
    exact = bb.search(pattern, bb.Settings())["nodes"]
    estimated = bb.estimate(pattern, bb.Settings(), dives=40)["estimated_nodes_mean"]
    assert abs(estimated - exact) <= 0.25 * exact


def _row(
    header: dict[str, Any], record: dict[str, Any], ref: list[Any]
) -> tuple[dict[int, Q], Q]:
    """A recorded row as exact coefficients by column and its right side (README C2)."""
    if ref[0] == "c":
        square, edge = ref[1], ref[2]
        vertices = [(Q(x), Q(y)) for x, y in header["cells"][square]]
        (x0, y0), (x1, y1) = vertices[edge], vertices[(edge + 1) % len(vertices)]
        a, b = y1 - y0, x0 - x1
        return {2 * square: a, 2 * square + 1: b}, a * x0 + b * y0
    pair, ux, uy, v = record["cuts"][ref[1]]
    i, j = header["pairs"][pair]
    ux, uy = Q(ux), Q(uy)
    return {2 * i: ux, 2 * i + 1: uy, 2 * j: -ux, 2 * j + 1: -uy}, -Q(v)


def _least(combined: dict[int, Q], boxes: list[list[Q]]) -> Q:
    total = Q(0)
    for column, coefficient in combined.items():
        box = boxes[column // 2]
        lo, hi = (box[0], box[1]) if column % 2 == 0 else (box[2], box[3])
        total += coefficient * (lo if coefficient > 0 else hi)
    return total


def _dual(
    header: dict[str, Any],
    record: dict[str, Any],
    weights: list[Any],
    boxes: list[list[Q]],
    cost: tuple[int, int] | None = None,
) -> Q:
    """`min over the boxes of (cost + y A) . z - y b`, exactly (README C3 and C4)."""
    combined: dict[int, Q] = {} if cost is None else {cost[0]: Q(cost[1])}
    right = Q(0)
    for ref, weight in weights:
        y = Q(weight)
        assert y >= 0
        coefficients, rhs = _row(header, record, ref)
        for column, value in coefficients.items():
            combined[column] = combined.get(column, Q(0)) + y * value
        right += y * rhs
    return _least(combined, boxes) - right


def _h_lower(cs: list[Q]) -> Q:
    """(|cos| lower + |sin| lower)/2 from interval enclosures [cl, ch, sl, sh]."""

    def least(lo: Q, hi: Q) -> Q:
        return lo if lo >= 0 else (-hi if hi <= 0 else Q(0))

    return (least(cs[0], cs[1]) + least(cs[2], cs[3])) / 2


def _meets_multiple(lo: Q, hi: Q, multiples: dict[str, list[str]]) -> bool:
    return any(lo <= Q(m[1]) and hi >= Q(m[0]) for m in multiples.values())


def _gap_lower(ti: list[Q], tj: list[Q], trig: dict[str, list[Q]], header: dict[str, Any]) -> Q:
    """README P1, in exact rationals; g_lo = 1 is always a valid fallback."""
    lo, hi = tj[0] - ti[1], tj[1] - ti[0]
    multiples = header["half_pi_multiples"]
    if lo <= 0 <= hi or hi - lo >= Q(multiples["1"][0]) or _meets_multiple(lo, hi, multiples):
        return Q(1)
    values = []
    for p_, q_ in ((tj[0], ti[1]), (tj[1], ti[0])):
        cp, cq = trig[bb.rational(p_)], trig[bb.rational(q_)]

        def product(a: tuple[Q, Q], b: tuple[Q, Q]) -> tuple[Q, Q]:
            values_ = [x * y for x in a for y in b]
            return min(values_), max(values_)

        cos_p, sin_p, cos_q, sin_q = (
            (cp[0], cp[1]),
            (cp[2], cp[3]),
            (cq[0], cq[1]),
            (cq[2], cq[3]),
        )
        a, b = product(cos_p, cos_q), product(sin_p, sin_q)
        c, d = product(sin_p, cos_q), product(cos_p, sin_q)
        values.append(_h_lower([a[0] + b[0], a[1] + b[1], c[0] - d[1], c[1] - d[0]]))
    return max(Q(1), Q(1, 2) + min(values))


def _clip_min(u: tuple[Q, Q], plane: tuple[Q, Q, Q], dx: tuple[Q, Q], dy: tuple[Q, Q]) -> Q:
    """Exact min of u . d over the d-box meet n . d >= r (vertices of the clipped box)."""
    nx, ny, r = plane
    corners = [(dx[0], dy[0]), (dx[1], dy[0]), (dx[1], dy[1]), (dx[0], dy[1])]
    vertices = []
    for index, start in enumerate(corners):
        end = corners[(index + 1) % 4]
        fs, fe = nx * start[0] + ny * start[1] - r, nx * end[0] + ny * end[1] - r
        if fs >= 0:
            vertices.append(start)
        if fs * fe < 0:
            t = fs / (fs - fe)
            vertices.append(
                (start[0] + t * (end[0] - start[0]), start[1] + t * (end[1] - start[1]))
            )
    assert vertices
    return min(u[0] * x + u[1] * y for x, y in vertices)


def _possible_planes(
    pieces: list[list[str]],
    g_lo: Q,
    dx: tuple[Q, Q],
    dy: tuple[Q, Q],
    *,
    trig: dict[str, list[Q]],
    half_pi_lower: Q,
) -> list[tuple[Q, Q, Q]]:
    """README P3: every plane of the pieces that the d-box can meet, in exact rationals."""
    span = max(-dx[0], dx[1]) + max(-dy[0], dy[1])
    planes: list[tuple[Q, Q, Q]] = []

    def sup(nx: tuple[Q, Q], ny: tuple[Q, Q]) -> Q:
        return max(a * x for a in nx for x in dx) + max(b * y for b in ny for y in dy)

    for lo_s, hi_s, m_s in pieces:
        lo, hi, m = Q(lo_s), Q(hi_s), Q(m_s)
        if hi - lo < half_pi_lower:
            x = max(m - lo, hi - m)
            candidates = [(lo_s, g_lo), (hi_s, g_lo), (m_s, g_lo * (1 - x * x / 2))]
            for angle, base in candidates:
                cl, ch, sl, sh, nx, ny = trig[angle]
                r = base - max(ch - cl, sh - sl) * span
                if sup((cl, ch), (sl, sh)) >= base and sup((nx, nx), (ny, ny)) >= r:
                    planes.append((nx, ny, r))
        else:
            cl, ch, sl, sh, nx, ny = trig[m_s]
            tau = max(m - lo, hi - m) / 2
            perp = [
                -s_ * x + c_ * y for s_ in (sl, sh) for c_ in (cl, ch) for x in dx for y in dy
            ]
            big = max(-dx[0], dx[1]) ** 2 + max(-dy[0], dy[1]) ** 2
            root = Q(math.isqrt(int(big * 2**120)) + 1, 2**60)
            r = g_lo - 2 * tau * (max(abs(v) for v in perp) + tau * root)
            r -= max(ch - cl, sh - sl) * span
            if sup((nx, nx), (ny, ny)) >= r:
                planes.append((nx, ny, r))
    return planes


def _check_cuts(saved: dict[str, Any]) -> int:
    """Every recorded cut re-derived from the saved pieces and enclosures (README C2)."""
    header = saved["manifest"]["header"]
    trig = {key: [Q(v) for v in value] for key, value in saved["trig"].items()}
    half_pi_lower = Q(header["half_pi_multiples"]["1"][0])
    checked = 0
    for node in saved["nodes"]:
        angles = [[Q(lo), Q(hi)] for lo, hi in node["angles"]]
        for record in node["rounds"]:
            boxes = [[Q(v) for v in box] for box in record["boxes"]]
            for pair, ux, uy, v in record["cuts"]:
                i, j = header["pairs"][pair]
                dx = (boxes[j][0] - boxes[i][1], boxes[j][1] - boxes[i][0])
                dy = (boxes[j][2] - boxes[i][3], boxes[j][3] - boxes[i][2])
                g_lo = _gap_lower(angles[i], angles[j], trig, header)
                planes = _possible_planes(
                    record["pairs"][str(pair)],
                    g_lo,
                    dx,
                    dy,
                    trig=trig,
                    half_pi_lower=half_pi_lower,
                )
                u = (Q(ux), Q(uy))
                assert Q(v) <= min(_clip_min(u, plane, dx, dy) for plane in planes)
                checked += 1
    return checked


@pytest.mark.parametrize("obbt_rounds", [0, 3])
def test_a_certificate_round_trips_and_its_closures_recheck_exactly(
    obbt_rounds: int, tmp_path: Path
) -> None:
    pattern = three_in_a_row(("2.80", "2.85"))
    settings = bb.Settings(obbt_rounds=obbt_rounds)
    result = bb.search(pattern, settings, certificate=tmp_path)
    assert result["verdict"] == "certified-infeasible"
    saved = bb.load_certificate(tmp_path, result["certificate_manifest"])
    header, nodes = saved["manifest"]["header"], saved["nodes"]
    assert saved["manifest"]["summary"]["complete"]
    assert len(nodes) == result["nodes"]
    assert (tmp_path / "README.txt").read_text(encoding="utf-8").count(
        result["certificate_manifest"]
    ) == 1
    children: dict[int, list[dict[str, Any]]] = {}
    for node in nodes:
        if node["parent"] is not None:
            children.setdefault(node["parent"], []).append(node)
    roots = [node for node in nodes if node["parent"] is None]
    assert len(roots) == 1
    assert roots[0]["angles"] == header["root_angles"]
    checked = {"lp": 0, "bounds": 0}
    for node in nodes:
        kids = children.get(node["id"], [])
        if node["closed"] is None:
            if "angle" in node["split"]:
                square, at = node["split"]["angle"]
                assert sorted(kid["angles"][square] for kid in kids) == sorted(
                    [[node["angles"][square][0], at], [at, node["angles"][square][1]]]
                )
            else:
                pair, windows = node["split"]["pair"]
                assert sorted(
                    [w[1], w[2]] for kid in kids for w in kid["windows"] if w[0] == pair
                ) == sorted(windows)
            continue
        assert not kids
        for record in node["rounds"]:
            boxes = [[Q(v) for v in box] for box in record["boxes"]]
            for column, sign, value, weights in record.get("bounds", []):
                assert Q(value) <= _dual(header, record, weights, boxes, (column, sign))
                slot = 2 * (column % 2) + (0 if sign > 0 else 1)
                boxes[column // 2][slot] = Q(value) * sign
                checked["bounds"] += 1
            if "farkas" in record:
                assert node["closed"] == "lp"
                assert _dual(header, record, record["farkas"], boxes) > 0
                checked["lp"] += 1
    if obbt_rounds == 0:
        assert checked["lp"] == result["prune_reasons"]["lp"] > 0
    else:
        assert checked["bounds"] > 0
    assert _check_cuts(saved) > 0


# ---------------------------------------------------------------------------
# The Taylor relaxation (opt-in) and the interval form's unchanged certificates
# ---------------------------------------------------------------------------


def _h(angle: float) -> float:
    mpmath.mp.prec = 100
    value = (abs(mpmath.cos(angle)) + abs(mpmath.sin(angle))) / 2
    return float(value)


def test_taylor_lines_lie_below_the_supports() -> None:
    """`constant + h(centre + t) >= a + b t` for every line, every |t| <= rho."""
    rng = random.Random(21)
    checked = 0
    for _ in range(300):
        centre = rng.uniform(-1.8, 1.8)
        rho = rng.choice((1e-3, 0.02, 0.1, 0.4)) * rng.random()
        span = (centre - rho, centre + rho)
        lines = bb.taylor_lines(*bb.cos_sin(centre), rho, span, constant=0.5)
        assert lines
        for _ in range(30):
            t = rng.uniform(-rho, rho)
            for _, _, a, b in lines:
                assert 0.5 + _h(centre + t) >= a + b * t - 1e-15
                checked += 1
    assert checked > 5000


def _taylor_pair_solver(
    rng: random.Random,
) -> tuple[bb.Solver, bb.Node, tuple[bb.Box, ...]] | None:
    """Two small cells near each other, a narrow angle box each, in Taylor mode."""
    ci = (Q(rng.randint(150, 200), 100), Q(rng.randint(150, 200), 100))
    offset = (Q(rng.randint(-130, 130), 100), Q(rng.randint(-130, 130), 100))
    cj = (ci[0] + offset[0], ci[1] + offset[1])
    size = Q(rng.randint(5, 30), 100)
    polygons = tuple(
        ((x, y), (x + size, y), (x + size, y + size), (x, y + size)) for x, y in (ci, cj)
    )
    solver = bb.Solver(bb.Pattern(("i", "j"), polygons, bb.cover.U), bb.Settings(taylor=True))
    width = rng.choice((0.3, 0.08, 0.02))
    angles = tuple(
        (start, start + width)
        for start in (rng.uniform(0.4, 1.9 - width), rng.uniform(0.4, 1.9 - width))
    )
    node = bb.Node(angles, solver.cell_boxes, (None,), 0)
    boxes = solver.contract(node)
    return None if boxes is None else (solver, node, boxes)


def test_disjoint_pair_poses_satisfy_every_taylor_cut() -> None:
    rng = random.Random(4)
    checked = 0
    for _ in range(120):
        made = _taylor_pair_solver(rng)
        if made is None:
            continue
        solver, node, boxes = made
        term = solver.pair_term(node, boxes, 0)
        if not term.taylor:
            continue
        centres = [0.5 * (lo + hi) for lo, hi in node.angles]
        for _ in range(40):
            pose = [
                (rng.uniform(b[0], b[1]), rng.uniform(b[2], b[3]), rng.uniform(*a))
                for b, a in zip(boxes, node.angles, strict=True)
            ]
            if separated(pose[0], pose[1]) < 0:
                continue
            dx, dy = pose[1][0] - pose[0][0], pose[1][1] - pose[0][1]
            dt = (pose[1][2] - centres[1]) - (pose[0][2] - centres[0])
            for ux, uy, w, v, _ in term.taylor:
                assert ux * dx + uy * dy - w * dt >= v - 1e-12
                checked += 1
    assert checked > 200


def test_contained_squares_satisfy_every_wall_row() -> None:
    rng = random.Random(8)
    cap = float(bb.cover.U)
    checked = 0
    for _ in range(80):
        x0 = rng.choice((0.5, 0.55, cap - 0.8))
        cell = (
            (Q(x0), Q(2)),
            (Q(x0) + Q(1, 4), Q(2)),
            (Q(x0) + Q(1, 4), Q(9, 4)),
            (Q(x0), Q(9, 4)),
        )
        solver = bb.Solver(bb.Pattern(("s",), (cell,), bb.cover.U), bb.Settings(taylor=True))
        lo = rng.uniform(0.4, 1.9)
        node = bb.Node(((lo, lo + rng.choice((0.4, 0.1, 0.02))),), solver.cell_boxes, (), 0)
        solver.taylor = solver.taylor_context(node)
        rows = solver.wall_rows(solver.cell_boxes)
        centre = solver.taylor.centres[0]
        for _ in range(60):
            theta = rng.uniform(*node.angles[0])
            half = (abs(math.cos(theta)) + abs(math.sin(theta))) / 2
            z = (rng.uniform(half, cap - half), rng.uniform(half, cap - half))
            point = {0: z[0], 1: z[1], 2: theta - centre}
            for row in rows:
                value = sum(
                    c * point[col] for col, c in zip(row.columns, row.values, strict=True)
                )
                assert value <= row.rhs + 1e-12
                checked += 1
    assert checked > 500


def test_taylor_mode_certifies_crowded_rows_and_never_a_feasible_one() -> None:
    for right in (("2.80", "2.85"), ("2.94", "2.99")):
        result = bb.search(three_in_a_row(right), bb.Settings(taylor=True, max_seconds=20))
        assert result["verdict"] == "certified-infeasible"
        assert result["farkas_failures"] == 0
    feasible = bb.search(
        three_in_a_row(("3.05", "3.10")),
        bb.Settings(taylor=True, max_seconds=1, max_nodes=200),
    )
    assert feasible["verdict"] != "certified-infeasible"


@pytest.mark.parametrize(("right", "obbt_rounds"), [("2.80", 0), ("2.80", 3), ("2.94", 3)])
def test_interval_certificates_are_unchanged_by_the_taylor_option(
    right: str, obbt_rounds: int, tmp_path: Path
) -> None:
    # The pre-Taylor and current implementations produce the same interval chunks
    # on one host, but HiGHS-proposed multipliers need not match another build's bits.
    # Compare fresh interval runs around an actual opt-in run, then independently
    # re-prove every certificate instead of pinning one solver build's proposals.
    pattern = three_in_a_row((str(float(Q(right))), str(float(Q(right) + Q("0.05")))))
    cells = verifier.Cells(
        dict(zip(pattern.names, pattern.polygons, strict=True)),
        pattern.cap,
        {"kind": "test", "case": right, "obbt_rounds": obbt_rounds},
    )
    settings = {
        "default": bb.Settings(obbt_rounds=obbt_rounds),
        "taylor": bb.Settings(obbt_rounds=obbt_rounds, taylor=True),
        "interval": bb.Settings(obbt_rounds=obbt_rounds, taylor=False),
    }
    certificates: dict[str, dict[str, Any]] = {}
    for name, option in settings.items():
        directory = tmp_path / name
        result = bb.search(pattern, option, certificate=directory)
        assert result["verdict"] == "certified-infeasible"
        certificates[name] = bb.load_certificate(directory, result["certificate_manifest"])
        receipt = verifier.verify_certificate(
            directory, cells, manifest=result["certificate_manifest"]
        )
        assert receipt["status"] == "PASS", receipt["failures"]
        assert receipt["mode"] == "full"
        assert receipt["checked_nodes"] == receipt["nodes"] == result["nodes"] > 0
    baseline, enabled, interval = (
        certificates[name] for name in ("default", "taylor", "interval")
    )
    assert baseline["manifest"]["chunks"] == interval["manifest"]["chunks"]
    assert enabled["manifest"]["chunks"] != baseline["manifest"]["chunks"]
    assert enabled["manifest"]["schema"] == bb.TAYLOR_SCHEMA
    assert enabled["manifest"]["header"]["settings"]["taylor"] is True
    assert all("taylor" in node for node in enabled["nodes"])
    for saved in (baseline, interval):
        assert saved["manifest"]["schema"] == bb.CERTIFICATE_SCHEMA
        assert "taylor" not in saved["manifest"]["header"]["settings"]
        assert all("taylor" not in node for node in saved["nodes"])
