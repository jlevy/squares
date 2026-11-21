"""Lane r1052's self-test: the reader, both methods and the third formulation against
answers derived by hand, and broken packings that must be refused. It reads no
certificate.

Usage: r1052_selftest.py OUT_JSON [SCRATCH_DIR]
"""

from __future__ import annotations

import json
import random
import sys
import tempfile
import time
from fractions import Fraction as F
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import r1052_check as check  # noqa: E402
import r1052_clip as clip  # noqa: E402
import r1052_decide as decide_mod  # noqa: E402
import r1052_geom as geom  # noqa: E402
import r1052_poses as poses_a  # noqa: E402
import r1052_reader as reader  # noqa: E402
import r1052_writer as writer  # noqa: E402

RESULTS: list[tuple[str, bool]] = []


def ok(name: str, cond: bool) -> None:
    RESULTS.append((name, bool(cond)))


def refused(name: str, fn: Any, data: bytes, needle: str) -> None:
    try:
        fn(data)
    except reader.Refused as exc:
        ok(name, needle in str(exc))
        return
    ok(name, False)


def a_margin(p: tuple[F, F, F, F], r: tuple[F, F, F, F]) -> F:
    return poses_a.margin(poses_a.integer_pose(*p), poses_a.integer_pose(*r))


def b_pair(p: tuple[F, F, F, F], r: tuple[F, F, F, F]) -> tuple[str, F, F | None]:
    cp, cr = clip.corners_from_pose(*p), clip.corners_from_pose(*r)
    cls, area2, g2 = clip.pair(cp, cr)
    return cls, clip.fr(area2) / 2, (clip.fr(g2) if g2 is not None else None)


def pair_case(name: str, p: Any, r: Any, margin: F, cls: str, area: F, gap2: F | None) -> None:
    m = a_margin(p, r)
    ok(f"{name}: A margin {margin}", m == margin)
    ok(f"{name}: A class", poses_a.classify(m) == cls)
    ok(f"{name}: geom margin", geom.margin(p, r) == margin)
    ok(f"{name}: A symmetric", a_margin(r, p) == margin)
    got = b_pair(p, r)
    ok(f"{name}: B class", got[0] == cls)
    ok(f"{name}: B area {area}", got[1] == area)
    ok(f"{name}: B gap squared {gap2}", got[2] == gap2)
    back = b_pair(r, p)
    ok(f"{name}: B symmetric", back == got)


