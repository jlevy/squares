"""Audit wand125's mixed certificates on a declared net, and replay and compare them.

wand125/square-packing-bounds declares its own half-angle net in thirteen certificates,
the first three posted on jlevy/squares#366, each a rectangle density whose candidate
carries a ``proof_net`` (`CERTIFICATES`):

- at ``43050ed``, ``mixed_n18_L470`` for ``s(18) >= 47/10``, core side ``999/1000`` and
  ``{"step": "1/1001", "last": 415}``, 416 nodes;
- at ``65e408c``, ``mixed_n18_L4704`` for ``s(18) >= 588/125``, core side ``1999/2000``
  and ``{"step": "1/2006", "last": 831}``, 832 nodes;
- at ``65e408c``, ``mixed_n19_L48229`` for ``s(19) >= 48229/10000``, on
  ``mixed_n18_L470``'s net;
- at ``2fad66e``, ten more: ``mixed_n29_L581`` for ``s(29) >= 581/100``, a proof bundle
  like those above on ``mixed_n18_L470``'s net, and nine *check2* certificates, at
  ``n = 18, 19, 20, 26, 27, 28, 30, 39, 41``, on that net, on ``mixed_n18_L4704``'s, or
  on a finer one, core ``4999/5000`` and ``{"step": "1/5002", "last": 2072}``, 2073
  nodes.

A check2 directory ships no C++ records. Its candidate is in the same format, and its
bundle holds the source's run of its own adaptation of this repository's sqverify_fast
(``sqverify-proof-net``, build ``ab6e33e1...``) at every node, with the run's log, a
control and the adapted crate's source as a tarball, which nothing here opens.
``audit`` and ``bundle`` take that form for a check2 certificate (`audit_check2`,
`bundle_check2`), and ``cpp-sample`` runs the source's earlier C++ checker, which shares
no code with that crate, at chosen nodes of one.

`devtools.audit_wand125_point_and_mixed` takes the standard net (step ``83/40000``, 201
nodes) and core ``9977/10000`` as fixed, so it cannot audit these. This tool is the
first-party part of their import. It was written from the certificate format, the
bundles' data files and lemma N0 of ``sqverify_fast/SOUNDNESS.md``; ``audit``, ``bundle``
and ``compare`` import no source code and open no file of a ``code/`` folder, which they
compare only by digest. ``sample``, ``replay`` and ``control`` run the source's own
checker, from a bundle that ``bundle`` has first bound to the packet. Every command
takes ``--certificate``, ``n18-L470`` unless given.

- ``audit`` recomputes, from the packet's retained files alone, every premise that is
  plain arithmetic: the count, side and core the manifest states; nonnegative masses on
  nondegenerate rectangles inside the container, totalling exactly ``n - 1/100000``;
  lemma N0's five premises on the declared net; the net blocks of ``manifest.json`` and
  ``certificate.json`` equal to the facts recomputed here; one candidate digest
  throughout; and a replay record at threshold one at every node of the declared net.
  It decides no coverage.
- ``bundle`` checks an unpacked proof bundle against the packet:
  - every file its ``files-sha256.json`` lists has that digest, and nothing is
    unlisted;
  - the candidate, certificate and manifest are the retained files, every ``code/``
    file is the retained ``mixed_n50_L740`` copy or, where the certificate's directory
    retains its own (``mixed_n18_L4704``'s driver, whose one change raises the cap on
    its workers from 3 to 16), that copy, and ``proof/verify.cpp`` is the checker
    ``89b674a6...``;
  - at every oblique node, the shipped record's net index, tangent, bin floor and
    per-bin centre domain are lemma N0's exactly, and its input's first lines enclose
    the side, core, domain half-width, cosine and sine exactly, with threshold one; its
    rectangle lines enclose the eight images of every row of the candidate, with their
    densities, and list no point mass;
  - the axis record is at threshold one, with no unresolved cell.

  This binds the source's own runs to the declared net. It decides no coverage either.
- ``compare`` reads a copy of the bundle after the bundle's own driver has replayed it,
  as its README says, with the run's own record. It requires the run to have happened
  (exit zero, the driver's progress at every node, its binary in the copy, every record
  written after the start), and every regenerated record, and the rewritten certificate
  as a mapping, to equal the shipped and retained ones (finding DN-1 of the 5 October
  review, which found the first version matching a copy where nothing ran).
- ``sample`` unpacks the pinned tarball afresh, binds it, and replays a chosen set of
  net nodes with the source's per-node functions and its unchanged C++ checker, after
  the full driver's preconditions (`audit_wand125_point_and_mixed.n50_replay`): the CPU
  each node took against the bundle's own record of it, and the price of the rest. It
  decides only the nodes it ran.
- ``replay`` unpacks the pinned tarball twice, binds the first copy (``bundle``), runs
  the bundle's own driver in the second as its README says, recording the run's start,
  exit, end and the CPU of the driver and everything it waited for, and then compares
  the two (``compare``).
- ``control`` runs the source's checker on the original and two mutants at one oblique
  node, every mass scaled by 99/100 and every mass scaled so that an exact witness
  centre captures ``1 - 10^-6``, and runs the source's own net check on three corrupted
  net declarations. The original must return its shipped record and every other
  variant must be refused.
- ``processes`` snapshots a running ``replay``'s driver and workers from ``/proc``:
  their command lines and Python environment, to show the source's assertions were on
  for a run whose record predates ``replay``'s own record of it.
- ``control-sqverify-fast`` runs ``sqverify-fast`` on the same original and mass
  mutants, rebuilt from the retained candidate by the control receipt's factors and held
  to its exact captures, at the same node: the original must verify and each mutant must
  be refused.
- ``cpp-sample`` binds a check2 bundle from its pinned tarball, then runs the source's
  C++ checker ``89b674a6...``, built and driven by the source's own functions from the
  retained ``mixed_n50_L740`` code, at chosen oblique nodes at threshold one, each
  node's record held to lemma N0 and its input to the expanded candidate. It decides only
  the nodes it ran.
- ``compare-census`` sets this repository's sqverify-fast census row of a check2
  certificate beside the source's run of its copy of the crate, direction by direction:
  both must verify every node, and it counts where their node counts and bounds agree.

From ``packing/``::

    .venv/bin/python3 -m devtools.audit_wand125_declared_net audit --check
    .venv/bin/python3 -m devtools.audit_wand125_declared_net bundle --bundle DIR
    .venv/bin/python3 -m devtools.audit_wand125_declared_net compare \\
        --shipped DIR --fresh RUN_DIR --meta RUN_META
    .venv/bin/python3 -m devtools.audit_wand125_declared_net sample \\
        --certificate n19-L48229 --tarball TARBALL --work W --nodes 1,37,415 --workers 2
    .venv/bin/python3 -m devtools.audit_wand125_declared_net replay \\
        --certificate n19-L48229 --tarball TARBALL --work W --workers 2
    .venv/bin/python3 -m devtools.audit_wand125_declared_net control \\
        --certificate n19-L48229 --tarball TARBALL --work W
    .venv/bin/python3 -m devtools.audit_wand125_declared_net bundle \\
        --certificate n20-L4905 --tarball TARBALL --work W
    .venv/bin/python3 -m devtools.audit_wand125_declared_net cpp-sample \\
        --certificate n20-L4905 --tarball TARBALL --work W --nodes 1,679 --workers 1
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib
import json
import os
import platform
import resource
import shutil
import subprocess
import sys
import tarfile
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any

from devtools.retained_data import read_retained_bytes
from sqpack import retained_json

PROJECT = Path(__file__).resolve().parents[1]
WEB = PROJECT / "resources/web"
N50 = WEB / "wand125-point-and-mixed-2026-09-28/square-packing-bounds/certificates"
N50_DIRECTORY = N50 / "mixed_n50_L740"
#: The source's checker, ``code/mixed_rotated_verify.cpp``, by SHA-256: every mixed
#: certificate of the source so far runs this one.
CHECKER_SHA256 = "89b674a6feabe24d91c29431de1624907c4bff83280ceb481475455686693652"
#: The budget gap every mixed certificate leaves below ``n``.
GAP = Fraction(1, 100000)


@dataclass(frozen=True, slots=True)
class Certificate:
    """One certificate directory of the source on a declared net, as the source states it.

    ``n`` and ``side`` are the claim the directory's README states. ``own_code`` names
    the ``code/`` files that are not byte-identical to the retained ``mixed_n50_L740``
    copies and that the packet retains in the certificate's own directory instead. The
    tarball's digest and size are read from the packet's acquisition record, so the pin
    has one home.
    """

    key: str
    packet: Path
    name: str
    n: int
    side: Fraction
    tarball: str
    own_code: frozenset[str] = frozenset()
    #: ``proof``: the source's C++ records at every node, in ``certificate.json``, with a
    #: complete proof bundle; ``check2``: the source's run of its adaptation of this
    #: repository's sqverify_fast, in ``check2/receipt.json``, with no C++ records.
    kind: str = "proof"

    @property
    def directory(self) -> Path:
        return self.packet / "square-packing-bounds/certificates" / self.name

    @property
    def receipts(self) -> Path:
        return self.packet / "receipts" / self.key

    @property
    def check2(self) -> bool:
        return self.kind == "check2"

    @property
    def bundle_name(self) -> str:
        """The one top-level directory of the tarball."""
        return self.tarball.removesuffix(".tar.gz")

    def code_reference(self, name: str) -> Path:
        """The retained file a bundle's ``code/<name>`` must equal."""
        return (self.directory if name in self.own_code else N50_DIRECTORY) / "code" / name

    def tarball_pin(self) -> tuple[str, int]:
        """The tarball's SHA-256 and size, from the packet's acquisition record."""
        record = json.loads((self.packet / "acquisition/sources.json").read_text())
        path = f"certificates/{self.name}/{self.tarball}"
        for source in record["sources"]:
            for item in source["pinned_only"]:
                if item["path"] == path:
                    return item["sha256"], int(item["bytes"])
        raise AuditError(f"the packet pins no {path}")


FINER_NET_05 = WEB / "wand125-mixed-bounds-finer-net-2026-10-05"
FINER_NET_06 = WEB / "wand125-mixed-bounds-finer-net-2026-10-06"
CHECK2_06 = WEB / "wand125-mixed-bounds-check2-2026-10-06"
#: Every certificate of the source on a declared net, by the key a command takes.
CERTIFICATES = {
    certificate.key: certificate
    for certificate in (
        Certificate(
            "n18-L470",
            FINER_NET_05,
            "mixed_n18_L470",
            18,
            Fraction(47, 10),
            "n18-L4.7-proof-bundle.tar.gz",
        ),
        Certificate(
            "n18-L4704",
            FINER_NET_06,
            "mixed_n18_L4704",
            18,
            Fraction(588, 125),
            "n18-L4.704-proof-bundle.tar.gz",
            frozenset({"verify_mixed_full_proof.py"}),
        ),
        Certificate(
            "n19-L48229",
            FINER_NET_06,
            "mixed_n19_L48229",
            19,
            Fraction(48229, 10000),
            "n19-L4.8229-proof-bundle.tar.gz",
        ),
        Certificate(
            "n18-L4705",
            CHECK2_06,
            "mixed_n18_L4705",
            18,
            Fraction(941, 200),
            "n18-L4.705-check2-bundle.tar.gz",
            kind="check2",
        ),
        Certificate(
            "n19-L4825",
            CHECK2_06,
            "mixed_n19_L4825",
            19,
            Fraction(193, 40),
            "n19-L4.825-check2-bundle.tar.gz",
            kind="check2",
        ),
        Certificate(
            "n20-L4905",
            CHECK2_06,
            "mixed_n20_L4905",
            20,
            Fraction(981, 200),
            "n20-L4.905-check2-bundle.tar.gz",
            kind="check2",
        ),
        Certificate(
            "n26-L5545",
            CHECK2_06,
            "mixed_n26_L5545",
            26,
            Fraction(1109, 200),
            "n26-L5.545-check2-bundle.tar.gz",
            kind="check2",
        ),
        Certificate(
            "n27-L56435",
            CHECK2_06,
            "mixed_n27_L56435",
            27,
            Fraction(11287, 2000),
            "n27-L5.6435-check2-bundle.tar.gz",
            kind="check2",
        ),
        Certificate(
            "n28-L5735",
            CHECK2_06,
            "mixed_n28_L5735",
            28,
            Fraction(1147, 200),
            "n28-L5.735-check2-bundle.tar.gz",
            kind="check2",
        ),
        Certificate(
            "n29-L581",
            CHECK2_06,
            "mixed_n29_L581",
            29,
            Fraction(581, 100),
            "n29-L5.81-proof-bundle.tar.gz",
        ),
        Certificate(
            "n30-L58835",
            CHECK2_06,
            "mixed_n30_L58835",
            30,
            Fraction(11767, 2000),
            "n30-L5.8835-check2-bundle.tar.gz",
            kind="check2",
        ),
        Certificate(
            "n39-L665",
            CHECK2_06,
            "mixed_n39_L665",
            39,
            Fraction(133, 20),
            "n39-L6.65-check2-bundle.tar.gz",
            kind="check2",
        ),
        Certificate(
            "n41-L6775",
            CHECK2_06,
            "mixed_n41_L6775",
            41,
            Fraction(271, 40),
            "n41-L6.775-check2-bundle.tar.gz",
            kind="check2",
        ),
    )
}
#: The certificate a command reads when none is given: the first, T-096's.
DEFAULT = "n18-L470"
PACKET = CERTIFICATES[DEFAULT].packet
DIRECTORY = CERTIFICATES[DEFAULT].directory
RECEIPTS = CERTIFICATES[DEFAULT].receipts
N = CERTIFICATES[DEFAULT].n
SIDE = CERTIFICATES[DEFAULT].side


