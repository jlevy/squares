#!/usr/bin/env python3
"""Issue #804's five exact sides: the derived fact, its exact checks and the atlas inputs.

Hyukdong Kim's issue 804 states that the side of the best-known packing at 88, 126, 172,
199 and 263 is a stated root of a stated integer polynomial, irreducible over Q, and
attaches ``squares-exact-forms.zip``, whose ``exact_forms.json`` gives each polynomial,
highest degree first, with the side to 100 digits. The archive states no licence, so the
``hyukdongkim-exact-forms-2026-10-25`` packet keeps no byte of it: only the polynomials
and printed sides, as an exact fact, with the archive's address and digests. Nothing in
the archive is executed: ``exact_forms.json`` is read as JSON data, and the five Python
files in it are pinned by their digests and never opened as code.

- ``derive --archive ZIP [--check]`` holds ``ZIP`` to the issue's SHA-256 and the size
  measured at triage, and writes the packet's ``acquisition/sources.json`` (the attachment,
  every member's path, size and SHA-256, and the source's inputs pinned by Git blob, size
  and SHA-256) and ``facts/exact-forms.json`` (each count's polynomial and printed side).
- ``configurations --archive ZIP [--check]`` holds the author's later attachment,
  ``t244-exact-configurations.zip`` (2026-10-25T09:06:23Z), to the SHA-256 his comment
  states and the size measured when it was read, and each of its two certificates to its
  stated digest, and writes the ``hyukdongkim-t244-configurations-2026-10-25`` packet's
  ``acquisition/sources.json`` and one derived fact per count, ``facts/nN.json.gz``: the
  certificate's content, read as JSON data. Nothing here decides it, and no file of the
  archive is run.
- ``sides [--check]`` is offline. For each count it decides the polynomial primitive and
  irreducible over Q twice, by SymPy's ``factor_list`` and by ``sqpack.field`` through
  ``devtools.exact_sides.algebraic``; counts its real roots by Sturm's theorem; isolates
  the root the printed side names, narrowing it by exact bisection below ``10^-130``; and
  writes ``exact-sides.json`` beside this directory: the root's index among the real
  roots, its cut at `PLACES` places (the ledger's ``cut`` print) and at `CLAIM_PLACES`
  (the register's), and its exact order against the case's rational bounds, every exact
  member of the ledger's frozen start (``starts.yaml``) at 172 and 263 and `CASE_BOUNDS` at
  the three counts the ledger does not walk, and against Evan Daniel's #639 side at the
  count, which T-193 registers at 88, 126 and 199 (``upper-bounds-20261016/exact-sides.json``).
- ``poses --atlas DIR [--check]`` holds each ``best-<n>.json`` that the source read
  (evand/square-packing at `ATLAS_COMMIT`, ``site/www/data/p``) to its pinned blob and
  SHA-256, pairs its squares with the record witness's under each of the box's eight
  symmetries, and writes ``atlas-poses.json``: a measurement, which decides nothing.

A margin is ``house - root``, enclosed between two rationals from the root's enclosure;
both ends are printed to four significant figures. Floating point appears only in
``poses``, which measures binary64 inputs, and in the printed magnitudes.

From ``packing/``, with the project interpreter::

    python campaign/issue-intake/upper-bounds-issue804-20261025/review/exact_forms.py \\
        derive --archive ZIP [--check]
    python campaign/issue-intake/upper-bounds-issue804-20261025/review/exact_forms.py \\
        configurations --archive ZIP [--check]
    python campaign/issue-intake/upper-bounds-issue804-20261025/review/exact_forms.py \\
        sides [--check]
    python campaign/issue-intake/upper-bounds-issue804-20261025/review/exact_forms.py \\
        poses --atlas DIR [--check]
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import sys
import zipfile
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
import sympy
import yaml
from scipy.optimize import linear_sum_assignment

#: The repository root: this file is packing/campaign/issue-intake/<directory>/review/.
REPO = Path(__file__).resolve().parents[5]
PACKING = REPO / "packing"
sys.path.insert(0, str(PACKING))

from devtools import exact_sides  # noqa: E402

HERE = Path(__file__).resolve().parents[1]
PACKET = PACKING / "resources/web/hyukdongkim-exact-forms-2026-10-25"
FACT = PACKET / "facts/exact-forms.json"
SOURCES = PACKET / "acquisition/sources.json"
SIDES = HERE / "exact-sides.json"
POSES = HERE / "atlas-poses.json"
STARTS = HERE / "starts.yaml"
DANIEL = PACKING / "campaign/issue-intake/upper-bounds-20261016/exact-sides.json"
TOOL = "packing/campaign/issue-intake/upper-bounds-issue804-20261025/review/exact_forms.py"

ISSUE = "https://github.com/jlevy/squares/issues/804"
ATTACHMENT = "https://github.com/user-attachments/files/33917140/squares-exact-forms.zip"
#: The digest the issue states, and the size triage measured on 25 October 2026.
ARCHIVE_SHA256 = "c770f9c37dee6b248543f3e661318630a0f279bc6a8c7663cb2efc53e2814ee7"
ARCHIVE_BYTES = 14_112
FORMS_MEMBER = "squares-exact-forms/exact_forms.json"
#: The configurations the author attached to issue 804 at 2026-10-25T09:06:23Z, the
#: digests the comment states for the archive and its two certificates, and the size
#: measured when they were read; and where the second packet keeps what is derived.
CONFIGURATIONS_COMMENT = "https://github.com/jlevy/squares/issues/804#issuecomment-6395743853"
CONFIGURATIONS = (
    "https://github.com/user-attachments/files/33922338/t244-exact-configurations.zip"
)
CONFIGURATIONS_SHA256 = "16e6ad9d04f1def897478e59260880320bc7c06ae89e41fa83837c7dc29c9a2d"
CONFIGURATIONS_BYTES = 96_347
CONFIGURATION_MEMBERS = {
    172: (
        "t244-exact-configurations/n172.minpoly.json",
        "9230aa7aa4c6d4f4e31de4543b87e19db1e57bf4f8e105974c8bd45b203f02db",
    ),
    263: (
        "t244-exact-configurations/n263.minpoly.json",
        "de646870e0ecd0d6c042e4742de023ebbcdddb28aac4aa51469dbf53dc264686",
    ),
}
CONFIGURATIONS_PACKET = PACKING / "resources/web/hyukdongkim-t244-configurations-2026-10-25"
ATLAS_REPOSITORY = "evand/square-packing"
ATLAS_COMMIT = "659ee62e4a9d39542a1146e8b011cc3ab6407ede"
ATLAS_PATH = "site/www/data/p"
#: Each input's Git blob, size and SHA-256 at `ATLAS_COMMIT`, read through the GitHub
#: contents API on 25 October 2026. Every one was last changed at 122d0ba (10 October).
ATLAS_PINS = {
    88: (
        "af223f022c11a6973f2e5f0db1147d175ad16590",
        41_556,
        "f02441637e4a5fa4d9fc613e4fb9b2eab6f945e85bfbaa080cdb0f37f5d9cc63",
    ),
    126: (
        "fefd52c9cf42fa54df02042678ff6cc2a61da19f",
        62_690,
        "861d0ab5db3d6bdda716f22063a02778ac93ab5ca2e371581f7ebb65def6bf0d",
    ),
    172: (
        "9778b097541fa19dc4d394d4eab9b202bf977a70",
        85_344,
        "5c581ee5794dada18183038f1075630c0202d22cedf95ab84fc10bbeb6ddee8a",
    ),
    199: (
        "07891977090660b7f9e730fbdc4e00d245877e6e",
        97_939,
        "633ec9d3b46b1cceb3111e11f57a9c4c37969b5acccbd02ee8f12a12e204fde6",
    ),
    263: (
        "ad6fb297df432d8694f68a2f84d57f8c1cba6d1b",
        134_188,
        "9114dbc58b84852264c4186c954c535aec0afec5d9445d9b212264e88a801842",
    ),
}
COUNTS = tuple(ATLAS_PINS)
#: The case records' verified upper bounds at the three counts the ledger does not walk, as
#: their exact forms stood at main bb756e193 (25 October 2026). At 172 and 263 the ledger's
#: frozen start (``starts.yaml``) gives T-174's sides instead.
CASE_BOUNDS = {
    88: ("record T-127", Fraction(9882451030481246819427281665997, 10**30)),
    126: ("record T-139", Fraction(11742640687119285146522492579501, 10**30)),
    199: ("record T-127", Fraction(7308786086796403421851018497093, 5 * 10**29)),
}
#: What each count's #639 side is to the record: T-193's at the three counts the ledger does
#: not walk, and above T-174's certificates, so not recorded, at 172 and 263.
DANIEL_HELD = (
    "Evan Daniel's #639 side at the count, the one root of its polynomial in its interval "
    "(upper-bounds-20261016/exact-sides.json), which T-193 registers"
)
DANIEL_ABOVE_T174 = (
    "Evan Daniel's #639 side at the count (upper-bounds-20261016/exact-sides.json), which the "
    "16 October ledger did not record"
)
#: The places the ledger's ``cut`` print and the register's claim keep.
PLACES = 120
CLAIM_PLACES = 100
WIDTH = Fraction(1, 10**130)
#: The printed side's half-width, as the source prints it to 100 places.
PRINT_RADIUS = Fraction(1, 10**95)
X = sympy.Symbol("s")


def text_of(document: Any) -> str:
    return json.dumps(document, indent=1, ensure_ascii=False) + "\n"


def written(path: Path, document: Any, *, check: bool) -> int:
    """Write ``document`` to ``path``, or with ``check`` compare it with the file."""
    text = text_of(document)
    if check:
        if not path.is_file() or path.read_text(encoding="utf-8") != text:
            print(f"{path.relative_to(REPO)} differs from a fresh computation")
            return 1
        print(f"{path.relative_to(REPO)} matches")
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path.relative_to(REPO)}")
    return 0


def derive(archive: Path, *, check: bool) -> int:
    data = archive.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != ARCHIVE_SHA256 or len(data) != ARCHIVE_BYTES:
        sys.exit(f"{archive}: SHA-256 {digest}, {len(data)} bytes; not the issue's attachment")
    members: list[dict[str, Any]] = []
    with zipfile.ZipFile(archive) as bundle:
        for info in bundle.infolist():
            if info.is_dir():
                continue
            body = bundle.read(info)
            members.append(
                {
                    "path": info.filename,
                    "bytes": len(body),
                    "sha256": hashlib.sha256(body).hexdigest(),
                    "retained": False,
                }
            )
        rows = json.loads(bundle.read(FORMS_MEMBER).decode("utf-8"))
    forms: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda item: int(item["n"])):
        coefficients = [str(int(value)) for value in row["minimal_polynomial_descending"]]
        if int(row["degree"]) != len(coefficients) - 1:
            sys.exit(f"n = {row['n']}: degree {row['degree']} for {len(coefficients)} terms")
        forms.append(
            {
                "n": int(row["n"]),
                "degree": int(row["degree"]),
                "polynomial_high_to_low": coefficients,
                "printed_side": str(row["side_100_digits"]),
            }
        )
    if tuple(form["n"] for form in forms) != COUNTS:
        sys.exit(f"the archive states counts {[form['n'] for form in forms]}")
    forms_sha256 = next(m["sha256"] for m in members if m["path"] == FORMS_MEMBER)
    fact = {
        "format": "issue-804-exact-forms-fact-v1",
        "derived_by": TOOL,
        "source": {
            "issue": ISSUE,
            "attachment": ATTACHMENT,
            "archive_sha256": ARCHIVE_SHA256,
            "member": FORMS_MEMBER,
            "member_sha256": forms_sha256,
        },
        "note": (
            "Each count's polynomial and printed side as exact_forms.json states them, read "
            "as JSON data; the archive states no licence, so its bytes are not retained."
        ),
        "forms": forms,
    }
    sources = {
        "format": "issue-attachment-sources-v1",
        "issue": ISSUE,
        "attachment": {
            "url": ATTACHMENT,
            "bytes": ARCHIVE_BYTES,
            "sha256": ARCHIVE_SHA256,
            "sha256_stated_by_issue": True,
            "raw_asset_retained": False,
            "licence": "none stated",
        },
        "members": members,
        "inputs": {
            "repository": ATLAS_REPOSITORY,
            "commit": ATLAS_COMMIT,
            "retained": False,
            "files": [
                {
                    "path": f"{ATLAS_PATH}/best-{n}.json",
                    "blob": blob,
                    "bytes": size,
                    "sha256": sha,
                }
                for n, (blob, size, sha) in ATLAS_PINS.items()
            ],
        },
    }
    return written(FACT, fact, check=check) | written(SOURCES, sources, check=check)


def written_gzip(path: Path, document: Any, *, check: bool) -> int:
    """Write ``document`` as deterministic gzip JSON, or with ``check`` compare it."""
    data = gzip.compress(text_of(document).encode("utf-8"), mtime=0)
    if check:
        if not path.is_file() or path.read_bytes() != data:
            print(f"{path.relative_to(REPO)} differs from a fresh computation")
            return 1
        print(f"{path.relative_to(REPO)} matches")
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    print(f"wrote {path.relative_to(REPO)}")
    return 0


def configurations(archive: Path, *, check: bool) -> int:
    """Keep the author's two configurations as derived exact facts, read as JSON data.

    The archive is held to the digest the comment states and the size measured when it
    was read, and each certificate to its stated digest, before anything in it is parsed.
    Each fact keeps the certificate's content, the field polynomial, the root's interval,
    the side and every square's centre and half-angle tangent as elements of the field,
    with its source's digests; nothing here decides it.
    """
    data = archive.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != CONFIGURATIONS_SHA256 or len(data) != CONFIGURATIONS_BYTES:
        sys.exit(
            f"{archive}: SHA-256 {digest}, {len(data)} bytes; not the comment's attachment"
        )
    members: list[dict[str, Any]] = []
    status = 0
    with zipfile.ZipFile(archive) as bundle:
        for info in bundle.infolist():
            if info.is_dir():
                continue
            body = bundle.read(info)
            members.append(
                {
                    "path": info.filename,
                    "bytes": len(body),
                    "sha256": hashlib.sha256(body).hexdigest(),
                    "retained": False,
                }
            )
        measured = {member["path"]: member["sha256"] for member in members}
        for n, (member, sha) in CONFIGURATION_MEMBERS.items():
            if measured.get(member) != sha:
                sys.exit(f"{member}: SHA-256 {measured.get(member)}, not the stated {sha}")
            content = json.loads(bundle.read(member).decode("utf-8"))
            if int(content["n"]) != n or len(content["squares"]) != n:
                sys.exit(f"{member}: n = {content['n']} with {len(content['squares'])} squares")
            fact = {
                "format": "issue-804-configuration-fact-v1",
                "derived_by": TOOL,
                "source": {
                    "comment": CONFIGURATIONS_COMMENT,
                    "attachment": CONFIGURATIONS,
                    "archive_sha256": CONFIGURATIONS_SHA256,
                    "member": member,
                    "member_sha256": sha,
                },
                "note": (
                    "The certificate's content in evand/square-packing's minpoly.json "
                    "format (verify_exact.py), read as JSON data; the archive states no "
                    "licence, so its bytes are not retained. Not decided here."
                ),
                "field_degree": len(content["field"]["f"]) - 1,
                "squares": len(content["squares"]),
                "configuration": content,
            }
            status |= written_gzip(
                CONFIGURATIONS_PACKET / f"facts/n{n}.json.gz", fact, check=check
            )
    sources = {
        "format": "issue-attachment-sources-v1",
        "issue": ISSUE,
        "comment": CONFIGURATIONS_COMMENT,
        "attachment": {
            "url": CONFIGURATIONS,
            "bytes": CONFIGURATIONS_BYTES,
            "sha256": CONFIGURATIONS_SHA256,
            "sha256_stated_by_comment": True,
            "raw_asset_retained": False,
            "licence": "none stated",
        },
        "members": members,
    }
    return status | written(
        CONFIGURATIONS_PACKET / "acquisition/sources.json", sources, check=check
    )


def forms() -> list[dict[str, Any]]:
    return json.loads(FACT.read_text(encoding="utf-8"))["forms"]


def value_at(poly: Sequence[int], point: Fraction) -> Fraction:
    total = Fraction(0)
    for coefficient in poly:
        total = total * point + coefficient
    return total


def isolate(poly: Sequence[int], low: Fraction, high: Fraction) -> tuple[Fraction, Fraction]:
    """Narrow ``[low, high]``, where ``poly`` has one simple root, below `WIDTH`."""
    low_positive = value_at(poly, low) > 0
    while high - low >= WIDTH:
        middle = (low + high) / 2
        at = value_at(poly, middle)
        if at == 0:
            sys.exit("the root is rational, so the polynomial is not irreducible")
        if (at > 0) == low_positive:
            low = middle
        else:
            high = middle
    return low, high


def cut(low: Fraction, high: Fraction, places: int) -> str:
    """The root in ``[low, high]`` cut at ``places``: it lies in ``[cut, cut + 10^-places)``."""
    scale = 10**places
    floor_low, floor_high = math.floor(low * scale), math.floor(high * scale)
    if floor_low != floor_high:
        sys.exit("the root sits on a cut boundary; narrow it further")
    whole, fraction = divmod(floor_low, scale)
    return f"{whole}.{fraction:0{places}d}"


def magnitude(value: Fraction) -> str:
    return f"{float(value):.4g}"


def rational(text: str) -> Fraction:
    return Fraction(text.strip())


def case_bounds(n: int) -> list[tuple[str, str, Fraction]]:
    """The rational sides the root is ordered against at ``n``: each exact member of the
    ledger's frozen start, or where the ledger does not walk ``n``, `CASE_BOUNDS`."""
    if n in CASE_BOUNDS:
        label, side = CASE_BOUNDS[n]
        return [(label, "the case record's verified upper bound at main bb756e193", side)]
    starts = yaml.safe_load(STARTS.read_text(encoding="utf-8"))
    row = next(item for item in starts["counts"] if int(item["n"]) == n)
    return [
        (str(member["label"]), str(member["holders"]), rational(str(member["low"])))
        for member in row["members"]
        if str(member["model"]) == "exact" and str(member["low"]) == str(member["high"])
    ]


