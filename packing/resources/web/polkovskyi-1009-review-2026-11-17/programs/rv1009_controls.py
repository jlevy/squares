"""The controls of the plan, at one count.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Clean-room.

    python -I -B rv1009_controls.py CERT YAML PLAN.json ISSUE.json N OUT.json

Each control changes the certificate in a stated way and compares what both methods (or
the readers) decide with the outcome the plan states. The outcomes are rules over the
certificate's exact facts: its rows, its side, method A's margins and clearances. A
decision in which the two methods disagree fails its control. A whole-file control writes
the changed packing as the bytes of both forms and reads them back through the readers.

A control that changes one square, or only the side, decides every square and wall again
and, of the pairs, those that hold the changed square. For every other square it checks
that the row and the corners read back are the original's; a pair's decision is a function
of its two squares alone, so each pair it does not decide again has the original's
decision. A control that moves every square (a symmetry, a translation, a contraction)
decides everything again.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1009_axes as axes  # noqa: E402
import rv1009_clip as clip  # noqa: E402
import rv1009_decide as decide  # noqa: E402
import rv1009_files as files  # noqa: E402
import rv1009_forms as forms  # noqa: E402
import rv1009_geom as geom  # noqa: E402
import rv1009_issue as issue  # noqa: E402
import rv1009_reader as reader  # noqa: E402
import rv1009_write as write  # noqa: E402
from gmpy2 import mpq  # noqa: E402

F = Fraction
EPS = geom.PAST
WALLS = ("left", "bottom", "right", "top")
OPPOSITE = (2, 3, 0, 1)


def exact(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def sci(value: Fraction) -> str:
    return f"{float(value):.6e}"


def pair(value: Fraction) -> tuple[int, int]:
    return value.numerator, value.denominator


def pose_of(row: geom.Row) -> axes.Pose:
    return axes.pose_from_xyt(pair(row[0]), pair(row[1]), pair(row[2]))


def quad_of(row: geom.Row) -> list[clip.Point]:
    return clip.points(forms.pairs_of(geom.corners(row)))


class Original:
    """The certificate's exact facts."""

    def __init__(self, cert_data: bytes, yaml_data: bytes) -> None:
        self.cert_data = cert_data
        self.yaml_data = yaml_data
        self.cert = reader.read_cert(cert_data)
        self.wit = reader.read_witness(yaml_data)
        self.n = self.cert["n"]
        self.side = F(*self.cert["side"])
        self.rows = [tuple(F(*v) for v in row) for row in self.cert["poses"]]
        self.quads = [
            tuple((F(*p[0]), F(*p[1])) for p in quad) for quad in self.wit["squares"]
        ]
        self.result = files.decide_files(cert_data, yaml_data)
        native = self.result["native"]
        self.verdict = self.result["verdict"]
        self.margins = native["margins"]
        self.clear = native["clearances"]
        self.digest = native["margins_sha256"]
        self.touching = native["pair_touching"]
        self.overlapping = native["pair_overlapping"]
        self.wall_touching = native["wall_touching"]
        self.wall_crossing = native["wall_crossing"]
        self.senses = native["senses"]

    def margin(self, i: int, j: int) -> Fraction:
        if i > j:
            i, j = j, i
        return self.margins[decide.pair_index(self.n, i, j)]


def run(
    rows: list[geom.Row],
    side: Fraction,
    *,
    cert: bytes | None = None,
    wit: bytes | None = None,
    only: set[int] | None = None,
    a_from: str = "p",
) -> dict:
    cert_data = write.cert_bytes(rows, side) if cert is None else cert
    wit_data = write.witness_bytes([geom.corners(r) for r in rows], side) if wit is None else wit
    return files.decide_files(cert_data, wit_data, only=only, a_from=a_from)


def agree(result: dict) -> bool:
    """Both methods gave the same class at every wall and pair, and the files are one."""
    native = result.get("native")
    if native is None or "pair_disagree" not in native:
        return False
    return (
        not native["pair_disagree"]
        and not native["wall_disagree"]
        and not result["twin_fails"]
        and sorted({k for k, _w in native["wall_crossing"]}) == native["not_inside_b"]
    )


def same_data(orig: Original, got: dict, moved: set[int]) -> bool:
    """Every square not moved was read back with the original's row and corners."""
    if "rows_p" not in got or len(got["rows_p"]) != orig.n or len(got["quads_c"]) != orig.n:
        return False
    for k in range(orig.n):
        if k + 1 in moved:
            continue
        if tuple(F(*v) for v in got["rows_p"][k]) != orig.rows[k]:
            return False
        if forms.same_square(orig.wit["squares"][k], got["quads_c"][k]) is None:
            return False
    return True