class AuditError(Exception):
    """A premise or a binding that does not hold."""


def require(condition: bool, message: str, /) -> None:  # noqa: FBT001
    """Raise `AuditError` with ``message`` unless ``condition`` holds."""
    if not condition:
        raise AuditError(message)


def load_json(data: bytes) -> Any:
    """JSON with every decimal kept as its text, so that it reads as an exact rational."""
    return json.loads(data, parse_float=str)


def rho(a: Fraction) -> Fraction:
    """Half the width ``(cos phi + sin phi) / 2`` of a unit square at half-angle tangent a."""
    return (1 + 2 * a - a * a) / (2 * (1 + a * a))


def net_facts(core: Fraction, step: Fraction, count: int) -> dict[str, Fraction]:
    """The containment facts of a declared net (lemma N0), exactly."""
    last = step * (count - 1)
    shrink = core * (1 + step)
    return {
        "step": step,
        "count": Fraction(count),
        "endpoint": last,
        "endpoint_check": last * last + 2 * last - 1,
        "rotated_side_upper": shrink,
        "side_margin": 1 - shrink,
        "per_edge_margin": (1 - shrink) / 2,
        "tangent_form": core * (1 + step / (1 - step * step / 4)),
    }


def premises(facts: dict[str, Fraction], count: int) -> dict[str, bool]:
    """Lemma N0's premises (a) to (e) on the declared net."""
    return {
        "a_positive_step_and_count": facts["step"] > 0 and 2 <= count <= 1 << 16,
        "b_core_fits": facts["rotated_side_upper"] < 1,
        "c_reaches_past_pi_over_4": facts["endpoint_check"] > 0,
        "d_last_tangent_at_most_half": facts["endpoint"] <= Fraction(1, 2),
        "e_tangent_form": facts["tangent_form"] < 1,
    }