def daniel_side(n: int) -> tuple[exact_sides.Side, dict[str, Any]]:
    document = json.loads(DANIEL.read_text(encoding="utf-8"))
    row = next(item for item in document["rows"] if int(item["n"]) == n)
    poly = [int(value) for value in reversed(row["polynomial_low_to_high"])]
    low, high = (rational(end) for end in row["interval"])
    return exact_sides.algebraic(poly, (low, high)), row


def against_rational(
    root: exact_sides.Side, low: Fraction, high: Fraction, house: Fraction
) -> str:
    order = exact_sides.compare(root, house)
    if order >= 0:
        return {0: "equal", 1: "above"}[order]
    return f"below by {magnitude(house - high)} to {magnitude(house - low)}"


def side_row(form: dict[str, Any]) -> dict[str, Any]:
    n = int(form["n"])
    poly = [int(value) for value in form["polynomial_high_to_low"]]
    sympy_poly = sympy.Poly(poly, X, domain=sympy.ZZ)
    content = int(sympy_poly.content())
    _, factors = sympy_poly.factor_list()
    irreducible = (
        content == 1
        and len(factors) == 1
        and factors[0][1] == 1
        and factors[0][0].degree() == sympy_poly.degree()
    )
    printed = rational(form["printed_side"])
    low, high = printed - PRINT_RADIUS, printed + PRINT_RADIUS
    in_print = int(sympy_poly.count_roots(sympy.Rational(low), sympy.Rational(high)))
    if in_print != 1 or value_at(poly, low) * value_at(poly, high) >= 0:
        sys.exit(f"n = {n}: {in_print} roots within 1e-95 of the printed side")
    # sqpack.field decides irreducibility and the one root again, independently of SymPy.
    side = exact_sides.algebraic(poly, (low, high))
    low, high = isolate(poly, low, high)
    real_roots = int(sympy_poly.count_roots())
    below = int(sympy_poly.count_roots(None, sympy.Rational(low)))
    daniel, daniel_row = daniel_side(n)
    daniel_low, daniel_high = exact_sides.enclosure(daniel, WIDTH)
    same = tuple(int(c) for c in reversed(daniel_row["polynomial_low_to_high"])) == tuple(poly)
    order = exact_sides.compare(side, daniel)
    relation = {-1: "below", 0: "equal", 1: "above"}[order]
    to_daniel: dict[str, Any] = {
        "against": DANIEL_HELD if n in CASE_BOUNDS else DANIEL_ABOVE_T174,
        "degree": len(daniel_row["polynomial_low_to_high"]) - 1,
        "same_polynomial": same,
        "relation": relation,
    }
    if order < 0:
        to_daniel["margin"] = (
            f"{magnitude(daniel_low - high)} to {magnitude(daniel_high - low)}"
        )
    houses = [
        {
            "member": label,
            "holders": holders,
            "relation": against_rational(side, low, high, house),
        }
        for label, holders, house in case_bounds(n)
    ]
    return {
        "n": n,
        "degree": len(poly) - 1,
        "polynomial_high_to_low": [str(c) for c in poly],
        "primitive": content == 1,
        "irreducible_sympy": irreducible,
        "irreducible_sqpack_field": isinstance(side, exact_sides.Algebraic),
        "real_roots": real_roots,
        "root_index_ascending": below + 1,
        "interval": [str(low), str(high)],
        "printed_side_within": magnitude(abs(printed - low)),
        "print": cut(low, high, PLACES),
        "rounding": "cut",
        "claim_cut": cut(low, high, CLAIM_PLACES) + "…",
        "ceiling_40": exact_sides.ceiling(side, 40),
        "form": exact_sides.form(side)
        if isinstance(side, exact_sides.Algebraic)
        else str(side),
        "against_daniel_639": to_daniel,
        "against_case_bounds": houses,
    }


