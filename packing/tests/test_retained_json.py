"""The width-bounded layout retained results are written in."""

from __future__ import annotations

import enum
import json
import random
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from sqpack import retained_json
from sqpack.retained_json import WIDTH, dumps

#: A census in miniature: a header, a summary object, a table of records, a grid of rows.
CENSUS = {
    "name": "census",
    "totals": {"records": 3, "by_kind": {"a": 1, "b": 2}},
    "rows": [{"n": 1, "kind": "a", "faces": {"+x": [0.5, None]}}, {"n": 2, "kind": "b"}],
    "grid": [[1, 2], [3, 4]],
    "empty": {},
    "none": [],
}

#: `CENSUS` at width 40. `totals` would be a 50-character line, so it opens; so does the
#: first row, at 48 with its comma, while the second row and the grid fit.
CENSUS_AT_40 = """\
{
  "name": "census",
  "totals": {
    "records": 3,
    "by_kind": {"a":1,"b":2}
  },
  "rows": [
    {
      "n": 1,
      "kind": "a",
      "faces": {"+x":[0.5,null]}
    },
    {"n":2,"kind":"b"}
  ],
  "grid": [[1,2],[3,4]],
  "empty": {},
  "none": []
}
"""


class Colour(enum.IntEnum):
    RED = 1


class Real(float):
    pass


#: Every JSON type, nested deeply, with the corners the encoder has rules for: non-ASCII
#: text, escapes, large and negative numbers, floats that need their full repr, the
#: non-finite floats, 1 and 1.0 and True side by side, a tuple, subclasses of int and
#: float, empty containers, and lists of lists of objects.
NESTED = {
    "text": "Bašić — “quoted”\n\ttab \\ slash \u2028 \U0001f600 \x00",
    "numbers": [0, -1, 10**30, 0.1, 1e-300, -2.5e17, 1.0, -0.0, 1e16, 2**64],
    "same": [1, 1.0, True, 0, 0.0, False],
    "specials": [float("nan"), float("inf"), float("-inf")],
    "flags": [True, False, None],
    "kinds": (Colour.RED, Real(2.5), "x"),
    "deep": {"a": {"b": {"c": {"d": [{"e": [[], {}, [{"f": 1}]]}]}}}},
    "table": [[{"g": [1, [2, [3]]]}, []], [], [[[]]]],
    "mixed": [1, "two", [3], {"four": 4}],
    "": {"": ""},
}

WIDTHS = (1, 8, 20, 40, 120, WIDTH)
BRACKETS = frozenset("{[]}")


def canonical(document: object) -> str:
    """Compact JSON, which tells 1, 1.0 and True apart where `==` does not."""
    return json.dumps(document, separators=(",", ":"), ensure_ascii=False)


def generated(seed: int, size: int = 400) -> object:
    """A random nested document: short keys, scalars of every kind, some strings long,
    some lists of scalars long."""
    chance = random.Random(seed)

    def scalar() -> object:
        return chance.choice(
            [
                chance.randrange(-(10**6), 10**6),
                chance.random() * 10 ** chance.randrange(-8, 8),
                "s" * chance.randrange(0, 3 * size),
                None,
                True,
            ]
        )

    def value(depth: int) -> object:
        roll = chance.random()
        if depth < 6 and roll < 0.3:
            keys = [f"k{chance.randrange(40)}" for _ in range(chance.randrange(5))]
            return {key: value(depth + 1) for key in keys}
        if depth < 6 and roll < 0.5:
            return [value(depth + 1) for _ in range(chance.randrange(6))]
        if roll < 0.6:
            return [scalar() if chance.random() < 0.1 else chance.random() for _ in range(80)]
        return scalar()

    return {f"top{index}": value(0) for index in range(12)}


def held(line: str) -> tuple[str, object]:
    """What one line holds, after an optional key and before an optional comma: a value,
    the bracket that opens or closes one, or anything else."""
    text = line.strip().removesuffix(",")
    if text in BRACKETS:
        return "bracket", text
    decoder = json.JSONDecoder()
    try:
        found, end = decoder.raw_decode(text)
        if text.startswith(": ", end):
            if text[end + 2 :] in BRACKETS:
                return "bracket", text[end + 2 :]
            found, end = decoder.raw_decode(text, end + 2)
    except json.JSONDecodeError:
        return "other", text
    return ("value", found) if end == len(text) else ("other", text)


