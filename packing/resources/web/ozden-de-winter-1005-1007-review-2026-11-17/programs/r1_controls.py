"""The controls of the plan, run on one certificate file.

Lane R1, stage 4 review of #1005, #1006 and #1007.  Clean-room.

    python -I -B r1_controls.py PLAN.json LABEL PIN_ROOT OUT.json

PLAN.json is controls-plan.json, LABEL one of its files, and PIN_ROOT the directory
that holds the three pinned source trees under the names the plan gives
(``pin_dir``).  The program implements exactly the plan's controls, in the plan's
order, and refuses to run if its list and the plan's differ.  Each outcome is
evaluated as the plan states it, as a rule over the certificate's exact facts, and
compared with what method A (r1_axes) and method B (r1_area) decide.  A file of
tier twin runs the controls the plan marks on_twins; the others are run on the
report's first file, and the receipt lists them.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1_area  # noqa: E402
import r1_axes  # noqa: E402
import r1_decide  # noqa: E402
import r1_fmt  # noqa: E402
import r1_frame  # noqa: E402
import r1_read  # noqa: E402
import r1_twin  # noqa: E402

D = Fraction(1, 10**30)
WALLS = r1_frame.WALLS
OPPOSITE = {0: 2, 1: 3, 2: 0, 3: 1}
HALF = Fraction(1, 2)


class Ctx:
    """The certificate as read and decided, and what the controls need of it."""


# ------------------------------------------------------------------ helpers


def norm(squares):
    return [tuple(tuple(p) if isinstance(p, (tuple, list)) else p for p in sq) for sq in squares]


def build(ctx, squares, side):
    """A packing written in the file's own form, read back, and checked to be it."""
    squares = norm(squares)
    raw = r1_read.WRITERS[ctx.kind](len(squares), side, squares)
    packing = r1_read.READERS[ctx.kind](raw)
    if packing.n != len(squares) or packing.side != side or norm(packing.squares) != squares:
        raise RuntimeError("the control file did not read back as written")
    return packing


def reasons_text(reasons):
    return [{"kind": kind, "count": len(items), "first": items[:12]} for kind, items in reasons]


def brief(dec):
    verdict, reasons = dec.verdict()
    return {"verdict": verdict, "reasons": reasons_text(reasons)}


def agree(dec):
    return not dec.disagreements()


def centre_of(form, square):
    if form == "corners":
        return ((square[0][0] + square[2][0]) / 2, (square[0][1] + square[2][1]) / 2)
    return (square[0], square[1])


def touching_count(dec):
    return sum(1 for value in dec.margin.values() if value == 0)


def frames_margin_equal(dec, frames):
    return all(
        r1_frame.margin(frames[i - 1], frames[j - 1]) == value
        for (i, j), value in dec.margin.items()
    )


# ------------------------------------------------------------------ C0, K1, T0, T1


def c0(ctx):
    dec = ctx.dec
    pair_mismatch = sum(
        1
        for (i, j), value in dec.margin.items()
        if r1_frame.margin(ctx.frames[i - 1], ctx.frames[j - 1]) != value
    )
    square_mismatch = sum(
        1
        for k in range(ctx.n)
        if tuple(r1_frame.clearances(ctx.frames[k], ctx.side)) != tuple(dec.clear[k])
    )
    complete = len(dec.margin) == ctx.n * (ctx.n - 1) // 2
    return {
        "as_stated": pair_mismatch == 0 and square_mismatch == 0 and complete,
        "pairs_compared": len(dec.margin),
        "pair_mismatches": pair_mismatch,
        "squares_compared": ctx.n,
        "square_mismatches": square_mismatch,
    }


def k1(ctx):
    ceiling = r1_fmt.ceil_places(ctx.side, 12)
    return {
        "as_stated": ctx.claim >= ctx.side and ctx.claim == ceiling,
        "claim": r1_fmt.dec(ctx.claim, 12),
        "claim_at_least_side": ctx.claim >= ctx.side,
        "claim_is_twelve_place_ceiling": ctx.claim == ceiling,
        "claim_less_side": r1_fmt.exact_and_sci(ctx.claim - ctx.side),
    }


def t0(ctx):
    if ctx.twin is None:
        return {"as_stated": False, "twin": ctx.twin_file, "twin_refused": ctx.twin_refusal}
    relation = r1_twin.compare(ctx.packing, ctx.twin)
    return {
        "as_stated": relation["same_packing"],
        "twin": ctx.twin_file,
        "n_equal": relation["n_equal"],
        "side_equal": relation["side_equal"],
        "unequal_in_file_order": relation["unequal_in_file_order"],
        "twin_listing_relative_to_this_file": relation["second_file_listing_relative_to_first"],
    }


def t1(ctx):
    if ctx.twin is None:
        return {"as_stated": False, "twin_refused": ctx.twin_refusal}
    squares = list(ctx.squares)
    squares[0] = r1_frame.translate_square(ctx.form, squares[0], (D, Fraction(0)))
    moved = r1_read.Packing(ctx.form, ctx.n, ctx.side, squares, ctx.packing.ids, {})
    relation = r1_twin.compare(moved, ctx.twin)
    return {
        "as_stated": (
            not relation["same_packing"]
            and relation["side_equal"]
            and relation["unequal_in_file_order"] == {"count": 1, "first": [1]}
        ),
        "same_packing": relation["same_packing"],
        "unequal_in_file_order": relation["unequal_in_file_order"],
    }