def sides(*, check: bool) -> int:
    rows = []
    for form in forms():
        row = side_row(form)
        rows.append(row)
        print(
            row["n"],
            row["degree"],
            row["irreducible_sympy"],
            row["root_index_ascending"],
            "of",
            row["real_roots"],
            row["against_daniel_639"]["relation"],
            "; ".join(house["relation"] for house in row["against_case_bounds"]),
        )
    document = {
        "format": "issue-804-exact-sides-v1",
        "tool": TOOL,
        "fact": str(FACT.relative_to(REPO)),
        "fact_sha256": hashlib.sha256(FACT.read_bytes()).hexdigest(),
        "starts": str(STARTS.relative_to(REPO)),
        "places": PLACES,
        "claim_places": CLAIM_PLACES,
        "rows": rows,
    }
    return written(SIDES, document, check=check)


def witness(n: int) -> tuple[dict[str, Any], np.ndarray, np.ndarray, float]:
    path = PACKING / f"witnesses/known-best/n-{n:03d}.yaml"
    document = yaml.safe_load(path.read_text(encoding="utf-8"))["witness"]
    centres, angles = [], []
    for square in document["squares"]:
        cx, cy = (float(Fraction(str(v))) for v in square["center"])
        bx, by = (float(Fraction(str(v))) for v in square["basis"])
        centres.append((cx, cy))
        angles.append(math.degrees(math.atan2(by, bx)) % 90.0)
    record = {
        "id": str(document["id"]),
        "path": str(path.relative_to(REPO)),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }
    side = float(Fraction(str(document["side"])))
    return record, np.array(centres), np.array(angles), side