def lone_scalar(line: str) -> bool:
    kind, found = held(line)
    return kind == "value" and not isinstance(found, dict | list)


def unsplittable(line: str) -> bool:
    """A scalar, an empty container or a bracket: nothing the layout could open further."""
    kind, found = held(line)
    return kind == "bracket" or (kind == "value" and found in ({}, [])) or lone_scalar(line)


def test_a_small_document_is_laid_out_by_the_width() -> None:
    assert dumps(CENSUS, width=40) == CENSUS_AT_40


def test_at_the_default_width_whatever_fits_is_one_line() -> None:
    assert dumps(CENSUS) == (
        "{\n"
        '  "name": "census",\n'
        '  "totals": {"records":3,"by_kind":{"a":1,"b":2}},\n'
        '  "rows": [{"n":1,"kind":"a","faces":{"+x":[0.5,null]}},{"n":2,"kind":"b"}],\n'
        '  "grid": [[1,2],[3,4]],\n'
        '  "empty": {},\n'
        '  "none": []\n'
        "}\n"
    )


def test_a_table_too_wide_for_a_line_is_a_record_per_line() -> None:
    rows = [{"n": n, "kind": "k" * 10} for n in range(5)]
    lines = dumps({"rows": rows}, width=40).split("\n")
    assert lines[1] == '  "rows": ['
    assert [json.loads(line.strip().removesuffix(",")) for line in lines[2:7]] == rows
    assert lines[7:] == ["  ]", "}", ""]


def test_a_list_of_scalars_too_wide_for_a_line_is_filled() -> None:
    # '    0,1,2,3,4,5,' is sixteen characters; '    6,7,8,9,10,11' would be seventeen.
    assert dumps({"v": list(range(12))}, width=16) == (
        '{\n  "v": [\n    0,1,2,3,4,5,\n    6,7,8,9,10,\n    11\n  ]\n}\n'
    )


def test_a_scalar_wider_than_the_width_takes_a_line_of_its_own() -> None:
    long = "x" * 30
    assert dumps([1, long, 2, 3], width=20) == f'[\n  1,\n  "{long}",\n  2,3\n]\n'
    assert dumps({"a": long, "b": [long]}, width=20) == (
        f'{{\n  "a": "{long}",\n  "b": [\n    "{long}"\n  ]\n}}\n'
    )


def test_a_list_mixing_scalars_and_containers_is_an_element_per_line() -> None:
    assert dumps({"m": [1, [2, 3], {"a": 4}, "five"]}, width=20) == (
        '{\n  "m": [\n    1,\n    [2,3],\n    {"a":4},\n    "five"\n  ]\n}\n'
    )


def test_the_width_counts_the_indentation_the_key_and_the_comma() -> None:
    document = {"k": [1, 2], "z": 0}
    # '  "k": [1,2],' is thirteen characters.
    assert dumps(document, width=13) == '{\n  "k": [1,2],\n  "z": 0\n}\n'
    assert dumps(document, width=12) == '{\n  "k": [\n    1,2\n  ],\n  "z": 0\n}\n'
    # Without the comma the same value fits a character sooner.
    assert dumps({"k": [1, 2]}, width=12) == '{\n  "k": [1,2]\n}\n'


@pytest.mark.parametrize("width", WIDTHS)
@pytest.mark.parametrize("seed", range(6))
def test_no_line_is_wider_than_the_width_unless_it_is_one_scalar(seed: int, width: int) -> None:
    document = generated(seed, size=width)
    text = dumps(document, width=width)
    assert canonical(json.loads(text)) == canonical(document)
    over = [line for line in text.split("\n") if len(line) > width]
    # Below about twice the deepest indentation plus a key, an empty container or a
    # bracket can be wider than the width by its indentation alone; nothing else can.
    allowed = lone_scalar if width >= 40 else unsplittable
    assert [line for line in over if not allowed(line)] == []


