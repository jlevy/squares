"""From the two files of one count to a decision.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Clean-room.

``decide_files`` reads a form P file and a form C file, compares them square by square
(the twin relation), and decides the packing with method A on the poses of the form P
file and method B on the corners of the form C file, the form each reads natively.

With ``cross=True`` it also decides the packing the other way round: method A on the
poses taken from the form C corners and method B on the corners written from the form P
rows. Form P alone is then decided by both methods (A natively, B crossed), and so is
form C alone (B natively, A crossed); the two decisions must give the same margin at
every pair and the same clearance at every wall.

With ``a_from="c"`` method A reads the poses taken from the form C corners instead of the
form P rows, so that form C alone is decided by both methods in one call. ``only``
restricts the pairs decided, as ``rv1009_decide.decide`` says.
"""

from __future__ import annotations

from fractions import Fraction

import rv1009_axes as axes
import rv1009_clip as clip
import rv1009_decide as decide
import rv1009_forms as forms
import rv1009_reader as reader

NO_POSE = (0, 0, 1, 0, 0, 1)
PASSED = ("ACCEPT", "PARTIAL")


def poses_from_corners(squares: list) -> tuple[list, list[int]]:
    """A pose for each square of form C, and the squares that have none."""
    poses = []
    bad = []
    for k, quad in enumerate(squares):
        try:
            pose, _sense = forms.pose_from_corners(quad)
        except ValueError:
            bad.append(k + 1)
            pose = NO_POSE
        poses.append(pose)
    return poses, bad


def decide_files(
    cert_data: bytes,
    yaml_data: bytes,
    *,
    cross: bool = False,
    only: set[int] | None = None,
    a_from: str = "p",
) -> dict:
    """Read, compare and decide. Never raises on a bad file: a refusal is a verdict."""
    out: dict = {"verdict": "REFUSE", "problems": []}
    try:
        cert = reader.read_cert(cert_data)
    except reader.ReadError as exc:
        out["problems"].append(f"form P not read: {exc}")
        out["read_error_p"] = str(exc)
        cert = None
    try:
        wit = reader.read_witness(yaml_data)
    except reader.ReadError as exc:
        out["problems"].append(f"form C not read: {exc}")
        out["read_error_c"] = str(exc)
        wit = None
    if cert is None or wit is None:
        return out
    out["cert"] = {k: v for k, v in cert.items() if k != "poses"}
    out["witness"] = {k: v for k, v in wit.items() if k != "squares"}
    out["rows_p"] = cert["poses"]
    out["quads_c"] = wit["squares"]
    n = cert["n"]
    side = cert["side"]
    if wit["n"] != n:
        out["problems"].append("the two files state different counts")
        return out
    if Fraction(*wit["side"]) != Fraction(*side):
        out["problems"].append("the two files state different sides")
        return out
    out["n"] = n
    out["side"] = Fraction(*side)
    out["side_texts_equal"] = cert["side_text"] == wit["side_text"]

    # the twin relation: square k of form P is square k of form C
    corners_p = [forms.corners_from_xyt(*row) for row in cert["poses"]]
    relation = [
        forms.same_square(forms.pairs_of(corners_p[k]), wit["squares"][k]) for k in range(n)
    ]
    out["twin_fails"] = [k + 1 for k in range(n) if relation[k] is None]
    out["twin_relations"] = relation
    if out["twin_fails"]:
        out["problems"].append(f"{len(out['twin_fails'])} squares differ between the files")

    poses_p = [axes.pose_from_xyt(*row) for row in cert["poses"]]
    quads_c = [clip.points(q) for q in wit["squares"]]
    poses_c: list = []
    if cross or a_from == "c":
        poses_c, bad = poses_from_corners(wit["squares"])
        out["form_c_no_pose"] = bad
        if bad:
            out["problems"].append(f"{len(bad)} squares of form C have no pose")
    native = decide.decide(poses_c if a_from == "c" else poses_p, quads_c, side, only=only)
    out["native"] = native
    if native["verdict"] not in PASSED:
        out["problems"].append("the packing is refused")

    if cross:
        quads_p = [clip.points(forms.pairs_of(c)) for c in corners_p]
        crossed = decide.decide(poses_c, quads_p, side, keep_margins=False, only=only)
        out["crossed"] = crossed
        if crossed["verdict"] not in PASSED:
            out["problems"].append("the packing is refused the other way round")
        one = native.get("margins_sha256")
        out["margin_digests_equal"] = one is not None and one == crossed.get("margins_sha256")
        if not out["margin_digests_equal"]:
            out["problems"].append("the margins of the two decisions differ")
        out["clearances_equal"] = (
            native.get("clearances") is not None
            and native.get("clearances") == crossed.get("clearances")
        )
        if not out["clearances_equal"]:
            out["problems"].append("the clearances of the two decisions differ")

    if not out["problems"]:
        out["verdict"] = "ACCEPT" if only is None else "PARTIAL"
    return out
