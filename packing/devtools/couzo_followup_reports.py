"""Couzo's five follow-up rational certificates at 2d32a6e: derived custody and replay.

Francisco Couzo's repository states no licence, and this packet takes the derived-only
form of the known-best retention policy (``resources/web/known-best-packings/README.md``,
``devtools.upper_bound_packets``): no upstream byte enters Git. ``acquire`` reads a
local Git object store at the pinned commit, never a checkout, and writes exact rational
Witness/v2 facts and the complete pinned tree. The packet keeps no certificate, decimal
pose, SVG, prose or program.

Every digest comparison here crosses one boundary (OR-16): Couzo's repository, whose
bytes stay outside Git. The expected values are its commit, tree and blob identities,
pinned in ``REVISION``, ``TREE`` and ``PARENT`` and recorded in full in the acquisition
record. ``read_facts`` (``check-packet``) rebuilds the tree root from every leaf and each
certificate's text from the retained facts, holding it against its pinned blob identity,
the only retained witness of the unretained bytes; that catches an edited, rounded or
dropped coordinate. It also holds the seven certificates the author calls unchanged
against the issue451 packet's acquisition roster. No comparison names a file this
repository wrote, decides geometry or pins code.

Only the five rational certificates enter geometry decisions, through the maintained
two-route kernel of ``devtools.evand_arrangement_reports``: a positive, a
duplicate-square and an outside-container job for each count. No source program,
optimizer, KKT or local/global optimality claim is replayed.

From ``packing/``, with the project interpreter::

    python -m devtools.couzo_followup_reports acquire --git-dir SCRATCH/couzo.git
    python -m devtools.couzo_followup_reports check-packet
    python -m devtools.couzo_followup_reports certify --jobs-dir SCRATCH/jobs --workers 2
    python -m devtools.couzo_followup_reports check [--replay]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_output_file

from devtools import couzo_extended_reports as extended
from devtools import couzo_refinement_reports as earlier
from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools.upper_bound_packets import parse_couzo
from sqpack.witness import (
    WitnessError,
    validate_witness_document,
    witness_document,
    witness_envelope,
)
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/couzo-followup-refinements-2026-10-08"
REPOSITORY = "franciscouzo/square-packing"
SOURCE = f"https://github.com/{REPOSITORY}"
REVISION = "2d32a6e96f55c5dc1a2dd0e3581098e7c0105252"
TREE = "1e98bf6ddb40deac1874eabc0c109b30edb6e2ad"
PARENT = earlier.REVISION
COMMITTED = "2026-10-08T22:12:27Z"
RETRIEVED = "2026-10-09"
COMMENT = "https://github.com/jlevy/squares/pull/460#issuecomment-6070798890"
NUMBERS = (84, 86, 105, 175, 270)
UNCHANGED = (108, 127, 131, 155, 180, 228, 306)
SOURCE_ID = "couzo-followup-refinements-2026-10-08"
SOURCE_KEY = "[Couzo follow-up refinements 2026-10-08]"
REPORT_EVIDENCE = "E-couzo-460-followup-rational-report"
ACQUISITION_FORMAT = "external-source-acquisition-v1"
RECEIPT_FORMAT = "couzo-460-followup-exact-replay-v1"
WITNESS_PREFIX = "W-couzo-460-followup-n"
CLAIM_LIMITATIONS = (
    "Complete 2d32a6e rational centre/half-angle certificate converted exactly from "
    "the pinned source, whose bytes are not retained. Finite construction feasibility "
    "only; no optimizer, KKT, local minimum, rigidity, novelty, priority or global "
    "optimality claim."
)
LICENSING_REVIEW = (
    "The pinned tree has no licence file and its README states no reuse terms. "
    "certificates/README.md names the MIT-licensed exact contact solver that wrote the "
    "certificates; that notice does not license this bundle. No redistribution "
    "permission or licence determination is asserted."
)
QUALIFICATION = (
    "Five author-reported exact rational certificates at n=84,86,105,175,270, kept as "
    "derived rational Witness/v2 facts that rebuild each pinned certificate blob. The "
    "seven other certificates and their decimal poses are byte-identical to the issue451 "
    "packet's ffd900d originals. The two n375/n378 inputs at this commit are recorded by "
    "identity only. No raw upstream byte, author program or optimality claim."
)
#: The certificate format's one comment line, reconstructed with every certificate.
LAYOUT_HEADER = (
    "# exact certificate: unit squares, centre (x, y), rotation (c, s) = "
    "((1-t^2)/(1+t^2), 2t/(1+t^2)); check with verify_cert.py\n"
)
#: The source comment's table, quoted as printed: S_n rounded up to twelve places.
COMMENT_SIDES = {
    84: "9.697934799015",
    86: "9.820535407497",
    105: "10.789303783749",
    175: "13.767155163543",
    270: "16.936723022877",
}
OUTSIDE_HORIZON = (375, 378)
PINNED_ONLY = ("README.md", "certificates/README.md")
MAX_SOURCE_BYTES = 1_000_000
MAX_LITERAL_CHARS = 400
MAX_SCALAR_BITS = 512
JOB_TIMEOUT = kernel.JOB_TIMEOUT
JOBS = kernel.JOBS
ROUTES = kernel.ROUTES
SCHEMA = "../../../../witnesses/witness.schema.yaml"
LITERAL = re.compile(r"-?[0-9]+(?:/[1-9][0-9]*)?")
SHA1 = re.compile(r"[0-9a-f]{40}")
SOURCE_FIELDS = {
    "id",
    "source_url",
    "source_commit",
    "committed_utc",
    "source_key",
    "author",
    "licence",
    "retention_policy",
    "raw_asset_retained",
    "licensing_review",
    "subtree_scope",
    "pinned_only",
    "cases",
    "unchanged",
    "outside_horizon",
    "custody",
    "qualification",
}
CASE_FIELDS = {
    "n",
    "file",
    "source_blob",
    "size",
    "sha256",
    "side",
    "comment_side",
    "derived_fact",
    "decimal_pose",
    "prior",
}


class ReportError(kernel.ReportError):
    """Refuse incomplete source custody, derived facts, geometry or receipts."""


def ensure_private(path: Path) -> None:
    if path.is_symlink() or not path.resolve().is_relative_to(REPO.resolve()):
        raise ReportError("scientific custody/output must remain private")


def certificate_path(n: int) -> str:
    return f"certificates/n{n}.cert"


def fact_path(n: int) -> Path:
    return PACKET / f"facts/n-{n:03d}.yaml"


def sources_path() -> Path:
    return PACKET / "acquisition/sources.json"


def receipt_path() -> Path:
    return PACKET / "receipts/exact-certification.json.xz"


def private_input_paths() -> tuple[Path, ...]:
    """The acquisition record, all five derived facts and the fifteen-job receipt."""
    return (sources_path(), *(fact_path(n) for n in NUMBERS), receipt_path())


def exact(text: Any, where: str) -> Fraction:
    """A canonical rational literal, bounded in length and in bits."""
    if (
        type(text) is not str
        or len(text) > MAX_LITERAL_CHARS
        or LITERAL.fullmatch(text) is None
    ):
        raise ReportError(f"{where}: not a bounded rational literal")
    value = Fraction(text)
    if legacy.literal(value) != text:
        raise ReportError(f"{where}: rational literal is not in lowest terms")
    if max(abs(value.numerator).bit_length(), value.denominator.bit_length()) > MAX_SCALAR_BITS:
        raise ReportError(f"{where}: rational literal exceeds the bounded profile")
    return value


def render(certificate: legacy.Certificate) -> str:
    """The source certificate's exact text, from its numbers and the fixed layout."""
    return (
        LAYOUT_HEADER
        + f"{certificate.n} {legacy.literal(certificate.side)}\n"
        + "".join(
            f"{legacy.literal(p.x)} {legacy.literal(p.y)} {legacy.literal(p.t)}\n"
            for p in certificate.poses
        )
    )