# ------------------------------------------------------------------ reading controls


def _refusal(ctx, raw):
    try:
        packing = r1_read.READERS[ctx.kind](raw)
    except r1_read.Refusal as exc:
        return None, str(exc)
    return packing, None


def _side_twice(ctx):
    return f"{2 * ctx.side.numerator}/{2 * ctx.side.denominator}"


def _side_plus_one(ctx):
    return r1_fmt.frac(ctx.side + 1)


def _yaml_lines(ctx):
    lines = ctx.text.split("\n")
    side_at = [i for i, line in enumerate(lines) if line.startswith("  side: ")]
    starts = [i for i, line in enumerate(lines) if re.fullmatch(r"  - id: .*", line)]
    if len(side_at) != 1 or len(starts) != ctx.n:
        raise RuntimeError("the YAML text is not in the block style the edits assume")
    return lines, side_at[0], starts


def _json_tree(ctx):
    tree = json.loads(ctx.text)
    again, why = _refusal(ctx, json.dumps(tree, indent=1).encode())
    if again is None or again.side != ctx.side or norm(again.squares) != norm(ctx.squares):
        raise RuntimeError(f"the JSON document does not survive re-serialisation: {why}")
    return tree


def _json_side_swap(ctx, tree, replacement):
    text = json.dumps(tree, indent=1)
    old = json.dumps("side") + ": " + json.dumps(tree_side(ctx, tree))
    if text.count(old) != 1:
        raise RuntimeError("the side entry is not unique in the JSON text")
    return text.replace(old, replacement)


def tree_side(ctx, tree):
    return tree["side"] if ctx.kind == "centre-json" else tree["witness"]["side"]


def mutate(ctx, which):
    """The certificate's own document with one stated change, as bytes."""
    if ctx.kind == "witness-yaml":
        lines, side_at, starts = _yaml_lines(ctx)
        if which == "R1":
            end = len(lines)
            for i in range(starts[-1] + 1, len(lines)):
                if re.match(r"  [^ -]", lines[i]) or re.match(r"\S", lines[i]):
                    end = i
                    break
            tail = lines[end:] if end < len(lines) else [""]
            lines = lines[: starts[-1]] + tail
        elif which == "R2":
            lines[side_at] = "  side: " + _side_twice(ctx)
        elif which == "R3":
            lines[starts[1]] = lines[starts[0]]
        elif which == "R4":
            lines[side_at] = "  side: 17.5"
        elif which == "R5":
            at = next(i for i in range(starts[0], len(lines)) if lines[i].startswith("    - - "))
            body = lines[at][len("    - - ") :]
            body = "'+" + body[1:] if body.startswith("'") else "+" + body
            lines[at] = "    - - " + body
        elif which == "R6":
            lines.insert(side_at + 1, "  side: " + _side_plus_one(ctx))
        elif which == "R7":
            hits = [i for i, line in enumerate(lines) if line == "    origin: lower-left"]
            if len(hits) != 1:
                raise RuntimeError("origin line not unique")
            lines[hits[0]] = "    origin: container-center"
        return "\n".join(lines).encode()
    tree = _json_tree(ctx)
    witness = tree if ctx.kind == "centre-json" else tree["witness"]
    if which == "R1":
        witness["squares"].pop()
    elif which == "R2":
        witness["side"] = _side_twice(ctx)
    elif which == "R3":
        if ctx.kind == "centre-json":
            witness["squares"][0].append("0")
        else:
            witness["squares"][1]["id"] = witness["squares"][0]["id"]
    elif which == "R4":
        return _json_side_swap(ctx, tree, json.dumps("side") + ": 17.5").encode()
    elif which == "R5":
        if ctx.kind == "centre-json":
            witness["squares"][0][0] = "+" + witness["squares"][0][0]
        else:
            first = witness["squares"][0]["corners"][0]
            first[0] = "+" + first[0]
    elif which == "R6":
        both = (
            json.dumps("side") + ": " + json.dumps(tree_side(ctx, tree)) + ", "
            + json.dumps("side") + ": " + json.dumps(_side_plus_one(ctx))
        )
        return _json_side_swap(ctx, tree, both).encode()
    elif which == "R7":
        if ctx.kind == "centre-json":
            changed = witness["format"].replace("cos, sin]", "sin, cos]")
            if changed == witness["format"]:
                raise RuntimeError("format sentence has no 'cos, sin]'")
            witness["format"] = changed
        else:
            witness["coordinates"]["origin"] = "container-center"
    return json.dumps(tree, indent=1).encode()


REFUSAL_PHRASE = {
    "R1": lambda ctx: f"states {ctx.n} squares and {ctx.n - 1} are listed",
    "R3": lambda ctx: (
        "not an array of four scalars" if ctx.kind == "centre-json" else "duplicate square ids"
    ),
    "R4": lambda ctx: "resolves to float" if ctx.kind == "witness-yaml" else "not an integer",
    "R5": lambda ctx: "not a rational scalar",
    "R6": lambda ctx: "duplicate key",
    "R7": lambda ctx: (
        "format sentence not the one analysed"
        if ctx.kind == "centre-json"
        else "witness.coordinates.origin is"
    ),
}