def read_directory(directory: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """The retained candidate, certificate and manifest."""
    return (
        load_json(read_retained_bytes(directory / "candidate.json")),
        load_json(read_retained_bytes(directory / "certificate.json")),
        load_json(read_retained_bytes(directory / "manifest.json")),
    )


def measure(candidate: dict[str, Any], stated: Certificate) -> tuple[Fraction, int]:
    """The candidate's count, side and rows: its total mass and its positive rows.

    The count and side are the claim's; there are no point masses and no scaling; every
    row is a nonnegative mass on a nondegenerate rectangle inside ``[0, L]^2``; and the
    masses total exactly ``n - 1/100000``, as ``total_mass`` states.
    """
    n = candidate["n"]
    side = Fraction(candidate["L"])
    require((n, side) == (stated.n, stated.side), f"the candidate is n = {n}, L = {side}")
    require(candidate["points"] == [], "the candidate has point masses")
    require(candidate.get("scaling_factor", "1") == "1", "the candidate is scaled")
    total = Fraction(0)
    positive = 0
    for index, row in enumerate(candidate["rectangles"]):
        x1, y1, x2, y2 = (Fraction(value) for value in row["rectangle"])
        mass = Fraction(row["mass"])
        require(mass >= 0, f"row {index} has a negative mass")
        if mass > 0:
            positive += 1
            require(
                0 <= x1 < x2 <= side and 0 <= y1 < y2 <= side,
                f"row {index} is degenerate or outside [0, L]^2",
            )
        total += mass
    require(total == Fraction(candidate["total_mass"]), "total_mass is not the sum")
    require(total == n - GAP, f"the mass {total} is not n - 1/100000")
    return total, positive


def declared_net(
    candidate: dict[str, Any],
) -> tuple[Fraction, int, dict[str, Fraction], dict[str, bool]]:
    """The candidate's declared net: its step, its node count, its facts and lemma N0's
    premises on it, every premise required to hold."""
    core = Fraction(candidate["B"])
    net = candidate["proof_net"]
    require(set(net) == {"step", "last"}, f"proof_net has fields {sorted(net)}")
    require(isinstance(net["last"], int), "proof_net.last is not an integer")
    step, count = Fraction(net["step"]), int(net["last"]) + 1
    facts = net_facts(core, step, count)
    checks = premises(facts, count)
    require(all(checks.values()), f"a premise of lemma N0 fails: {checks}")
    return step, count, facts, checks


#: The net facts the source states in a manifest, certificate or bundle.json net block.
STATED_NET = (
    "step",
    "count",
    "endpoint",
    "endpoint_check",
    "rotated_side_upper",
    "side_margin",
    "per_edge_margin",
)


def semantic_digest(candidate: dict[str, Any]) -> str:
    """The source's candidate digest: SHA-256 of the compact, key-sorted JSON of the
    fields that define the certificate, ``proof_net`` among them where declared."""
    keys = ["n", "L", "B", "rectangles", "points", "total_mass"]
    keys += ["proof_net"] if "proof_net" in candidate else []
    text = json.dumps(
        {key: candidate[key] for key in keys}, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(text.encode()).hexdigest()


#: The eight check2 runs whose log names an input other than the published candidate.json
#: (finding FN-1 of the 6 October review of T-102 to T-111): the SHA-256 of the bytes each
#: read, as its own summary records it. Each read the published side, core, net, node
#: count and mass, and the source's pre-publication run of the same build read the
#: published bytes, but these bytes are not published. A check2 run that names any other
#: input, or a published one where this names an unpublished one, is refused.
UNPUBLISHED_RUN_INPUTS = {
    "n19-L4825": "9132b84eceb4c9913bcf3065be58828665c5b12469c585f1700c1408c7f43cb7",
    "n20-L4905": "c446837b499de48ede56a5b3a660abf81615b6332a36314012bca642306cd07f",
    "n26-L5545": "6ea9cce160259694f48b9bb5f1ba3222332b7d8051284278f11a4413c6933c95",
    "n27-L56435": "e6561fe4d114945a99f81aee05ef3028fb95ee60cf139990e8cd1deffc312dbf",
    "n28-L5735": "c0218bf04ce2fe50a714cde1a4fe124ec1c90aebc50e5b5d65259cd094522bfd",
    "n30-L58835": "6b3d9075e5faa99015409f531c8d3cdc3af69356d9a933e987da5f505ec9d766",
    "n39-L665": "012755340a2a7dd214891d3e123ddc29e8dfd6f03c07dccedaf563c02da931ca",
    "n41-L6775": "cbc04bd94c0f7041178419115990eb193ba52a79bc67efa2a2b7d00f8d9588b2",
}
#: The factor every check2 control scales each mass by: 0.985 in the control's own words.
CHECK2_CONTROL_FACTOR = Fraction(197, 200)
#: The source's second run of its check2 check before publication, on another host; not in
#: the bundle, so not listed.
PREPUBLICATION = "verification/prepublication-receipt.json"
#: The schema ``mixed_n30_L58925``'s pre-publication receipt of 10 October names: its build
#: under ``verifier``, and its control as tries. The earlier receipts name none.
PREPUBLICATION_V1 = "fine-net-check2-receipt/v1"
#: The one file a check2 directory's ``files-sha256.json`` lists that is not the
#: directory's own: the README inside the tarball, shorter than the directory's, which
#: `bundle` holds to its listed digest.
BUNDLE_README = "README.md"


def audit_check2(
    directory: Path, stated: Certificate, pins: dict[str, str] | None = None
) -> dict[str, Any]:
    """Every exact premise of a check2 certificate, from the retained files alone.

    A check2 directory carries no C++ records: ``bundle.json`` states the claim and the
    net's facts, ``check2/receipt.json`` the source's run of its adaptation of this
    repository's sqverify_fast at every node, and ``files-sha256.json`` every file's
    digest. Besides the measure and lemma N0's premises, the last net bin must hold an
    orientation of ``[0, pi/4]``; the net block must be the facts recomputed here; one
    candidate digest, recomputed here by the source's rule, must be stated throughout; the
    receipt must report every node of this net verified at threshold one, by a run that
    read this side, core, step, count and mass, from the published candidate or from the
    unpublished input `UNPUBLISHED_RUN_INPUTS` names for it (finding FN-1 of the 6
    October review); the control must be this candidate with every mass scaled by
    197/200, refused; the source's pre-publication run (`PREPUBLICATION`) by the same
    build must verify every node on the published bytes, in either shape
    `prepublication_run` reads, with its control refused; and every file
    ``files-sha256.json`` lists, the tarball's own README apart (`BUNDLE_README`), must be
    the directory's, retained or pinned. It decides no coverage.

    ``pins`` are the pinned-only digests by upstream path, the packet's acquisition
    record's unless given; `devtools.fine_net_followup` passes the raw digests of the
    ``.gz`` files of a release asset unpacked outside any packet.
    """
    raw = read_retained_bytes(directory / "candidate.json")
    candidate = load_json(raw)
    total, positive = measure(candidate, stated)
    step, count, facts, checks = declared_net(candidate)
    core, side = Fraction(candidate["B"]), Fraction(candidate["L"])
    floor = (count - Fraction(3, 2)) * step
    require(not reaches_past_pi_over_8(floor), "the last net bin holds no orientation")
    digest = semantic_digest(candidate)
    require(
        candidate.get("scaling_source_digest", digest) == digest,
        "the candidate's own digest is not its semantic digest",
    )
    stated_bundle = load_json(read_retained_bytes(directory / "bundle.json"))
    require(stated_bundle["schema"] == "fine-net-check2-v1", "bundle.json schema")
    require(
        (stated_bundle["n"], Fraction(stated_bundle["L"]), Fraction(stated_bundle["B"]))
        == (stated.n, side, core)
        and stated_bundle["proof_net"] == candidate["proof_net"]
        and stated_bundle["angle_count"] == count
        and Fraction(stated_bundle["total_mass"]) == total
        and stated_bundle["candidate_digest"] == digest
        and stated_bundle["candidate_sha256"] == sha256(raw),
        "bundle.json states another claim, net, mass or candidate",
    )
    for field in STATED_NET:
        value = stated_bundle["net"][field]
        require(Fraction(str(value)) == facts[field], f"bundle.json net {field} is {value}")
    receipt_bytes = read_retained_bytes(directory / "check2/receipt.json")
    require(stated_bundle["receipt_sha256"] == sha256(receipt_bytes), "receipt digest")
    receipt = load_json(receipt_bytes)
    summary = receipt["verifier_summary"]
    premises_run = summary["premises"]
    require(
        receipt["status"] == "VERIFIED"
        and receipt["directions"] == count
        and receipt["failed"] == 0
        and receipt["candidate_digest"] == digest
        and receipt["file_sha256"] == sha256(raw)
        and summary["status"] == "VERIFIED"
        and summary["directions"] == count
        and summary["refused_directions"] == []
        and summary["threshold"] == "1"
        and summary["fault_injected_at_box"] is None,
        "the source's receipt does not verify every node of this candidate",
    )
    require(
        Fraction(premises_run["L"]) == side
        and Fraction(premises_run["B"]) == core
        and Fraction(premises_run["D"]) == step
        and premises_run["angle_count"] == count
        and Fraction(premises_run["mass_exact"]) == total
        and premises_run["format"] == "M"
        and premises_run["centre_domain"] == "per-bin",
        "the source's run read another side, core, net or mass",
    )
    run_input = str(premises_run["input_sha256"])
    published = run_input == sha256(raw)
    require(
        published != (stated.key in UNPUBLISHED_RUN_INPUTS)
        and (published or UNPUBLISHED_RUN_INPUTS[stated.key] == run_input),
        f"the source's run read {run_input[:8]}..., neither the published candidate nor the"
        " unpublished input UNPUBLISHED_RUN_INPUTS names for it",
    )
    control = load_json(read_retained_bytes(directory / "check2/control.json"))
    require(control_refused(control), "the source's control was not refused")
    require(
        control_factor(control) == CHECK2_CONTROL_FACTOR
        and control.get("candidate_file_sha256", sha256(raw)) == sha256(raw),
        "the source's control is not this candidate with every mass scaled by 197/200",
    )
    second = load_json(read_retained_bytes(directory / PREPUBLICATION))
    second_build, second_refused = prepublication_run(second)
    require(
        second["status"] == "VERIFIED"
        and second["verdict"] == "PASS"
        and second["directions_verified"] == second["directions_expected"] == count
        and second["candidate_digest"] == digest
        and second["file_sha256"] == second["input_sha256"] == sha256(raw)
        and second_build["source_sha256"] == summary["build"]["source_sha256"],
        "the source's pre-publication run does not verify every node of this candidate",
    )
    listed = load_json(read_retained_bytes(directory / "files-sha256.json"))
    pins = pinned_digests(stated) if pins is None else pins
    for name, value in listed.items():
        if name == BUNDLE_README:
            continue
        path = directory / name
        found = (
            sha256(read_retained_bytes(path))
            if path.exists() or path.with_name(path.name + ".gz").exists()
            else pins.get(f"certificates/{stated.name}/{name}")
        )
        require(found == value, f"{name} is not the file the directory lists")
    return {
        "kind": "wand125-declared-net-audit/v1",
        "format": "check2",
        "certificate": stated.name,
        "claim": f"s({stated.n}) >= {side.numerator}/{side.denominator}",
        "rectangles": len(candidate["rectangles"]),
        "positive_rectangles": positive,
        "mass": str(total),
        "core": str(core),
        "net": {name: str(value) for name, value in facts.items()},
        "premises": checks | {"f_last_bin_holds_an_orientation": True},
        "candidate_digest": digest,
        "listed_files": len(listed),
        "listed_files_in_directory": len(listed) - (BUNDLE_README in listed),
        "source_check": {
            "status": receipt["status"],
            "directions": receipt["directions"],
            "nodes": summary["nodes"],
            "direction_cpu_seconds": summary["direction_cpu_seconds"],
            "threads": summary["threads"],
            "source_sha256": summary["build"]["source_sha256"],
            "verifier": receipt["verifier"],
            "control": control["kind"],
            "control_status": "REFUSED",
        },
        "run_input": {"sha256": run_input, "published_candidate": published},
        "prepublication_check": {
            "status": second["status"],
            "input_is_published_candidate": True,
            "directions": second["directions_verified"],
            "seconds": second["seconds"],
            "target": second_build["target"],
            "control_refused_directions": second_refused,
        },
        "status": "EXACT_PREMISES_HOLD",
        "scope": (
            "Exact premises only, from the retained files: the measure, lemma N0's premises"
            " on the declared net and its last bin, the net block bundle.json states, one"
            " candidate digest, the source's receipt of its own run at every node and the"
            " input that run read (run_input), its control, its pre-publication run on the"
            " published bytes, and every listed file's digest. No coverage is decided here."
        ),
    }


def control_refused(control: dict[str, Any]) -> bool:
    """Whether the source's control record says its checker refused every try.

    Two forms occur: a status of its own (``REFUSED``), or, in ``mixed_n18_L4705``, a
    list of tries, each with its own status, under ``refused``.
    """
    if "tries" in control:
        return control["refused"] is True and all(
            each["status"] == "REFUSED" and each["exit"] != 0 for each in control["tries"]
        )
    return control["status"] == "REFUSED" and control["exit"] != 0


def control_factor(control: dict[str, Any]) -> Fraction | None:
    """The factor a source control record says it scaled every mass by.

    ``mixed_n18_L4705``'s record states it per try (``197/200``); the others state it in
    their kind, ``every mass x 0.985, 32 directions``.
    """
    if "tries" in control:
        factors = {Fraction(each["factor"]) for each in control["tries"]}
        return factors.pop() if len(factors) == 1 else None
    prefix = "every mass x "
    kind = str(control["kind"])
    if not kind.startswith(prefix):
        return None
    return Fraction(kind.removeprefix(prefix).split(",")[0])


def prepublication_run(second: dict[str, Any]) -> tuple[dict[str, Any], Any]:
    """The build a pre-publication receipt states and the directions its control refused,
    read by the receipt's shape.

    The earlier receipts name no schema: their build is under ``build`` and their control
    has a status of its own, which must be ``REFUSED``. `PREPUBLICATION_V1` puts the build
    under ``verifier`` and gives the control as one try, which must have refused at
    197/200 (`control_refused`, `control_factor`). A receipt of any other schema, or with
    no build under its shape's field, is refused.
    """
    schema = second.get("schema")
    control = second["control"]
    if schema is None:
        field = "build"
        require(
            control["status"] == "REFUSED",
            "the source's pre-publication control was not refused",
        )
        refused = control["refused_directions"]
    else:
        require(schema == PREPUBLICATION_V1, f"no reader for pre-publication schema {schema}")
        field = "verifier"
        tries = control.get("tries")
        require(
            isinstance(tries, list) and len(tries) == 1,
            "the source's pre-publication control is not one try",
        )
        require(
            control_refused(control) and control_factor(control) == CHECK2_CONTROL_FACTOR,
            "the source's pre-publication control was not refused at 197/200",
        )
        refused = tries[0]["refused"]
    build: dict[str, Any] | None = second.get(field)
    require(isinstance(build, dict), f"the pre-publication receipt states no build in {field}")
    assert build is not None
    return build, refused


def pinned_digests(stated: Certificate) -> dict[str, str]:
    """Every pinned-only file of the certificate's packet, by its upstream path."""
    record = json.loads((stated.packet / "acquisition/sources.json").read_text())
    return {
        item["path"]: item["sha256"]
        for source in record["sources"]
        for item in source["pinned_only"]
    }


def audit(directory: Path | None = None, *, key: str = DEFAULT) -> dict[str, Any]:
    """Every exact premise of the certificate, from the retained files alone."""
    stated = CERTIFICATES[key]
    if stated.check2:
        return audit_check2(directory or stated.directory, stated)
    candidate, certificate, manifest = read_directory(directory or stated.directory)
    n = candidate["n"]
    side, core = Fraction(candidate["L"]), Fraction(candidate["B"])
    total, positive = measure(candidate, stated)
    _step, count, facts, checks = declared_net(candidate)
    for name, block in (("manifest", manifest["net"]), ("certificate", certificate["net"])):
        for field in STATED_NET:
            require(
                Fraction(str(block[field])) == facts[field],
                f"{name} net {field} is {block[field]}",
            )
    digest = candidate["scaling_source_digest"]
    require(
        manifest["candidate_digest"] == certificate["candidate_digest"] == digest,
        "the candidate digest differs between files",
    )
    require(
        (manifest["n"], Fraction(manifest["L"]), Fraction(manifest["B"])) == (n, side, core),
        "the manifest states another count, side or core",
    )
    require(Fraction(manifest["budget"]) == total, "the manifest's budget is not the mass")
    require(manifest["source_sha256"] == CHECKER_SHA256, "the manifest names another checker")
    require(certificate["status"] == "ALL_ANGLES_VERIFIED_AND_REPLAYED", "not all verified")
    require(
        (certificate["n"], Fraction(certificate["L"]), Fraction(certificate["B"]))
        == (n, side, core)
        and Fraction(certificate["total_mass"]) == total
        and Fraction(certificate["budget_gap"]) == GAP
        and certificate["point_mass"] == "0"
        and certificate["angle_count"] == count,
        "the certificate states another measure or net",
    )
    results = certificate["results"]
    require(set(results) == {str(r) for r in range(count)}, "a net node has no record")
    axis = results["0"]
    require(
        axis["status"] == "AXIS_CERTIFICATE_REPLAYED"
        and axis["gamma"] == "1"
        and axis["digest"] == digest,
        "the axis record is not a replay at threshold one",
    )
    least: tuple[float, int] | None = None
    nodes = 0
    for r in range(1, count):
        record = results[str(r)]
        require(
            record["status"] == "ANGLE_RESULT_REPLAYED"
            and record["index"] == r
            and record["candidate_digest"] == digest,
            f"node {r} has no replay record of this candidate",
        )
        lower = float(record["lower"])
        require(lower >= 1, f"node {r} records a lower bound below one")
        nodes += int(record["nodes"])
        if least is None or lower < least[0]:
            least = (lower, r)
    assert least is not None
    return {
        "kind": "wand125-declared-net-audit/v1",
        "certificate": stated.name,
        "claim": f"s({n}) >= {side.numerator}/{side.denominator}",
        "rectangles": len(candidate["rectangles"]),
        "positive_rectangles": positive,
        "mass": str(total),
        "core": str(core),
        "net": {key: str(value) for key, value in facts.items()},
        "premises": checks,
        "candidate_digest": digest,
        "checker_sha256": CHECKER_SHA256,
        "oblique_records": count - 1,
        "oblique_nodes": nodes,
        "least_oblique_lower": {"lower": least[0], "index": least[1]},
        "axis": {"cells": axis["cells"], "integer_minimum": axis["integer_minimum"]},
        "status": "EXACT_PREMISES_HOLD",
        "scope": (
            "Exact premises only, from the retained files: the measure, lemma N0's premises"
            " on the declared net, the net blocks the manifest and certificate state, one"
            " candidate digest, and a replay record at threshold one at every node. No"
            " coverage is decided here."
        ),
    }


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def enclosure(line: str) -> tuple[Fraction, Fraction]:
    """An input line's two hexadecimal binary64 ends, as exact rationals."""
    low, high = line.split()
    return Fraction(float.fromhex(low)), Fraction(float.fromhex(high))


def orbit(side: Fraction, row: list[Fraction]) -> list[tuple[Fraction, ...]]:
    """The eight images of ``[x1, y1, x2, y2]`` under the container's symmetries."""
    x1, y1, x2, y2 = row
    return [
        (left, bottom, right, top)
        for a1, b1, a2, b2 in ((x1, y1, x2, y2), (y1, x1, y2, x2))
        for left, right in ((a1, a2), (side - a2, side - a1))
        for bottom, top in ((b1, b2), (side - b2, side - b1))
    ]


def rectangle_block(candidate: dict[str, Any], lines: list[str]) -> None:
    """An input's rectangle lines enclose the expanded candidate, row by row.

    After the header, an input lists eight lines per candidate row, each the enclosures
    of an image's ``x1, y1, x2, y2`` and density, then the count of point masses. Each
    row's eight lines must enclose its eight images, matched as a multiset, with
    density ``mass / 8 / area``; no point mass is listed.
    """
    side = Fraction(candidate["L"])
    rows = candidate["rectangles"]
    require(len(lines) == 8 * len(rows) + 1 and lines[-1].strip() == "0", "the point count")
    for index, row in enumerate(rows):
        corners = [Fraction(value) for value in row["rectangle"]]
        area = (corners[2] - corners[0]) * (corners[3] - corners[1])
        density = Fraction(row["mass"]) / 8 / area
        expected = [(*image, density) for image in orbit(side, corners)]
        for line in lines[8 * index : 8 * index + 8]:
            tokens = line.split()
            require(
                len(tokens) == 10, f"row {index}: a rectangle line has {len(tokens)} fields"
            )
            bounds = [
                (Fraction(float.fromhex(tokens[k])), Fraction(float.fromhex(tokens[k + 1])))
                for k in range(0, 10, 2)
            ]
            match = next(
                (
                    image
                    for image in expected
                    if all(
                        low <= exact <= high
                        for (low, high), exact in zip(bounds, image, strict=True)
                    )
                ),
                None,
            )
            if match is None:
                raise AuditError(f"row {index}: a line encloses none of its images")
            expected.remove(match)


def bundle(root: Path, directory: Path | None = None, *, key: str = DEFAULT) -> dict[str, Any]:
    """Bind an unpacked proof bundle to the packet and its records to the declared net."""
    stated = CERTIFICATES[key]
    directory = directory or stated.directory
    if stated.check2:
        return bundle_check2(root, directory, stated)
    listed: dict[str, str] = json.loads((root / "files-sha256.json").read_text())
    present = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "files-sha256.json"
    }
    require(present == set(listed), f"unlisted or missing: {sorted(present ^ set(listed))[:5]}")
    for name, digest in listed.items():
        require(sha256((root / name).read_bytes()) == digest, f"{name} differs from its list")
    for name in ("candidate.json", "certificate.json", "manifest.json"):
        require(
            (root / "proof" / name).read_bytes() == read_retained_bytes(directory / name),
            f"proof/{name} is not the retained file",
        )
    code = sorted(path.name for path in (root / "code").iterdir())
    require(
        code == sorted(path.name for path in N50_DIRECTORY.joinpath("code").iterdir()), "code/"
    )
    for name in code:
        reference = stated.code_reference(name)
        require(
            sha256((root / "code" / name).read_bytes())
            == sha256(read_retained_bytes(reference)),
            f"code/{name} is not the retained copy {reference.relative_to(WEB)}",
        )
    require(
        sha256((root / "requirements.txt").read_bytes())
        == sha256((N50_DIRECTORY / "requirements.txt").read_bytes()),
        "requirements.txt is not the retained copy",
    )
    require(sha256((root / "proof/verify.cpp").read_bytes()) == CHECKER_SHA256, "verify.cpp")
    candidate, certificate, _manifest = read_directory(directory)
    side, core = Fraction(candidate["L"]), Fraction(candidate["B"])
    step = Fraction(candidate["proof_net"]["step"])
    count = int(candidate["proof_net"]["last"]) + 1
    digest = candidate["scaling_source_digest"]
    images = 8 * len(candidate["rectangles"])
    block: list[str] | None = None
    seconds = 0.0
    nodes = 0
    for r in range(1, count):
        folder = root / "proof" / f"net{r:03d}"
        result = json.loads((folder / "result.json").read_text())
        manifest = result["manifest"]
        domain = manifest["domain"]
        t = step * r
        floor = max(Fraction(0), t - step / 2)
        low = rho(floor)
        half_width = side / 2 - low
        require(
            result["status"] == "ANGLE_VERIFIED"
            and result["frontier"] == []
            and result["exact_witnesses"] == []
            and float(result["lower"]) >= 1,
            f"node {r}: the shipped run did not verify it",
        )
        require(
            manifest["candidate_digest"] == digest
            and manifest["net_index"] == r
            and Fraction(manifest["t"]) == t
            and manifest["gamma"] == "1"
            and manifest["source_sha256"] == CHECKER_SHA256,
            f"node {r}: the record is not this candidate's at t = {t}",
        )
        require(
            domain["index"] == r
            and Fraction(domain["t"]) == t
            and Fraction(domain["original_t_lower"]) == floor
            and Fraction(domain["centre_low"]) == low
            and Fraction(domain["centre_high"]) == side - low
            and Fraction(manifest["E"]) == half_width,
            f"node {r}: the centre domain is not the per-bin domain at step {step}",
        )
        text = (folder / "input.txt").read_bytes()
        require(sha256(text) == manifest["input_sha256"], f"node {r}: the input's digest")
        lines = text.decode().splitlines()
        cosine = (1 - t * t) / (1 + t * t)
        sine = 2 * t / (1 + t * t)
        for position, exact in enumerate((side, core, half_width, cosine, sine, Fraction(1))):
            low_end, high_end = enclosure(lines[position])
            require(low_end <= exact <= high_end, f"node {r}: input line {position + 1}")
        require(int(lines[6]) == images, f"node {r}: the input lists {lines[6]} rectangles")
        # The rectangle lines are the same at every node: checked against the expanded
        # candidate once, and held byte for byte to that at every other node.
        if block is None:
            rectangle_block(candidate, lines[7:])
            block = lines[7:]
        require(lines[7:] == block, f"node {r}: the rectangle lines differ from node 1's")
        record = certificate["results"][str(r)]
        require(
            (int(record["nodes"]), float(record["lower"]))
            == (int(result["nodes"]), float(result["lower"])),
            f"node {r}: the certificate's record is not the run's",
        )
        seconds += float(result["seconds"])
        nodes += int(result["nodes"])
    axis = json.loads((root / "proof/axis/result.json").read_text())
    require(
        axis["status"] == "AXIS_VERIFIED"
        and axis["net_index"] == 0
        and axis["gamma"] == "1"
        and axis["digest"] == digest
        and Fraction(axis["mass"]) == Fraction(candidate["total_mass"])
        and axis["integer_unresolved"] == 0
        and axis["witness"] is None
        and Fraction(axis["integer_minimum"]) >= 1,
        "the axis record is not a complete run at threshold one",
    )
    return {
        "kind": "wand125-declared-net-bundle/v1",
        "certificate": stated.name,
        "status": "BUNDLE_BOUND_TO_PACKET_AND_NET",
        "listed_files": len(listed),
        "code_files": len(code),
        "oblique_inputs": count - 1,
        "rectangle_images": images,
        "rectangle_lines": "ENCLOSE_THE_EXPANDED_CANDIDATE",
        "upstream_oblique_seconds": seconds,
        "upstream_oblique_nodes": nodes,
        "axis": {
            "cells": axis["cells"],
            "integer_minimum": axis["integer_minimum"],
            "seconds": axis["seconds"],
        },
        "scope": (
            "The bundle's files against its own list and the packet, every shipped record"
            " and input header against the declared net's tangent, per-bin domain and"
            " threshold, and every input's rectangle lines against the expanded candidate."
            " No coverage is decided here."
        ),
    }


def read_jsonl_gz(path: Path) -> list[dict[str, Any]]:
    """The records of a gzipped JSON-lines log."""
    return [json.loads(line) for line in gzip.decompress(path.read_bytes()).splitlines()]


def control_witnesses(
    candidate: dict[str, Any], tried: list[dict[str, Any]], factor: Fraction
) -> int:
    """Recompute every exact witness of a control log on the candidate scaled by ``factor``.

    Each witness's centre must lie in its node's per-bin domain, its logged exact capture
    must equal the capture `check_sqverify_fast.mixed_exact` computes there on the scaled
    measure, an evaluator written apart from the crate, and that capture must be below
    one: so the control is a provably invalid measure, refused (finding FN-2 of the 6
    October review of T-102 to T-111). Returns how many were recomputed.
    """
    exact = importlib.import_module("devtools.check_sqverify_fast").mixed_exact
    scaled_candidate = {
        "L": candidate["L"],
        "B": candidate["B"],
        "proof_net": candidate["proof_net"],
        "rectangles": [
            {"rectangle": row["rectangle"], "mass": str(Fraction(row["mass"]) * factor)}
            for row in candidate["rectangles"]
        ],
    }
    side = Fraction(candidate["L"])
    step = Fraction(candidate["proof_net"]["step"])
    count = 0
    for record in tried:
        witness = record.get("witness") or {}
        if not witness.get("exact_below_threshold"):
            continue
        r = int(record["r"])
        low = rho(max(Fraction(0), step * r - step / 2))
        x, y = (Fraction(value) for value in witness["exact_pose"])
        logged = Fraction(witness["exact_coverage"])
        require(
            low <= x <= side - low and low <= y <= side - low,
            f"control node {r}: the witness is outside the per-bin domain",
        )
        require(
            exact(scaled_candidate, x, y, r) == logged < 1,
            f"control node {r}: the witness's capture is not the logged one below one",
        )
        count += 1
    require(count > 0, "the control log has no exact witness")
    return count


def bundle_check2(root: Path, directory: Path, stated: Certificate) -> dict[str, Any]:
    """Bind an unpacked check2 bundle to the packet, and its run log to the declared net.

    - every file ``files-sha256.json`` lists has that digest, and nothing is unlisted;
      the list is the retained one; every listed file but the bundle's own README is the
      directory's, by its bytes where the packet retains it and by its pin where not;
      the adapted crate's tarball is compared by digest only and never opened;
    - the run log ``check2/run.jsonl.gz`` holds one record per net node, every one
      ``verified`` at threshold one with a certified lower bound of at least one, the
      axis by the vertex sweep and every oblique node by branch and bound, and ends with
      the summary the receipt states;
    - the one control log, ``check2/control.jsonl.gz`` or, in ``mixed_n18_L4705``,
      ``check2/control-197_200.jsonl.gz``, ends with a summary ``REFUSED`` on the
      candidate with every mass scaled by a factor below one, its refused directions
      are the ones it did not verify, and they and its witnesses below threshold are as
      many as ``control.json`` states.

    It decides no coverage: the source's run is of its adaptation of this repository's
    sqverify_fast, and its log is what that run printed.
    """
    listed: dict[str, str] = json.loads((root / "files-sha256.json").read_text())
    require(
        (root / "files-sha256.json").read_bytes()
        == read_retained_bytes(directory / "files-sha256.json"),
        "files-sha256.json is not the retained list",
    )
    present = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "files-sha256.json"
    }
    require(present == set(listed), f"unlisted or missing: {sorted(present ^ set(listed))[:5]}")
    pins = pinned_digests(stated)
    retained = 0
    for name, digest in listed.items():
        data = (root / name).read_bytes()
        require(sha256(data) == digest, f"{name} differs from its list")
        if name == BUNDLE_README:
            continue
        path = directory / name
        if path.exists() or path.with_name(path.name + ".gz").exists():
            require(data == read_retained_bytes(path), f"{name} is not the retained file")
            retained += 1
        else:
            require(
                pins.get(f"certificates/{stated.name}/{name}") == digest,
                f"{name} is not the pinned file",
            )
    candidate = load_json(read_retained_bytes(directory / "candidate.json"))
    count = int(candidate["proof_net"]["last"]) + 1
    total = Fraction(candidate["total_mass"])
    receipt = json.loads(read_retained_bytes(directory / "check2/receipt.json"))
    run = read_jsonl_gz(root / "check2/run.jsonl.gz")
    summary, directions = run[-1], run[:-1]
    require(
        summary == receipt["verifier_summary"], "the run log's summary is not the receipt's"
    )
    require(
        sorted(record["r"] for record in directions) == list(range(count)),
        "the run log does not hold one record per net node",
    )
    for record in directions:
        r = record["r"]
        require(
            record["verdict"] == "verified"
            and record["threshold"] == "1"
            and record["min_certified_lower_bound"] >= 1
            and record["method"]
            == ("axis-vertex-sweep" if r == 0 else "interval-branch-and-bound"),
            f"node {r}: the run log does not verify it at threshold one",
        )
    oblique = [record for record in directions if record["r"] > 0]
    require(
        sum(record["nodes"] for record in oblique) == summary["nodes"],
        "the run log's nodes do not total its summary's",
    )
    least = min(oblique, key=lambda record: (record["min_certified_lower_bound"], record["r"]))
    axis = next(record for record in directions if record["r"] == 0)
    logs = sorted((root / "check2").glob("control*.jsonl.gz"))
    require(len(logs) == 1, f"the bundle has {len(logs)} control logs")
    control = read_jsonl_gz(logs[0])
    control_summary, tried = control[-1], control[:-1]
    factor = Fraction(control_summary["premises"]["mass_exact"]) / total
    below = sum(
        1 for record in tried if (record.get("witness") or {}).get("exact_below_threshold")
    )
    stated_control = load_json(read_retained_bytes(directory / "check2/control.json"))
    last_try = stated_control["tries"][-1] if "tries" in stated_control else stated_control
    stated_refused = last_try.get("refused", last_try.get("refused_directions"))
    refused = sorted(record["r"] for record in tried if record["verdict"] != "verified")
    require(
        control_summary["status"] == "REFUSED"
        and len(tried) == control_summary["directions"]
        and sorted(control_summary["refused_directions"]) == refused
        and len(refused) == stated_refused
        and below == last_try["exact_below_threshold"]
        and factor == CHECK2_CONTROL_FACTOR,
        "the control log is not a refusal of this candidate scaled by 197/200, as"
        " control.json states",
    )
    control_premises = control_summary["premises"]
    require(
        Fraction(control_premises["L"]) == Fraction(candidate["L"])
        and Fraction(control_premises["B"]) == Fraction(candidate["B"])
        and Fraction(control_premises["D"]) == Fraction(candidate["proof_net"]["step"])
        and control_premises["angle_count"] == count
        and control_premises["format"] == "M"
        and control_premises["centre_domain"] == "per-bin"
        and control_summary["threshold"] == "1",
        "the control ran on another side, core, net or threshold",
    )
    witnesses = control_witnesses(candidate, tried, factor)
    return {
        "kind": "wand125-declared-net-bundle/v1",
        "format": "check2",
        "certificate": stated.name,
        "status": "BUNDLE_BOUND_TO_PACKET_AND_NET",
        "listed_files": len(listed),
        "retained_files_equal": retained,
        "pinned_files_equal": len(listed) - retained - 1,
        "run_log": {
            "directions": len(directions),
            "oblique_nodes": summary["nodes"],
            "direction_seconds": summary["direction_seconds"],
            "direction_cpu_seconds": summary["direction_cpu_seconds"],
            "threads": summary["threads"],
            "target": summary["build"]["target"],
            "source_sha256": summary["build"]["source_sha256"],
            "least_oblique": {"r": least["r"], "lower": least["min_certified_lower_bound"]},
            "axis_lower": axis["min_certified_lower_bound"],
        },
        "control_log": {
            "witnesses_recomputed": witnesses,
            "file": logs[0].relative_to(root).as_posix(),
            "directions": len(tried),
            "refused": len(refused),
            "factor": str(factor),
            "exact_below_threshold": below,
        },
        "scope": (
            "The bundle's files against its own list and the packet, and the source's run"
            " and control logs against the declared net, threshold one and the receipt. The"
            " run is of the source's adaptation of this repository's sqverify_fast, whose"
            " tarball is held by digest and not opened. No coverage is decided here."
        ),
    }