def mapped(
    centres: np.ndarray, angles: np.ndarray, side: float, symmetry: int
) -> tuple[np.ndarray, np.ndarray]:
    """The image under one of the box's eight symmetries: a swap of the axes, then
    reflections in x and in y, each turning every square's angle the other way."""
    x, y, turned = centres[:, 0], centres[:, 1], angles.copy()
    if symmetry & 1:
        x, y, turned = y, x, -turned
    if symmetry & 2:
        x, turned = side - x, -turned
    if symmetry & 4:
        y, turned = side - y, -turned
    return np.stack([x, y], axis=1), turned % 90.0


def pose_row(n: int, atlas: Path) -> dict[str, Any]:
    blob, size, sha = ATLAS_PINS[n]
    path = atlas / f"best-{n}.json"
    data = path.read_bytes()
    git_blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data, usedforsecurity=False)
    if (git_blob.hexdigest(), len(data), hashlib.sha256(data).hexdigest()) != (blob, size, sha):
        sys.exit(f"{path}: not the pinned best-{n}.json at {ATLAS_COMMIT[:7]}")
    document = json.loads(data.decode("utf-8"))
    squares = np.array(document["squares"], dtype=float)
    record, w_centres, w_angles, side = witness(n)
    if len(squares) != n or len(w_centres) != n:
        sys.exit(f"n = {n}: {len(squares)} atlas squares, {len(w_centres)} witness squares")
    best: tuple[float, int, np.ndarray, np.ndarray] | None = None
    for symmetry in range(8):
        centres, angles = mapped(squares[:, :2], squares[:, 2] % 90.0, side, symmetry)
        cost = np.linalg.norm(w_centres[:, None, :] - centres[None, :, :], axis=2)
        rows, cols = linear_sum_assignment(cost)
        moves = cost[rows, cols]
        turns = np.abs(w_angles[rows] - angles[cols])
        turns = np.minimum(turns, 90.0 - turns)
        if best is None or float(moves.max()) < best[0]:
            best = (float(moves.max()), symmetry, moves, turns)
    assert best is not None
    largest, symmetry, moves, turns = best
    return {
        "n": n,
        "atlas_file": f"{ATLAS_REPOSITORY}@{ATLAS_COMMIT[:7]} {ATLAS_PATH}/best-{n}.json",
        "atlas_side": str(document["s"]),
        "witness": record,
        "best_symmetry": symmetry,
        "max_move": float(f"{largest:.4g}"),
        "moved_beyond_1e-12": int((moves > 1e-12).sum()),
        "moved_beyond_1e-6": int((moves > 1e-6).sum()),
        "moved_beyond_1e-3": int((moves > 1e-3).sum()),
        "moved_beyond_0.1": int((moves > 0.1).sum()),
        "max_turn_deg": float(f"{float(turns.max()):.4g}"),
    }