def reading_refused(which):
    def run(ctx):
        raw = mutate(ctx, which)
        packing, why = _refusal(ctx, raw)
        phrase = REFUSAL_PHRASE[which](ctx)
        return {
            "as_stated": raw != ctx.raw and packing is None and phrase in (why or ""),
            "text_changed": raw != ctx.raw,
            "refused": packing is None,
            "refusal": why,
            "expected_phrase": phrase,
        }

    return run


def r2(ctx):
    raw = mutate(ctx, "R2")
    packing, why = _refusal(ctx, raw)
    if packing is None:
        return {"as_stated": False, "refusal": why}
    same = (
        packing.n == ctx.n
        and packing.side == ctx.side
        and norm(packing.squares) == norm(ctx.squares)
    )
    notes, base = packing.notes, ctx.packing.notes
    flagged = (
        not notes["side_written_in_lowest_terms"]
        and base["side_written_in_lowest_terms"]
        and notes["scalars_in_lowest_terms"] == base["scalars_in_lowest_terms"] - 1
        and notes["scalars"] == base["scalars"]
    )
    return {
        "as_stated": raw != ctx.raw and same and flagged,
        "text_changed": raw != ctx.raw,
        "values_equal": same,
        "only_the_side_flagged": flagged,
        "side_as_written": _side_twice(ctx)[:60] + "...",
    }


# ------------------------------------------------------------------ gross controls


def g1(ctx):
    squares = list(ctx.squares)
    squares[-1] = squares[0]
    dec, _, _ = r1_decide.decide(build(ctx, squares, ctx.side))
    verdict, reasons = dec.verdict()
    n = ctx.n
    carried = all(dec.margin[(k, n)] == ctx.dec.margin[(1, k)] for k in range(2, n))
    return {
        "as_stated": (
            verdict == "REFUSE"
            and reasons == [("overlapping", [(1, n)])]
            and dec.margin[(1, n)] == -1
            and dec.area_b.get((1, n)) == 1
            and carried
            and agree(dec)
        ),
        **brief(dec),
        "margin_1_n": r1_fmt.frac(dec.margin[(1, n)]),
        "area_1_n_by_b": r1_fmt.frac(dec.area_b.get((1, n), 0)),
        "margins_of_k_n_equal_those_of_1_k": carried,
    }


def g2(ctx):
    squares = list(ctx.squares)
    squares[0] = r1_frame.translate_square(ctx.form, squares[0], (ctx.side, Fraction(0)))
    dec, _, _ = r1_decide.decide(build(ctx, squares, ctx.side))
    verdict, reasons = dec.verdict()
    want = ctx.dec.clear[0][2] - ctx.side
    return {
        "as_stated": (
            verdict == "REFUSE"
            and reasons == [("crossing", [(1, "right")]), ("area-inside-below-1", [1])]
            and dec.clear[0][2] == want
            and dec.inside_b[0] == 0
            and agree(dec)
        ),
        **brief(dec),
        "right_clearance_of_square_1": r1_fmt.exact_and_sci(dec.clear[0][2]),
        "is_R1_less_S": dec.clear[0][2] == want,
        "area_inside_by_b": r1_fmt.frac(dec.inside_b[0]),
    }


def g3(ctx):
    squares = list(ctx.squares)
    first = squares[0]
    if ctx.form == "corners":
        squares[0] = ((first[0][0] + D, first[0][1]),) + tuple(first[1:])
    else:
        squares[0] = (first[0], first[1], first[2] + D, first[3])
    dec, _, _ = r1_decide.decide(build(ctx, squares, ctx.side))
    verdict, reasons = dec.verdict()
    return {
        "as_stated": (
            verdict == "REFUSE"
            and reasons == [("not-unit", [1])]
            and not dec.unit_a[0]
            and not dec.unit_b[0]
            and agree(dec)
        ),
        **brief(dec),
        "unit_by_a": dec.unit_a[0],
        "why_a": dec.why_a[0],
        "unit_by_b": dec.unit_b[0],
    }


def _g4(ctx, sq):
    if ctx.form == "corners":
        return (sq[3], sq[2], sq[1], sq[0])
    return (sq[0], sq[1], -sq[2], -sq[3])


def _g5(ctx, sq):
    if ctx.form == "corners":
        return (sq[1], sq[2], sq[3], sq[0])
    return (sq[0], sq[1], -sq[3], sq[2])


def _g6(ctx, sq):
    if ctx.form == "corners":
        return tuple((y, x) for x, y in sq)
    return (sq[1], sq[0], sq[3], sq[2])


def _g7(ctx, sq):
    side = ctx.side
    if ctx.form == "corners":
        return tuple((side - y, x) for x, y in sq)
    return (side - sq[1], sq[0], -sq[3], sq[2])


def _g8(ctx, sq):
    side = ctx.side
    if ctx.form == "corners":
        return tuple((side - x, y) for x, y in sq)
    return (side - sq[0], sq[1], -sq[2], sq[3])