#: Files the bundle's driver writes in its copy of the bundle, besides each node's
#: record: compared by their content, never by their bytes.
DRIVER_OUTPUTS = frozenset(
    {"bundle.json", "files-sha256.json", "proof/replay-progress.json", "proof/certificate.json"}
)
#: What the driver builds and leaves in its copy: present only where it ran.
DRIVER_BINARY = "proof/replay-verify"


def read_meta(path: Path) -> dict[str, str]:
    """The run's own record (`key: value` lines, as the replay's runner writes them)."""
    meta: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition(": ")
        if separator and key and not key.startswith(" "):
            meta.setdefault(key, value)
    return meta


#: The snapshot of a running replay's processes that `processes` writes beside its record.
PROCESSES = "processes.json"


def optimizing(argv: list[str]) -> bool:
    """Whether a Python command line asks for ``-O``: an ``O`` among the short options
    before the script, ``-c`` or ``-m``."""
    for token in argv[1:]:
        if not token.startswith("-") or token in {"-c", "-m"}:
            return False
        if not token.startswith("--") and "O" in token[1:]:
            return True
    return False


def asserts_were_on(run: dict[str, str], snapshot: Path) -> bool:
    """Whether the run record, or a snapshot taken during the run, shows that the
    driver and its workers ran with Python's assertions on."""
    if run.get("asserts") == "on":
        return True
    if not snapshot.is_file():
        return False
    taken = json.loads(snapshot.read_text(encoding="utf-8"))
    start, end = run.get("start", ""), run.get("end", "")
    return (
        taken.get("status") == "ASSERTS_ON"
        and bool(start)
        and start <= taken.get("taken", "")
        and (not end or taken.get("taken", "") <= end)
        and len(taken.get("processes") or []) >= 2
    )