def admit_certificate(text: str, n: int) -> legacy.Certificate:
    """Parse one complete certificate and refuse any byte the layout does not rebuild."""
    try:
        certificate = legacy.parse(text, expected_n=n)
    except legacy.CertificateError as error:
        raise ReportError(f"n={n}: {error}") from error
    for where, value in (
        ("side", certificate.side),
        *(
            (f"square {i}", value)
            for i, pose in enumerate(certificate.poses, start=1)
            for value in (pose.x, pose.y, pose.t, *pose.basis)
        ),
    ):
        exact(legacy.literal(value), f"n={n} {where}")
    if render(certificate) != text:
        raise ReportError(f"n={n}: certificate is not in the fixed source layout")
    return certificate


def fact(certificate: legacy.Certificate) -> dict[str, Any]:
    """The derived Witness/v2: exactly the positive job's deciding witness, with source."""
    witness = kernel.to_witness(
        certificate, witness_prefix=WITNESS_PREFIX, claim_limitations=CLAIM_LIMITATIONS
    )
    witness["source"] = {
        "key": SOURCE_KEY,
        "path": f"packing/resources/web/{PACKET.name}/acquisition/sources.json",
        "url": f"{SOURCE}/blob/{REVISION}/{certificate_path(certificate.n)}",
        "retrieved": RETRIEVED,
        "revision": REVISION,
    }
    return witness