SYMMETRIES = {
    # id: (transform, clearance permutation, corners files exchange the sense)
    "G4": (_g4, (0, 1, 2, 3), True),
    "G5": (_g5, (0, 1, 2, 3), False),
    "G6": (_g6, (1, 0, 3, 2), True),
    "G7": (_g7, (3, 0, 1, 2), False),
    "G8": (_g8, (2, 1, 0, 3), True),
}


def symmetry(which):
    transform, permutation, flips = SYMMETRIES[which]

    def run(ctx):
        squares = [transform(ctx, sq) for sq in ctx.squares]
        dec, _, _ = r1_decide.decide(build(ctx, squares, ctx.side))
        base = ctx.dec
        margins = dec.margin == base.margin
        clear = all(
            tuple(dec.clear[k]) == tuple(base.clear[k][p] for p in permutation)
            for k in range(ctx.n)
        )
        sign = -1 if (flips and ctx.form == "corners") else 1
        senses = dec.sense_a == [sign * s for s in base.sense_a] and dec.sense_b == [
            sign * s for s in base.sense_b
        ]
        return {
            "as_stated": (
                dec.verdict() == base.verdict() and margins and clear and senses and agree(dec)
            ),
            **brief(dec),
            "margins_equal": margins,
            "clearances_as_stated": clear,
            "senses_as_stated": senses,
            "counterclockwise_by_a": sum(1 for s in dec.sense_a if s > 0),
        }

    return run


def _contract(ctx, sq):
    if ctx.form == "corners":
        cx, cy = centre_of("corners", sq)
        return r1_frame.translate_square("corners", sq, (-cx / 100, -cy / 100))
    return (sq[0] * 99 / 100, sq[1] * 99 / 100, sq[2], sq[3])


def _upright(ctx, sq):
    cx, cy = centre_of(ctx.form, sq)
    if ctx.form == "corners":
        return (
            (cx - HALF, cy - HALF),
            (cx + HALF, cy - HALF),
            (cx + HALF, cy + HALF),
            (cx - HALF, cy + HALF),
        )
    return (cx, cy, Fraction(1), Fraction(0))


def against_closed_form(transform):
    def run(ctx):
        squares = [transform(ctx, sq) for sq in ctx.squares]
        packing = build(ctx, squares, ctx.side)
        dec, _, _ = r1_decide.decide(packing)
        verdict, reasons = dec.verdict()
        equal = frames_margin_equal(dec, r1_frame.of_packing(packing))
        overlapping = [items for kind, items in reasons if kind == "overlapping"]
        return {
            "as_stated": (
                equal and agree(dec) and verdict == "REFUSE" and bool(overlapping)
                and len(dec.margin) == ctx.n * (ctx.n - 1) // 2
            ),
            **brief(dec),
            "margins_equal_closed_form": equal,
            "overlapping_pairs": len(overlapping[0]) if overlapping else 0,
            "least_margin": r1_fmt.sci(min(dec.margin.values())),
        }

    return run


# ------------------------------------------------------------------ sharp side controls


def side_rule(ctx, lowering, squares=None, base=None, base_clear=None):
    """The side lowered by `lowering` with the squares as they are (patched)."""
    squares = ctx.squares if squares is None else squares
    base = ctx.base if base is None else base
    base_clear = ctx.dec.clear if base_clear is None else base_clear
    packing = build(ctx, squares, base[0].side - lowering)
    dec, _, _ = r1_decide.redecide(packing, base, set())
    verdict, reasons = dec.verdict()
    want_clear = [
        (c[0], c[1], c[2] - lowering, c[3] - lowering) for c in base_clear
    ]
    crossing = [
        (k + 1, WALLS[w]) for k in range(ctx.n) for w in range(4) if want_clear[k][w] < 0
    ]
    want_reasons = []
    if crossing:
        want_reasons = [
            ("crossing", crossing),
            ("area-inside-below-1", sorted({k for k, _ in crossing})),
        ]
    rule = (
        [tuple(c) for c in dec.clear] == want_clear
        and dec.margin == base[0].margin
        and reasons == want_reasons
        and verdict == ("REFUSE" if crossing else "ACCEPT")
        and agree(dec)
    )
    at_wall = [
        (k + 1, WALLS[w]) for k in range(ctx.n) for w in (2, 3) if dec.clear[k][w] == 0
    ]
    out = {
        "side_rule_holds": rule,
        "lowering": r1_fmt.exact_and_sci(lowering),
        **brief(dec),
        "crossing": {"count": len(crossing), "first": crossing[:12]},
        "at_right_or_top_wall_exactly": {"count": len(at_wall), "first": at_wall[:12]},
    }
    return out, dec, verdict


def s1(which):
    def run(ctx):
        lowering = {
            "S0": Fraction(1),
            "S1a": D,
            "S1b": Fraction(1, ctx.side.denominator),
            "S1c": ctx.W,
            "S1d": ctx.W + D,
            "S1e": ctx.side - ctx.claim,
            "S1f": ctx.side - ctx.claim + Fraction(1, 10**12),
        }[which]
        out, dec, verdict = side_rule(ctx, lowering)
        ok = out["side_rule_holds"]
        if which == "S1a":
            out["branch"] = "touching wall (W = 0)" if ctx.W == 0 else "W above 0"
            out["prior_refused"] = verdict == "REFUSE"
        elif which == "S1c":
            ok = ok and verdict == ctx.dec.verdict()[0] and out["at_right_or_top_wall_exactly"]["count"] > 0
        elif which in ("S0", "S1d"):
            ok = ok and verdict == "REFUSE"
        elif which == "S1e":
            out["prior_accepted"] = verdict == "ACCEPT"
        elif which == "S1f":
            out["prior_refused"] = verdict == "REFUSE"
        out = {"as_stated": ok, **out}
        return out

    return run


