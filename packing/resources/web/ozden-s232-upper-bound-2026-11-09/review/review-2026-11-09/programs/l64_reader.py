"""Strict reader for rational Witness/v2 files, written clean room for lane L64.

Written on 2026-11-09 from the text of `packing/witnesses/witness.schema.yaml` and the
layout of the five certificates of issues 927 to 931, before any producer program
(`verifier/sqcheck.py`) or any of this repository's witness or verifier code was read.

It returns integers only: each scalar as a (numerator, denominator) pair. The two
deciding methods (`l64_sat.py` in `fractions.Fraction`, `l64_clip.py` in `gmpy2.mpq`)
build their own numbers from those pairs, so the reader is all they share.

It fails closed. Anything outside the layout it expects raises `ReadError`:
non-ASCII bytes, carriage returns, tabs, YAML features the layout never uses (tags,
anchors, aliases, flow collections, block scalars, quotes other than single quotes,
comments), duplicate keys, unknown keys, a scalar that is not an integer or `p/q` with a
positive denominator, a negative zero, a count that is not `n`, a repeated id, and a
corner list that is not four points of two scalars. Whether a file ends with a newline
is recorded and decides nothing (the JSON twins of issues 927 to 931 end without one).
YAML is parsed with PyYAML's `BaseLoader`, under which every scalar is a string, so no
implicit typing (floats, sexagesimals, underscores) can change a value.
"""

from __future__ import annotations

import gzip
import json
import re
from pathlib import Path

import yaml

from l64_util import sha256_file