def descendants(pid: int) -> list[int]:
    """``pid`` and every process below it, from ``/proc``."""
    children: dict[int, list[int]] = {}
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            fields = (entry / "stat").read_text().rsplit(")", 1)[1].split()
        except OSError:
            continue
        children.setdefault(int(fields[1]), []).append(int(entry.name))
    found, queue = [], [pid]
    while queue:
        current = queue.pop()
        found.append(current)
        queue += children.get(current, [])
    return sorted(found)


def processes(pid: int) -> dict[str, Any]:
    """A snapshot of a running replay: the driver ``pid`` and every process below it.

    For each process, its command line, working directory and the environment
    variables that change how Python or NumPy run. Status ``ASSERTS_ON`` when the
    driver's command line is the bundle's driver and no Python process among them asks
    for ``-O`` or has ``PYTHONOPTIMIZE`` set.
    """
    rows: list[dict[str, Any]] = []
    for each in descendants(pid):
        base = Path("/proc") / str(each)
        try:
            argv = (base / "cmdline").read_bytes().decode().split("\0")[:-1]
            environ = (base / "environ").read_bytes().decode(errors="replace").split("\0")
            cwd = str((base / "cwd").readlink())
        except OSError:
            continue
        kept = {
            name: value
            for name, _, value in (item.partition("=") for item in environ)
            if name.startswith("PYTHON") or name in {"OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS"}
        }
        python = bool(argv) and Path(argv[0]).name.startswith("python")
        rows.append(
            {
                "pid": each,
                "argv": argv,
                "cwd": cwd,
                "environment": kept,
                "python": python,
                "optimizing": python and (optimizing(argv) or "PYTHONOPTIMIZE" in kept),
            }
        )
    driver = rows[0]["argv"] if rows else []
    on = (
        bool(rows)
        and driver[1:3] == ["code/verify_mixed_full_proof.py", "proof"]
        and not any(row["optimizing"] for row in rows)
    )
    return {
        "kind": "wand125-declared-net-processes/v1",
        "status": "ASSERTS_ON" if on else "NOT_SHOWN",
        "taken": utc_now(),
        "driver_pid": pid,
        "processes": rows,
    }


def record_name(r: int) -> str:
    return "proof/axis/replayed.json" if r == 0 else f"proof/net{r:03d}/replayed.json"


def compare(
    shipped: Path,
    fresh: Path,
    meta: Path,
    directory: Path | None = None,
    *,
    key: str = DEFAULT,
) -> dict[str, Any]:
    """A replay by the bundle's own driver, in a copy of the bundle, against the shipped
    run: that the run happened, and that every record it regenerated is the shipped one.

    The run happened when its runner's record says it started and exited zero, the
    driver's progress record counts every node done, the driver's binary is in the copy,
    every node's record and the rewritten certificate were written after the run
    started. The source's checks ran when the run record says the driver's assertions
    were on, or a snapshot of the running processes (`processes`, ``processes.json``
    beside the record) shows no ``-O`` and no ``PYTHONOPTIMIZE`` in the driver or any
    worker during the run: the checks are Python ``assert`` statements (finding FN-1 of
    the 6 October review). Every regenerated record equals the shipped one and the
    retained certificate's, field by field; the copy's certificate equals the retained
    one as a mapping, whatever its order; and every other shipped file is unchanged. The
    copy's `bundle.json` is held to the shipped one's statuses as a consistency check
    only: the driver does not write it, so it shows nothing about the run (FN-2).
    """
    stated = CERTIFICATES[key]
    directory = directory or stated.directory
    candidate, certificate, _manifest = read_directory(directory)
    count = int(candidate["proof_net"]["last"]) + 1
    run = read_meta(meta)
    differing: list[str] = []
    if run.get("exit") != "0":
        differing.append(f"the run did not exit zero: {run.get('exit')}")
    started = run.get("start", "")
    start_time = datetime.fromisoformat(started).timestamp() if started else None
    if not asserts_were_on(run, meta.parent / PROCESSES):
        differing.append("nothing shows the driver's assertions were on during the run")
    progress_path = fresh / "proof/replay-progress.json"
    progress = json.loads(progress_path.read_text()) if progress_path.is_file() else {}
    if progress != {"done": count, "total": count}:
        differing.append(f"the driver's progress record is {progress or 'missing'}")
    if not (fresh / DRIVER_BINARY).is_file() or (shipped / DRIVER_BINARY).exists():
        differing.append("the driver's binary is not in the copy alone")
    matching = 0
    for r in range(count):
        name = record_name(r)
        after = fresh / name
        if not after.is_file():
            differing.append(f"{name}: missing")
            continue
        if start_time is None or after.stat().st_mtime < start_time:
            differing.append(f"{name}: not written by this run")
            continue
        regenerated = load_json(after.read_bytes())
        if regenerated != load_json((shipped / name).read_bytes()):
            differing.append(f"{name}: differs from the shipped record")
        elif regenerated != certificate["results"][str(r)]:
            differing.append(f"{name}: differs from the retained certificate's record")
        else:
            matching += 1
    rewritten = fresh / "proof/certificate.json"
    if start_time is None or rewritten.stat().st_mtime < start_time:
        differing.append("proof/certificate.json: not rewritten by this run")
    elif load_json(rewritten.read_bytes()) != certificate:
        differing.append("proof/certificate.json: differs from the retained certificate")
    fresh_bundle = json.loads((fresh / "bundle.json").read_text())
    if (fresh_bundle.get("status"), fresh_bundle.get("certificate")) != (
        "REPLAYED_PROOF_BUNDLE",
        "ALL_ANGLES_VERIFIED_AND_REPLAYED",
    ):
        differing.append(f"bundle.json reports {fresh_bundle}")
    unchanged = 0
    for path in sorted(shipped.rglob("*")):
        name = path.relative_to(shipped).as_posix()
        if not path.is_file() or name.endswith("replayed.json") or name in DRIVER_OUTPUTS:
            continue
        other = fresh / name
        if not other.is_file() or other.read_bytes() != path.read_bytes():
            differing.append(f"{name}: changed by the replay")
        else:
            unchanged += 1
    return {
        "kind": "wand125-declared-net-compare/v2",
        "certificate": stated.name,
        "status": "FULL_REPLAY_MATCHES_SHIPPED" if not differing else "MISMATCH",
        "run": {key: run.get(key) for key in ("start", "end", "exit")},
        "progress": progress,
        "fresh_status": fresh_bundle.get("certificate"),
        "fresh_bundle_status": fresh_bundle.get("status"),
        "certificate_rewritten": rewritten.is_file()
        and rewritten.read_bytes() != (shipped / "proof/certificate.json").read_bytes(),
        "records_matching": matching,
        "records": count,
        "unchanged_shipped_files": unchanged,
        "differing": differing,
        "certificate_sha256": sha256(read_retained_bytes(directory / "certificate.json")),
    }


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def unpack(stated: Certificate, tarball: Path, into: Path) -> tuple[Path, dict[str, Any]]:
    """The pinned tarball, unpacked afresh under ``into``.

    Refused unless its size and SHA-256 are the packet's pin, or if any member lies
    outside its one top-level directory or is not a plain file or directory. The members'
    file times are the archive's, so a record a later run writes is newer than every
    shipped one.
    """
    digest, size = stated.tarball_pin()
    require(
        tarball.stat().st_size == size and file_sha256(tarball) == digest,
        f"{tarball} is not the pinned {stated.tarball}",
    )
    if into.exists():
        shutil.rmtree(into)
    into.mkdir(parents=True)
    with tarfile.open(tarball, "r:gz") as archive:
        for member in archive.getmembers():
            name = PurePosixPath(member.name)
            require(
                name.parts[0] == stated.bundle_name
                and ".." not in name.parts
                and not name.is_absolute()
                and (member.isfile() or member.isdir()),
                f"unexpected archive member: {member.name}",
            )
        archive.extractall(into, filter="data")
    return into / stated.bundle_name, {"name": stated.tarball, "sha256": digest, "bytes": size}


def shipped_modules() -> Any:
    """`devtools.audit_wand125_point_and_mixed`, whose replay functions run the source's
    per-node checks on any mixed bundle, its declared net included."""
    return importlib.import_module("devtools.audit_wand125_point_and_mixed")


def sample(
    key: str, tarball: Path, work: Path, nodes: list[int], workers: int
) -> dict[str, Any]:
    """Replay ``nodes`` of the net with the source's checker, after binding the bundle.

    The bundle is unpacked afresh and bound by `bundle`; then
    `audit_wand125_point_and_mixed.n50_replay` repeats the full driver's preconditions in
    its order and calls the source's per-node functions, unchanged, on each node, with
    the checker the source's ``compile_verifier`` builds. Each node passes only if it
    returns the shipped record. The price of the rest is the sample's CPU over the
    bundle's own seconds on the same nodes, times the bundle's seconds on every node.
    """
    stated = CERTIFICATES[key]
    mixed = shipped_modules()
    root, pin = unpack(stated, tarball, work / "sample")
    binding = bundle(root, key=key)
    runtime = mixed.replay_runtime()
    started = utc_now()
    report = mixed.n50_replay(root, nodes, workers)
    rows = report.pop("rows")
    return {
        "kind": "wand125-declared-net-sample/v1",
        "certificate": stated.name,
        "status": report.pop("status"),
        "nodes": report.pop("indices"),
        "workers": workers,
        "started": started,
        "ended": utc_now(),
        "rows": rows,
        "sample_cpu_seconds": round(sum(row["cpu_seconds"] for row in rows), 1),
        **report,
        "tarball": pin,
        "binding": {
            field: binding[field] for field in ("status", "listed_files", "code_files")
        },
        "environment": runtime,
        "host": mixed.host_facts(),
        "loadavg_end": list(os.getloadavg()),
    }


def numpy_version() -> str:
    try:
        return importlib.import_module("numpy").__version__
    except ImportError:
        return "absent"


def compiler_version() -> str:
    try:
        output = subprocess.run(
            ["c++", "--version"], capture_output=True, text=True, check=True
        )
    except OSError, subprocess.CalledProcessError:
        return "absent"
    return output.stdout.splitlines()[0]