def certificate_from_fact(n: int, witness: Any) -> legacy.Certificate:
    """Recover every centre and half-angle exactly; refuse a basis that is not one."""
    if (
        type(witness) is not dict
        or witness.get("n") != n
        or type(witness.get("n")) is not int
        or witness.get("representation") != "center-basis"
        or witness.get("scalar") != {"kind": "rational"}
        or type(witness.get("squares")) is not list
        or len(witness["squares"]) != n
    ):
        raise ReportError(f"n={n}: derived fact is not a complete rational centre-basis")
    side = exact(witness.get("side"), f"n={n} side")
    poses = []
    for index, square in enumerate(witness["squares"], start=1):
        if (
            type(square) is not dict
            or set(square) != {"id", "center", "basis"}
            or square["id"] != index
            or type(square["center"]) is not list
            or type(square["basis"]) is not list
            or len(square["center"]) != 2
            or len(square["basis"]) != 2
        ):
            raise ReportError(f"n={n} square {index}: incomplete exact pose")
        x, y = (exact(value, f"n={n} square {index}") for value in square["center"])
        c, s = (exact(value, f"n={n} square {index}") for value in square["basis"])
        if c == -1:
            raise ReportError(f"n={n} square {index}: no finite half-angle")
        pose = legacy.Pose(x, y, s / (1 + c))
        if pose.basis != (c, s):
            raise ReportError(f"n={n} square {index}: basis is not an exact rotation")
        poses.append(pose)
    return legacy.Certificate(n, side, tuple(poses))


def git(git_dir: Path, *arguments: str) -> bytes:
    """Read the local object store only: no checkout, network, hook or author program."""
    completed = subprocess.run(
        ["git", "--git-dir", str(git_dir), *arguments],
        capture_output=True,
        check=False,
        timeout=60,
    )
    if completed.returncode:
        raise ReportError(f"git {arguments[0]} failed: {completed.stderr.decode()[:200]}")
    return completed.stdout


def read_commit(git_dir: Path) -> None:
    raw = git(git_dir, "cat-file", "commit", REVISION)
    if extended.git_identity("commit", raw) != REVISION:
        raise ReportError("acquired commit object differs from its pinned identity")
    head = raw.decode("utf-8").split("\n\n", 1)[0].splitlines()
    trees = [line[5:] for line in head if line.startswith("tree ")]
    parents = [line[7:] for line in head if line.startswith("parent ")]
    committer = [line for line in head if line.startswith("committer ")]
    if trees != [TREE] or parents != [PARENT] or len(committer) != 1:
        raise ReportError("pinned commit's tree or parent differs")
    if not committer[0].endswith(" 1791497547 +0000"):
        raise ReportError("pinned commit's committer time differs")