def s2c(ctx):
    shift = (-ctx.Wall[0], -ctx.Wall[1])
    squares = [r1_frame.translate_square(ctx.form, sq, shift) for sq in ctx.squares]
    packing = build(ctx, squares, ctx.side - ctx.SIGMA)
    result = r1_decide.decide(packing)
    dec = result[0]
    want = [
        (c[0] - ctx.Wall[0], c[1] - ctx.Wall[1], c[2] + ctx.Wall[0] - ctx.SIGMA,
         c[3] + ctx.Wall[1] - ctx.SIGMA)
        for c in ctx.dec.clear
    ]
    contacts = [sum(1 for c in dec.clear if c[w] == 0) for w in range(4)]
    ok = (
        dec.verdict() == ctx.dec.verdict()
        and dec.margin == ctx.dec.margin
        and [tuple(c) for c in dec.clear] == want
        and contacts[0] > 0
        and contacts[1] > 0
        and contacts[2] + contacts[3] > 0
        and agree(dec)
    )
    ctx.s2 = (squares, result, want)
    return {
        "as_stated": ok,
        **brief(dec),
        "translation": [r1_fmt.sci(shift[0]), r1_fmt.sci(shift[1])],
        "side_lowered_by_SIGMA": r1_fmt.exact_and_sci(ctx.SIGMA),
        "margins_equal": dec.margin == ctx.dec.margin,
        "contacts_left_bottom_right_top": contacts,
    }


def s2p(ctx):
    if not hasattr(ctx, "s2"):
        return {"as_stated": False, "error": "S2c did not run"}
    squares, result, want = ctx.s2
    out, dec, verdict = side_rule(ctx, D, squares=squares, base=result, base_clear=want)
    return {"as_stated": out["side_rule_holds"] and verdict == "REFUSE", **out}


# ------------------------------------------------------------------ sharp pair controls


def _moved_pair(ctx, i, j, mover, target):
    """Square `mover` of the pair (i, j), 0-based, moved to the margin `target`."""
    other = i if mover == j else j
    shift = r1_frame.closing_shift(ctx.frames[other], ctx.frames[mover], target)
    return shift


def _patched_with(ctx, mover, shift):
    squares = list(ctx.squares)
    squares[mover] = r1_frame.translate_square(ctx.form, squares[mover], shift)
    packing = build(ctx, squares, ctx.side)
    dec, _, _ = r1_decide.redecide(packing, ctx.base, {mover})
    frames = r1_frame.of_packing(packing)
    return dec, frames


def p0p(ctx):
    touching = sorted(key for key, value in ctx.dec.margin.items() if value == 0)
    for i, j in touching:
        shift = _moved_pair(ctx, i - 1, j - 1, j - 1, -D)
        if shift is None:
            continue
        dec, frames = _patched_with(ctx, j - 1, shift)
        verdict, reasons = dec.verdict()
        closed = r1_frame.margin(frames[i - 1], frames[j - 1])
        return {
            "as_stated": (
                verdict == "REFUSE"
                and dec.margin[(i, j)] == -D
                and closed == -D
                and dec.class_b[(i, j)] == "overlapping"
                and agree(dec)
            ),
            "pair": [i, j],
            "touching_pairs_in_the_certificate": len(touching),
            **brief(dec),
            "margin": r1_fmt.frac(dec.margin[(i, j)]),
            "closed_form": r1_fmt.frac(closed),
            "class_by_b": dec.class_b[(i, j)],
        }
    return {
        "as_stated": True,
        "no_subject": "no pair of the certificate touches",
        "touching_pairs_in_the_certificate": len(touching),
    }


def _eligible(ctx, mover, partner, shift):
    """Every other margin and every clearance of `mover` exceeds the shift's length.

    It is enough to test the least of the other margins and the least clearance.
    """
    length2 = shift[0] * shift[0] + shift[1] * shift[1]
    others = [value for value, other in ctx.two_least[mover] if other != partner]
    for value in (others[0] if others else None, min(ctx.dec.clear[mover])):
        if value is not None and (value <= 0 or value * value <= length2):
            return False
    return True


def choose_pair(ctx):
    if hasattr(ctx, "p1"):
        return ctx.p1
    positive = sorted((value, key) for key, value in ctx.dec.margin.items() if value > 0)
    choice = None
    for rank, (value, (i, j)) in enumerate(positive):
        for mover, partner in ((j - 1, i - 1), (i - 1, j - 1)):
            past = r1_frame.closing_shift(ctx.frames[partner], ctx.frames[mover], -D)
            if past is not None and _eligible(ctx, mover, partner, past):
                choice = {"pair": (i, j), "mover": mover, "partner": partner, "rank": rank,
                          "margin": value, "eligible": True}
                break
        if choice:
            break
    if choice is None and positive:
        value, (i, j) = positive[0]
        choice = {"pair": (i, j), "mover": j - 1, "partner": i - 1, "rank": 0,
                  "margin": value, "eligible": False}
    ctx.p1 = choice
    return choice


