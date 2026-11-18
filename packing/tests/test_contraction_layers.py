"""`devtools.contraction_margin` through several L layers and a uniform dilation (OR-1).

Option D (think-b0w5) measures a predecessor "through any construction": a certificate
built by ``k`` L steps on a base and then dilated carries the base's padding, while its own
uniform-contraction margin is the dilation alone, since its grid squares touch
(`devtools.measure_identity.read_l_layers`). Synthetic packings whose answers are known by
construction come first: a base with a gap, whose padding the layers carry, and the
control where the base binds and the grid does not, through which nothing more is carried
than the whole certificate's own margin. Layers whose corner square sits on either arm
read alike, and a tilted or misplaced added square, a dilation below 1 and a malformed
target are refused. Last, Francisco Couzo's ``4e4c8ce`` certificate at 631, his 490 with
three layers dilated by ``1 + 1e-24``, read as the retained receipt states it.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import contraction_margin as cm
from devtools import evand_exact_certificates as legacy
from devtools import measure_identity as identity
from devtools import upper_bound_reports as reports

HALF = Fraction(1, 2)
#: Two upright unit squares a tenth apart in a box of side 21/10: padding 1/10.
GAP = ((HALF, HALF, Fraction(0)), (Fraction(8, 5), HALF, Fraction(0)))
#: Two upright unit squares that touch in a box of side 2: no padding.
TOUCH = ((HALF, HALF, Fraction(0)), (Fraction(3, 2), HALF, Fraction(0)))
#: An upright square and one at half-angle tangent 1/2 in a box of side 29/10, which
#: contracts to 12/5 as test_contraction_margin's ROTATED does: a worse arrangement than
#: TOUCH. It keeps ``floor`` of its side, so one L step on it adds as many squares
#: contracted as not.
NARROW = ((HALF, Fraction(7, 10), Fraction(0)), (Fraction(11, 5), Fraction(7, 10), HALF))
DILATION = 1 + Fraction(1, 10**6)
WEB = reports.WEB
COUZO = WEB / "couzo-index-2026-10-15/source/certificates/best/n631.cert"
LATER = WEB / "mishapolk-issue719-2026-10-22/facts/n-631.yaml.gz"
RECEIPT = WEB / "mishapolk-issue719-2026-10-22/measure/contraction-n631-through-490.json"


def _composite(
    base: tuple[tuple[Fraction, Fraction, Fraction], ...],
    side: Fraction,
    layers: int,
    *,
    corner_on_top: bool = True,
    dilation: Fraction = DILATION,
) -> str:
    """The evand-cert text of ``layers`` L steps on ``base`` at ``side``, then dilated."""
    poses = list(base)
    for layer in range(layers):
        width = side + layer
        whole = int(width)
        top = whole + (1 if corner_on_top else 0)
        right = whole + (0 if corner_on_top else 1)
        # The right arm first, as Couzo writes it, so the order is not the writer's.
        poses += [(width + HALF, k + HALF, Fraction(0)) for k in range(right)]
        poses += [(k + HALF, width + HALF, Fraction(0)) for k in range(top)]
    rows = "".join(f"{x * dilation} {y * dilation} {t}\n" for x, y, t in poses)
    return f"{len(poses)} {(side + layers) * dilation}\n{rows}"


def _count(text: str) -> int:
    return int(text.split(maxsplit=1)[0])


def _spec(tmp_path: Path, text: str, label: str = "base") -> str:
    path = tmp_path / "composite.cert"
    path.write_text(text, encoding="utf-8")
    return f"{label}=l-base:{_count(text)}:evand-cert:{path}"


def _plain(tmp_path: Path, text: str, name: str) -> str:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return f"later=evand-cert:{path}"


def test_layers_carry_the_base_padding_the_whole_certificate_lacks(tmp_path: Path) -> None:
    """Two layers on the gapped pair, dilated: the base contracts by 1/10 to side 2, so the
    construction carries side 4, while the whole certificate contracts only by its
    dilation, since its grid squares touch."""
    text = _composite(GAP, Fraction(21, 10), 2)
    read = cm.read_certificate(_spec(tmp_path, text), 2)
    assert read.layered is not None
    assert (read.layered.layers, read.layered.dilation) == (2, DILATION)
    assert read.certificate.side == Fraction(21, 10)
    record = cm.margin(read)
    assert Fraction(record["contracted_side"]) == 2
    block = record["construction"]
    assert block["layers"] == 2
    assert Fraction(block["contracted_extended_side"]) == 4
    stated = Fraction(41, 10) * DILATION
    assert Fraction(block["margin_through"]) == stated - 4
    assert record["routes_accept"] is True
    assert block["routes_accept"] is True
    whole = cm.margin(
        cm.read_certificate(f"whole=evand-cert:{tmp_path / 'composite.cert'}", _count(text))
    )
    assert Fraction(whole["margin"]) < Fraction(block["margin_through"]) / 1000


def test_a_rival_is_compared_with_the_side_carried_through_the_construction(
    tmp_path: Path,
) -> None:
    """The narrowed rotated pair with one layer, dilated, carries 12/5 + 1 = 17/5 through
    its construction. Read at the extended count, 7, a rival at or above that side lies
    within its margin, the same construction undilated among them, and seven squares of
    the 3 by 3 grid, at 3, outside it, a new result by option D's test; the command says
    the same. (The pair at side 16/5 contracts across ``floor``, so its layers would add
    fewer squares contracted, which the module refuses: review A8(a) of #1030.)"""
    text = _composite(NARROW, Fraction(29, 10), 1)
    base = _spec(tmp_path, text)
    m = _count(text)
    same = _composite(NARROW, Fraction(29, 10), 1, dilation=Fraction(1))
    cells = [(x, y) for x in (1, 3, 5) for y in (1, 3, 5)][:7]
    better = "7 3\n" + "".join(f"{x}/2 {y}/2 0\n" for x, y in cells)
    assert _count(same) == _count(better) == m
    for name, rival, inside in (("same.cert", same, True), ("better.cert", better, False)):
        record = cm.margin(
            cm.read_certificate(base, 2),
            routes=False,
            against=cm.read_certificate(_plain(tmp_path, rival, name), m),
            through=True,
        )
        assert Fraction(record["construction"]["contracted_extended_side"]) == Fraction(17, 5)
        against = record["against"]
        assert (against["n"], against["within_margin"]) == (m, inside)
        assert against["compared"].startswith("through the construction")
    out = tmp_path / "out.json"
    rival = _plain(tmp_path, better, "rival.cert")
    command = ["--n", "2", base, "--against", rival, "--no-routes", "--out", str(out)]
    assert cm.main([*command, "--through"]) == 0
    assert json.loads(out.read_text(encoding="utf-8"))["against"]["within_margin"] is False
    # Without --through the rival is read at the base's count, which it is not, and the
    # refusal says how to compare it through the construction (review A2 of #1030).
    assert cm.main(command) == 2


def test_where_the_base_binds_the_layers_carry_no_more_than_the_dilation(
    tmp_path: Path,
) -> None:
    """The control: the touching pair with two layers, dilated. Its base contracts by
    nothing, so what the construction carries is the dilation alone, the whole
    certificate's own margin."""
    text = _composite(TOUCH, Fraction(2), 2)
    record = cm.margin(cm.read_certificate(_spec(tmp_path, text), 2))
    assert record["margin"] == "0"
    block = record["construction"]
    assert Fraction(block["margin_through"]) == 4 * DILATION - 4
    whole = cm.margin(
        cm.read_certificate(f"whole=evand-cert:{tmp_path / 'composite.cert'}", _count(text))
    )
    assert Fraction(whole["margin"]) == Fraction(block["margin_through"])


def test_a_layer_may_put_its_corner_on_either_arm(tmp_path: Path) -> None:
    on_top = identity.read_l_layers(
        _spec(tmp_path, _composite(GAP, Fraction(21, 10), 1)).split("l-base:", 1)[1], 2
    )
    on_right = identity.read_l_layers(
        _spec(tmp_path, _composite(GAP, Fraction(21, 10), 1, corner_on_top=False)).split(
            "l-base:", 1
        )[1],
        2,
    )
    assert on_top.base == on_right.base
    assert (on_top.layers, on_right.layers) == (1, 1)


@pytest.mark.parametrize(
    ("change", "words"),
    [
        (lambda rows: [*rows[:-1], rows[-1].replace(" 0", " 1/7")], "no L construction"),
        (lambda rows: [*rows[:-1], "1/3 1/3 0"], "no L construction"),
    ],
)
def test_an_added_square_that_is_no_layer_is_refused(
    tmp_path: Path, change: object, words: str
) -> None:
    head, *rows = _composite(GAP, Fraction(21, 10), 1).splitlines()
    text = "\n".join([head, *change(rows)]) + "\n"  # type: ignore[operator]
    with pytest.raises(identity.MeasureError, match=words):
        identity.read_l_layers(_spec(tmp_path, text).split("l-base:", 1)[1], 2)


def test_a_shrinking_factor_and_a_malformed_target_are_refused(tmp_path: Path) -> None:
    small = _composite(GAP, Fraction(21, 10), 1, dilation=Fraction(99, 100))
    with pytest.raises(identity.MeasureError, match="no L construction"):
        identity.read_l_layers(_spec(tmp_path, small).split("l-base:", 1)[1], 2)
    for target in ("x:evand-cert:a.cert", "5:no-such-format:a.cert", "5:evand-cert:"):
        with pytest.raises(identity.MeasureError, match="M:FORMAT:PATH"):
            identity.read_l_layers(target, 2)
    with pytest.raises(identity.MeasureError, match="no count above"):
        identity.read_l_layers("2:evand-cert:a.cert", 2)


def test_couzo_631_is_his_490_with_three_layers_and_a_dilation() -> None:
    """Couzo's ``4e4c8ce`` certificate at 631 reads as 490 squares with three layers,
    dilated by exactly 1 + 1e-24, and the retained receipt's construction is reproduced:
    his base contracts by 2.60e-11, which #719's 631 does not pass."""
    layered = identity.read_l_layers(f"631:evand-cert:{COUZO}", 490)
    assert layered.layers == 3
    assert layered.dilation == 1 + Fraction(1, 10**24)
    retained = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert retained["construction"]["layers"] == 3
    record = cm.margin(
        cm.read_certificate(f"couzo-4e4c8ce=l-base:631:evand-cert:{COUZO}", 490),
        routes=False,
        against=cm.read_certificate(f"mishapolk-719=witness-center-basis:{LATER}", 631),
        through=True,
    )
    for field in ("contracted_extended_side", "margin_through", "extended_side"):
        assert record["construction"][field] == retained["construction"][field]
    assert record["against"]["within_margin"] is retained["against"]["within_margin"] is True
    assert (
        legacy.literal(Fraction(retained["construction"]["margin_through"]))
        == (retained["construction"]["margin_through"])
    )


def test_a_contraction_that_changes_the_layers_square_count_is_refused(
    tmp_path: Path,
) -> None:
    """One square in a box of side 41/20 with one layer: contracted, the base's side falls
    to 1, whose L step adds 3 squares where the construction added 5, so the packing the
    layers would carry has another count and is refused (review A8(a) of #1030)."""
    text = _composite(((HALF, HALF, Fraction(0)),), Fraction(41, 20), 1)
    read = cm.read_certificate(_spec(tmp_path, text), 1)
    with pytest.raises(cm.ContractionError, match="4 squares, not the construction's 6"):
        cm.margin(read, routes=False)


def test_a_dilated_base_is_not_compared_with_another_base(tmp_path: Path) -> None:
    """Two bases compare exactly only when neither construction is dilated, so a dilated
    one is refused there (review A8(b) of #1030); undilated, the bases compare."""
    dilated = _composite(GAP, Fraction(21, 10), 1)
    plain = _composite(GAP, Fraction(21, 10), 1, dilation=Fraction(1))
    first = cm.read_certificate(_spec(tmp_path, dilated, "dilated"), 2)
    (tmp_path / "other").mkdir()
    second = cm.read_certificate(_spec(tmp_path / "other", plain, "plain"), 2)
    with pytest.raises(cm.ContractionError, match="dilated: a dilated construction"):
        cm.margin(first, routes=False, against=second)
    undilated = cm.read_certificate(_spec(tmp_path, plain, "undilated"), 2)
    record = cm.margin(undilated, routes=False, against=second)
    assert record["against"]["within_margin"] is True


def test_a_malformed_rival_and_a_through_without_a_base_are_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A malformed ``--against`` and a ``--through`` whose certificate is no ``l-base``
    end in a refusal, never a traceback (review A8(c) of #1030)."""
    base = _spec(tmp_path, _composite(GAP, Fraction(21, 10), 1))
    assert cm.main(["--n", "2", base, "--against", "nocolon", "--no-routes"]) == 2
    assert "refused:" in capsys.readouterr().err
    plain = _plain(tmp_path, _composite(GAP, Fraction(21, 10), 1), "plain.cert")
    assert cm.main(["--n", "7", plain, "--against", plain, "--through", "--no-routes"]) == 2
    assert "--through needs an l-base" in capsys.readouterr().err