def read_tree(git_dir: Path) -> dict[str, dict[str, Any]]:
    """Every leaf of the pinned tree, rebuilt to its root before anything is read."""
    listing = git(git_dir, "ls-tree", "-r", "-l", "-z", "--full-tree", REVISION)
    leaves: dict[str, dict[str, Any]] = {}
    for entry in listing.decode("utf-8").split("\0"):
        if not entry:
            continue
        meta, _, path = entry.partition("\t")
        mode, kind, sha, size = meta.split()
        if path in leaves:
            raise ReportError("duplicate pinned tree path")
        leaves[path] = {
            "path": path,
            "mode": mode,
            "type": kind,
            "sha": sha,
            "size": int(size),
            "url": f"https://api.github.com/repos/{REPOSITORY}/git/blobs/{sha}",
        }
    if check_tree(leaves) != TREE:
        raise ReportError("pinned tree leaves do not rebuild the pinned root")
    return dict(sorted(leaves.items()))


def check_tree(leaves: Any) -> str:
    try:
        return extended.tree_root(leaves)
    except ValueError as error:
        raise ReportError(f"pinned tree: {error}") from error


def read_blob(git_dir: Path, leaf: dict[str, Any]) -> bytes:
    raw = git(git_dir, "cat-file", "blob", leaf["sha"])
    if (
        len(raw) > MAX_SOURCE_BYTES
        or len(raw) != leaf["size"]
        or extended.git_identity("blob", raw) != leaf["sha"]
    ):
        raise ReportError(f"{leaf['path']}: blob bytes differ from the pinned tree")
    return raw


def printed_side(text: str, n: int) -> str:
    """The decimal pose's printed side, a quote; its poses decide nothing here."""
    count, side, rows = parse_couzo(text)
    if count != n or len(rows) != n:
        raise ReportError(f"n{n}.txt: decimal pose count differs")
    try:
        value = Decimal(side)
    except InvalidOperation as error:
        raise ReportError(f"n{n}.txt: invalid printed side") from error
    if not value.is_finite() or value <= 0:
        raise ReportError(f"n{n}.txt: invalid printed side")
    return side


def prior_state(n: int) -> dict[str, Any]:
    """The selected and verified ceilings this certificate is compared with, frozen."""
    packing = legacy.case_record(n)
    reported, verified = packing["reported_upper_bound"], packing["verified_upper_bound"]
    prior: dict[str, Any] = {
        "selected_source_key": reported["source_key"],
        "selected_exact": reported["exact_form"],
        "verified_exact": verified["exact_form"],
        "verified_evidence": list(verified["evidence"]),
    }
    if n == 105:
        prior["earlier_couzo_451_exact"] = legacy.literal(earlier.read_facts()[105].side)
    return prior


def check_prior(n: int, side: Fraction, prior: Any) -> None:
    keys = {"selected_source_key", "selected_exact", "verified_exact", "verified_evidence"}
    if n == 105:
        keys.add("earlier_couzo_451_exact")
    if type(prior) is not dict or set(prior) != keys:
        raise ReportError(f"n={n}: incomplete frozen comparison")
    for key in keys - {"selected_source_key", "verified_evidence"}:
        if not side < exact(prior[key], f"n={n} {key}"):
            raise ReportError(f"n={n}: certificate side is not below its comparison {key}")


def check_unchanged(leaves: dict[str, Any]) -> list[dict[str, Any]]:
    """The seven certificates and poses the author calls unchanged, held to issue451's."""
    pins = earlier.source_pins()
    if tuple(pins) != (105, *UNCHANGED):
        raise ReportError("issue451 acquisition roster differs")
    rows = []
    for n in UNCHANGED:
        row: dict[str, Any] = {"n": n}
        for role, field in (("certificate", "certificate_blob"), ("decimal_pose", "pose_blob")):
            path = pins[n][role]["path"]
            if leaves.get(path, {}).get("sha") != pins[n][role]["git_blob"]:
                raise ReportError(f"{path}: not byte-identical to the issue451 original")
            row[field] = pins[n][role]["git_blob"]
        rows.append(row)
    return rows