def p1(target_past):
    def run(ctx):
        choice = choose_pair(ctx)
        if choice is None:
            return {"as_stated": False, "error": "no pair with a positive margin"}
        i, j = choice["pair"]
        target = -D if target_past else Fraction(0)
        shift = r1_frame.closing_shift(
            ctx.frames[choice["partner"]], ctx.frames[choice["mover"]], target
        )
        dec, frames = _patched_with(ctx, choice["mover"], shift)
        verdict, reasons = dec.verdict()
        closed = r1_frame.margin(frames[i - 1], frames[j - 1])
        exact = dec.margin[(i, j)] == target and closed == target
        if target_past:
            if choice["eligible"]:
                ok = (
                    verdict == "REFUSE"
                    and reasons == [("overlapping", [(i, j)])]
                    and dec.area_b.get((i, j), 0) > 0
                )
            else:
                ok = verdict == "REFUSE" and any(
                    kind == "overlapping" and (i, j) in items for kind, items in reasons
                )
        else:
            if choice["eligible"]:
                ok = (
                    (verdict, reasons) == ctx.dec.verdict()
                    and reasons == []
                    and dec.class_b[(i, j)] == "touching"
                    and touching_count(dec) == touching_count(ctx.dec) + 1
                )
            else:
                ok = dec.class_b[(i, j)] == "touching"
        return {
            "as_stated": ok and exact and agree(dec),
            "pair": [i, j],
            "square_moved": choice["mover"] + 1,
            "eligible": choice["eligible"],
            "rank_among_positive_margins": choice["rank"],
            "margin_in_the_certificate": r1_fmt.exact_and_sci(choice["margin"]),
            "shift_length_squared": r1_fmt.sci(shift[0] * shift[0] + shift[1] * shift[1]),
            **brief(dec),
            "margin": r1_fmt.frac(dec.margin[(i, j)]),
            "closed_form": r1_fmt.frac(closed),
            "class_by_b": dec.class_b[(i, j)],
            "area_by_b": r1_fmt.sci(dec.area_b.get((i, j), Fraction(0))),
            "touching_pairs": touching_count(dec),
        }

    return run


# ------------------------------------------------------------------ sharp wall controls


def choose_at_wall(ctx, w):
    key = ("w1", w)
    if key in ctx.cache:
        return ctx.cache[key]
    order = sorted((ctx.dec.clear[k][w], k) for k in range(ctx.n))
    choice = None
    for value, k in order:
        reach = value + D
        if not ctx.two_least[k] or ctx.two_least[k][0][0] > reach:
            choice = (k, value)
            break
    ctx.cache[key] = choice
    return choice


def w1(w, past):
    wall = WALLS[w]

    def run(ctx):
        choice = choose_at_wall(ctx, w)
        if choice is None:
            return {"as_stated": True, "no_subject": "no eligible square at this wall"}
        k, value = choice
        amount = value + D if past else value
        dec, _ = _patched_with(ctx, k, r1_frame.wall_shift(wall, amount))
        verdict, reasons = dec.verdict()
        if past:
            ok = (
                verdict == "REFUSE"
                and reasons == [("crossing", [(k + 1, wall)]), ("area-inside-below-1", [k + 1])]
                and dec.clear[k][w] == -D
            )
        else:
            ok = (
                (verdict, reasons) == ctx.dec.verdict()
                and reasons == []
                and dec.clear[k][w] == 0
                and dec.wall_b[k][w][0] == "touching"
                and dec.clear[k][OPPOSITE[w]] == ctx.dec.clear[k][OPPOSITE[w]] + value
            )
        return {
            "as_stated": ok and agree(dec),
            "square": k + 1,
            "clearance_in_the_certificate": r1_fmt.exact_and_sci(value),
            "least_clearance_at_the_wall": r1_fmt.exact_and_sci(ctx.Wall[w]),
            **brief(dec),
            "clearance": r1_fmt.frac(dec.clear[k][w]),
            "class_by_b": dec.wall_b[k][w][0],
        }

    return run


def w2(w, past):
    wall = WALLS[w]

    def run(ctx):
        amount = ctx.Wall[w] + (D if past else 0)
        shift = r1_frame.wall_shift(wall, amount)
        squares = [r1_frame.translate_square(ctx.form, sq, shift) for sq in ctx.squares]
        dec, _, _ = r1_decide.decide(build(ctx, squares, ctx.side))
        verdict, reasons = dec.verdict()
        opposite = OPPOSITE[w]
        want = []
        for c in ctx.dec.clear:
            row = list(c)
            row[w] -= amount
            row[opposite] += amount
            want.append(tuple(row))
        crossing = [(k + 1, wall) for k in range(ctx.n) if want[k][w] < 0]
        want_reasons = []
        if crossing:
            want_reasons = [
                ("crossing", crossing),
                ("area-inside-below-1", [k for k, _ in crossing]),
            ]
        ok = (
            [tuple(c) for c in dec.clear] == want
            and dec.margin == ctx.dec.margin
            and agree(dec)
        )
        if past:
            ok = ok and verdict == "REFUSE" and reasons == want_reasons and bool(crossing)
        else:
            ok = ok and (verdict, reasons) == ctx.dec.verdict()
        return {
            "as_stated": ok,
            "translated_by": r1_fmt.exact_and_sci(amount),
            **brief(dec),
            "margins_equal": dec.margin == ctx.dec.margin,
            "clearances_as_stated": [tuple(c) for c in dec.clear] == want,
            "at_the_wall_exactly": sum(1 for c in dec.clear if c[w] == 0),
        }

    return run


