"""`devtools.measure_identity`: the pose-by-pose identity measures, once (think-jv2s, OR-1).

Negative controls first: a malformed binary64 packing, an unknown kind, a packet with no
certificate at the count and a count that differs are each refused, by the reader and by
the command. Then the measures on packings whose answer is known by construction: a
packing against its own mirror image, against itself reordered, and against its binary64
transcription. Last, the retained receipts the tool replaces, reproduced key for key: the
amundsk-n303-2026-10-23 packet's #755 (T-239) against T-230, which the T-240 review
cross-checked, and two pairs of the evand-regularized-2026-10-20 packet's; and the T-240
review's own box-centred figures for T-230 against T-239. Every test reads retained files
only; none needs the network.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import check_half_angle_area as area
from devtools import measure_identity as identity
from devtools import upper_bound_reports as reports

WEB = reports.WEB
AMUNDSK = "amundsk-n303-2026-10-23"
REGULARIZED = "evand-regularized-2026-10-20"
#: The keys each retained receipt's pair holds that `identity.measure` computes.
MEASURED = ("side_difference", "side_difference_exact", "nearest_centre", "assignment")
#: Three unit squares in a box of side 4, one turned by tan(theta/2) = 1/3, placed so that
#: no symmetry of the box but the identity maps their centres onto themselves.
THREE = "3 4\n1/2 1/2 0\n2 2 1/3\n7/2 3/2 0\n"
#: Two of them in a box of side 3.
TWO = "2 3\n1/2 1/2 0\n2 2 1/3\n"


def _file(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="ascii")
    return path


# --------------------------------------------------------------------------- refusals


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("", "header"),
        ("2\n1 1 0\n2 2 0\n", "header"),
        ("02 4\n1 1 0\n2 2 0\n", "header"),
        ("3 4\n1 1 0\n2 2 0\n", "states 3 squares"),
        ("2 4\n1 1 0\n", "1 square rows"),
        ("2 4\n1 1 0\n2 2 0\n3 3 0\n", "3 square rows"),
        ("2 4\n1 1\n2 2 0\n", "2 numbers"),
        ("2 4\n1 1 0 0\n2 2 0\n", "4 numbers"),
        ("2 4\n1 1 nan\n2 2 0\n", "not a decimal number"),
        ("2 4\n1 1 inf\n2 2 0\n", "not a decimal number"),
        ("2 4\n1_0 1 0\n2 2 0\n", "not a decimal number"),
        ("2 4\n0x1p1 1 0\n2 2 0\n", "not a decimal number"),
        ("2 4\n1/2 1 0\n2 2 0\n", "not a decimal number"),
        ("2 4\n1 1 1e999\n2 2 0\n", "not finite"),
        ("2 -4\n1 1 0\n2 2 0\n", "positive"),
        ("2 0\n1 1 0\n2 2 0\n", "positive"),
    ],
)
def test_a_malformed_binary64_packing_is_refused(text: str, message: str) -> None:
    with pytest.raises(identity.MeasureError, match=message):
        identity.read_binary64(text.encode("ascii"), 2)


def test_a_binary64_packing_that_is_not_ascii_is_refused() -> None:
    with pytest.raises(identity.MeasureError, match="ASCII"):
        identity.read_binary64("2 4\n1 1 0\n2 2 0°\n".encode(), 2)


@pytest.mark.parametrize(
    ("spec", "message"),
    [
        ("evand-cert", "KIND:TARGET"),
        ("evand-cert:", "KIND:TARGET"),
        ("=evand-cert:x.cert", "empty label"),
        ("nonsense:x.cert", "unknown kind"),
        ("packet:not-a-packet", "not a dated packet name"),
        ("packet:mishapolk-n204-2026-10-22", "no certificate at 3"),
        ("evand-cert:no-such-file.cert", "no-such-file"),
    ],
)
def test_a_spec_that_names_no_packing_of_the_count_is_refused(spec: str, message: str) -> None:
    with pytest.raises(identity.MeasureError, match=message):
        identity.read_packing(spec, 3)


def test_a_file_of_another_count_is_refused_by_its_adapter(tmp_path: Path) -> None:
    path = _file(tmp_path, "three.cert", THREE)
    with pytest.raises(identity.MeasureError, match="n=4"):
        identity.read_packing(f"evand-cert:{path}", 4)
    with pytest.raises(identity.MeasureError, match="states 3 squares, not 4"):
        identity.read_packing(f"binary64-xyd:{path}", 4)


def test_packings_of_two_counts_or_two_labels_alike_are_not_measured(tmp_path: Path) -> None:
    three = identity.read_packing(f"three=evand-cert:{_file(tmp_path, 'a.cert', THREE)}", 3)
    two = identity.read_packing(f"two=evand-cert:{_file(tmp_path, 'b.cert', TWO)}", 2)
    with pytest.raises(identity.MeasureError, match="3 squares, two 2"):
        identity.compare(three, two)
    with pytest.raises(identity.MeasureError, match="share a label"):
        identity.receipt(3, three, [three])
    with pytest.raises(identity.MeasureError, match="nothing to measure"):
        identity.receipt(3, three, [])


def test_the_command_refuses_a_malformed_input_and_writes_nothing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    good = _file(tmp_path, "good.cert", THREE)
    bad = _file(tmp_path, "bad.txt", "3 4\n1 1 0\n2 2 0\n")
    out = tmp_path / "out.json"
    argv = ["--n", "3", f"evand-cert:{good}", f"binary64-xyd:{bad}", "--out", str(out)]
    assert identity.main(argv) == 2
    assert "2 square rows for n = 3" in capsys.readouterr().err
    assert not out.exists()


# --------------------------------------------------------------------------- known answers


def test_a_binary64_angle_is_read_modulo_a_quarter_turn_on_the_unit_circle() -> None:
    side, squares = identity.read_binary64(b"# a comment\n2 4.5\n1 1.25 120\n3 3 -30\n", 2)
    assert side == Fraction(9, 2)
    (x, y, c, s), (_u, _v, p, q) = squares
    assert (x, y) == (1, Fraction(5, 4))
    assert c * c + s * s == 1
    assert (c, s) == identity.rotation_from_degrees(30.0)
    assert abs(float(s) - 0.5) < 1e-15
    assert (p, q) == (c, -s)


def test_a_packing_against_its_mirror_image_and_reordered_moves_nothing(tmp_path: Path) -> None:
    view = identity.read_packing(f"view=evand-cert:{_file(tmp_path, 'v.cert', THREE)}", 3)
    mirrored = identity.Packing(
        "mirror",
        {},
        view.side,
        tuple(area.symmetric(view.side, square, 4) for square in reversed(view.squares)),
    )
    pair = identity.compare(view, mirrored)
    assert pair["nearest_centre"]["one_to_one"] is True
    assert pair["nearest_centre"]["symmetry"] == 4
    assert set(pair["nearest_centre"]["moved_beyond"].values()) == {0}
    assert pair["assignment"]["symmetry"] == 4
    assert pair["assignment"]["largest_move"] == "0"
    assert pair["assignment"]["largest_turn_degrees"] == "0"
    assert pair["centred"]["symmetry"] == 4
    assert pair["centred"]["bottleneck"] == "0"
    assert pair["centred"]["nearest_one_to_one"] is True
    assert pair["side_difference_exact"] == "0"


def test_a_binary64_transcription_lies_within_its_rounding_of_the_exact_packing(
    tmp_path: Path,
) -> None:
    exact = _file(tmp_path, "exact.cert", TWO)
    # tan(theta/2) = 1/3 is theta = 36.869897645844021... degrees.
    rounded = _file(tmp_path, "rounded.txt", "2 3\n0.5 0.5 0\n2 2 36.86989764584402\n")
    out = tmp_path / "measure/identity.json"
    argv = [
        "--n",
        "2",
        f"exact=evand-cert:{exact}",
        f"binary64-xyd:{rounded}",
        "--out",
        str(out),
    ]
    assert identity.main(argv) == 0
    receipt = json.loads(out.read_text("utf-8"))
    assert receipt["format"] == identity.FORMAT
    (pair,) = receipt["pairs"]
    assert pair["against"] == f"binary64-xyd:{rounded}"
    assert receipt["inputs"][pair["against"]]["outside_repository"] is True
    assert pair["nearest_centre"]["moved_beyond"]["1e-9"] == 0
    assert pair["nearest_centre"]["turned_beyond_1e-6"] == 0
    assert float(pair["nearest_centre"]["largest_turn_degrees"]) < 1e-12
    assert pair["assignment"]["largest_move"] == "0"


# --------------------------------------------------------------------------- the receipts


def test_it_reproduces_the_amundsk_755_receipt_against_t230_key_for_key() -> None:
    """The amundsk-n303-2026-10-23 packet's measure/identity.json, #755 (registered as
    T-239) against T-230, the house it started from: every measure, the bands, and both
    packings' tilt classes."""
    view = identity.read_packing(f"#755=packet:{AMUNDSK}", 303)
    house = identity.read_packing("T-230 (#728), the house=packet:evand-n303-2026-10-22", 303)
    retained = json.loads((WEB / AMUNDSK / "measure/identity.json").read_text("utf-8"))
    (expected,) = (pair for pair in retained["pairs"] if pair["against"] == house.label)
    pair = identity.compare(view, house)
    for key in (*MEASURED, "bands"):
        assert pair[key] == expected[key], key
    for packing in (view, house):
        assert identity.tilts(packing.measured) == retained["tilts"][packing.label]