def acquire_contents(git_dir: Path) -> dict[str, bytes]:
    """Preflight complete custody and every derived fact before producing any output."""
    read_commit(git_dir)
    leaves = read_tree(git_dir)
    cases = []
    outputs: dict[str, bytes] = {}
    for n in NUMBERS:
        leaf = leaves[certificate_path(n)]
        raw = read_blob(git_dir, leaf)
        certificate = admit_certificate(raw.decode("utf-8"), n)
        text = witness_document(fact(certificate), schema=SCHEMA)
        validate_witness_document(
            load_yaml(text),
            path=fact_path(n),
            fallback_schema=ROOT / "witnesses/witness.schema.yaml",
        )
        outputs[f"facts/n-{n:03d}.yaml"] = text.encode()
        pose = leaves[f"n{n}.txt"]
        prior = prior_state(n)
        check_prior(n, certificate.side, prior)
        cases.append(
            {
                "n": n,
                "file": certificate_path(n),
                "source_blob": leaf["sha"],
                "size": leaf["size"],
                "sha256": hashlib.sha256(raw).hexdigest(),
                "side": legacy.literal(certificate.side),
                "comment_side": COMMENT_SIDES[n],
                "derived_fact": f"facts/n-{n:03d}.yaml",
                "decimal_pose": {
                    "file": pose["path"],
                    "blob": pose["sha"],
                    "printed_side": printed_side(read_blob(git_dir, pose).decode("utf-8"), n),
                },
                "prior": prior,
            }
        )
    outside = []
    for n in OUTSIDE_HORIZON:
        pose = leaves[f"n{n}.txt"]
        outside.append(
            {
                "n": n,
                "file": pose["path"],
                "blob": pose["sha"],
                "printed_side": printed_side(read_blob(git_dir, pose).decode("utf-8"), n),
            }
        )
    record = {
        "format": ACQUISITION_FORMAT,
        "sources": [
            {
                "id": SOURCE_ID,
                "source_url": SOURCE,
                "source_commit": REVISION,
                "committed_utc": COMMITTED,
                "source_key": SOURCE_KEY,
                "author": "Francisco Couzo",
                "licence": None,
                "retention_policy": "metadata-and-derived-numerical-facts-only",
                "raw_asset_retained": False,
                "licensing_review": LICENSING_REVIEW,
                "subtree_scope": [certificate_path(n) for n in NUMBERS],
                "pinned_only": [
                    {"path": path, "blob": leaves[path]["sha"], "reason": "prose, not copied"}
                    for path in PINNED_ONLY
                ],
                "cases": cases,
                "unchanged": check_unchanged(leaves),
                "outside_horizon": outside,
                "custody": {
                    "repository": REPOSITORY,
                    "commit": {
                        "sha": REVISION,
                        "tree": {"sha": TREE},
                        "parents": [{"sha": PARENT}],
                    },
                    "tree": leaves,
                },
                "qualification": QUALIFICATION,
            }
        ],
    }
    outputs["acquisition/sources.json"] = (
        json.dumps(record, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    ).encode()
    return outputs


def acquire(git_dir: Path, destination: Path | None = None) -> None:
    destination = PACKET if destination is None else destination
    ensure_private(destination)
    if (destination / "facts").exists() or (destination / "acquisition").exists():
        raise ReportError("acquisition writes a fresh derived packet only")
    outputs = acquire_contents(git_dir)
    for name, raw in outputs.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        ensure_private(target.parent)
        with atomic_output_file(target) as temporary:
            temporary.write_bytes(raw)


def read_record(path: Path) -> dict[str, Any]:
    ensure_private(path)
    with path.open("rb") as stream:
        raw = stream.read(extended.MAX_DECODED_BYTES + 1)
    if len(raw) > extended.MAX_DECODED_BYTES:
        raise ReportError("acquisition record exceeds its byte ceiling")
    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=extended.unique_object,
        parse_constant=extended.reject_constant,
    )
    if (
        type(value) is not dict
        or set(value) != {"format", "sources"}
        or value["format"] != ACQUISITION_FORMAT
        or type(value["sources"]) is not list
        or len(value["sources"]) != 1
        or type(value["sources"][0]) is not dict
    ):
        raise ReportError("one complete derived acquisition record is required")
    return value["sources"][0]