# ------------------------------------------------------------------ the sweeps


def _raw_a(ctx, square):
    if ctx.form == "corners":
        return r1_axes.from_corners(square)
    return r1_axes.from_centre(*square)


def _raw_b(ctx, square):
    if ctx.form == "corners":
        points = r1_area.points_from_corners(square)
    else:
        points = r1_area.points_from_centre(*square)
    return r1_area.counterclockwise(points)


def _raw_frame(ctx, square):
    if ctx.form == "corners":
        return r1_frame.from_corners(square)
    return r1_frame.from_centre(*square)


def pall(ctx):
    _, sq_a, sq_b = ctx.base
    failures = []
    closings = 0
    not_closed = 0
    pairs = 0
    for i in range(ctx.n):
        for j in range(i + 1, ctx.n):
            pairs += 1
            for target, want in ((Fraction(0), "touching"), (-D, "overlapping")):
                shift = r1_frame.closing_shift(ctx.frames[i], ctx.frames[j], target)
                if shift is None:
                    not_closed += 1
                    continue
                closings += 1
                moved = r1_frame.translate_square(ctx.form, ctx.squares[j], shift)
                am = _raw_a(ctx, moved)
                bm = _raw_b(ctx, moved)
                one = r1_area.pair(sq_b[i], bm)
                two = r1_area.pair(bm, sq_b[i])
                ok = (
                    am.unit
                    and r1_axes.margin(sq_a[i], am) == target
                    and r1_axes.margin(am, sq_a[i]) == target
                    and r1_frame.margin(ctx.frames[i], _raw_frame(ctx, moved)) == target
                    and one[0] == want
                    and one == two
                    and (one[1] > 0) == (target < 0)
                )
                if not ok and len(failures) < 10:
                    failures.append([i + 1, j + 1, r1_fmt.frac(target)])
    expected = ctx.n * (ctx.n - 1) // 2
    return {
        "as_stated": not failures and not_closed == 0 and pairs == expected
        and closings == 2 * expected,
        "pairs": pairs,
        "closings": closings,
        "pairs_with_coincident_centres": not_closed // 2,
        "failures": failures,
    }


def wall_sweep(ctx):
    failures = []
    moves = 0
    for k in range(ctx.n):
        for w, wall in enumerate(WALLS):
            for extra, want in ((Fraction(0), "touching"), (D, "overlapping")):
                moves += 1
                amount = ctx.dec.clear[k][w] + extra
                moved = r1_frame.translate_square(
                    ctx.form, ctx.squares[k], r1_frame.wall_shift(wall, amount)
                )
                am = _raw_a(ctx, moved)
                bm = _raw_b(ctx, moved)
                inside = r1_area.area_inside_box(bm, ctx.side)
                ok = (
                    am.unit
                    and r1_axes.clearances(am, ctx.side)[w] == -extra
                    and r1_area.walls(bm, ctx.side)[w][0] == want
                    and ((inside == 1) if extra == 0 else (inside < 1))
                )
                if not ok and len(failures) < 10:
                    failures.append([k + 1, wall, r1_fmt.frac(extra)])
    return {
        "as_stated": not failures and moves == 8 * ctx.n,
        "squares": ctx.n,
        "moves": moves,
        "failures": failures,
    }


# ------------------------------------------------------------------ the list


IMPLEMENTED = {
    "C0": c0,
    "K1": k1,
    "T0": t0,
    "T1": t1,
    "R1": reading_refused("R1"),
    "R2": r2,
    "R3": reading_refused("R3"),
    "R4": reading_refused("R4"),
    "R5": reading_refused("R5"),
    "R6": reading_refused("R6"),
    "R7": reading_refused("R7"),
    "G1": g1,
    "G2": g2,
    "G3": g3,
    "G4": symmetry("G4"),
    "G5": symmetry("G5"),
    "G6": symmetry("G6"),
    "G7": symmetry("G7"),
    "G8": symmetry("G8"),
    "G9": against_closed_form(_contract),
    "G10": against_closed_form(_upright),
    "S0": s1("S0"),
    "S1a": s1("S1a"),
    "S1b": s1("S1b"),
    "S1c": s1("S1c"),
    "S1d": s1("S1d"),
    "S1e": s1("S1e"),
    "S1f": s1("S1f"),
    "S2c": s2c,
    "S2p": s2p,
    "P0p": p0p,
    "P1c": p1(False),
    "P1p": p1(True),
    "PALL": pall,
    "WALL": wall_sweep,
}
for _w, _name in enumerate(WALLS):
    IMPLEMENTED[f"W1c-{_name}"] = w1(_w, False)
    IMPLEMENTED[f"W1p-{_name}"] = w1(_w, True)
    IMPLEMENTED[f"W2c-{_name}"] = w2(_w, False)
    IMPLEMENTED[f"W2p-{_name}"] = w2(_w, True)