def test_reader() -> None:
    side = F(5, 2)
    poses = [(F(1, 2), F(1, 2), F(1), F(0)), (F(3, 2), F(3, 2), F(3, 5), F(4, 5))]
    j = writer.form_j(side, poses)
    got = reader.read_form_j(j)
    ok("J read: n", got["n"] == 2)
    ok("J read: side", got["side"] == side)
    ok("J read: poses", got["poses"] == poses)
    ok("J read: all canonical", got["noncanonical"] == [])
    ok("J read: blob id of empty", reader.git_blob_id(b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")
    ok("J read: blob id of hello", reader.git_blob_id(b"hello\n") == "ce013625030ba8dba906f756967f9e9ca394464a")
    text = j.decode()
    cases = [
        ("J dup key", text.replace('"n": 2,', '"n": 2, "n": 2,', 1), "twice"),
        ("J float", text.replace('"side": "5/2"', '"side": 2.5', 1), "fraction or exponent"),
        ("J exponent", text.replace('"n": 2', '"n": 2e0', 1), "fraction or exponent"),
        ("J NaN", text.replace('"side": "5/2"', '"side": NaN', 1), "non-finite"),
        ("J extra key", text.replace('"n": 2,', '"n": 2, "origin": "x",', 1), "unexpected"),
        ("J missing key", text.replace('"square_size": "1",', "", 1), "missing"),
        ("J n mismatch", text.replace('"n": 2', '"n": 3', 1), "3 and 2"),
        ("J n bool", text.replace('"n": 2', '"n": true', 1), "positive integer"),
        ("J number scalar", text.replace('"1/2"', "0", 1), "not a string"),
        ("J plus sign", text.replace('"1/2"', '"+1/2"', 1), "not an exact scalar"),
        ("J leading zero", text.replace('"1/2"', '"01/2"', 1), "not an exact scalar"),
        ("J zero denominator", text.replace('"1/2"', '"1/0"', 1), "not an exact scalar"),
        ("J exponent string", text.replace('"1/2"', '"5e-1"', 1), "not an exact scalar"),
        ("J square size", text.replace('"square_size": "1"', '"square_size": "2"', 1), "square_size"),
        ("J five scalars", text.replace('"0"\n  ]', '"0",\n   "0"\n  ]', 1), "four scalars"),
        ("J top list", "[" + text + "]", "not an object"),
    ]
    for name, mutated, needle in cases:
        ok(f"{name}: mutation applied", mutated != text)
        refused(name, reader.read_form_j, mutated.encode(), needle)
    refused("J not UTF-8", reader.read_form_j, j.replace(b"control", b"contr\xffl"), "UTF-8")
    two = reader.read_form_j(text.replace('"side": "5/2"', '"side": "10/4"', 1).encode())
    ok("J side 10/4: value", two["side"] == side)
    ok("J side 10/4: flagged", two["noncanonical"] == ["side"])
    dec = reader.read_form_j(text.replace('"side": "5/2"', '"side": "2.50"', 1).encode())
    ok("J decimal side: value", dec["side"] == side and dec["scalar_forms"].get("decimal") == 1)

    corners = [geom.corners(p) for p in poses]
    c = writer.form_c(side, corners)
    gc = reader.read_form_c(c)
    ok("C read: n", gc["n"] == 2)
    ok("C read: side", gc["side"] == side)
    ok("C read: corners", gc["corners"] == corners)
    ok("C read: ids", gc["ids"] == ["square-1", "square-2"])
    ok("C read: canonical", gc["noncanonical"] == [])
    centred = reader.read_form_c(writer.form_c(side, corners, origin="container-center"))
    ok("C container-center: corners", centred["corners"] == corners)
    ctext = c.decode()
    first = ctext.split("    - - ", 1)[1].split("\n", 1)[0]
    ccases = [
        ("C anchor", ctext.replace("    corners:\n", "    corners: &a\n", 1), "anchor"),
        ("C alias", ctext.replace("  scalar:\n    kind: rational\n", "  scalar: &s\n    kind: rational\n", 1), "anchor"),
        ("C tag", ctext.replace("  side: 5/2", "  side: !!str 5/2", 1), "explicit tag"),
        ("C dup key", ctext.replace("  side: 5/2\n", "  side: 5/2\n  side: 5/2\n", 1), "twice"),
        ("C directive", "%YAML 1.1\n---\n" + ctext, "directive"),
        ("C two documents", ctext + "---\na: 1\n", "documents"),
        ("C plain float side", ctext.replace("  side: 5/2", "  side: 2.5", 1), "float"),
        ("C center-angle", ctext.replace("representation: corners", "representation: center-angle", 1), "representation"),
        ("C kind decimal", ctext.replace("kind: rational", "kind: decimal", 1), "kind"),
        ("C square size", ctext.replace("square_size: '1'", "square_size: '2'", 1), "square_size"),
        ("C square size plain", ctext.replace("square_size: '1'", "square_size: 1", 1), "square_size"),
        ("C five corners", ctext.replace("    corners:\n", f"    corners:\n    - - {first}\n      - 0\n", 1), "5 items"),
        ("C missing id", ctext.replace("  - id: square-1\n    corners:", "  - corners:", 1), "missing"),
        ("C dup id", ctext.replace("id: square-2", "id: square-1", 1), "twice"),
        ("C plus sign", ctext.replace(f"    - - {first}", f"    - - +{first}", 1), "not an exact scalar"),
        ("C zero denominator", ctext.replace("  side: 5/2", "  side: 5/0", 1), "not an exact scalar"),
        ("C n mismatch", ctext.replace("  n: 2", "  n: 3", 1), "3 and 2"),
        ("C contract", ctext.replace("Witness/v2", "Witness/v1", 1), "contract"),
        ("C unknown key", ctext.replace("  representation:", "  extra: 1\n  representation:", 1), "unexpected"),
        ("C block scalar", ctext.replace("  side: 5/2", "  side: |\n    5/2", 1), "block"),
        ("C merge key", ctext.replace("  scalar:\n", "  <<: {}\n  scalar:\n", 1), "key that is not a string"),
        ("C bool coordinate", ctext.replace(f"    - - {first}", "    - - true", 1), "bool"),
    ]
    for name, mutated, needle in ccases:
        ok(f"{name}: mutation applied", mutated != ctext)
        refused(name, reader.read_form_c, mutated.encode(), needle)
    q = reader.read_form_c(ctext.replace("  side: 5/2", "  side: '2.5'", 1).encode())
    ok("C quoted decimal side", q["side"] == side and q["scalar_forms"].get("decimal") == 1)
    r = reader.read_form_c(ctext.replace("  side: 5/2", "  side: 10/4", 1).encode())
    ok("C side 10/4", r["side"] == side and r["noncanonical"] == ["witness.side"])
    ok("C int coordinate read", reader.read_form_c(ctext.replace(f"    - - {first}", "    - - 7", 1).encode())["corners"][0][0][0] == 7)


def test_pairs() -> None:
    g = F(1, 10)
    ax = (F(1, 2), F(1, 2), F(1), F(0))
    pair_case("side by side apart", ax, (F(3, 2) + g, F(1, 2), F(1), F(0)), g, "apart", F(0), g * g)
    pair_case("side by side contact", ax, (F(3, 2), F(1, 2), F(0), F(1)), F(0), "contact", F(0), None)
    pair_case("side by side overlap", ax, (F(3, 2) - g, F(1, 2), F(-1), F(0)), -g, "overlap", g, None)
    o = (F(0), F(0), F(1), F(0))
    pair_case("diagonal apart", o, (1 + g, 1 + g, F(0), F(-1)), g, "apart", F(0), 2 * g * g)
    pair_case("corner contact", o, (F(1), F(1), F(1), F(0)), F(0), "contact", F(0), None)
    pair_case("identical", o, o, F(-1), "overlap", F(1), None)
    pair_case("offset overlap", o, (F(1, 2), F(1, 4), F(1), F(0)), F(-1, 2), "overlap", F(3, 8), None)
    t = (F(6, 5) + g, F(0), F(3, 5), F(4, 5))
    pair_case("turned apart", o, t, g, "apart", F(0), g * g)
    pair_case("turned contact", o, (F(6, 5), F(0), F(-4, 5), F(3, 5)), F(0), "contact", F(0), None)
    u = (F(3, 5), F(4, 5))
    pair_case("turned edge contact", (F(0), F(0), *u), (u[0], u[1], *u), F(0), "contact", F(0), None)
    w = (F(20, 29), F(21, 29))
    pair_case("turned half overlap", (F(0), F(0), *w), (w[0] / 2, w[1] / 2, -w[1], w[0]), F(-1, 2), "overlap", F(1, 2), None)


def test_walls_and_units() -> None:
    s = F(2)
    rows = [
        ((F(1, 2), F(1), F(1), F(0)), (F(0), F(1, 2), F(1), F(1, 2)), F(1)),
        ((F(2, 5), F(1), F(0), F(1)), (F(-1, 10), F(1, 2), F(11, 10), F(1, 2)), F(9, 10)),
        ((F(7, 10), F(1), F(3, 5), F(4, 5)), (F(0), F(3, 10), F(3, 5), F(3, 10)), F(1)),
        ((F(3, 5), F(1), F(3, 5), F(4, 5)), (F(-1, 10), F(3, 10), F(7, 10), F(3, 10)), F(95, 96)),
    ]
    for k, (pose, clear, inside) in enumerate(rows):
        ip = poses_a.integer_pose(*pose)
        ok(f"wall row {k}: A clearances", poses_a.clearances(s, ip) == clear)
        ok(f"wall row {k}: geom clearances", geom.clearances(s, pose) == clear)
        wb = clip.walls(clip.q(s), clip.corners_from_pose(*pose))
        ok(f"wall row {k}: B clearances", tuple(clip.fr(v) for v in wb["clearances"]) == clear)
        want = {n: poses_a.wall_class(c) for n, c in zip(decide_mod.WALLS, clear, strict=True)}
        ok(f"wall row {k}: B classes", wb["classes"] == want)
        ok(f"wall row {k}: B inside {inside}", clip.fr(wb["inside2"]) / 2 == inside)
    bad = (F(0), F(0), F(3, 5), F(3, 5))
    ok("non-unit pose: A", not poses_a.is_unit(poses_a.integer_pose(*bad)))
    ok("non-unit pose: B", not clip.unit_square(clip.corners_from_pose(*bad))[0])
    rh = [(F(0), F(0)), (F(1), F(0)), (F(8, 5), F(4, 5)), (F(3, 5), F(4, 5))]
    ok("rhombus: A", not poses_a.pose_from_corners(rh)[0])
    ok("rhombus: B", not clip.unit_square([(clip.q(x), clip.q(y)) for x, y in rh])[0])
    sq = geom.corners((F(1), F(1), F(3, 5), F(4, 5)))
    order = [sq[0], sq[2], sq[1], sq[3]]
    ok("non-cyclic: A", not poses_a.pose_from_corners(order)[0])
    ok("non-cyclic: B", not clip.unit_square([(clip.q(x), clip.q(y)) for x, y in order])[0])
    cw = sq[::-1]
    okA, pose = poses_a.pose_from_corners(cw)
    ok("clockwise: A unit", okA)
    ok("clockwise: B sense", clip.unit_square([(clip.q(x), clip.q(y)) for x, y in cw]) == (True, -1))
    if pose is not None:
        ok("clockwise: A pose centre", (pose[0], pose[1]) == (F(1), F(1)))
    fold = [(F(0), F(0)), (F(1), F(0)), (F(0), F(0)), (F(1), F(0))]
    ok("folded: B", not clip.unit_square([(clip.q(x), clip.q(y)) for x, y in fold])[0])
    ok("folded: A", not poses_a.pose_from_corners(fold)[0])


def grid(side: F) -> list[tuple[F, F, F, F]]:
    return [(F(1, 2), F(1, 2), F(1), F(0)), (F(3, 2), F(1, 2), F(0), F(1)),
            (F(1, 2), F(3, 2), F(-1), F(0)), (F(3, 2), F(3, 2), F(0), F(-1))]


def random_direction(rng: random.Random, places: int) -> tuple[F, F]:
    t = F(rng.randrange(-10**places, 10**places), 10**places)
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def scattered(rng: random.Random, count: int, places: int) -> tuple[F, list[tuple[F, F, F, F]]]:
    cols = 1
    while cols * cols < count:
        cols += 1
    poses = []
    for k in range(count):
        a, b = random_direction(rng, places)
        cx = F(3, 4) + F(3, 2) * (k % cols) + F(rng.randrange(-10**places, 10**places), 10**(places + 2))
        cy = F(3, 4) + F(3, 2) * (k // cols) + F(rng.randrange(-10**places, 10**places), 10**(places + 2))
        poses.append((cx, cy, a, b))
    return F(3, 2) * cols + F(1, 1000), poses


def test_packings(scratch: Path) -> None:
    s = F(2)
    res = decide_mod.decide(s, poses=grid(s))
    ok("grid: ACCEPT", res["verdict"] == "ACCEPT")
    contacts = sorted(k for k, row in res["pairs"].items() if row[1] == "contact")
    ok("grid: six contacts", contacts == [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    walls_touch = sum(1 for row in res["walls"] if row is not None for c in row["clearances"] if c == 0)
    ok("grid: eight wall contacts", walls_touch == 8)
    resc = decide_mod.decide(s, corners=[geom.corners(p) for p in grid(s)])
    ok("grid by corners: ACCEPT", resc["verdict"] == "ACCEPT")
    ok("grid by corners: same margins", {k: v[0] for k, v in resc["pairs"].items()} == {k: v[0] for k, v in res["pairs"].items()})
    over = grid(s)
    over[3] = (F(3, 2) - F(1, 10**30), over[3][1], over[3][2], over[3][3])
    r2 = decide_mod.decide(s, poses=over)
    ok("grid overlap by 1e-30: REFUSE", r2["verdict"] == "REFUSE")
    ok("grid overlap by 1e-30: exactly pair 3,4", [k for k, v in r2["pairs"].items() if v[1] == "overlap"] == [(2, 3)])
    ok("grid overlap by 1e-30: margin", r2["pairs"][(2, 3)][0] == -F(1, 10**30))
    r3 = decide_mod.decide(s - F(1, 10**30), poses=grid(s))
    ok("grid side short by 1e-30: REFUSE", r3["verdict"] == "REFUSE" and not r3["disagreements"])
    r4 = decide_mod.decide(s, poses=[*grid(s)[:3], (F(3, 2), F(3, 2), F(3, 5), F(3, 5))])
    ok("grid with a non-unit square: REFUSE", r4["verdict"] == "REFUSE" and r4["problems"][0].startswith("square 4"))

    rng = random.Random(1052)
    side, poses = scattered(rng, 16, 28)
    res = decide_mod.decide(side, poses=poses)
    ok("scattered 16: ACCEPT", res["verdict"] == "ACCEPT")
    corner_res = decide_mod.decide(side, corners=[geom.corners(p) for p in poses])
    ok("scattered 16: by corners equal", {k: v[0] for k, v in corner_res["pairs"].items()} == {k: v[0] for k, v in res["pairs"].items()})
    ok("scattered 16: geom margins", all(geom.margin(poses[i], poses[j]) == v[0] for (i, j), v in res["pairs"].items()))
    ok("scattered 16: geom clearances", all(geom.clearances(side, poses[k]) == row["clearances"] for k, row in enumerate(res["walls"]) if row))
    closings = 0
    for i in range(len(poses)):
        for j in range(i + 1, len(poses)):
            for target, cls in ((F(0), "contact"), (-F(1, 10**30), "overlap")):
                moved = geom.close_toward(poses[i], poses[j], target)
                m = a_margin(poses[i], moved)
                got = b_pair(poses[i], moved)
                ok(f"close {i},{j} to {target}", m == target and got[0] == cls and geom.margin(poses[i], moved) == target)
                closings += 1
    ok("closings counted", closings == 240)
    for k in range(len(poses)):
        for wall in range(4):
            for beyond, cls in ((F(0), "contact"), (F(1, 10**30), "crossing")):
                moved = geom.to_wall(side, poses[k], wall, beyond)
                c = poses_a.clearances(side, poses_a.integer_pose(*moved))[wall]
                wb = clip.walls(clip.q(side), clip.corners_from_pose(*moved))
                name = decide_mod.WALLS[wall]
                ok(f"wall move {k} {name} {beyond}", c == -beyond and wb["classes"][name] == cls and
                   (clip.fr(wb["inside2"]) == 2) == (beyond == 0))

    # the check end to end on a synthetic twin pair
    jb = writer.form_j(side, poses)
    cb = writer.form_c(side, [geom.corners(p) for p in poses])
    (scratch / "j.json").write_bytes(jb)
    (scratch / "c.yaml").write_bytes(cb)
    claim = check.ceiling_at(side, 12)
    claim_text = check.decimal(claim, 12)
    rc = check.main(["x", str(scratch / "j.json"), str(scratch / "c.yaml"), reader.git_blob_id(jb),
                     reader.git_blob_id(cb), "16", claim_text, str(scratch / "check.json")])
    ok("check twin: ACCEPT", rc == 0)
    rotated = [geom.corners(p)[1:] + geom.corners(p)[:1] for p in poses]
    cb2 = writer.form_c(side, rotated)
    (scratch / "c2.yaml").write_bytes(cb2)
    rc2 = check.main(["x", str(scratch / "j.json"), str(scratch / "c2.yaml"), "-", "-", "16", claim_text,
                      str(scratch / "check2.json")])
    ok("check twin with rotated corner lists: ACCEPT", rc2 == 0)
    wrong = [list(c) for c in rotated]
    wrong[5][0] = (wrong[5][0][0] + F(1, 10**30), wrong[5][0][1])
    (scratch / "c3.yaml").write_bytes(writer.form_c(side, wrong))
    rc3 = check.main(["x", str(scratch / "j.json"), str(scratch / "c3.yaml"), "-", "-", "16", claim_text,
                      str(scratch / "check3.json")])
    got3 = json.loads((scratch / "check3.json").read_text())
    ok("check twin with one corner moved: REFUSE", rc3 == 1 and got3["twin"]["squares_differing"] == [6])
    rc4 = check.main(["x", str(scratch / "j.json"), str(scratch / "c.yaml"), "0" * 40, "-", "16", claim_text,
                      str(scratch / "check4.json")])
    ok("check with a wrong blob id: REFUSE", rc4 == 1)
    low = check.decimal(check.floor_at(side, 12) - F(1, 10**12), 12)
    rc5 = check.main(["x", str(scratch / "j.json"), str(scratch / "c.yaml"), "-", "-", "16", low,
                      str(scratch / "check5.json")])
    ok("check with a claim below the side: REFUSE", rc5 == 1)


def test_decide_compares() -> None:
    """decide must notice a method that disagrees, and a square B finds partly outside."""
    s = F(2)
    real_pair, real_walls = clip.pair, clip.walls

    def wrong_pair(p: Any, r: Any, *, distance: bool = True) -> tuple[str, Any, Any]:
        cls, area2, g2 = real_pair(p, r, distance=distance)
        return ("apart" if cls == "contact" else cls), area2, g2

    def wrong_walls(side: Any, p: Any) -> dict[str, Any]:
        row = real_walls(side, p)
        row["inside2"] = row["inside2"] / 2
        return row

    try:
        clip.pair = wrong_pair
        res = decide_mod.decide(s, poses=grid(s))
        ok("decide: a B class disagreeing with A is caught", res["verdict"] == "REFUSE" and len(res["disagreements"]) == 6)
        clip.pair = real_pair
        clip.walls = wrong_walls
        res = decide_mod.decide(s, poses=grid(s))
        ok("decide: B's area inside below 1 is refused", res["verdict"] == "REFUSE" and len(res["problems"]) == 4)
        clip.walls = real_walls

        def shifted_walls(side: Any, p: Any) -> dict[str, Any]:
            row = real_walls(side, p)
            c = list(row["clearances"])
            c[2] = c[2] + clip.mpq(1, 10**30)
            row["clearances"] = tuple(c)
            return row

        def short_gap(p: Any, r: Any, *, distance: bool = True) -> tuple[str, Any, Any]:
            cls, area2, g2 = real_pair(p, r, distance=distance)
            return cls, area2, (g2 / 4 if g2 is not None else None)

        apart = [(F(1, 2), F(1, 2), F(1), F(0)), (F(5, 2), F(1, 2), F(1), F(0))]
        clip.walls = shifted_walls
        res = decide_mod.decide(F(3), poses=apart)
        ok("decide: a B clearance off by 1e-30 is caught", res["verdict"] == "REFUSE" and len(res["disagreements"]) == 2)
        clip.walls = real_walls
        clip.pair = short_gap
        res = decide_mod.decide(F(3), poses=apart)
        ok("decide: a B gap below A's margin is caught", res["verdict"] == "REFUSE" and len(res["disagreements"]) == 1)
    finally:
        clip.pair, clip.walls = real_pair, real_walls
    res = decide_mod.decide(s, poses=grid(s))
    ok("decide: restored", res["verdict"] == "ACCEPT")
    res = decide_mod.decide(F(3), poses=[(F(1, 2), F(1, 2), F(1), F(0)), (F(5, 2), F(1, 2), F(1), F(0))])
    ok("decide: two apart, gap 1", res["verdict"] == "ACCEPT" and res["pairs"][(0, 1)][2] == 1)


def main(argv: list[str]) -> int:
    t0 = time.process_time()
    out = Path(argv[1])
    with tempfile.TemporaryDirectory(dir=argv[2] if len(argv) > 2 else None) as tmp:
        test_reader()
        test_pairs()
        test_walls_and_units()
        test_decide_compares()
        test_packings(Path(tmp))
    failed = [name for name, good in RESULTS if not good]
    receipt = {
        "program": "r1052_selftest.py",
        "checks": len(RESULTS),
        "failed": failed,
        "verdict": "PASSED" if not failed else "FAILED",
        "cpu_seconds": round(time.process_time() - t0, 1),
        "python": sys.version.split()[0],
    }
    out.write_text(json.dumps(receipt, indent=1) + "\n")
    print(f"{receipt['verdict']} {len(RESULTS) - len(failed)} of {len(RESULTS)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
