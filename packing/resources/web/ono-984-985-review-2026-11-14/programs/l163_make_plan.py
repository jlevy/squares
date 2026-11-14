"""Lane L163 controls plan: states each control and its outcome before any is run.

Usage: l163_make_plan.py OUT.json LABEL CHECK.json FACTS.json [LABEL CHECK.json FACTS.json ...]

Decides nothing. Every expectation comes from the check receipt (the unmodified file's
contacts and margin digests) or from the plan facts (closed-form outcomes).
"""

from __future__ import annotations

import json
import sys

DELTA = "1/1000000000000000000000000000000"
TRANSPOSE = {"left": "bottom", "bottom": "left", "right": "top", "top": "right"}
TURN = {"left": "bottom", "bottom": "right", "right": "top", "top": "left"}


def plan_for(label: str, check: dict, facts: dict) -> list[dict]:  # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
    n = facts["n"]
    main = check["main"]
    contacts = [list(x) for x in main["wall_contacts"]]
    mdig = main["margin_list_sha256"]
    cdig = main["clearance_multiset_sha256"]

    def lb(cs: list[list]) -> list[list]:  # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
        return [x for x in cs if x[1] in ("left", "bottom")]  # pyright: ignore[reportUnknownVariableType]

    out: list[dict] = []  # pyright: ignore[reportMissingTypeArgument]

    def add(cid: str, what: str, stated: str, **expect: object) -> None:
        out.append({"id": cid, "what": what, "stated": stated, "expect": expect})

    g1 = [x for x in contacts if x[0] != n] + [[n, w] for w in facts["G1"]["contacts_square_1"]]
    add(
        "G1",
        f"square {n} given square 1's centre and t",
        f"refused: exactly the pair (1, {n}) overlapping, margin -1, B area 1; contacts {sorted(g1)}",
        verdict="REFUSE",
        overlapping=[[1, n]],
        touching=[],
        margin_of={"pair": [1, n], "value": "-1/1", "area_b": "1"},
        contacts=sorted(g1),
    )
    add(
        "G2",
        "square 1 translated by (S, 0)",
        "refused: square 1 across the right wall by both methods and not inside by B's area; no pair overlapping or touching; other contacts unchanged",
        verdict="REFUSE",
        overlapping=[],
        touching=[],
        crossings=[[1, "right"]],
        contacts=sorted(x for x in contacts if x[0] != 1),
    )
    add("G3", f"square {n}'s entry deleted", f"the reader refuses: {n - 1} entries", reader_refuses_with="entries")
    add("G4", "the side written as 2p/2q", "the reader refuses: not in lowest terms", reader_refuses_with="lowest terms")
    g5 = facts["G5"]
    k = g5["square"]
    for sign, cid in (("plus", "G5a"), ("minus", "G5b")):
        f = g5[sign]
        cross = [[k, w] for w in f["crossing_walls"]]
        after = sorted([x for x in contacts if x[0] != k] + [[k, w] for w in f["contact_walls"]])
        verdict = "REFUSE" if cross else "ACCEPT"
        add(
            cid,
            f"square {k} (touching the left wall, t = {g5['t']}) with t {'+' if sign == 'plus' else '-'} 1e-30",
            f"{'refused' if cross else 'accepted'}: square {k}'s left clearance exactly {f['clearances_sci'][0]}"
            + (f", across the left wall by both" if cross else ", off the wall by both")
            + "; no pair changes class",
            verdict=verdict,
            overlapping=[],
            touching=[],
            crossings=cross,
            contacts=after,
            clearances_of={"square": k, "values": f["clearances"]},
        )
    g6 = facts["G6"]
    add(
        "G6",
        "every t negated (the rotation read the other way)",
        f"refused: exactly {g6['overlapping_pairs']} pairs overlapping by both methods (list digest {g6['overlapping_list_sha256'][:8]}), none touching; every square still inside, contacts and clearances unchanged",
        verdict="REFUSE",
        overlapping_count=g6["overlapping_pairs"],
        overlapping_sha256=g6["overlapping_list_sha256"],
        touching=[],
        crossings=[],
        contacts=sorted(contacts),
        clearance_multiset_sha256=cdig,
    )
    add("G7", "the .cert twin's side altered in one digit, kept in lowest terms", "refused: the twin differs from the JSON file", twin_differs=True)
    add(
        "G8",
        "every square transposed: (cx, cy, t) -> (cy, cx, -t)",
        "accepted; contacts transposed; the margin list unchanged",
        verdict="ACCEPT",
        overlapping=[],
        touching=[],
        contacts=sorted([x[0], TRANSPOSE[x[1]]] for x in contacts),
        margin_list_sha256=mdig,
    )
    for cid, form in (("G9", "(t + 1)/(1 - t), the angle plus 90 degrees"), ("G10", "(t - 1)/(1 + t), the angle less 90 degrees")):
        add(
            cid,
            f"every t replaced by {form}",
            "accepted; the same squares: contacts, margin list and clearance list unchanged",
            verdict="ACCEPT",
            overlapping=[],
            touching=[],
            contacts=sorted(contacts),
            margin_list_sha256=mdig,
            clearance_multiset_sha256=cdig,
        )
    add(
        "G11",
        "the packing turned a quarter about the box centre: (cx, cy, t) -> (S - cy, cx, t)",
        "accepted; contacts turned (left to bottom, bottom to right, right to top, top to left); margin list unchanged",
        verdict="ACCEPT",
        overlapping=[],
        touching=[],
        contacts=sorted([x[0], TURN[x[1]]] for x in contacts),
        margin_list_sha256=mdig,
    )
    s1 = facts["S1"]
    for cid, what in (
        ("S1a", "the side lowered by one unit of its own last place"),
        ("S1b", "the side lowered by 1e-30"),
        ("S1c", f"the side set to its 12-place floor, {facts['side']['floor12']}"),
    ):
        cr = s1[cid]["crossing"]
        add(
            cid,
            what,
            f"refused: exactly {cr} across, by both; pairs unchanged",
            verdict="REFUSE",
            overlapping=[],
            touching=[],
            crossings=sorted(cr),
            contacts=sorted(lb(contacts) + s1[cid]["touching_after"]),
            margin_list_sha256=mdig,
        )
    add(
        "S1d",
        f"the side set to its 12-place ceiling, the claim {facts['side']['ceil12']}",
        f"accepted; contacts only {s1['S1d']['contacts_after']}",
        verdict="ACCEPT",
        overlapping=[],
        touching=[],
        crossings=[],
        contacts=sorted(s1["S1d"]["contacts_after"]),
        margin_list_sha256=mdig,
    )
    s4 = facts["S4"]
    pair = s4["pair"]
    add(
        "S4c",
        f"square {s4['moving']} moved toward square {s4['toward']} along their centre line to exact contact",
        f"accepted: the pair {pair} alone touching by both, margin exactly 0; contacts unchanged",
        verdict="ACCEPT",
        overlapping=[],
        touching=[pair],
        margin_of={"pair": pair, "value": "0/1", "area_b": "0"},
        contacts=sorted(contacts),
        move={"moving": s4["moving"], "toward": s4["toward"], "delta": "0/1"},
    )
    add(
        "S4p",
        "the same, 1e-30 past contact",
        f"refused: the pair {pair} alone overlapping by both, margin exactly -1e-30; contacts unchanged",
        verdict="REFUSE",
        overlapping=[pair],
        touching=[],
        margin_of={"pair": pair, "value": "-" + DELTA},
        contacts=sorted(contacts),
        move={"moving": s4["moving"], "toward": s4["toward"], "delta": DELTA},
    )
    s5 = facts["S5"]
    add(
        "S5",
        f"every positive pair below {s5['threshold']} closed along its centre line, square j toward square i (pair-level)",
        f"{s5['pairs']} of {s5['pairs']}: touching at contact by both, margin exactly 0; overlapping past by both, margin exactly -1e-30; closing times digest {s5['closing_times_sha256'][:8]}",
        pairs=s5["pairs"],
        closing_times_sha256=s5["closing_times_sha256"],
    )
    s6 = facts["S6"]
    add(
        "S6",
        "every square moved to its nearest wall by its clearance, and 1e-30 past (square-level)",
        f"{n} of {n}: contact at, crossing past, by both; clearance exactly 0 and -1e-30; inside by B's area at contact, not past",
        squares=n,
        nearest_list_sha256=s6["list_sha256"],
    )
    return out