def check_source(source: dict[str, Any]) -> dict[str, Any]:
    """Fixed identity, derived-only retention and the complete pinned tree."""
    if (
        set(source) != SOURCE_FIELDS
        or source["id"] != SOURCE_ID
        or source["source_url"] != SOURCE
        or source["source_commit"] != REVISION
        or source["committed_utc"] != COMMITTED
        or source["source_key"] != SOURCE_KEY
        or source["author"] != "Francisco Couzo"
        or source["licence"] is not None
        or source["retention_policy"] != "metadata-and-derived-numerical-facts-only"
        or source["raw_asset_retained"] is not False
        or source["licensing_review"] != LICENSING_REVIEW
        or source["qualification"] != QUALIFICATION
        or source["subtree_scope"] != [certificate_path(n) for n in NUMBERS]
    ):
        raise ReportError("source identity or derived-only retention differs")
    custody = source["custody"]
    if (
        type(custody) is not dict
        or set(custody) != {"repository", "commit", "tree"}
        or custody["repository"] != REPOSITORY
        or custody["commit"]
        != {"sha": REVISION, "tree": {"sha": TREE}, "parents": [{"sha": PARENT}]}
    ):
        raise ReportError("pinned commit metadata differs")
    leaves = custody["tree"]
    if check_tree(leaves) != TREE:
        raise ReportError("retained leaves do not rebuild the pinned tree")
    if source["pinned_only"] != [
        {"path": path, "blob": leaves[path]["sha"], "reason": "prose, not copied"}
        for path in PINNED_ONLY
    ]:
        raise ReportError("hash-pinned prose roster differs")
    if source["unchanged"] != check_unchanged(leaves):
        raise ReportError("unchanged-certificate roster differs")
    outside = source["outside_horizon"]
    if (
        type(outside) is not list
        or [row.get("n") for row in outside if type(row) is dict] != list(OUTSIDE_HORIZON)
        or any(
            set(row) != {"n", "file", "blob", "printed_side"}
            or row["file"] != f"n{row['n']}.txt"
            or leaves[row["file"]]["sha"] != row["blob"]
            or type(row["printed_side"]) is not str
            for row in outside
        )
    ):
        raise ReportError("outside-horizon identity roster differs")
    return leaves


def check_files(destination: Path) -> None:
    expected = {
        "README.md",
        "acquisition/sources.json",
        *(f"facts/n-{n:03d}.yaml" for n in NUMBERS),
    }
    files = set()
    for path in destination.rglob("*"):
        if path.is_symlink():
            raise ReportError("derived packet files cannot be symlinks")
        if path.is_file():
            files.add(path.relative_to(destination).as_posix())
    if files - {"receipts/exact-certification.json.xz"} != expected:
        raise ReportError("unexpected or missing derived packet file")