def partial(orig: Original, fine: bool) -> str:
    """The verdict a partial decision must give: PARTIAL when what it decided is fine and
    the original was accepted, REFUSE otherwise."""
    return "PARTIAL" if fine and orig.verdict == "ACCEPT" else "REFUSE"


def unchanged_squares(orig: Original, native: dict, moved: set[int]) -> bool:
    return all(
        native["clearances"][k] == orig.clear[k] for k in range(orig.n) if k + 1 not in moved
    )


def wall_sets(clear: list[tuple[Fraction, ...]]) -> tuple[list, list]:
    """(touching, crossing) as lists of (square, wall) from clearances."""
    touching = []
    crossing = []
    for k, row in enumerate(clear):
        for w in range(4):
            if row[w] == 0:
                touching.append((k + 1, WALLS[w]))
            elif row[w] < 0:
                crossing.append((k + 1, WALLS[w]))
    return touching, crossing


class Controls:
    def __init__(self, orig: Original, plan: dict, claim: Fraction) -> None:
        self.o = orig
        self.plan = {c["id"]: c for c in plan["controls"]}
        self.claim = claim
        self.done: list[dict] = []

    def record(self, ident: str, ok: bool, **notes: object) -> None:
        if ident not in self.plan:
            msg = f"control {ident} is not in the plan"
            raise KeyError(msg)
        self.done.append(
            {
                "id": ident,
                "stated": self.plan[ident]["stated"],
                "outcome": "as stated" if ok else "NOT AS STATED",
                **notes,
            }
        )
        sys.stdout.write(f"  {ident}: {'as stated' if ok else 'NOT AS STATED'}\n")
        sys.stdout.flush()

    # C0 ------------------------------------------------------------------------------
    def c0(self) -> None:
        o = self.o
        bad_pairs = 0
        idx = 0
        for i in range(o.n):
            for j in range(i + 1, o.n):
                if geom.corner_margin(o.quads[i], o.quads[j]) != o.margins[idx]:
                    bad_pairs += 1
                idx += 1
        bad_walls = sum(
            1 for k in range(o.n) if geom.clearances(o.rows[k], o.side) != o.clear[k]
        )
        self.record(
            "C0",
            bad_pairs == 0 and bad_walls == 0,
            pairs=idx,
            pair_mismatches=bad_pairs,
            square_mismatches=bad_walls,
        )

    # readers ---------------------------------------------------------------------------
    def readers(self) -> None:
        o = self.o
        quads = [geom.corners(r) for r in o.rows]
        # R1: the last square deleted from the original bytes, the count as stated
        cert_lines = o.cert_data.decode("ascii").split("\n")[:-1]
        wit_lines = o.yaml_data.decode("ascii").split("\n")[:-1]
        cut_p = ("\n".join(cert_lines[:-1]) + "\n").encode("ascii")
        cut_c = ("\n".join(wit_lines[:-10]) + "\n").encode("ascii")
        cut_right = wit_lines[-10].startswith("  - id: ") and len(cert_lines[-1].split(" ")) == 3
        got_p = files.decide_files(cut_p, o.yaml_data, only=set())
        got_c = files.decide_files(o.cert_data, cut_c, only=set())
        ok = (
            cut_right
            and "squares are listed" in got_p.get("read_error_p", "")
            and "read_error_c" not in got_p
            and "squares are listed" in got_c.get("read_error_c", "")
            and "read_error_p" not in got_c
        )
        self.record("R1", ok, form_p=got_p.get("read_error_p"), form_c=got_c.get("read_error_c"))
        # R2: the side as 2p/2q in both forms
        text = f"{2 * o.side.numerator}/{2 * o.side.denominator}"
        got = run(
            o.rows,
            o.side,
            cert=write.cert_bytes(o.rows, o.side, side_text=text),
            wit=write.witness_bytes(quads, o.side, side_text=text),
            only=set(),
        )
        ok = (
            got["verdict"] == partial(o, True)
            and agree(got)
            and got["cert"]["noncanonical"] == ["side"]
            and got["witness"]["noncanonical"] == ["side"]
            and got["side"] == o.side
            and same_data(o, got, set())
            and got["native"]["clearances"] == o.clear
        )
        self.record("R2", ok, verdict=got["verdict"], side_text=text[:40] + "...")
        # R3: order
        ids = [f"square-{k + 1}" for k in range(o.n)]
        ids[0], ids[1] = ids[1], ids[0]
        got_c = run(o.rows, o.side, wit=write.witness_bytes(quads, o.side, ids=ids))
        swapped = [o.rows[1], o.rows[0], *o.rows[2:]]
        got_p = run(o.rows, o.side, cert=write.cert_bytes(swapped, o.side), only=set())
        ok = (
            "out of order" in got_c.get("read_error_c", "")
            and got_p["verdict"] == "REFUSE"
            and got_p.get("twin_fails") == [1, 2]
            and got_p["problems"] == ["2 squares differ between the files"]
            and same_data(o, got_p, {1, 2})
            and tuple(F(*v) for v in got_p["rows_p"][0]) == o.rows[1]
            and tuple(F(*v) for v in got_p["rows_p"][1]) == o.rows[0]
        )
        self.record(
            "R3",
            ok,
            form_c=got_c.get("read_error_c"),
            form_p_twin_fails=got_p.get("twin_fails"),
            form_p_problems=got_p["problems"],
        )
        # R4: the side as a decimal
        scaled = o.side.numerator * 10**40 // o.side.denominator
        digits = str(scaled)
        decimal = f"{digits[:-40]}.{digits[-40:]}"
        got_p = run(o.rows, o.side, cert=write.cert_bytes(o.rows, o.side, side_text=decimal))
        got_c = run(o.rows, o.side, wit=write.witness_bytes(quads, o.side, side_text=decimal))
        unquoted = write.witness_bytes(quads, o.side, side_text="SIDE").replace(
            b"  side: 'SIDE'\n", f"  side: {decimal}\n".encode()
        )
        got_f = run(o.rows, o.side, wit=unquoted)
        ok = (
            "not a scalar" in got_p.get("read_error_p", "")
            and "not a scalar" in got_c.get("read_error_c", "")
            and "scalar of kind float" in got_f.get("read_error_c", "")
        )
        self.record(
            "R4",
            ok,
            form_p=got_p.get("read_error_p"),
            form_c_quoted=got_c.get("read_error_c"),
            form_c_float=got_f.get("read_error_c"),
        )
        # R5: a plus sign on the first coordinate of square 1, in the original bytes
        first = len(o.cert["comments"]) + 1
        plus_lines = list(cert_lines)
        plus_lines[first] = "+" + plus_lines[first]
        got_p = files.decide_files(("\n".join(plus_lines) + "\n").encode("ascii"), o.yaml_data, only=set())
        wit_text = o.yaml_data.decode("ascii")
        marker = "    - - '"
        at = wit_text.index(marker) + len(marker)
        wit_plus = wit_text[:at] + "+" + wit_text[at:]
        got_c = files.decide_files(o.cert_data, wit_plus.encode("ascii"), only=set())
        ok = (
            "square 1 x: not a scalar" in got_p.get("read_error_p", "")
            and "read_error_c" not in got_p
            and "square 1 corner 1 x: not a scalar" in got_c.get("read_error_c", "")
            and "read_error_p" not in got_c
        )
        self.record("R5", ok, form_p=got_p.get("read_error_p"), form_c=got_c.get("read_error_c"))

    # gross -----------------------------------------------------------------------------
    def gross(self) -> None:
        o = self.o
        n = o.n
        # G1: square n placed on square 1
        rows = [*o.rows[:-1], o.rows[0]]
        got = run(rows, o.side, only={n})
        native = got["native"]
        want = {(k, n): o.margin(1, k) for k in range(2, n)}
        want[(1, n)] = F(-1)
        want_over = sorted({(1, n)} | {(k, n) for k in range(2, n) if o.margin(1, k) < 0})
        ok = (
            got["verdict"] == "REFUSE"
            and agree(got)
            and native["margins_of"] == want
            and native["pair_overlapping"] == want_over
            and native["clearances"][n - 1] == o.clear[0]
            and unchanged_squares(o, native, {n})
            and same_data(o, got, {n})
        )
        area_ok = native["overlap_area_b"] == 1 if want_over == [(1, n)] else None
        ok = ok and area_ok is not False
        self.record(
            "G1",
            ok,
            verdict=got["verdict"],
            overlapping=native["pair_overlapping"][:5],
            overlap_area=str(native["overlap_area_b"]),
        )
        # G2: square 1 translated by (S, 0)
        x, y, t = o.rows[0]
        rows = [(x + o.side, y, t), *o.rows[1:]]
        got = run(rows, o.side, only={1})
        native = got["native"]
        le, bo, ri, to = o.clear[0]
        want_clear = (le + o.side, bo, ri - o.side, to)
        want_cross = sorted({c for c in o.wall_crossing if c[0] != 1} | {(1, "right")}
                            | ({(1, "bottom")} if bo < 0 else set())
                            | ({(1, "top")} if to < 0 else set()))
        inside = clip.area_in_box(quad_of(rows[0]), mpq(o.side.numerator, o.side.denominator))
        ok = (
            got["verdict"] == "REFUSE"
            and agree(got)
            and native["clearances"][0] == want_clear
            and sorted(native["wall_crossing"]) == want_cross
            and (inside == 0) == (le >= 0)
            and native["pair_overlapping"] == []
            and native["pairs_decided"] == n - 1
            and same_data(o, got, {1})
            and unchanged_squares(o, native, {1})
        )
        self.record(
            "G2",
            ok,
            verdict=got["verdict"],
            crossing=native["wall_crossing"][:5],
            square_1_right_clearance=exact(native["clearances"][0][2])[:60],
            square_1_area_inside=str(inside),
        )
        # G3: one corner of form C moved by the least step
        quads = [list(q) for q in o.quads]
        quads[0][0] = (quads[0][0][0] + EPS, quads[0][0][1])
        raw = forms.pairs_of(tuple(quads[0]))
        try:
            forms.pose_from_corners(raw)
            no_pose = False
        except ValueError:
            no_pose = True
        got = run(o.rows, o.side, wit=write.witness_bytes(quads, o.side))
        native = got["native"]
        ok = (
            got["verdict"] == "REFUSE"
            and native["verdict"] == "REFUSE"
            and native.get("not_unit_b") == [1]
            and native.get("not_unit_a") == []
            and got["twin_fails"] == [1]
            and no_pose
        )
        self.record(
            "G3",
            ok,
            verdict=got["verdict"],
            not_unit_by_b=native.get("not_unit_b"),
            twin_fails=got["twin_fails"],
            pose_from_corners_refused=no_pose,
        )
        # G4, G5: other listings of form C
        for ident, relist, want_sense in (
            ("G4", lambda q: (q[0], q[3], q[2], q[1]), -1),
            ("G5", lambda q: (q[1], q[2], q[3], q[0]), 1),
        ):
            listed = [relist(q) for q in o.quads]
            got = run(o.rows, o.side, wit=write.witness_bytes(listed, o.side), a_from="c")
            native = got["native"]
            ok = (
                got["verdict"] == o.verdict
                and agree(got)
                and got["form_c_no_pose"] == []
                and native["margins_sha256"] == o.digest
                and native["clearances"] == o.clear
                and native["senses"] == [want_sense * s for s in o.senses]
                and native["pair_counts_b"] == o.result["native"]["pair_counts_b"]
            )
            self.record(
                ident,
                ok,
                verdict=got["verdict"],
                senses_ccw=sum(1 for s in native["senses"] if s == 1),
                senses_cw=sum(1 for s in native["senses"] if s == -1),
            )
        # G6, G7, G8: symmetries of the plane, both forms
        s = o.side
        for ident, move, perm in (
            ("G6", lambda r: (r[1], r[0], geom.transposed_t(r[2])), (1, 0, 3, 2)),
            ("G7", lambda r: (s - r[1], r[0], r[2]), (3, 0, 1, 2)),
            ("G8", lambda r: (s - r[0], r[1], -r[2]), (2, 1, 0, 3)),
        ):
            rows = [move(r) for r in o.rows]
            got = run(rows, o.side)
            native = got["native"]
            want_clear = [tuple(row[perm[w]] for w in range(4)) for row in o.clear]
            ok = (
                got["verdict"] == o.verdict
                and agree(got)
                and native["margins_sha256"] == o.digest
                and native["clearances"] == want_clear
            )
            self.record(ident, ok, verdict=got["verdict"])

    # the side --------------------------------------------------------------------------
    def side_rule(self, delta: Fraction) -> tuple[bool, dict, dict]:
        """The side lowered by ``delta``: right and top clearances lowered by exactly
        ``delta``, everything else unchanged; contacts and crossings exactly those of the
        new clearances; accepted exactly when nothing crosses and no pair overlapped."""
        o = self.o
        got = run(o.rows, o.side - delta, only=set())
        native = got["native"]
        want_clear = [(le, bo, ri - delta, to - delta) for le, bo, ri, to in o.clear]
        touching, crossing = wall_sets(want_clear)
        want_verdict = partial(o, not crossing)
        ok = (
            got["verdict"] == want_verdict
            and agree(got)
            and native["clearances"] == want_clear
            and same_data(o, got, set())
            and native["wall_touching"] == touching
            and native["wall_crossing"] == crossing
        )
        notes = {
            "delta": sci(delta),
            "verdict": got["verdict"],
            "contacts": len(native["wall_touching"]),
            "contacts_first": native["wall_touching"][:8],
            "crossings": len(native["wall_crossing"]),
            "crossings_first": native["wall_crossing"][:8],
        }
        return ok, notes, {"verdict": got["verdict"], "touching": touching, "crossing": crossing}

    def sides(self) -> None:
        o = self.o
        w = min(min(row[2], row[3]) for row in o.clear)
        at = [(k + 1, WALLS[x]) for k, row in enumerate(o.clear) for x in (2, 3) if row[x] == w]
        ok, notes, _facts = self.side_rule(EPS)
        self.record("S1a", ok, **notes)
        ok, notes, _facts = self.side_rule(F(1, o.side.denominator))
        self.record("S1b", ok, step=f"1/{o.side.denominator}", **notes)
        ok, notes, facts = self.side_rule(w)
        if w >= 0 and o.verdict == "ACCEPT":
            ok = ok and facts["verdict"] == "PARTIAL" and set(facts["touching"]) == (
                set(at) | {c for c in o.wall_touching if c[1] in ("left", "bottom")}
            )
        self.record("S1c", ok, least_right_or_top_clearance=exact(w), attained_at=at[:8], **notes)
        ok, notes, facts = self.side_rule(w + EPS)
        ok = ok and facts["verdict"] == "REFUSE" and set(at) <= set(facts["crossing"])
        self.record("S1d", ok, **notes)
        ok, notes, _facts = self.side_rule(o.side - self.claim)
        self.record("S1e", ok, new_side="the claim", **notes)
        ok, notes, _facts = self.side_rule(o.side - self.claim + F(1, 10**12))
        self.record("S1f", ok, new_side="the claim less 1e-12", **notes)

    # the extent --------------------------------------------------------------------------
    def extent(self) -> None:
        o = self.o
        ls, bs, rs, ts = (min(row[w] for row in o.clear) for w in range(4))
        width = o.side - ls - rs
        height = o.side - bs - ts
        ext = max(width, height)
        rows = geom.translated(o.rows, -ls, -bs)
        for ident, new_side in (("E1c", ext), ("E1p", ext - EPS)):
            got = run(rows, new_side)
            native = got["native"]
            want_clear = [
                (le - ls, bo - bs, ri - rs - (width - new_side), to - ts - (height - new_side))
                for le, bo, ri, to in o.clear
            ]
            touching, crossing = wall_sets(want_clear)
            want_verdict = "ACCEPT" if (not crossing and not o.overlapping) else "REFUSE"
            ok = (
                got["verdict"] == want_verdict
                and agree(got)
                and native["clearances"] == want_clear
                and native["margins_sha256"] == o.digest
                and native["wall_touching"] == touching
                and native["wall_crossing"] == crossing
            )
            if ident == "E1c":
                walls_touched = sorted({w for _k, w in touching})
                need = {"left", "bottom"} | ({"right"} if width >= height else set()) | (
                    {"top"} if height >= width else set()
                )
                ok = ok and not crossing and set(walls_touched) == need
            else:
                ok = ok and bool(crossing) and got["verdict"] == "REFUSE"
            self.record(
                ident,
                ok,
                verdict=got["verdict"],
                width=exact(width),
                height=exact(height),
                extent_less_side=sci(ext - o.side),
                side_less_extent=exact(o.side - ext),
                contacts=touching[:12],
                contacts_count=len(touching),
                crossings=crossing[:12],
            )

    # contraction -------------------------------------------------------------------------
    def contraction(self) -> None:
        o = self.o
        n = o.n
        pair_scale = []
        for i in range(n):
            for j in range(i + 1, n):
                pair_scale.append(geom.contact_scale_pair(o.rows[i], o.rows[j]))
        wall_scale = [geom.contact_scale_walls(r, o.side) for r in o.rows]
        star = max(max(pair_scale), max(max(row) for row in wall_scale))
        for ident, lam in (("K1c", star), ("K1p", star * (1 - EPS))):
            rows = geom.scaled(o.rows, lam)
            got = run(rows, o.side * lam)
            native = got["native"]
            want_touch = []
            want_over = []
            idx = 0
            for i in range(1, n + 1):
                for j in range(i + 1, n + 1):
                    if pair_scale[idx] == lam:
                        want_touch.append((i, j))
                    elif pair_scale[idx] > lam:
                        want_over.append((i, j))
                    idx += 1
            want_wt = []
            want_wc = []
            for k in range(n):
                for w in range(4):
                    if wall_scale[k][w] == lam:
                        want_wt.append((k + 1, WALLS[w]))
                    elif wall_scale[k][w] > lam:
                        want_wc.append((k + 1, WALLS[w]))
            want_verdict = "ACCEPT" if not want_over and not want_wc else "REFUSE"
            ok = (
                got["verdict"] == want_verdict
                and agree(got)
                and native["pair_touching"] == want_touch
                and native["pair_overlapping"] == want_over
                and native["wall_touching"] == want_wt
                and native["wall_crossing"] == want_wc
            )
            if ident == "K1c":
                ok = ok and want_verdict == "ACCEPT" and bool(want_touch or want_wt)
            else:
                ok = ok and want_verdict == "REFUSE"
            self.record(
                ident,
                ok,
                verdict=got["verdict"],
                one_less_factor=exact(1 - lam) if ident == "K1c" else sci(1 - lam),
                one_less_factor_sci=sci(1 - lam),
                side_margin=exact(o.side * (1 - lam)) if ident == "K1c" else sci(o.side * (1 - lam)),
                side_margin_sci=sci(o.side * (1 - lam)),
                pairs_touching=native["pair_touching"][:8],
                pairs_touching_count=len(native["pair_touching"]),
                pairs_overlapping=native["pair_overlapping"][:8],
                pairs_overlapping_count=len(native["pair_overlapping"]),
                walls_touching=native["wall_touching"][:8],
                walls_crossing=native["wall_crossing"][:8],
            )

    # one pair ----------------------------------------------------------------------------
    def clear_of_others(self, moved: geom.Row, skip: set[int], side: Fraction) -> bool:
        o = self.o
        if min(geom.clearances(moved, side)) <= 0:
            return False
        return all(
            geom.margin(o.rows[k], moved) > 0 for k in range(o.n) if k + 1 not in skip
        )

    def one_pair(self) -> None:
        o = self.o
        n = o.n
        order = sorted(
            ((o.margins[decide.pair_index(n, i, j)], i, j)
             for i in range(1, n + 1) for j in range(i + 1, n + 1))
        )
        chosen = None
        tried = 0
        for _m, i, j in order[:400]:
            for fixed, mover in ((i, j), (j, i)):
                tried += 1
                at, _s = geom.close_pair(o.rows[fixed - 1], o.rows[mover - 1], F(0))
                past, _s = geom.close_pair(o.rows[fixed - 1], o.rows[mover - 1], -EPS)
                if self.clear_of_others(at, {i, j}, o.side) and self.clear_of_others(
                    past, {i, j}, o.side
                ):
                    chosen = (fixed, mover, at, past)
                    break
            if chosen:
                break
        eligible = chosen is not None
        if chosen is None:
            _m, i, j = order[0]
            at, _s = geom.close_pair(o.rows[i - 1], o.rows[j - 1], F(0))
            past, _s = geom.close_pair(o.rows[i - 1], o.rows[j - 1], -EPS)
            chosen = (i, j, at, past)
        fixed, mover, at, past = chosen
        lo, hi = min(fixed, mover), max(fixed, mover)
        for ident, moved, target in (("P1c", at, F(0)), ("P1p", past, -EPS)):
            rows = list(o.rows)
            rows[mover - 1] = moved
            got = run(rows, o.side, only={mover})
            native = got["native"]
            new_margin = native["margins_of"][(lo, hi)]
            others_over = sorted(
                (min(k, mover), max(k, mover))
                for k in range(1, n + 1)
                if k not in (fixed, mover) and geom.margin(o.rows[k - 1], moved) < 0
            )
            others_touch = sorted(
                (min(k, mover), max(k, mover))
                for k in range(1, n + 1)
                if k not in (fixed, mover) and geom.margin(o.rows[k - 1], moved) == 0
            )
            want_over = sorted(set(others_over) | ({(lo, hi)} if target < 0 else set()))
            want_touch = sorted(set(others_touch) | ({(lo, hi)} if target == 0 else set()))
            moved_clear = geom.clearances(moved, o.side)
            crossing = any(c < 0 for c in moved_clear) or any(k != mover for k, _w in o.wall_crossing)
            want_verdict = partial(o, not want_over and not crossing)
            ok = (
                got["verdict"] == want_verdict
                and agree(got)
                and new_margin == target
                and native["pairs_decided"] == n - 1
                and native["pair_overlapping"] == want_over
                and native["pair_touching"] == want_touch
                and same_data(o, got, {mover})
                and unchanged_squares(o, native, {mover})
                and native["clearances"][mover - 1] == moved_clear
            )
            if eligible:
                ok = ok and want_verdict == partial(o, target == 0)
                ok = ok and want_over == ([(lo, hi)] if target < 0 else [])
                ok = ok and want_touch == ([(lo, hi)] if target == 0 else [])
            self.record(
                ident,
                ok,
                verdict=got["verdict"],
                pair=[lo, hi],
                square_moved=mover,
                eligible=eligible,
                candidates_tried=tried,
                original_margin=exact(o.margin(lo, hi))[:80],
                original_margin_sci=sci(o.margin(lo, hi)),
                new_margin=exact(new_margin),
                overlapping=native["pair_overlapping"][:6],
                touching=native["pair_touching"][:6],
            )

    # one square at each wall ---------------------------------------------------------------
    def one_wall(self) -> None:
        o = self.o
        n = o.n
        for w in range(4):
            order = sorted((o.clear[k][w], k + 1) for k in range(n))
            chosen = None
            for value, k in order[:60]:
                x, y, t = o.rows[k - 1]
                shifts = []
                for step in (value, value + EPS):
                    if w == 0:
                        shifts.append((x - step, y, t))
                    elif w == 1:
                        shifts.append((x, y - step, t))
                    elif w == 2:
                        shifts.append((x + step, y, t))
                    else:
                        shifts.append((x, y + step, t))
                fine = all(
                    all(geom.margin(o.rows[m], sh) > 0 for m in range(n) if m != k - 1)
                    for sh in shifts
                )
                if fine:
                    chosen = (k, value, shifts)
                    break
            for ident, which, target in ((f"W1c-{WALLS[w]}", 0, F(0)), (f"W1p-{WALLS[w]}", 1, -EPS)):
                if chosen is not None:
                    k, value, shifts = chosen
                    rows = list(o.rows)
                    rows[k - 1] = shifts[which]
                    got = run(rows, o.side, only={k})
                    native = got["native"]
                    want = list(o.clear[k - 1])
                    want[w] = target
                    want[OPPOSITE[w]] = o.clear[k - 1][OPPOSITE[w]] + value - target
                    base_t = [c for c in o.wall_touching if c[0] != k]
                    base_c = [c for c in o.wall_crossing if c[0] != k]
                    mine_t = [(k, WALLS[x]) for x in range(4) if want[x] == 0]
                    mine_c = [(k, WALLS[x]) for x in range(4) if want[x] < 0]
                    want_verdict = partial(o, target == 0)
                    inside = clip.area_in_box(
                        quad_of(rows[k - 1]), mpq(o.side.numerator, o.side.denominator)
                    )
                    ok = (
                        got["verdict"] == want_verdict
                        and agree(got)
                        and native["clearances"][k - 1] == tuple(want)
                        and sorted(native["wall_touching"]) == sorted(base_t + mine_t)
                        and sorted(native["wall_crossing"]) == sorted(base_c + mine_c)
                        and native["pairs_decided"] == n - 1
                        and native["pair_overlapping"] == []
                        and native["pair_touching"] == []
                        and same_data(o, got, {k})
                        and unchanged_squares(o, native, {k})
                        and (inside == 1) == (target == 0)
                    )
                    self.record(
                        ident,
                        ok,
                        verdict=got["verdict"],
                        square=k,
                        original_clearance=exact(value),
                        new_clearance=exact(native["clearances"][k - 1][w]),
                        fallback=False,
                    )
                else:
                    # no eligible square: the whole packing moved to the wall
                    value = order[0][0]
                    step = value - target
                    dx = -step if w == 0 else (step if w == 2 else F(0))
                    dy = -step if w == 1 else (step if w == 3 else F(0))
                    rows = geom.translated(o.rows, dx, dy)
                    got = run(rows, o.side)
                    native = got["native"]
                    want_clear = []
                    for row in o.clear:
                        new = list(row)
                        new[w] = row[w] - step
                        new[OPPOSITE[w]] = row[OPPOSITE[w]] + step
                        want_clear.append(tuple(new))
                    touching, crossing = wall_sets(want_clear)
                    want_verdict = "ACCEPT" if not crossing and not o.overlapping else "REFUSE"
                    ok = (
                        got["verdict"] == want_verdict
                        and agree(got)
                        and native["clearances"] == want_clear
                        and native["margins_sha256"] == o.digest
                        and native["wall_touching"] == touching
                        and native["wall_crossing"] == crossing
                        and (bool(crossing) == (target < 0))
                    )
                    self.record(
                        ident,
                        ok,
                        verdict=got["verdict"],
                        fallback=True,
                        least_clearance=exact(value),
                        contacts=touching[:8],
                        crossings=crossing[:8],
                    )

    # every square, every pair -----------------------------------------------------------
    def wall_all(self) -> None:
        o = self.o
        side_q = mpq(o.side.numerator, o.side.denominator)
        bad = 0
        moves = 0
        for k in range(o.n):
            x, y, t = o.rows[k]
            value = min(o.clear[k])
            w = o.clear[k].index(value)
            for target in (F(0), -EPS):
                step = value - target
                if w == 0:
                    row = (x - step, y, t)
                elif w == 1:
                    row = (x, y - step, t)
                elif w == 2:
                    row = (x + step, y, t)
                else:
                    row = (x, y + step, t)
                moves += 1
                got = axes.wall_clearances(pose_of(row), pair(o.side))
                quad = quad_of(row)
                cls = clip.wall_classes(quad, side_q)[w][0]
                inside = clip.area_in_box(quad, side_q)
                fine = (
                    got[w] == target
                    and geom.clearances(row, o.side)[w] == target
                    and cls == ("touch" if target == 0 else "overlap")
                    and (inside == 1) == (target == 0)
                    and (inside < 1) == (target < 0)
                )
                if not fine:
                    bad += 1
        self.record("WALL", bad == 0, squares=o.n, moves=moves, not_as_stated=bad)

    def pair_all(self) -> None:
        o = self.o
        n = o.n
        poses = [pose_of(r) for r in o.rows]
        quads = [quad_of(r) for r in o.rows]
        corners = [geom.corners(r) for r in o.rows]
        bad = 0
        closings = 0
        for i in range(n):
            for j in range(i + 1, n):
                for target in (F(0), -EPS):
                    moved, _s = geom.close_pair(o.rows[i], o.rows[j], target)
                    closings += 1
                    a_margin = axes.pair_margin(poses[i], pose_of(moved))
                    cls, area = clip.pair_class(quads[i], quad_of(moved))
                    fine = (
                        a_margin == target
                        and cls == ("touch" if target == 0 else "overlap")
                        and (area > 0) == (target < 0)
                    )
                    if target == 0:
                        fine = fine and geom.corner_margin(corners[i], geom.corners(moved)) == 0
                    if not fine:
                        bad += 1
        self.record("PALL", bad == 0, pairs=n * (n - 1) // 2, closings=closings, not_as_stated=bad)

    # the sense of the tangent ------------------------------------------------------------
    def sense(self) -> None:
        o = self.o
        flipped = [(x, y, -t) for x, y, t in o.rows]
        got = run(
            o.rows, o.side, cert=write.cert_bytes(flipped, o.side), wit=o.yaml_data, only=set()
        )
        want = [k + 1 for k, (_x, _y, t) in enumerate(o.rows) if t not in (0, 1, -1)]
        both = run(flipped, o.side)
        ok = got["twin_fails"] == want and agree(both)
        if want:
            ok = ok and got["verdict"] == "REFUSE"
        self.record(
            "X1",
            ok,
            squares_with_tangent_0_or_1=o.n - len(want),
            twin_fails=len(got["twin_fails"]),
            mirrored_packing_verdict=both["verdict"],
            mirrored_pairs_overlapping=len(both["native"]["pair_overlapping"]),
            mirrored_walls_crossing=len(both["native"]["wall_crossing"]),
        )


def main(argv: list[str]) -> int:
    cert_path, yaml_path, plan_path, issue_path, n_text, out_path = argv[1:7]
    n = int(n_text)
    started = time.process_time()
    plan = json.loads(Path(plan_path).read_text(encoding="ascii"))
    stated = issue.read_issue(issue_path)
    claim = F(stated["claims"][n]["claim"])
    orig = Original(Path(cert_path).read_bytes(), Path(yaml_path).read_bytes())
    if orig.n != n:
        msg = "the certificate is not of the count named"
        raise SystemExit(msg)
    sys.stdout.write(f"n={n} original {orig.verdict}\n")
    controls = Controls(orig, plan, claim)
    skip = set(argv[7].split(",")) if len(argv) > 7 else set()
    steps = (
        ("C0", controls.c0),
        ("R", controls.readers),
        ("G", controls.gross),
        ("S", controls.sides),
        ("E", controls.extent),
        ("K", controls.contraction),
        ("P", controls.one_pair),
        ("W", controls.one_wall),
        ("WALL", controls.wall_all),
        ("PALL", controls.pair_all),
        ("X", controls.sense),
    )
    timing = {}
    for name, step in steps:
        if name in skip:
            continue
        t0 = time.process_time()
        step()
        timing[name] = round(time.process_time() - t0, 1)
    planned = [c["id"] for c in plan["controls"]]
    ran = [c["id"] for c in controls.done]
    complete = sorted(planned) == sorted(ran)
    as_stated = sum(1 for c in controls.done if c["outcome"] == "as stated")
    everything = complete and as_stated == len(planned)
    receipt = {
        "program": "rv1009_controls.py",
        "lane": "c-review-1009-1117",
        "n": n,
        "original_verdict": orig.verdict,
        "least_step": "1/10^40",
        "controls_planned": len(planned),
        "controls_run": len(ran),
        "controls_as_stated": as_stated,
        "verdict": "EVERY_CONTROL_AS_STATED" if everything else "NOT_EVERY_CONTROL_AS_STATED",
        "controls": controls.done,
        "cpu_seconds_by_group": timing,
        "cpu_seconds": round(time.process_time() - started, 1),
    }
    Path(out_path).write_text(json.dumps(receipt, indent=1) + "\n", encoding="ascii")
    sys.stdout.write(
        f"n={n} {receipt['verdict']} {as_stated} of {len(planned)} cpu={receipt['cpu_seconds']}s\n"
    )
    return 0 if everything else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