def main() -> None:
    out = sys.argv[1]
    args = sys.argv[2:]
    plan: dict[str, object] = {"lane": "L163", "program": "l163_make_plan.py", "delta": DELTA, "counts": {}}
    for k in range(0, len(args), 3):
        label, check_path, facts_path = args[k : k + 3]
        with open(check_path, encoding="utf-8") as fh:
            check = json.load(fh)
        with open(facts_path, encoding="utf-8") as fh:
            facts = json.load(fh)
        plan["counts"][label] = plan_for(label, check, facts)  # pyright: ignore[reportIndexIssue]
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("{\n")
        fh.write(f' "lane": "L163",\n "program": "l163_make_plan.py",\n "delta": "{DELTA}",\n "counts": {{\n')
        labels = list(plan["counts"])  # pyright: ignore[reportArgumentType]
        for li, label in enumerate(labels):
            fh.write(f'  "{label}": [\n')
            rows = plan["counts"][label]  # pyright: ignore[reportIndexIssue]
            for ri, c in enumerate(rows):
                fh.write("   " + json.dumps(c, sort_keys=False) + ("," if ri < len(rows) - 1 else "") + "\n")
            fh.write("  ]" + ("," if li < len(labels) - 1 else "") + "\n")
        fh.write(" }\n}\n")
    with open(out, encoding="utf-8") as fh:
        assert json.load(fh) == json.loads(json.dumps(plan))
    print("plan", {k: len(v) for k, v in plan["counts"].items()})  # pyright: ignore[reportAttributeAccessIssue]


if __name__ == "__main__":
    main()