@pytest.mark.parametrize(
    ("n", "against", "path"),
    [
        (204, "T-223 (#678)", "couzo-issue678-2026-10-18/source/certificates/best/n204.cert"),
        (
            229,
            "T-199 (#674 update)",
            "evand-n229-dilation-update-2026-10-18/source/search/packer/candidates/s229_v2.cert",
        ),
    ],
    ids=["204", "229"],
)
def test_it_reproduces_the_evand_regularized_receipt_key_for_key(
    n: int, against: str, path: str
) -> None:
    """The evand-regularized-2026-10-20 packet's measure/identity.json, which holds the
    measures the later packets loaded: its view at 0075967 against T-223 at 204 and T-199
    at 229, the view read through the packet's own declaration."""
    view = identity.read_packing(f"packet:{REGULARIZED}", n)
    other = identity.read_packing(f"evand-cert:{WEB / path}", n)
    retained = json.loads((WEB / REGULARIZED / "measure/identity.json").read_text("utf-8"))
    (expected,) = (
        pair for pair in retained["pairs"] if pair["n"] == n and pair["against"] == against
    )
    assert expected["view"] == "evand 0075967"
    measured = identity.measure(view.measured, other.measured)
    for key in MEASURED:
        assert measured[key] == expected[key], key


def test_its_centred_assignment_reproduces_the_t240_review_of_t230_against_t239() -> None:
    """The T-240 review's clean-room identity.py (couzo-issue763-2026-10-23,
    review/review-2026-10-24/out/identity.json, ``T230@303 vs T239@303``) read both
    packings from their files and aligned the boxes by their centres; its ``anchored``
    variant aligned them by the lower-left corner, as the retained receipts do. Its figures:
    best symmetry the identity at a summed squared cost of 0.7426570629257025, the runner-up
    at 22.29062185443106; the largest move 0.5473247224491699 (anchored
    0.5473306947705245) and the RMS move 0.04950771060143781; squares moved beyond 0.1,
    1e-2, 1e-3, 1e-6 and 1e-9: 12, 31, 72, 303 and 303 (anchored 12, 31, 72, 266 and 266);
    16 squares turned beyond a degree and none reversed; nearest centres one to one."""
    t230 = identity.read_packing(
        "T-230=evand-cert:"
        + str(WEB / "evand-n303-2026-10-22/source/search/packer/candidates/s303_r303w0.cert"),
        303,
    )
    t239 = identity.read_packing(
        "T-239=witness-center-basis:" + str(reports.ROOT / "witnesses/known-best/n-303.yaml"),
        303,
    )
    pair = identity.compare(t230, t239)
    centred = pair["centred"]
    assert (centred["symmetry"], centred["total_squared"]) == (0, "0.742657")
    assert centred["runner_up_total_squared"] == "22.2906"
    assert (centred["largest_move"], centred["bottleneck"]) == ("0.547325", "0.547325")
    assert centred["rms_move"] == "0.0495077"
    assert centred["moved_beyond"] == {
        "1e-9": 303,
        "1e-6": 303,
        "1e-3": 72,
        "1e-2": 31,
        "1e-1": 12,
    }
    assert centred["nearest_one_to_one"] is True
    assert (centred["turned_beyond_1_degree"], centred["tilts_reversed_beyond_1_degree"]) == (
        16,
        0,
    )
    anchored = pair["assignment"]
    assert anchored["largest_move"] == "0.547331"
    assert anchored["moved_beyond"] == {
        "1e-9": 266,
        "1e-6": 266,
        "1e-3": 72,
        "1e-2": 31,
        "1e-1": 12,
    }
    assert pair["nearest_centre"]["one_to_one"] is True