def test_the_document_always_opens() -> None:
    assert dumps({"a": 1}) == '{\n  "a": 1\n}\n'
    assert dumps([1, 2, 3]) == "[\n  1,2,3\n]\n"
    assert dumps([1, {"b": 2}]) == '[\n  1,\n  {"b":2}\n]\n'
    assert dumps("text") == '"text"\n'
    assert dumps(None) == "null\n"


def test_empty_containers_are_written_closed() -> None:
    assert dumps({}) == "{}\n"
    assert dumps([]) == "[]\n"
    assert dumps({"a": {}, "b": [], "c": {"d": {}, "e": []}}, width=1) == (
        '{\n  "a": {},\n  "b": [],\n  "c": {\n    "d": {},\n    "e": []\n  }\n}\n'
    )


@pytest.mark.parametrize("width", WIDTHS)
@pytest.mark.parametrize(
    "document",
    [CENSUS, NESTED, [NESTED, CENSUS], [[1, 2], [3]], [], {}, [1, 2], "text", 3, None],
)
def test_the_text_parses_to_what_json_writes_in_its_order(document: object, width: int) -> None:
    assert canonical(json.loads(dumps(document, width=width))) == canonical(document)
    kept = dumps(document, width=width, sort_keys=True, ensure_ascii=False)
    assert canonical(json.loads(kept)) == json.dumps(
        document, separators=(",", ":"), ensure_ascii=False, sort_keys=True
    )


@pytest.mark.parametrize("ensure_ascii", [True, False])
def test_each_scalar_is_written_as_json_writes_it(*, ensure_ascii: bool) -> None:
    scalars = [*NESTED["numbers"], *NESTED["same"], *NESTED["specials"], *NESTED["kinds"]]
    scalars += [NESTED["text"], "", '\u0000\u001f"\\/', None, 0.1 + 0.2, 1e-7, -(2**70)]
    lines = dumps(scalars, width=1, ensure_ascii=ensure_ascii).split("\n")[1:-2]
    written = [line.strip().removesuffix(",") for line in lines]
    assert written == [json.dumps(value, ensure_ascii=ensure_ascii) for value in scalars]


def test_the_text_ends_in_exactly_one_newline() -> None:
    for document in (CENSUS, NESTED, {}, [], 0):
        text = dumps(document)
        assert text.endswith("\n")
        assert not text.endswith("\n\n")


def test_the_text_depends_only_on_the_document_and_the_width() -> None:
    document = generated(7)
    assert dumps(document) == dumps(json.loads(json.dumps(document)))
    assert isinstance(document, dict)
    reordered = dict(reversed(list(document.items())))
    assert dumps(reordered, sort_keys=True) == dumps(document, sort_keys=True)
    assert dumps(reordered) != dumps(document)


def test_sort_keys_sorts_every_level() -> None:
    document = {"b": {"z": 1, "y": {"q": 1, "p": 2}}, "a": [{"d": 1, "c": 2}]}
    assert dumps(document, sort_keys=True) == (
        '{\n  "a": [{"c":2,"d":1}],\n  "b": {"y":{"p":2,"q":1},"z":1}\n}\n'
    )
    assert dumps(document, sort_keys=True, width=1) == (
        '{\n  "a": [\n    {\n      "c": 2,\n      "d": 1\n    }\n  ],\n  "b": {\n'
        '    "y": {\n      "p": 2,\n      "q": 1\n    },\n    "z": 1\n  }\n}\n'
    )
    assert list(json.loads(dumps(document))) == ["b", "a"]


@pytest.mark.parametrize("width", [1, WIDTH])
def test_ensure_ascii_escapes_keys_and_values_at_every_level(width: int) -> None:
    document = {"é": {"ü": ["ß", {"ø": "—"}]}}
    escaped = dumps(document, width=width)
    assert escaped.isascii()
    assert "\\u00e9" in escaped
    assert "\\u2014" in escaped
    kept = dumps(document, ensure_ascii=False, width=width)
    assert "é" in kept
    assert "—" in kept
    assert canonical(json.loads(escaped)) == canonical(json.loads(kept)) == canonical(document)