def replay(
    key: str, tarball: Path, work: Path, workers: int, out: Path | None = None
) -> dict[str, Any]:
    """The bundle's own driver over every node, as its README says, then `compare`.

    The pinned tarball is unpacked twice. The first copy is bound by `bundle`, whose
    receipt is written beside the run's; the driver runs in the second,
    ``OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 code/verify_mixed_full_proof.py
    proof --workers W`` with this interpreter as ``python3``. The source's checks are
    Python ``assert`` statements, so the runner refuses to start under ``-O`` or
    ``PYTHONOPTIMIZE`` and removes ``PYTHONOPTIMIZE`` from the driver's environment
    (finding FN-1 of the 6 October review). The run's record, ``run.meta``, holds its
    start, exit and end, that its assertions were on, and the CPU of the driver and of
    every process it waited for, its pooled workers and their checker runs among them,
    read from ``wait4``; ``run.stdout`` is what it printed.
    """
    stated = CERTIFICATES[key]
    require(
        not sys.flags.optimize and not os.environ.get("PYTHONOPTIMIZE"),
        "assertions are off: the source's checks are asserts, so drop -O and PYTHONOPTIMIZE",
    )
    out = out or stated.receipts / "full"
    out.mkdir(parents=True, exist_ok=True)
    shipped, pin = unpack(stated, tarball, work / "shipped")
    write_or_check(stated.receipts / "bundle.json", bundle(shipped, key=key), check=False)
    fresh, _pin = unpack(stated, tarball, work / "run")
    command = [sys.executable, "code/verify_mixed_full_proof.py", "proof"]
    command += ["--workers", str(workers)]
    environment = {
        name: value for name, value in os.environ.items() if name != "PYTHONOPTIMIZE"
    } | {"OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    require(not optimizing(command), "the driver's command line asks for -O")
    lines = [
        "command: OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 " + " ".join(command),
        f"cwd: {fresh}",
        f"tarball: {pin['name']} sha256 {pin['sha256']} bytes {pin['bytes']}",
        f"python: {platform.python_version()} numpy {numpy_version()}",
        f"cxx: {compiler_version()}",
        (
            f"host: {platform.system()} {platform.release()} {platform.machine()},"
            f" {os.cpu_count()} cpus"
        ),
        f"niceness: {os.nice(0)}",
        "asserts: on",
        (
            "asserts_basis: the runner refuses -O and PYTHONOPTIMIZE, and the driver runs"
            " without -O and with PYTHONOPTIMIZE removed from its environment"
        ),
        f"start: {utc_now()}",
        "loadavg_start: " + " ".join(f"{value:.2f}" for value in os.getloadavg()),
    ]
    clock = time.monotonic()
    with (out / "run.stdout").open("wb") as stdout:
        process = subprocess.Popen(
            command, cwd=fresh, env=environment, stdout=stdout, stderr=subprocess.STDOUT
        )
        _pid, status, usage = os.wait4(process.pid, 0)
        process.returncode = os.waitstatus_to_exitcode(status)
    lines += [
        f"exit: {process.returncode}",
        f"end: {utc_now()}",
        "loadavg_end: " + " ".join(f"{value:.2f}" for value in os.getloadavg()),
        f"wall_seconds: {time.monotonic() - clock:.1f}",
        f"cpu_user_seconds: {usage.ru_utime:.1f}",
        f"cpu_system_seconds: {usage.ru_stime:.1f}",
        f"cpu_seconds: {usage.ru_utime + usage.ru_stime:.1f}",
        f"max_rss_kb: {usage.ru_maxrss}",
    ]
    (out / "run.meta").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return compare(shipped, fresh, out / "run.meta", key=key)


#: The factor ``control``'s first mutant scales every mass by.
CONTROL_FACTOR = Fraction(99, 100)
#: How far below 1 the second mutant's capture at the exact witness centre is.
NEAR_THRESHOLD = Fraction(1, 10**6)
#: How long one control run of the source's checker may take.
CONTROL_TIMEOUT = 3600


def scaled(data: dict[str, Any], factor: Fraction) -> dict[str, Any]:
    """A copy of a candidate with every mass, and the total, multiplied by ``factor``."""
    mutated = dict(data)
    mutated["rectangles"] = [
        row | {"mass": str(Fraction(row["mass"]) * factor)} for row in data["rectangles"]
    ]
    mutated["total_mass"] = str(
        sum((Fraction(row["mass"]) for row in mutated["rectangles"]), Fraction())
    )
    return mutated


#: What each corrupted net's refusal must name, by the source's net check and by
#: ``sqverify-fast``'s admission: a control refused for another premise would not hold its
#: rule (finding DN-6 of the 5 October review).
NET_REFUSALS = {
    "coarser-step": ("Core containment is not strict", "B (1 + D)"),
    "short-net": ("Net does not reach tan(pi/8)", "pi/4"),
    "extra-field": ("Invalid proof_net fields", "does not know"),
}


def reaches_past_pi_over_8(t: Fraction) -> bool:
    """Whether a half-angle tangent is at least ``tan(pi/8)``: ``(1 + t)^2 >= 2``."""
    return (1 + t) ** 2 >= 2


def sharp_extent(core: Fraction, step: Fraction) -> Fraction:
    """The widest a concentric core of side ``core`` reaches across the unit square when
    the core's angle is half a step of half-angle tangent from the square's:
    ``B (cos d + sin d)`` at ``tan(d/2) = step/2``. It increases with the offset, so a
    core fits strictly inside every unit square assigned to its node exactly when this is
    below 1."""
    z = step / 2
    return core * (1 + 2 * z - z * z) / (1 + z * z)


def coarser_net(core: Fraction) -> dict[str, Any]:
    """The finest net of steps ``1/q`` on which the core does not fit, and which is
    otherwise sound: its last node reaches ``tan(pi/8)`` and the bin below it still holds
    an orientation of ``[0, pi/4]``.

    The core does not fit when `sharp_extent` is at least 1: then a unit square at a bin's
    edge does not hold its core strictly inside, so the containment the argument needs
    fails, and not only the sufficient test ``B (1 + D) < 1`` (finding FN-3 of the 6
    October review, which found ``D = (1 - B)/B`` still fits). Only the core's fit fails.
    """
    q = int(core / (1 - core))
    while q > 1:
        step = Fraction(1, q)
        last = next(k for k in range(q + 1) if reaches_past_pi_over_8(k * step))
        sound = not reaches_past_pi_over_8((last - Fraction(1, 2)) * step)
        if sharp_extent(core, step) >= 1 and sound:
            return {"step": str(step), "last": last}
        q -= 1
    raise AuditError(f"no coarser net isolates the core's fit at B = {core}")


def corrupted_nets(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Three corrupted net declarations, each a copy of the candidate, each breaking one
    premise of the declared net and no other.

    ``coarser-step`` is `coarser_net`, on which a core at a bin's edge does not fit
    strictly inside its unit square;
    ``short-net`` drops the last node, so the net stops before ``tan(pi/8)``;
    ``extra-field`` adds a field the format does not have.
    """
    core = Fraction(data["B"])
    net = data["proof_net"]
    return {
        "coarser-step": data | {"proof_net": coarser_net(core)},
        "short-net": data | {"proof_net": net | {"last": int(net["last"]) - 1}},
        "extra-field": data | {"proof_net": net | {"offset": str(Fraction(net["step"]) / 2)}},
    }


def sqverify_fast_refusal(binary: Path, path: Path, n: int) -> dict[str, Any]:
    """A corrupted net under ``sqverify-fast``: admission must refuse it."""
    argv = [str(binary.resolve()), "--candidate", str(path), "--n", str(n), "--directions"]
    result = subprocess.run(
        [*argv, "0"], capture_output=True, text=True, check=False, timeout=600
    )
    refused = result.returncode != 0 and not any(
        '"verified"' in line for line in result.stdout.splitlines()
    )
    return {
        "returncode": result.returncode,
        "stderr": result.stderr.strip()[-400:],
        "verdict": "REFUSED" if refused else "ACCEPTED",
    }


def control(
    key: str,
    tarball: Path,
    work: Path,
    index: int | None = None,
    sqverify_fast: Path | None = None,
) -> dict[str, Any]:
    """The source's checker on the certificate and its mutants: the stage-4 controls.

    The bundle is unpacked afresh and bound, and the full driver's preconditions run. At
    one oblique node, the least recorded lower bound unless given, a centre of low
    capture is found (`audit_wand125_rectangles.least_covered`) and evaluated exactly.
    ``scale-masses`` multiplies every mass by 99/100 and ``near-threshold`` by the factor
    that leaves that centre's exact capture at ``1 - 10^-6``; each must leave it below 1,
    so each mutant is provably invalid at that node. Each variant is exported by the
    source's ``export`` and run by the checker its ``compile_verifier`` builds, with the
    shipped record's node count as the limit; the original must return the shipped
    record, and both mutants must stop unresolved. Each corrupted net declaration
    (`corrupted_nets`) must be refused by the source's ``candidate_net``, which the
    driver and every export read the net through, and by ``sqverify-fast`` when a binary
    is given.
    """
    stated = CERTIFICATES[key]
    mixed = shipped_modules()
    rectangles = importlib.import_module("devtools.audit_wand125_rectangles")
    root, pin = unpack(stated, tarball, work / "control-bundle")
    bundle(root, key=key)
    runtime = mixed.replay_runtime()
    driver = mixed.driver_preconditions(root)
    certificate = load_json(read_retained_bytes(stated.directory / "certificate.json"))
    oblique = {r: certificate["results"][str(r)] for r in range(1, driver.count)}
    chosen = (
        min(oblique, key=lambda r: (float(oblique[r]["lower"]), r)) if index is None else index
    )
    require(chosen in oblique, "a control runs one oblique net node")
    saved = mixed.check_angle_record(driver.root, chosen, driver.model[-1], driver.domains)
    spec = saved["manifest"]
    density = importlib.import_module("mixed_density_check")
    net_audit = importlib.import_module("mixed_net_audit")
    side, core, rects, points = driver.model[:4]
    data = json.loads((driver.root / "candidate.json").read_text())
    require(not points, "the witness search reads rectangle measures only")
    c, s = rectangles.net_rotation(Fraction(spec["t"]))
    domain = (side / 2, Fraction(spec["domain"]["centre_high"]))
    centre = rectangles.least_covered(rects, (c, s), core, domain)
    at_centre = rectangles.coverage_exact(rects, centre, c, s, core)
    near = (1 - NEAR_THRESHOLD) / at_centre
    variants = {
        "original": data,
        "scale-masses": scaled(data, CONTROL_FACTOR),
        "near-threshold": scaled(data, near),
    }
    gamma = Fraction(spec["gamma"])
    binary = work / "control-verify"
    driver.rotated.compile_verifier(binary)
    shipped_input = (driver.root / f"net{chosen:03}" / "input.txt").read_bytes()
    runs: list[dict[str, Any]] = []
    for label, variant in variants.items():
        folder = work / "control" / label
        shutil.rmtree(folder, ignore_errors=True)
        folder.mkdir(parents=True)
        (folder / "candidate.json").write_text(json.dumps(variant, indent=2) + "\n")
        model = density.expand(variant)
        manifest = driver.rotated.export(
            model, chosen, folder / "input.txt", gamma, net_audit.candidate_net(variant)
        )
        at_witness = rectangles.coverage_exact(model[2], centre, c, s, core)
        item: dict[str, Any] = {
            "name": label,
            "candidate_digest": model[-1],
            "input_sha256": manifest["input_sha256"],
            "total_mass": str(model[-2]),
            "witness_coverage_exact": str(at_witness),
            "witness_coverage": float(at_witness),
        }
        if label == "original":
            require(
                manifest == spec and (folder / "input.txt").read_bytes() == shipped_input,
                "the original's export is not the shipped proof's",
            )
        else:
            require(at_witness < 1, f"{label} leaves the witness covered")
            item["factor"] = str(CONTROL_FACTOR if label == "scale-masses" else near)
        run = mixed.control_direction(binary, folder, saved["nodes"], CONTROL_TIMEOUT)
        output = run.get("output") or {}
        if label == "original":
            matches = run.get("returncode") == 0 and run.get("frontier_boxes") == 0
            matches = matches and all(
                output.get(field) == saved[field]
                for field in ("status", "nodes", "leaves", "lower")
            )
            run["verdict"] = "ACCEPTED" if matches else "NOT_ACCEPTED"
        elif "verdict" not in run:
            unresolved = output.get("status") == "ANGLE_UNRESOLVED" and run["frontier_boxes"]
            run["verdict"] = "REFUSED" if unresolved else "ACCEPTED"
        runs.append(item | {"run": run})
        print(json.dumps({"name": label, "verdict": run["verdict"]}), flush=True)
    nets: list[dict[str, Any]] = []
    for label, variant in corrupted_nets(data).items():
        folder = work / "control" / label
        shutil.rmtree(folder, ignore_errors=True)
        folder.mkdir(parents=True)
        path = folder / "candidate.json"
        path.write_text(json.dumps(variant, indent=2) + "\n")
        source_rule, admission_rule = NET_REFUSALS[label]
        try:
            net_audit.candidate_net(variant)
        except ValueError as error:
            own = source_rule in str(error)
            source = {"verdict": "REFUSED" if own else "REFUSED_FOR_ANOTHER_PREMISE"}
            source["message"] = str(error)
        else:
            source = {"verdict": "ACCEPTED"}
        item = {"name": label, "proof_net": variant["proof_net"], "source": source}
        if sqverify_fast is not None:
            admission = sqverify_fast_refusal(sqverify_fast, path, stated.n)
            if admission["verdict"] == "REFUSED" and admission_rule not in admission["stderr"]:
                admission["verdict"] = "REFUSED_FOR_ANOTHER_PREMISE"
            item["sqverify_fast"] = admission
        nets.append(item)
        print(json.dumps({"name": label, "verdict": source["verdict"]}), flush=True)
    original, *mutants = runs
    refused = all(item["run"]["verdict"] == "REFUSED" for item in mutants) and all(
        item["source"]["verdict"] == "REFUSED"
        and item.get("sqverify_fast", {"verdict": "REFUSED"})["verdict"] == "REFUSED"
        for item in nets
    )
    passed = original["run"]["verdict"] == "ACCEPTED"
    return {
        "kind": "wand125-declared-net-control/v1",
        "status": "CONTROLS_REFUSED" if passed and refused else "CONTROL_FAILED",
        "certificate": stated.name,
        "n": stated.n,
        "side": str(stated.side),
        "index": chosen,
        "index_choice": "the least lower bound of the certificate's oblique records"
        if index is None
        else "given",
        "shipped_record": {
            field: saved[field] for field in ("status", "nodes", "leaves", "lower")
        },
        "gamma": str(gamma),
        "checker": {
            "source_sha256": spec["source_sha256"],
            "compile": "the shipped compile_verifier: c++ -O2 -std=c++17 -ffp-contract=off "
            "-fno-fast-math",
            "binary_sha256": file_sha256(binary),
            "argv": ["verify", "input.txt", str(saved["nodes"])],
        },
        "witness": {
            "centre": [str(value) for value in centre],
            "t": spec["t"],
            "domain": [str(value) for value in domain],
            "coverage_exact": str(at_centre),
            "coverage": float(at_centre),
        },
        "runs": runs,
        "nets": nets,
        "sqverify_fast": None if sqverify_fast is None else file_sha256(sqverify_fast),
        "tarball": pin,
        "environment": runtime,
        "host": mixed.host_facts(),
        "scope": (
            "Stage-4 negative controls on the certificate itself: the source's export and"
            " the C++ checker its compile_verifier builds, at one net node with the shipped"
            " record's node limit, on the original and two mutants that leave an exact"
            " witness centre covered below 1 there; and three corrupted net declarations"
            " under the source's net check and, where given, sqverify-fast's admission."
        ),
    }


def sqverify_fast_row(binary: Path, path: Path, n: int, index: int) -> dict[str, Any]:
    """One node of one candidate under ``sqverify-fast``, with ``--confirm``."""
    argv = [str(binary.resolve()), "--candidate", str(path), "--n", str(n)]
    argv += ["--directions", str(index), "--confirm"]
    result = subprocess.run(argv, capture_output=True, text=True, check=False, timeout=3600)
    rows = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
    row = next((line for line in rows if line.get("r") == index), {})
    witness = row.get("witness") or {}
    return {
        "returncode": result.returncode,
        "verdict": row.get("verdict"),
        "nodes": row.get("nodes"),
        "min_certified_lower_bound": row.get("min_certified_lower_bound"),
        "exact_below_threshold": witness.get("exact_below_threshold"),
        "stderr": result.stderr.strip()[-400:],
    }


def control_sqverify_fast(key: str, binary: Path, work: Path) -> dict[str, Any]:
    """``sqverify-fast`` on the same original and mutants as the source's checker.

    Reads the certificate's ``control`` receipt, rebuilds each mass mutant from the
    retained candidate by the factor the receipt records, checks that it is the mutant
    the source's checker ran (its total mass, and its exact capture at the receipt's
    witness centre, recomputed here, below 1), and runs ``sqverify-fast`` at the same
    node. The original must verify there and every mutant must be refused.
    """
    stated = CERTIFICATES[key]
    receipt = json.loads((stated.receipts / "control.json").read_text(encoding="utf-8"))
    require(receipt["status"] == "CONTROLS_REFUSED", "the control receipt did not pass")
    rectangles = importlib.import_module("devtools.audit_wand125_rectangles")
    data = load_json(read_retained_bytes(stated.directory / "candidate.json"))
    side, core = Fraction(data["L"]), Fraction(data["B"])
    index = int(receipt["index"])
    t = Fraction(receipt["witness"]["t"])
    require(t == index * Fraction(data["proof_net"]["step"]), "the receipt's tangent")
    c, s = rectangles.net_rotation(t)
    x, y = (Fraction(value) for value in receipt["witness"]["centre"])
    work.mkdir(parents=True, exist_ok=True)
    runs: list[dict[str, Any]] = []
    for item in receipt["runs"]:
        factor = Fraction(item.get("factor", "1"))
        variant = data if item["name"] == "original" else scaled(data, factor)
        require(Fraction(variant["total_mass"]) == Fraction(item["total_mass"]), item["name"])
        images: list[tuple[Fraction, ...]] = []
        for row in variant["rectangles"]:
            corners = [Fraction(value) for value in row["rectangle"]]
            area = (corners[2] - corners[0]) * (corners[3] - corners[1])
            density = Fraction(row["mass"]) / 8 / area
            images += [(*image, density) for image in orbit(side, corners)]
        at_witness = rectangles.coverage_exact(images, (x, y), c, s, core)
        require(
            at_witness == Fraction(item["witness_coverage_exact"]),
            f"{item['name']}: the capture at the witness is not the receipt's",
        )
        require(item["name"] == "original" or at_witness < 1, f"{item['name']} is covered")
        path = work / f"{stated.name}-{item['name']}.json"
        path.write_text(json.dumps(variant), encoding="utf-8")
        row = sqverify_fast_row(binary, path, stated.n, index)
        expect = "verified" if item["name"] == "original" else "refused"
        held = (
            row["returncode"] == 0 and row["verdict"] == "verified"
            if expect == "verified"
            else row["returncode"] == 1 and row["verdict"] not in (None, "verified")
        )
        runs.append(
            {
                "name": item["name"],
                "factor": str(factor),
                "witness_coverage_exact": str(at_witness),
                "expect": expect,
                "held": held,
                **row,
            }
        )
    nets = [
        {"name": item["name"], **item["sqverify_fast"]}
        for item in receipt["nets"]
        if "sqverify_fast" in item
    ]
    passed = all(run["held"] for run in runs) and all(
        item["verdict"] == "REFUSED" for item in nets
    )
    return {
        "kind": "wand125-declared-net-control-sqverify-fast/v1",
        "status": "CONTROLS_REFUSED" if passed and nets else "CONTROL_FAILED",
        "certificate": stated.name,
        "index": index,
        "binary_sha256": file_sha256(binary),
        "runs": runs,
        "nets": nets,
        "scope": (
            "sqverify-fast at the node of the source checker's control receipt, on the"
            " original and the same two mass mutants, rebuilt here from the retained"
            " candidate and evaluated exactly at the receipt's witness centre by"
            " audit_wand125_rectangles.coverage_exact; and the corrupted nets the control"
            " receipt ran through its admission."
        ),
    }


#: The branch-and-bound nodes `cpp_sample` allows the source's C++ checker at one node.
CPP_NODE_LIMIT = 4_000_000
#: The modules of the retained source code `cpp_sample` imports; dropped from the cache
#: first, so that the run never uses another copy's.
SOURCE_MODULES = ("mixed_density_check", "mixed_net_audit", "mixed_rotated_verify")


def _cpp_node(job: tuple[str, str, int, str, str, int]) -> dict[str, Any]:
    """Run the source's ``run`` at one oblique node (worker): its record, CPU and wall."""
    code, candidate, index, out, binary, limit = job
    if code not in sys.path:
        sys.path.insert(0, code)
    rotated = importlib.import_module("mixed_rotated_verify")
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.monotonic()
    result = rotated.run(Path(candidate), index, Path(out), Path(binary), limit, Fraction(1))
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    return {
        "status": result["status"],
        "nodes": result["nodes"],
        "lower": result["lower"],
        "frontier_boxes": len(result["frontier"]),
        "exact_witnesses": len(result["exact_witnesses"]),
        "manifest": result["manifest"],
        "wall_seconds": time.monotonic() - start,
        "cpu_seconds": (after.ru_utime - before.ru_utime) + (after.ru_stime - before.ru_stime),
    }


def source_code_copy(work: Path) -> Path:
    """The retained ``mixed_n50_L740`` code in a fresh folder, each file held to its
    retained bytes and the checker to `CHECKER_SHA256`."""
    code = work / "code"
    if code.exists():
        shutil.rmtree(code)
    code.mkdir(parents=True)
    for path in sorted(N50_DIRECTORY.joinpath("code").iterdir()):
        (code / path.name).write_bytes(read_retained_bytes(path))
    require(
        sha256((code / "mixed_rotated_verify.cpp").read_bytes()) == CHECKER_SHA256,
        "the retained checker is not 89b674a6...",
    )
    return code


def check_node_manifest(
    manifest: dict[str, Any], candidate: dict[str, Any], index: int, input_text: bytes
) -> None:
    """The source's record of one node: lemma N0's tangent and per-bin domain, threshold
    one, this candidate, and an input whose header encloses them exactly."""
    side, core = Fraction(candidate["L"]), Fraction(candidate["B"])
    step = Fraction(candidate["proof_net"]["step"])
    t = step * index
    floor = max(Fraction(0), t - step / 2)
    low = rho(floor)
    domain = manifest["domain"]
    require(
        manifest["candidate_digest"] == semantic_digest(candidate)
        and manifest["net_index"] == index
        and Fraction(manifest["t"]) == t
        and manifest["gamma"] == "1"
        and manifest["source_sha256"] == CHECKER_SHA256
        and manifest["input_sha256"] == sha256(input_text),
        f"node {index}: the run is not this candidate's at t = {t}",
    )
    require(
        domain["index"] == index
        and Fraction(domain["original_t_lower"]) == floor
        and Fraction(domain["centre_low"]) == low
        and Fraction(domain["centre_high"]) == side - low
        and Fraction(manifest["E"]) == side / 2 - low,
        f"node {index}: the centre domain is not the per-bin domain",
    )
    lines = input_text.decode().splitlines()
    cosine, sine = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
    for position, exact in enumerate((side, core, side / 2 - low, cosine, sine, Fraction(1))):
        low_end, high_end = enclosure(lines[position])
        require(low_end <= exact <= high_end, f"node {index}: input line {position + 1}")
    require(
        int(lines[6]) == 8 * len(candidate["rectangles"]),
        f"node {index}: the input lists {lines[6]} rectangles",
    )
    rectangle_block(candidate, lines[7:])


def cpp_sample(
    key: str, tarball: Path, work: Path, nodes: list[int], workers: int
) -> dict[str, Any]:
    """The source's own C++ checker at chosen oblique nodes of a check2 certificate.

    A check2 directory ships no C++ records: the source checked it with its adaptation of
    this repository's sqverify_fast. The checker its earlier certificates ship,
    ``mixed_rotated_verify.cpp`` (`CHECKER_SHA256`), shares no code with that crate. The
    pinned tarball is unpacked and bound first (`bundle_check2`). Then the retained
    ``mixed_n50_L740`` code is copied to ``work``, every file held to its retained bytes,
    with the retained candidate; the source's own net and symmetry checks run on it
    (``candidate_net``, ``symmetry``); the source's ``compile_verifier`` builds the checker;
    and the source's ``run`` checks each node at threshold one, with a budget of
    `CPP_NODE_LIMIT` nodes. Each node's record is held to lemma N0's tangent and per-bin
    domain and its input to the expanded candidate (`check_node_manifest`). A node passes
    when the checker returns ``ANGLE_VERIFIED`` with no frontier and no witness and a
    lower bound of at least one. It decides only the nodes it ran.
    """
    stated = CERTIFICATES[key]
    require(stated.check2, f"{key} ships the source's C++ records: use sample")
    require(all(index >= 1 for index in nodes), "the axis node is not an input of run")
    root, pin = unpack(stated, tarball, work / "bundle")
    binding = bundle(root, key=key)
    code = source_code_copy(work)
    raw = read_retained_bytes(stated.directory / "candidate.json")
    candidate_path = work / "candidate.json"
    candidate_path.write_bytes(raw)
    candidate = load_json(raw)
    for name in SOURCE_MODULES:
        sys.modules.pop(name, None)
    if str(code) in sys.path:
        sys.path.remove(str(code))
    sys.path.insert(0, str(code))
    density = importlib.import_module("mixed_density_check")
    net_audit = importlib.import_module("mixed_net_audit")
    rotated = importlib.import_module("mixed_rotated_verify")
    require(Path(rotated.SOURCE).resolve().parent == code.resolve(), "another checker")
    data = json.loads(raw)
    model = density.expand(data)
    net_audit.symmetry(model)
    step, last = net_audit.candidate_net(data)
    require(
        (Fraction(step), last + 1) == declared_net(candidate)[:2] and max(nodes) <= last,
        "the source's net is not the declared net, or a node lies outside it",
    )
    require(model[-1] == semantic_digest(candidate), "the source's digest is another")
    binary = work / "verify"
    started = utc_now()
    rotated.compile_verifier(binary)
    runs = work / "runs"
    if runs.exists():
        shutil.rmtree(runs)
    runs.mkdir()
    jobs = [
        (
            str(code),
            str(candidate_path),
            index,
            str(runs / f"net{index:04d}"),
            str(binary),
            CPP_NODE_LIMIT,
        )
        for index in nodes
    ]
    logged = {
        record["r"]: record for record in read_jsonl_gz(root / "check2/run.jsonl.gz")[:-1]
    }
    rows: list[dict[str, Any]] = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for index, report in zip(nodes, pool.map(_cpp_node, jobs), strict=True):
            folder = runs / f"net{index:04d}"
            check_node_manifest(
                report.pop("manifest"), candidate, index, (folder / "input.txt").read_bytes()
            )
            verified = (
                report["status"] == "ANGLE_VERIFIED"
                and report["frontier_boxes"] == 0
                and report["exact_witnesses"] == 0
                and float(report["lower"]) >= 1
            )
            rows.append(
                {"index": index, "verified": verified}
                | report
                | {
                    "check2_lower": logged[index]["min_certified_lower_bound"],
                    "check2_nodes": logged[index]["nodes"],
                    "check2_seconds": logged[index]["seconds"],
                }
            )
    return {
        "kind": "wand125-declared-net-cpp-sample/v1",
        "certificate": stated.name,
        "status": "SAMPLE_VERIFIED" if all(row["verified"] for row in rows) else "NOT_VERIFIED",
        "nodes": nodes,
        "workers": workers,
        "node_limit": CPP_NODE_LIMIT,
        "threshold": "1",
        "started": started,
        "ended": utc_now(),
        "rows": rows,
        "sample_cpu_seconds": round(sum(row["cpu_seconds"] for row in rows), 1),
        "candidate_digest": model[-1],
        "checker_sha256": CHECKER_SHA256,
        "tarball": pin,
        "binding": {field: binding[field] for field in ("status", "listed_files")},
        "environment": {
            "python": platform.python_version(),
            "cxx": compiler_version(),
            "niceness": os.nice(0),
        },
        "loadavg_end": list(os.getloadavg()),
        "scope": (
            "The source's C++ checker, mixed_rotated_verify.cpp 89b674a6..., run fresh by"
            " the source's own driver functions from the retained mixed_n50_L740 code at the"
            " listed oblique nodes of the declared net, at threshold one. It shares no code"
            " with sqverify_fast. Not a complete check: it decides the listed nodes only."
        ),
    }


#: Where the census keeps each certificate's per-direction receipts, by packet.
CENSUS = PROJECT / "benchmarks/measure-verifier/census-mixed"


def compare_census(key: str, tarball: Path, work: Path) -> dict[str, Any]:
    """This repository's sqverify-fast census row against the source's check2 run log.

    The pinned tarball is unpacked and bound first (`bundle_check2`). Then, direction by
    direction, the census row's receipts (``census-mixed/<packet>/<name>.jsonl.gz``) are
    set beside the source's ``check2/run.jsonl.gz``: both must hold one record per net
    node, every one verified. It counts the directions whose node counts and certified
    lower bounds are identical between the two runs, and the largest difference where
    not. Agreement here is not a second implementation: the source's verifier is a copy
    of this repository's crate. Identical counts at every direction say the two ran the
    same algorithm on the same input; differences say where the two builds' code or
    inputs differ. It decides nothing beyond the census row.
    """
    stated = CERTIFICATES[key]
    require(stated.check2, f"{key} ships no check2 run log")
    root, pin = unpack(stated, tarball, work / "bundle")
    binding = bundle(root, key=key)
    count = int(binding["run_log"]["directions"])
    ours_path = CENSUS / stated.packet.name / f"{stated.name}.jsonl.gz"
    ours_rows = read_jsonl_gz(ours_path)
    ours = {row["r"]: row for row in ours_rows if "r" in row}
    theirs = {row["r"]: row for row in read_jsonl_gz(root / "check2/run.jsonl.gz")[:-1]}
    require(
        sorted(ours) == sorted(theirs) == list(range(count)),
        "the two runs do not each hold one record per net node",
    )
    require(
        all(ours[r]["verdict"] == theirs[r]["verdict"] == "verified" for r in ours),
        "a direction is not verified by both runs",
    )
    same_nodes = [r for r in range(1, count) if ours[r]["nodes"] == theirs[r]["nodes"]]
    same_bound = [
        r
        for r in range(count)
        if ours[r]["min_certified_lower_bound"] == theirs[r]["min_certified_lower_bound"]
    ]
    gaps = [
        abs(ours[r]["min_certified_lower_bound"] - theirs[r]["min_certified_lower_bound"])
        for r in range(count)
    ]
    least = {
        name: min(
            (r for r in range(1, count)),
            key=lambda r, rows=rows: (rows[r]["min_certified_lower_bound"], r),
        )
        for name, rows in (("census", ours), ("source", theirs))
    }
    return {
        "kind": "wand125-declared-net-census-comparison/v1",
        "certificate": stated.name,
        "status": "BOTH_VERIFY_EVERY_DIRECTION",
        "directions": count,
        "identical_node_counts": len(same_nodes),
        "identical_lower_bounds": len(same_bound),
        "largest_lower_bound_difference": max(gaps),
        "oblique_nodes": {
            "census": sum(ours[r]["nodes"] for r in range(1, count)),
            "source": sum(theirs[r]["nodes"] for r in range(1, count)),
        },
        "least_oblique": {
            name: {
                "r": r,
                "lower": (ours if name == "census" else theirs)[r]["min_certified_lower_bound"],
            }
            for name, r in least.items()
        },
        "census_receipts": ours_path.relative_to(PROJECT).as_posix(),
        "census_receipts_sha256": file_sha256(ours_path),
        "tarball": pin,
        "scope": (
            "This repository's sqverify-fast census row beside the source's run of its copy"
            " of the same crate, direction by direction. Agreement shows the two builds ran"
            " alike; it is not a second implementation, and it decides nothing beyond the"
            " census row."
        ),
    }


def write_or_check(path: Path, value: dict[str, Any], *, check: bool) -> int:
    text = retained_json.dumps(value)
    if check:
        if not path.is_file() or path.read_text(encoding="utf-8") != text:
            print(f"{path} differs from a fresh run")
            return 1
        print("RECEIPT_MATCHES")
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


def parse_nodes(text: str) -> list[int]:
    """``1,37,100-102`` as a sorted list of node indices."""
    nodes: set[int] = set()
    for part in text.split(","):
        first, _, last = part.partition("-")
        nodes.update(range(int(first), int(last or first) + 1))
    return sorted(nodes)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    audit_parser = commands.add_parser("audit", help="exact premises from the packet")
    audit_parser.add_argument("--check", action="store_true")
    bundle_parser = commands.add_parser("bundle", help="bind an unpacked bundle")
    source = bundle_parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--bundle", type=Path, help="an unpacked bundle")
    source.add_argument("--tarball", type=Path, help="the pinned tarball, unpacked afresh")
    bundle_parser.add_argument("--work", type=Path, help="where --tarball is unpacked")
    compare_parser = commands.add_parser("compare", help="compare a replay with the shipped")
    compare_parser.add_argument("--shipped", type=Path, required=True)
    compare_parser.add_argument("--fresh", type=Path, required=True)
    compare_parser.add_argument(
        "--meta", type=Path, required=True, help="the run's own record: start, exit, end"
    )
    sample_parser = commands.add_parser("sample", help="replay chosen nodes, and price")
    sample_parser.add_argument("--nodes", type=parse_nodes, required=True, help="1,37,100-102")
    cpp_parser = commands.add_parser(
        "cpp-sample", help="the source's C++ checker at chosen nodes of a check2 certificate"
    )
    cpp_parser.add_argument("--nodes", type=parse_nodes, required=True, help="1,37,100-102")
    replay_parser = commands.add_parser("replay", help="the bundle's driver over every node")
    control_parser = commands.add_parser("control", help="the original and its mutants")
    control_parser.add_argument("--index", type=int, help="the oblique node; least by default")
    control_parser.add_argument(
        "--sqverify-fast", type=Path, help="a binary to run the corrupted nets through too"
    )
    processes_parser = commands.add_parser(
        "processes", help="snapshot a running replay's driver and workers"
    )
    processes_parser.add_argument("--pid", type=int, required=True, help="the driver's pid")
    census_parser = commands.add_parser(
        "compare-census", help="the census row beside the source's check2 run log"
    )
    fast_parser = commands.add_parser(
        "control-sqverify-fast", help="sqverify-fast on the control receipt's variants"
    )
    fast_parser.add_argument("--sqverify-fast", type=Path, required=True)
    fast_parser.add_argument("--work", type=Path, required=True)
    for running in (sample_parser, cpp_parser, replay_parser, control_parser, census_parser):
        running.add_argument("--tarball", type=Path, required=True)
        running.add_argument("--work", type=Path, required=True)
    for running in (sample_parser, cpp_parser, replay_parser):
        running.add_argument("--workers", type=int, default=1)
    for each in (
        audit_parser,
        bundle_parser,
        compare_parser,
        sample_parser,
        cpp_parser,
        census_parser,
        replay_parser,
        control_parser,
        fast_parser,
        processes_parser,
    ):
        each.add_argument("--certificate", choices=sorted(CERTIFICATES), default=DEFAULT)
        each.add_argument("--out", type=Path, help="the receipt; the packet's by default")
    args = parser.parse_args(argv)
    try:
        return run_command(args)
    except AuditError as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 1


#: The status each running command's receipt reports when it passes.
PASSING = {
    "sample": "SAMPLE_REPLAYED",
    "cpp-sample": "SAMPLE_VERIFIED",
    "compare-census": "BOTH_VERIFY_EVERY_DIRECTION",
    "control": "CONTROLS_REFUSED",
    "control-sqverify-fast": "CONTROLS_REFUSED",
    "replay": "FULL_REPLAY_MATCHES_SHIPPED",
    "compare": "FULL_REPLAY_MATCHES_SHIPPED",
}


def run_command(args: argparse.Namespace) -> int:
    """Run one parsed command and write its receipt: 0 when it passes."""
    key = args.certificate
    receipts = CERTIFICATES[key].receipts
    if args.command == "audit":
        out = args.out or receipts / "audit.json"
        return write_or_check(out, audit(key=key), check=args.check)
    if args.command == "bundle":
        out = args.out or receipts / "bundle.json"
        if args.tarball is None:
            return write_or_check(out, bundle(args.bundle, key=key), check=False)
        require(args.work is not None, "--tarball needs --work")
        root, pin = unpack(CERTIFICATES[key], args.tarball, args.work / "bundle")
        return write_or_check(out, bundle(root, key=key) | {"tarball": pin}, check=False)
    if args.command == "processes":
        out = args.out or receipts / "full" / PROCESSES
        return write_or_check(out, processes(args.pid), check=False)
    if args.command == "sample":
        result = sample(key, args.tarball, args.work, args.nodes, args.workers)
        first, last = args.nodes[0], args.nodes[-1]
        out = args.out or receipts / f"sample/nodes-{first:03d}-{last:03d}.json"
    elif args.command == "cpp-sample":
        result = cpp_sample(key, args.tarball, args.work, args.nodes, args.workers)
        first, last = args.nodes[0], args.nodes[-1]
        out = args.out or receipts / f"cpp-sample/nodes-{first:04d}-{last:04d}.json"
    elif args.command == "compare-census":
        result = compare_census(key, args.tarball, args.work)
        out = args.out or receipts / "compare-census.json"
    elif args.command == "control":
        result = control(key, args.tarball, args.work, args.index, args.sqverify_fast)
        out = args.out or receipts / "control.json"
    elif args.command == "control-sqverify-fast":
        result = control_sqverify_fast(key, args.sqverify_fast, args.work)
        out = args.out or receipts / "control-sqverify-fast.json"
    elif args.command == "replay":
        full = args.out or receipts / "full"
        result = replay(key, args.tarball, args.work, args.workers, full)
        out = full / "compare.json"
    else:
        result = compare(args.shipped, args.fresh, args.meta, key=key)
        out = args.out or receipts / "full/compare.json"
    write_or_check(out, result, check=False)
    return 0 if result["status"] == PASSING[args.command] else 1


if __name__ == "__main__":
    sys.exit(main())