SCALAR = re.compile(r"(-?)(0|[1-9][0-9]*)(?:/([1-9][0-9]*))?")
POS_INT = re.compile(r"[1-9][0-9]*")
YAML_FORBIDDEN = set('!&*%@`|>{}[]"#')
WITNESS_KEYS = {
    "id",
    "n",
    "side",
    "square_size",
    "representation",
    "scalar",
    "coordinates",
    "squares",
    "claim",
    "source",
    "certificate",
}
WITNESS_REQUIRED = WITNESS_KEYS - {"source", "certificate"}
ENVELOPE = {
    "contract": "packing.squares:Witness/v2",
    "envelope": "witness",
    "status": "enforced",
}
COORDINATES = {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"}


class ReadError(Exception):
    """The file is not a rational Witness/v2 file of the expected layout."""


class _StrictLoader(yaml.BaseLoader):
    """PyYAML BaseLoader (every scalar a str) that refuses duplicate or non-scalar keys."""

    def construct_mapping(self, node, deep=False):  # noqa: ANN001, ANN201
        if not isinstance(node, yaml.MappingNode):
            raise ReadError(f"expected a mapping at {node.start_mark}")
        out: dict[str, object] = {}
        for key_node, value_node in node.value:
            if not isinstance(key_node, yaml.ScalarNode):
                raise ReadError(f"non-scalar key at {key_node.start_mark}")
            key = self.construct_scalar(key_node)
            if key in out:
                raise ReadError(f"duplicate key {key!r} at {key_node.start_mark}")
            out[key] = self.construct_object(value_node, deep=True)
        return out

    def construct_sequence(self, node, deep=False):  # noqa: ANN001, ANN201
        if not isinstance(node, yaml.SequenceNode):
            raise ReadError(f"expected a sequence at {node.start_mark}")
        return [self.construct_object(child, deep=True) for child in node.value]


def parse_scalar(text: object) -> tuple[int, int]:
    """An integer or p/q string, as (numerator, denominator) with denominator > 0."""
    if not isinstance(text, str):
        raise ReadError(f"scalar is not a string: {text!r}")
    m = SCALAR.fullmatch(text)
    if m is None:
        raise ReadError(f"not an integer or p/q scalar: {text[:60]!r}")
    sign, whole, den = m.groups()
    num = int(whole)
    if sign == "-" and num == 0:
        raise ReadError(f"negative zero: {text[:60]!r}")
    if sign == "-":
        num = -num
    return num, (int(den) if den is not None else 1)


def _load_text(path: Path) -> tuple[bytes, str]:
    """ASCII text with LF line ends and no tabs; a final newline is recorded, not required."""
    raw = path.read_bytes()
    data = gzip.decompress(raw) if path.suffix == ".gz" else raw
    try:
        text = data.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ReadError(f"non-ASCII byte at offset {exc.start}") from None
    if "\r" in text:
        raise ReadError("carriage return in file")
    if "\t" in text:
        raise ReadError("tab in file")
    return data, text


def _check_yaml_text(text: str) -> None:
    bad = sorted(set(text) & YAML_FORBIDDEN)
    if bad:
        raise ReadError(f"YAML feature characters this layout never uses: {bad}")


def _point(obj: object, where: str) -> tuple[int, int, int, int]:
    if not isinstance(obj, list) or len(obj) != 2:
        raise ReadError(f"{where}: a point is not two scalars")
    xn, xd = parse_scalar(obj[0])
    yn, yd = parse_scalar(obj[1])
    return xn, xd, yn, yd


def _parse_witness(doc: object, expected_n: int | None, allow: tuple[str, ...]) -> dict:
    if not isinstance(doc, dict) or set(doc) != {"softschema", "witness"}:
        raise ReadError("top level must hold exactly softschema and witness")
    env = doc["softschema"]
    if not isinstance(env, dict) or set(env) != {"contract", "schema", "envelope", "status"}:
        raise ReadError("softschema envelope keys differ")
    for key, want in ENVELOPE.items():
        if env[key] != want:
            raise ReadError(f"softschema.{key} is {env[key]!r}, not {want!r}")
    if not isinstance(env["schema"], str) or not env["schema"].endswith("witness.schema.yaml"):
        raise ReadError("softschema.schema does not name witness.schema.yaml")
    w = doc["witness"]
    if not isinstance(w, dict):
        raise ReadError("witness is not a mapping")
    unknown = set(w) - WITNESS_KEYS
    missing = WITNESS_REQUIRED - set(w)
    if unknown or missing:
        raise ReadError(f"witness keys: unknown {sorted(unknown)}, missing {sorted(missing)}")
    if w["square_size"] != "1":
        raise ReadError("square_size is not '1'")
    rep = w["representation"]
    if rep not in allow:
        raise ReadError(f"representation {rep!r} not in {allow}")
    if w["scalar"] != {"kind": "rational"}:
        raise ReadError(f"scalar is {w['scalar']!r}, not exactly kind: rational")
    if w["coordinates"] != COORDINATES:
        raise ReadError(f"coordinates are {w['coordinates']!r}")
    if not isinstance(w["n"], str) or not POS_INT.fullmatch(w["n"]):
        raise ReadError(f"n is {w['n']!r}")
    n = int(w["n"])
    if expected_n is not None and n != expected_n:
        raise ReadError(f"n is {n}, expected {expected_n}")
    side = parse_scalar(w["side"])
    if side[0] <= 0:
        raise ReadError("side is not positive")
    squares = w["squares"]
    if not isinstance(squares, list) or len(squares) != n:
        raise ReadError(f"squares: {len(squares) if isinstance(squares, list) else '?'} for n = {n}")
    out_squares = []
    seen: set[int] = set()
    scalars = 0
    lowest = 0
    for k, sq in enumerate(squares):
        where = f"square #{k + 1}"
        if not isinstance(sq, dict):
            raise ReadError(f"{where}: not a mapping")
        if rep == "corners":
            if set(sq) != {"id", "corners"}:
                raise ReadError(f"{where}: keys {sorted(sq)}")
        elif set(sq) != {"id", "center", "basis"}:
            raise ReadError(f"{where}: keys {sorted(sq)}")
        sid = sq["id"]
        if not isinstance(sid, str) or not POS_INT.fullmatch(sid):
            raise ReadError(f"{where}: id {sid!r}")
        sid_int = int(sid)
        if sid_int in seen:
            raise ReadError(f"{where}: repeated id {sid_int}")
        seen.add(sid_int)
        entry: dict[str, object] = {"id": sid_int}
        if rep == "corners":
            corners = sq["corners"]
            if not isinstance(corners, list) or len(corners) != 4:
                raise ReadError(f"{where}: corners is not four points")
            pts = [_point(c, f"{where} corner {j}") for j, c in enumerate(corners)]
            entry["corners"] = pts
            vals = [(p[0], p[1]) for p in pts] + [(p[2], p[3]) for p in pts]
        else:
            centre = _point(sq["center"], f"{where} center")
            basis = _point(sq["basis"], f"{where} basis")
            entry["center"] = centre
            entry["basis"] = basis
            vals = [(centre[0], centre[1]), (centre[2], centre[3])]
            vals += [(basis[0], basis[1]), (basis[2], basis[3])]
        for num, den in vals:
            scalars += 1
            if _gcd(abs(num), den) == 1:
                lowest += 1
        out_squares.append(entry)
    for key in ("claim", "source", "certificate"):
        if key in w and not isinstance(w[key], dict):
            raise ReadError(f"{key} is not a mapping")
    return {
        "n": n,
        "id": w["id"],
        "representation": rep,
        "side": side,
        "side_text": w["side"],
        "squares": out_squares,
        "ids_in_order": [s["id"] for s in out_squares] == list(range(1, n + 1)),
        "scalars": scalars,
        "scalars_in_lowest_terms": lowest,
        "claim": w.get("claim"),
        "source": w.get("source"),
        "certificate": w.get("certificate"),
        "raw_squares": squares,
    }


def _gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def read_witness(
    path: str | Path,
    expected_n: int | None = None,
    allow: tuple[str, ...] = ("corners",),
) -> dict:
    """Read a rational Witness/v2 YAML file (optionally gzipped) strictly."""
    path = Path(path)
    try:
        data, text = _load_text(path)
        _check_yaml_text(text)
        try:
            doc = yaml.load(text, Loader=_StrictLoader)  # noqa: S506 - BaseLoader: strings only
        except yaml.YAMLError as exc:
            raise ReadError(f"YAML: {exc}") from None
        out = _parse_witness(doc, expected_n, allow)
    except ReadError as exc:
        raise ReadError(f"{path.name}: {exc}") from None
    out["path"] = str(path)
    out["sha256"] = sha256_file(path)
    out["bytes"] = len(data)
    out["lines"] = text.count("\n")
    out["final_newline"] = text.endswith("\n")
    return out


def _json_pairs(pairs: list[tuple[str, object]]) -> dict:
    out: dict[str, object] = {}
    for key, value in pairs:
        if key in out:
            raise ReadError(f"JSON duplicate key {key!r}")
        out[key] = value
    return out


def _refuse(text: str) -> None:
    raise ReadError(f"JSON non-string number or constant {text!r}")


def _stringify(obj: object) -> object:
    """JSON values as BaseLoader would give them: ints become decimal strings."""
    if isinstance(obj, bool) or obj is None:
        raise ReadError(f"JSON value {obj!r} has no YAML string twin")
    if isinstance(obj, int):
        return str(obj)
    if isinstance(obj, list):
        return [_stringify(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _stringify(v) for k, v in obj.items()}
    return obj


def read_twin_json(path: str | Path, yaml_result: dict) -> dict:
    """Read the JSON twin and require it to hold exactly the YAML file's witness."""
    path = Path(path)
    try:
        return _read_twin_json(path, yaml_result)
    except ReadError as exc:
        raise ReadError(f"{path.name}: {exc}") from None


def _read_twin_json(path: Path, yaml_result: dict) -> dict:
    data, text = _load_text(path)
    try:
        doc = json.loads(
            text,
            object_pairs_hook=_json_pairs,
            parse_float=_refuse,
            parse_constant=_refuse,
        )
    except json.JSONDecodeError as exc:
        raise ReadError(f"JSON: {exc}") from None
    if not isinstance(doc, dict) or set(doc) != {"softschema", "witness"}:
        raise ReadError("JSON top level must hold exactly softschema and witness")
    w = doc["witness"]
    if not isinstance(w, dict) or not isinstance(w.get("n"), int) or isinstance(w["n"], bool):
        raise ReadError("JSON witness.n is not an integer")
    as_yaml = _stringify(doc)
    twin = _parse_witness(as_yaml, yaml_result["n"], (yaml_result["representation"],))
    if twin["side_text"] != yaml_result["side_text"]:
        raise ReadError("JSON side differs from the YAML side")
    if twin["raw_squares"] != yaml_result["raw_squares"]:
        raise ReadError("JSON squares differ from the YAML squares")
    for key in ("id", "claim", "source", "certificate"):
        if twin[key] != yaml_result[key]:
            raise ReadError(f"JSON {key} differs from the YAML {key}")
    for sq in w["squares"]:
        if not isinstance(sq["id"], int) or isinstance(sq["id"], bool):
            raise ReadError("JSON square id is not an integer")
    return {
        "path": str(path),
        "sha256": sha256_file(path),
        "bytes": len(data),
        "final_newline": text.endswith("\n"),
        "same_witness_as_yaml": True,
    }