def poses(atlas: Path, *, check: bool) -> int:
    rows = [pose_row(n, atlas) for n in COUNTS]
    for row in rows:
        print(row["n"], row["witness"]["id"], row["max_move"], row["moved_beyond_1e-6"])
    document = {
        "format": "issue-804-atlas-poses-v1",
        "tool": TOOL,
        "note": (
            "Each atlas packing the source read, paired square by square with the record "
            "witness at its count by an optimal assignment on centres, under the symmetry "
            "of the box that makes the largest move least. A measurement; it decides nothing."
        ),
        "rows": rows,
    }
    return written(POSES, document, check=check)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", maxsplit=1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    derive_parser = commands.add_parser("derive")
    derive_parser.add_argument("--archive", type=Path, required=True)
    derive_parser.add_argument("--check", action="store_true")
    configurations_parser = commands.add_parser("configurations")
    configurations_parser.add_argument("--archive", type=Path, required=True)
    configurations_parser.add_argument("--check", action="store_true")
    sides_parser = commands.add_parser("sides")
    sides_parser.add_argument("--check", action="store_true")
    poses_parser = commands.add_parser("poses")
    poses_parser.add_argument("--atlas", type=Path, required=True)
    poses_parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "derive":
        return derive(args.archive, check=args.check)
    if args.command == "configurations":
        return configurations(args.archive, check=args.check)
    if args.command == "sides":
        return sides(check=args.check)
    return poses(args.atlas, check=args.check)


if __name__ == "__main__":
    sys.exit(main())