@pytest.mark.parametrize("width", [1, 20, WIDTH])
@pytest.mark.parametrize(
    "document",
    [
        float("nan"),
        [float("inf")],
        {"a": [1, 2, float("-inf")]},
        {"a": {"b": [{"c": float("nan")}, 1]}},
        {"v": [0.5] * 50 + [float("nan")]},
    ],
)
def test_allow_nan_is_honoured_wherever_the_value_stands(document: object, width: int) -> None:
    assert canonical(json.loads(dumps(document, width=width))) == canonical(document)
    with pytest.raises(ValueError, match="Out of range float values"):
        dumps(document, width=width, allow_nan=False)


def test_keys_are_converted_and_refused_as_json_does() -> None:
    document = {1: {2.5: "x"}, None: {True: [None], False: 0}}
    for width in (1, WIDTH):
        assert canonical(json.loads(dumps(document, width=width))) == canonical(document)
    with pytest.raises(TypeError):
        dumps({(1, 2): 0})
    with pytest.raises(TypeError):
        dumps({"a": {(1, 2): 0}}, width=1)


def test_default_converts_what_json_cannot_write_at_every_level() -> None:
    document = {"path": Path("a/b"), "rows": [{"path": Path("c")}], "deep": {"x": {Path("d")}}}
    with pytest.raises(TypeError):
        dumps(document)
    for width in (1, WIDTH):
        text = dumps(document, default=str, width=width)
        assert canonical(json.loads(text)) == json.dumps(
            document, default=str, separators=(",", ":"), ensure_ascii=False
        )
    as_object = dumps({"inner": Path("e")}, default=lambda value: {"path": str(value)}, width=1)
    assert as_object == '{\n  "inner": {\n    "path": "e"\n  }\n}\n'


def test_a_circular_document_is_refused_rather_than_followed() -> None:
    looped: dict[str, object] = {}
    looped["self"] = looped
    with pytest.raises(ValueError, match="Circular reference"):
        dumps(looped)
    listed: list[object] = []
    listed.append(listed)
    with pytest.raises(ValueError, match="Circular reference"):
        dumps(listed, width=1)
    nested: dict[str, object] = {"a": {"b": [1, 2]}}
    inner = nested["a"]
    assert isinstance(inner, dict)
    inner["back"] = nested
    with pytest.raises(ValueError, match="Circular reference"):
        dumps({"top": nested})


def test_the_encoder_sees_each_value_a_bounded_number_of_times(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Deciding a fit by encoding a value, then its children again, would encode a vector
    thirty levels down thirty times, 31 times the document in all; measured bottom up, the
    encoder sees less than twice the document (1.47 times on 2026-10-03)."""
    encoded: list[int] = []
    real = retained_json._compact  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001

    def counting(
        encoder: json.JSONEncoder, string: Callable[[str], str]
    ) -> Callable[[Any], str]:
        compact = real(encoder, string)

        def counted(value: Any) -> str:
            text = compact(value)
            encoded.append(len(text))
            return text

        return counted

    monkeypatch.setattr(retained_json, "_compact", counting)
    records = [
        {"id": n, "centre": [0.5 * n, 1.5], "faces": {"+x": {"gap": 0.25}}} for n in range(300)
    ]
    document: object = {"samples": [0.001 * n for n in range(5000)], "records": records}
    for level in range(30):
        document = {"level": level, "inner": document}
    dumps(document)
    assert sum(encoded) <= 2 * len(canonical(document))


def test_without_the_c_encoder_the_text_is_the_same(monkeypatch: pytest.MonkeyPatch) -> None:
    documents = [CENSUS, NESTED, generated(3)]
    expected = [dumps(document, width=width) for document in documents for width in (20, WIDTH)]
    monkeypatch.setattr(retained_json, "_C_MAKE_ENCODER", None)
    written = [dumps(document, width=width) for document in documents for width in (20, WIDTH)]
    assert written == expected