def read_facts(destination: Path | None = None) -> dict[int, legacy.Certificate]:
    """Admit the derived packet: every certificate rebuilt to its pinned blob."""
    destination = PACKET if destination is None else destination
    ensure_private(destination)
    check_files(destination)
    source = read_record(destination / "acquisition/sources.json")
    leaves = check_source(source)
    cases = source["cases"]
    if type(cases) is not list or [row.get("n") for row in cases if type(row) is dict] != list(
        NUMBERS
    ):
        raise ReportError("complete derived count roster differs")
    certificates = {}
    for n, row in zip(NUMBERS, cases, strict=True):
        if (
            set(row) != CASE_FIELDS
            or row["file"] != certificate_path(n)
            or row["derived_fact"] != f"facts/n-{n:03d}.yaml"
            or row["comment_side"] != COMMENT_SIDES[n]
        ):
            raise ReportError(f"n={n}: derived source descriptor differs")
        path = destination / row["derived_fact"]
        ensure_private(path)
        with path.open("rb") as stream:
            raw = stream.read(MAX_SOURCE_BYTES + 1)
        if len(raw) > MAX_SOURCE_BYTES:
            raise ReportError(f"n={n}: derived fact exceeds its byte ceiling")
        try:
            document = load_yaml(raw.decode("utf-8"))
            if (
                not isinstance(document, dict)
                or document.get("softschema")
                != witness_envelope({}, schema=SCHEMA)["softschema"]
            ):
                raise ReportError(f"n={n}: derived fact schema envelope differs")
            witness = validate_witness_document(
                document, path=path, fallback_schema=ROOT / "witnesses/witness.schema.yaml"
            )
        except (UnicodeDecodeError, yaml.YAMLError, WitnessError) as error:
            raise ReportError(f"n={n}: derived fact is not a valid witness: {error}") from error
        certificate = certificate_from_fact(n, witness)
        text = render(certificate).encode()
        leaf = leaves[row["file"]]
        if (
            extended.git_identity("blob", text) != leaf["sha"]
            or row["source_blob"] != leaf["sha"]
            or len(text) != leaf["size"]
            or row["size"] != leaf["size"]
            or hashlib.sha256(text).hexdigest() != row["sha256"]
        ):
            raise ReportError(f"n={n}: derived facts do not rebuild the pinned certificate")
        if document != witness_envelope(fact(certificate), schema=SCHEMA):
            raise ReportError(f"n={n}: derived witness metadata differs")
        pose = row["decimal_pose"]
        if (
            type(pose) is not dict
            or set(pose) != {"file", "blob", "printed_side"}
            or pose["file"] != f"n{n}.txt"
            or leaves[pose["file"]]["sha"] != pose["blob"]
            or type(pose["printed_side"]) is not str
        ):
            raise ReportError(f"n={n}: decimal pose identity differs")
        if row["side"] != legacy.literal(certificate.side):
            raise ReportError(f"n={n}: recorded exact side differs")
        check_prior(n, certificate.side, row["prior"])
        certificates[n] = certificate
    return certificates


def validate_certification(value: Any, facts: dict[int, legacy.Certificate]) -> dict[int, Any]:
    if (
        type(value) is not dict
        or set(value) != {"format", "routes", "cases"}
        or value["format"] != RECEIPT_FORMAT
        or value["routes"] != list(ROUTES)
        or type(value["cases"]) is not list
        or len(value["cases"]) != len(NUMBERS) * len(JOBS)
        or list(facts) != list(NUMBERS)
    ):
        raise ReportError("incomplete fifteen-job exact receipt envelope")
    positives = {}
    for (n, control), row in zip(
        ((n, control) for n in NUMBERS for control in JOBS), value["cases"], strict=True
    ):
        kernel.validate_job(
            row,
            facts[n],
            control,
            witness_prefix=WITNESS_PREFIX,
            claim_limitations=CLAIM_LIMITATIONS,
        )
        if control == "positive":
            positives[n] = row
    return positives


def _stable(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value for key, value in row.items() if key not in {"cpu_seconds", "wall_seconds"}
    }


def check_certification(
    numbers: list[int] | None = None, *, replay: bool = False
) -> dict[int, Any]:
    """Admit the retained receipt; with ``replay``, decide the selected counts again."""
    selected = list(NUMBERS) if numbers is None else numbers
    if not selected or len(set(selected)) != len(selected) or set(selected) - set(NUMBERS):
        raise ReportError("empty, repeated or unknown replay selection")
    facts = read_facts()
    ensure_private(receipt_path())
    record = kernel.read_xz(receipt_path())
    positives = validate_certification(record, facts)
    if replay:
        for (n, control), row in zip(
            ((n, control) for n in NUMBERS for control in JOBS), record["cases"], strict=True
        ):
            if n not in selected:
                continue
            fresh = kernel.run_case(
                facts[n],
                control,
                witness_prefix=WITNESS_PREFIX,
                claim_limitations=CLAIM_LIMITATIONS,
            )
            if _stable(fresh) != _stable(row):
                raise ReportError(f"n={n} {control}: fresh replay differs from the receipt")
    return positives