def main(argv):
    if len(argv) != 5:
        raise SystemExit(__doc__)
    plan_path, label, pin_root, out_path = argv[1:]
    started = time.process_time()
    with open(plan_path, "rb") as handle:
        plan_raw = handle.read()
    plan = json.loads(plan_raw)
    planned = [control["id"] for control in plan["controls"]]
    if sorted(planned) != sorted(IMPLEMENTED) or len(set(planned)) != len(planned):
        raise SystemExit("the plan's controls and the program's differ")
    spec = plan["files"][label]
    twin_spec = plan["files"][spec["twin"]]
    path = os.path.join(pin_root, spec["pin_dir"], spec["path"])
    twin_path = os.path.join(pin_root, twin_spec["pin_dir"], twin_spec["path"])

    ctx = Ctx()
    ctx.kind = spec["form"]
    try:
        ctx.packing, ctx.raw = r1_read.read_file(path, ctx.kind)
    except r1_read.Refusal as exc:
        r1_fmt.write_json(out_path, {
            "program": "r1_controls.py", "label": label, "file": spec["path"],
            "summary": "CERTIFICATE_NOT_READ", "refusal": str(exc),
        })
        print("CERTIFICATE_NOT_READ", label, exc)
        return 1
    ctx.text = ctx.packing.text
    ctx.form = ctx.packing.form
    ctx.n = ctx.packing.n
    ctx.side = ctx.packing.side
    ctx.squares = norm(ctx.packing.squares)
    ctx.claim = Fraction(spec["claim"])
    ctx.twin_file = twin_spec["path"]
    try:
        ctx.twin, _ = r1_read.read_file(twin_path, twin_spec["form"])
        ctx.twin_refusal = None
    except r1_read.Refusal as exc:
        ctx.twin, ctx.twin_refusal = None, str(exc)
    ctx.base = r1_decide.decide(ctx.packing)
    ctx.dec = ctx.base[0]
    ctx.frames = r1_frame.of_packing(ctx.packing)
    ctx.Wall = [min(c[w] for c in ctx.dec.clear) for w in range(4)]
    ctx.W = min(ctx.Wall[2], ctx.Wall[3])
    ctx.SIGMA = min(ctx.Wall[0] + ctx.Wall[2], ctx.Wall[1] + ctx.Wall[3])
    ctx.cache = {}
    by_square = [[] for _ in range(ctx.n)]
    for (i, j), value in ctx.dec.margin.items():
        by_square[i - 1].append((value, j - 1))
        by_square[j - 1].append((value, i - 1))
    # each square's two least margins, with the other square of each
    ctx.two_least = [sorted(items)[:2] for items in by_square]

    verdict, reasons = ctx.dec.verdict()
    receipt = {
        "program": "r1_controls.py",
        "lane": "R1 (c-review-1005-1117)",
        "label": label,
        "file": spec["path"],
        "form": ctx.kind,
        "sha256": hashlib.sha256(ctx.raw).hexdigest(),
        "plan_sha256": hashlib.sha256(plan_raw).hexdigest(),
        "certificate": {
            "verdict": verdict,
            "reasons": reasons_text(reasons),
            "n": ctx.n,
            "least_clearance_left_bottom_right_top": [r1_fmt.sci(v) for v in ctx.Wall],
            "W": r1_fmt.exact_and_sci(ctx.W),
            "SIGMA": r1_fmt.exact_and_sci(ctx.SIGMA),
            "touching_pairs": touching_count(ctx.dec),
        },
        "controls": [],
    }
    not_stated = []
    not_run = []
    tier = spec["tier"]
    receipt["tier"] = tier
    for control in plan["controls"]:
        if tier == "twin" and not control["on_twins"]:
            not_run.append(control["id"])
            continue
        t0_cpu = time.process_time()
        try:
            outcome = IMPLEMENTED[control["id"]](ctx)
        except Exception as exc:  # a control that cannot run is a control not as stated
            outcome = {"as_stated": False, "error": f"{type(exc).__name__}: {exc}"}
        entry = {"id": control["id"], "stated": control["stated"]}
        entry.update(outcome)
        entry["cpu_seconds"] = round(time.process_time() - t0_cpu, 1)
        receipt["controls"].append(entry)
        if not outcome["as_stated"]:
            not_stated.append(control["id"])
    receipt["as_stated"] = len(planned) - len(not_run) - len(not_stated)
    receipt["of"] = len(planned) - len(not_run)
    receipt["run_on_the_reports_first_file_only"] = not_run
    receipt["not_as_stated"] = not_stated
    receipt["summary"] = "EVERY_CONTROL_AS_STATED" if not not_stated else "NOT_AS_STATED"
    receipt["cpu_seconds"] = round(time.process_time() - started, 1)
    r1_fmt.write_json(out_path, receipt)
    print(receipt["summary"], label, f"{receipt['as_stated']} of {receipt['of']}",
          f"cpu {receipt['cpu_seconds']} s", not_stated)
    return 0 if not not_stated else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