def run_child(job: tuple[int, str], directory: Path, timeout: int) -> dict[str, Any]:
    n, control = job
    if type(n) is not int or n not in NUMBERS or control not in JOBS:
        raise ReportError("job outside the complete certificate/control roster")
    if type(timeout) is not int or not 1 <= timeout <= JOB_TIMEOUT:
        raise ReportError("invalid bounded worker/deadline selection")
    path = directory / f"n{n}-{control}.json"
    if path.exists():
        raise ReportError("refusing to overwrite a deciding job")
    command = [
        sys.executable,
        "-m",
        "devtools.couzo_followup_reports",
        "decide-job",
        "--n",
        str(n),
        "--control",
        control,
        "--output",
        str(path),
    ]
    try:
        completed = subprocess.run(command, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as error:
        path.with_suffix(".stdout.log").write_bytes(error.stdout or b"")
        path.with_suffix(".stderr.log").write_bytes(error.stderr or b"")
        raise ReportError(f"full native job {n}/{control} exceeded {timeout}s") from error
    path.with_suffix(".stdout.log").write_bytes(completed.stdout)
    path.with_suffix(".stderr.log").write_bytes(completed.stderr)
    if completed.returncode:
        raise ReportError(f"full native job {n}/{control} exited {completed.returncode}")
    with path.open("rb") as stream:
        raw = stream.read(kernel.MAX_BYTES + 1)
    if len(raw) > kernel.MAX_BYTES:
        raise ReportError("native job exceeds existing receipt ceiling")
    try:
        value = json.loads(raw, object_pairs_hook=extended.unique_object)
    except ValueError as error:
        raise ReportError(f"native job {n}/{control} is not strict JSON") from error
    if type(value) is not dict:
        raise ReportError("complete native job object required")
    return value


def certify(directory: Path, *, workers: int = 2, timeout: int = JOB_TIMEOUT) -> None:
    if (
        type(workers) is not int
        or not 1 <= workers <= 2
        or type(timeout) is not int
        or not 1 <= timeout <= JOB_TIMEOUT
    ):
        raise ReportError("invalid bounded worker/deadline selection")
    ensure_private(receipt_path())
    facts = read_facts()
    if directory.exists():
        raise ReportError("native job directory must be a fresh attempt")
    directory.mkdir(parents=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        cases = list(
            pool.map(
                lambda job: run_child(job, directory, timeout),
                ((n, control) for n in NUMBERS for control in JOBS),
            )
        )
    value = {"format": RECEIPT_FORMAT, "routes": list(ROUTES), "cases": cases}
    validate_certification(value, facts)
    ensure_private(receipt_path())
    kernel.save_xz(receipt_path(), value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    acquisition = sub.add_parser("acquire")
    acquisition.add_argument("--git-dir", type=Path, required=True)
    sub.add_parser("check-packet")
    campaign = sub.add_parser("certify")
    campaign.add_argument("--jobs-dir", type=Path, required=True)
    campaign.add_argument("--workers", type=int, default=2)
    campaign.add_argument("--timeout", type=int, default=JOB_TIMEOUT)
    check = sub.add_parser("check")
    check.add_argument("--n", type=int, nargs="+")
    check.add_argument("--replay", action="store_true")
    job = sub.add_parser("decide-job")
    job.add_argument("--n", type=int, choices=NUMBERS, required=True)
    job.add_argument("--control", choices=JOBS, required=True)
    job.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.action == "acquire":
        acquire(args.git_dir)
        print("five derived certificate facts and pinned custody written; no raw bytes")
    elif args.action == "check-packet":
        facts = read_facts()
        print(f"{len(facts)} certificates rebuilt to their pinned blobs; no geometry credit")
    elif args.action == "certify":
        certify(args.jobs_dir, workers=args.workers, timeout=args.timeout)
    elif args.action == "check":
        positives = check_certification(args.n, replay=args.replay)
        print(f"all {len(positives)} complete certificates and fifteen full jobs admitted")
    else:
        certificate = read_facts()[args.n]
        row = kernel.run_case(
            certificate,
            args.control,
            witness_prefix=WITNESS_PREFIX,
            claim_limitations=CLAIM_LIMITATIONS,
        )
        kernel.validate_job(
            row,
            certificate,
            args.control,
            witness_prefix=WITNESS_PREFIX,
            claim_limitations=CLAIM_LIMITATIONS,
        )
        if args.output.exists():
            raise ReportError("refusing to overwrite an actual deciding job")
        with atomic_output_file(args.output) as temporary:
            temporary.write_text(json.dumps(row, separators=(",", ":"), allow_nan=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
