"""Controls for the mixed rectangle-measure certificates of wand125/square-packing-bounds.

`devtools.audit_wand125_point_and_mixed` audits and replays 65 of them: n = 50
(T-048), the five of jlevy/squares#282 (T-069), the two of its comment of 2 October, the
n = 76 of its later comment that day, the six of that afternoon pinned at ``b00fc70``,
two of which supersede certificates at n = 85 and 92 and are named ``n85-L946`` and
``n92-L975``, the 22 of 3 October pinned at ``2aff207``, five of them at counts already
named, the 16 posted from 3 October 19:33 UTC to 4 October 07:17 UTC pinned at
``8aa6a10``, nine of them at counts already named, and the 12 posted from 4 October
07:51 to 19:04 UTC pinned at ``797bdf6``, ten of them at counts already named. The last
28 carry no source audit, so each is bound to its tarball by the digest at the pin, and
an earlier certificate is refused without its audit. Three families of check stand
between a certificate and a recorded replay, and each is held here to its positive case
and to two or more mutated controls that it must refuse:

- **the retained files**: the exact premises the source's statements rest on, from the
  packet's bytes alone;
- **the tarball and its bundle**: the pinned digest before use, whichever route delivered
  the file or whoever supplied it, a safe unpacking, and the bundle's binding to the
  packet before any of its code is imported;
- **the replay receipts**: the per-range records a split replay writes, their merge, and
  the audit's reading of whatever receipts a packet holds.

The range driver is held to its promises with a stand-in for the shipped per-angle
function: each angle recorded as it finishes, an interrupted range resumed where it
stopped, a deadline honoured, a torn last line cut, a finished range not fetched again.
The price is held to its samples. No checker is run here. Coverage is the source
checker's, replayed by `mixed-replay`.
"""

from __future__ import annotations

import concurrent.futures
import dataclasses
import hashlib
import io
import itertools
import json
import shutil
import tarfile
import urllib.error
from email.message import Message
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import acquire_source
from devtools import audit_wand125_point_and_mixed as audit
from devtools.retained_data import read_retained_bytes

G_PACKET = audit.G_PACKET
H_PACKET = audit.H_PACKET
I_PACKET = audit.I_PACKET
J_PACKET = audit.J_PACKET
K_PACKET = audit.K_PACKET
K_NAMES = sorted(name for name, c in audit.MIXED.items() if c.packet == K_PACKET)
L_PACKET = audit.L_PACKET
L_NAMES = sorted(name for name, c in audit.MIXED.items() if c.packet == L_PACKET)
M_PACKET = audit.M_PACKET
M_NAMES = sorted(name for name, c in audit.MIXED.items() if c.packet == M_PACKET)
N_PACKET = audit.N_PACKET
N_NAMES = sorted(name for name, c in audit.MIXED.items() if c.packet == N_PACKET)
UNAUDITED = K_NAMES + L_NAMES + M_NAMES + N_NAMES
NAMES = sorted(audit.MIXED, key=lambda name: (audit.MIXED[name].n, audit.MIXED[name].side))


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _repinned(certificate: audit.MixedCertificate, files: dict[str, bytes]) -> dict[Path, str]:
    """The packet's digest list with these files' digests in place of the pinned ones.

    A control built this way passes the pin check, so what refuses it is the content.
    """
    tree = dict(audit.read_subtree_manifest(certificate.subtree))
    for name, data in files.items():
        tree[certificate.directory / name] = _sha256(data)
    return tree


# --------------------------------------------------------------------------- retained files


@pytest.fixture(scope="module")
def audits() -> dict[str, dict[str, Any]]:
    return {name: audit.mixed_certificate(audit.MIXED[name]) for name in NAMES}


@pytest.mark.parametrize("name", NAMES)
def test_each_certificate_has_its_stated_exact_premises(
    audits: dict[str, dict[str, Any]], name: str
) -> None:
    certificate = audit.MIXED[name]
    facts = audits[name]
    assert facts["rectangles"] == certificate.rectangles
    assert Fraction(facts["total_mass"]) == certificate.n - Fraction(1, 100000)
    assert facts["candidate_digest"] == certificate.candidate_digest
    assert facts["checker_sha256"] == audit.N50_CHECKER_SHA256
    assert facts["code_identical_to_n50"]
    assert facts["least_lower"] >= 1
    assert facts["axis_integer_minimum"] >= 1
    assert facts["comparison"]["side_exceeds_green"]


def test_the_least_bounds_are_the_ones_the_sources_state(
    audits: dict[str, dict[str, Any]],
) -> None:
    least = {
        name: (facts["least_lower"], facts["least_lower_at"]) for name, facts in audits.items()
    }
    assert least["n50"] == (1.0000000004625813, 150)
    assert least["n84"] == (1.0000000008975796, 175)
    assert least["n85"] == (1.0000000017271347, 44)
    assert least["n90"] == (1.000000000041986, 122)
    assert least["n76"] == (1.000000000516032, 150)
    assert least["n83"] == (1.0000000002030356, 165)
    assert least["n85-L946"] == (1.0000000021147502, 182)
    assert least["n87"] == (1.0000000089739896, 176)
    assert least["n91"] == (1.0000000003906073, 191)
    assert least["n92-L975"] == (1.0000000022907243, 191)
    assert least["n96"] == (1.0000000030392873, 122)


def test_n50_agrees_with_its_own_exact_audit(audits: dict[str, dict[str, Any]]) -> None:
    earlier = audit.n50_certificate("L740")
    facts = audits["n50"]
    assert facts["side"] == earlier["side"]
    assert facts["candidate_digest"] == earlier["candidate_digest"]
    assert facts["least_lower"] == earlier["recorded_minimum_lower"]
    assert facts["centre_domains"] == earlier["centre_domains"]


def test_the_g_comparison_value_is_below_greens_bound(
    audits: dict[str, dict[str, Any]],
) -> None:
    """The n = 84 and 85 audits compare with 92667/10000, which is below Green's value."""
    for name in ("n84", "n85"):
        comparison = audits[name]["comparison"]
        assert audits[name]["source_audit"]["compared_with"] == "92667/10000"
        assert comparison["green"] == "Theorem 9, k=9, from n = 82"
        assert not comparison["source_value_exceeds_green"]
        assert comparison["side_exceeds_green"]


def test_the_g_packet_matches_its_acquisition_contract() -> None:
    assert acquire_source.check(G_PACKET, acquire_source.REPO) == []


@pytest.mark.parametrize(
    "packet",
    [G_PACKET, H_PACKET, I_PACKET, J_PACKET, K_PACKET, L_PACKET, M_PACKET, N_PACKET],
    ids=["g", "h", "i", "j", "k", "l", "m", "n"],
)
def test_each_october_packet_audit_recomputes_to_its_receipt(packet: Path) -> None:
    receipt = packet / "receipts/mixed-audit.json"
    expected = json.dumps(audit.mixed_audit(packet), indent=2, default=str) + "\n"
    assert receipt.read_text(encoding="utf-8") == expected


def test_the_h_packet_matches_its_acquisition_contract() -> None:
    assert acquire_source.check(H_PACKET, acquire_source.REPO) == []


def test_the_h_comparison_is_the_sources_own_rectangle_value(
    audits: dict[str, dict[str, Any]],
) -> None:
    """n = 76 compares with the source's 357/40 rectangle certificate, below 447/50."""
    facts = audits["n76"]
    assert facts["source_audit"]["compared_with"] == "357/40"
    assert Fraction(facts["source_audit"]["improvement_lower"]) == Fraction(3, 200)
    assert facts["comparison"]["side_exceeds_nagamochi"]


def test_the_i_packet_matches_its_acquisition_contract() -> None:
    assert acquire_source.check(I_PACKET, acquire_source.REPO) == []


def test_the_j_packet_matches_its_acquisition_contract() -> None:
    assert acquire_source.check(J_PACKET, acquire_source.REPO) == []


def test_the_3_october_certificates_take_their_sides_where_a_count_is_named() -> None:
    later = {name: c for name, c in audit.MIXED.items() if c.packet == J_PACKET}
    assert len(later) == 22
    assert {name for name in later if "-L" in name} == {
        "n76-L896",
        "n87-L955",
        "n90-L9725",
        "n91-L975",
        "n92-L977",
        "n96-L997",
    }
    assert audit.MIXED["n90-L9725"].tarball == "n90-L9.725-proof-bundle.tar.gz"
    assert audit.MIXED["n86"].directory.name == "mixed_n86_L950"
    assert {c.revision for c in later.values()} == {audit.J_REVISION}


def test_the_j_comparisons_are_exact_rationals_below_each_side(
    audits: dict[str, dict[str, Any]],
) -> None:
    """None of the 22 compares with a rounded Green value: each compares with a rational,
    exceeds Green's and Nagamochi's values, and states L minus that rational."""
    for name, certificate in audit.MIXED.items():
        if certificate.packet != J_PACKET:
            continue
        facts = audits[name]
        assert facts["source_audit"]["compared_field"] == "compared_with"
        assert Fraction(facts["source_audit"]["compared_with"]) != Fraction(92667, 10000)
        assert facts["comparison"]["side_exceeds_green"]
        assert facts["comparison"]["side_exceeds_nagamochi"]


def test_a_later_certificate_at_a_named_count_takes_its_side_as_well() -> None:
    """The afternoon's n = 85 and 92 supersede certificates the table already names."""
    later = {name: c for name, c in audit.MIXED.items() if c.packet == I_PACKET}
    assert set(later) == {"n83", "n85-L946", "n87", "n91", "n92-L975", "n96"}
    assert audit.MIXED["n85"].directory.name == "mixed_n85_L942"
    assert audit.MIXED["n85-L946"].directory.name == "mixed_n85_L946"
    assert audit.MIXED["n92-L975"].receipts == I_PACKET / "receipts/n92-L975"
    assert {c.revision for c in later.values()} == {audit.I_REVISION}
    assert len({c.tarball for c in audit.MIXED.values()}) == len(audit.MIXED)


def test_the_i_comparisons_are_greens_rounded_value_or_the_sources_own(
    audits: dict[str, dict[str, Any]],
) -> None:
    """n = 83, 85 and 87 compare with 92667/10000, below Green's value; the other three
    with the source's own earlier certificate, which the side exceeds."""
    for name in ("n83", "n85-L946", "n87"):
        assert audits[name]["source_audit"]["compared_with"] == "92667/10000"
        assert not audits[name]["comparison"]["source_value_exceeds_green"]
    earlier = {"n91": "1929/200", "n92-L975": "969/100", "n96": "248/25"}
    for name, value in earlier.items():
        facts = audits[name]
        assert facts["source_audit"]["compared_with"] == value
        assert Fraction(facts["side"]) - Fraction(value) == Fraction(
            facts["source_audit"]["improvement_lower"]
        )
        assert facts["comparison"]["side_exceeds_nagamochi"]


@pytest.mark.parametrize("name", ["n83", "n85-L946", "n87", "n91", "n92-L975", "n96"])
def test_each_i_pre_replay_receipt_is_bound_to_the_pin(name: str) -> None:
    """``mixed-fetch`` on each pinned tarball: the pin, the bundle and all 200 inputs."""
    certificate = audit.MIXED[name]
    record = json.loads((certificate.receipts / "fetch.json").read_text())
    digest, size = audit.tarball_pin(certificate)
    assert record["status"] == "BUNDLE_READY"
    assert record["certificate"] == name
    assert (record["tarball"]["sha256"], record["tarball"]["bytes"]) == (digest, size)
    assert record["tarball"]["revision"] == audit.I_REVISION
    assert record["bindings"] == {
        "status": "BUNDLE_BOUND_TO_PACKET",
        "listed_files": 621,
        "code_files": 10,
    }
    assert record["preconditions"]["candidate_digest"] == certificate.candidate_digest
    assert record["preconditions"]["checker_sha256"] == audit.N50_CHECKER_SHA256
    assert record["inputs"]["status"] == "ALL_INPUTS_ENCLOSE_THE_CANDIDATE"
    assert record["inputs"]["inputs"] == 200
    assert record["inputs"]["rectangle_images"] == 8 * certificate.rectangles
    assert record["bundle_records"]["frontier_boxes"] == 0


def _with_heavier_rectangle(data: bytes) -> bytes:
    candidate = json.loads(data)
    rectangle = candidate["rectangles"][0]
    rectangle["mass"] = str(Fraction(rectangle["mass"]) + Fraction(1, 10**9))
    return json.dumps(candidate).encode()


def test_a_heavier_rectangle_is_refused_even_when_repinned() -> None:
    certificate = audit.MIXED["n84"]
    files = audit.mixed_retained(certificate)
    files["candidate.json"] = _with_heavier_rectangle(files["candidate.json"])
    with pytest.raises(ValueError, match="total mass differs"):
        audit.mixed_certificate(certificate, files, _repinned(certificate, files))
    with pytest.raises(ValueError, match="not the pinned file"):
        audit.mixed_certificate(certificate, files)


def test_a_changed_angle_record_is_refused_by_the_source_audit() -> None:
    certificate = audit.MIXED["n85"]
    files = audit.mixed_retained(certificate)
    replay = json.loads(files["certificate.json"])
    replay["results"]["44"]["nodes"] += 1
    files["certificate.json"] = json.dumps(replay).encode()
    with pytest.raises(ValueError, match="binds another certificate"):
        audit.mixed_certificate(certificate, files, _repinned(certificate, files))


def test_an_angle_below_one_is_refused_even_with_a_matching_audit() -> None:
    """A forged certificate whose source audit is re-bound to it still fails at the angle."""
    certificate = audit.MIXED["n85"]
    files = audit.mixed_retained(certificate)
    replay = json.loads(files["certificate.json"])
    replay["results"]["44"]["lower"] = 0.9999999999
    files["certificate.json"] = json.dumps(replay).encode()
    source_audit = json.loads(files["completion-audit.json"])
    source_audit["certificate_sha256"] = _sha256(files["certificate.json"])
    files["completion-audit.json"] = json.dumps(source_audit).encode()
    with pytest.raises(ValueError, match="angle 44 is not a replayed record"):
        audit.mixed_certificate(certificate, files, _repinned(certificate, files))


def test_an_audit_naming_another_tarball_is_refused() -> None:
    certificate = audit.MIXED["n37"]
    files = audit.mixed_retained(certificate)
    source_audit = json.loads(files["completion-audit.json"])
    source_audit["archive_sha256"] = "0" * 64
    files["completion-audit.json"] = json.dumps(source_audit).encode()
    with pytest.raises(ValueError, match="binds another tarball"):
        audit.mixed_certificate(certificate, files, _repinned(certificate, files))


# ------------------------------------------------------------- certificates without an audit


def test_the_k_packet_matches_its_acquisition_contract() -> None:
    assert acquire_source.check(K_PACKET, acquire_source.REPO) == []


def test_the_4_october_certificates_take_their_sides_where_a_count_is_named() -> None:
    later = {name: audit.MIXED[name] for name in K_NAMES}
    assert len(later) == 16
    assert {name for name in later if "-L" in name} == {
        "n51-L747",
        "n69-L862",
        "n75-L894",
        "n84-L94075",
        "n86-L9503",
        "n88-L96125",
        "n93-L988",
        "n94-L994",
        "n95-L9965",
    }
    assert audit.MIXED["n95-L9965"].tarball == "n95-L9.965-proof-bundle.tar.gz"
    assert audit.MIXED["n42"].directory.name == "mixed_n42_L68475"
    assert {c.revision for c in later.values()} == {audit.K_REVISION}
    assert not any(c.source_audit for c in later.values())
    assert all(
        c.source_audit
        for c in audit.MIXED.values()
        if c.packet not in {K_PACKET, L_PACKET, M_PACKET, N_PACKET}
    )


def test_the_l_packet_matches_its_acquisition_contract() -> None:
    assert acquire_source.check(L_PACKET, acquire_source.REPO) == []


def test_the_evening_certificates_take_their_sides_where_a_count_is_named() -> None:
    later = {name: audit.MIXED[name] for name in L_NAMES}
    assert len(later) == 12
    assert {name for name in later if "-L" in name} == {
        "n58-L7935",
        "n70-L86575",
        "n71-L8721",
        "n73-L8813",
        "n76-L8965",
        "n87-L958",
        "n88-L962",
        "n90-L973",
        "n91-L97625",
        "n94-L995",
    }
    assert audit.MIXED["n94-L995"].tarball == "n94-L9.95-proof-bundle.tar.gz"
    assert audit.MIXED["n53"].directory.name == "mixed_n53_L76275"
    assert {c.revision for c in later.values()} == {audit.L_REVISION}
    assert not any(c.source_audit for c in later.values())


def test_the_m_packet_matches_its_acquisition_contract() -> None:
    assert acquire_source.check(M_PACKET, acquire_source.REPO) == []


def test_the_5_october_certificates_take_their_sides_at_named_counts() -> None:
    """Both raise a 4 October certificate at its count, so each is named by its side."""
    later = {name: audit.MIXED[name] for name in M_NAMES}
    assert set(later) == {"n67-L848", "n84-L9411"}
    assert audit.MIXED["n67"].packet == audit.MIXED["n84-L94075"].packet == K_PACKET
    assert audit.MIXED["n84-L9411"].tarball == "n84-L9.411-proof-bundle.tar.gz"
    assert audit.MIXED["n67-L848"].directory.name == "mixed_n67_L848"
    assert {c.revision for c in later.values()} == {audit.M_REVISION}
    assert not any(c.source_audit for c in later.values())


def test_the_n_packet_matches_its_acquisition_contract() -> None:
    assert acquire_source.check(N_PACKET, acquire_source.REPO) == []


def test_the_43050ed_pin_audits_n66_and_leaves_the_declared_net_to_sqverify_fast() -> None:
    """``d73ce20``'s n = 66 raises T-069's ``mixed_n66_L842``, so it is named by its side.
    The pin's other directory, ``mixed_n18_L470``, is on a net of its own (step 1/1001,
    416 directions) at core 999/1000, which this tool's fixed net and core cannot audit;
    no row names it."""
    assert N_NAMES == ["n66-L843"]
    certificate = audit.MIXED["n66-L843"]
    assert audit.MIXED["n66"].packet == audit.F_PACKET
    assert certificate.tarball == "n66-L8.43-proof-bundle.tar.gz"
    assert certificate.directory.name == "mixed_n66_L843"
    assert certificate.revision == audit.N_REVISION
    assert not certificate.source_audit
    assert not any(c.directory.name == "mixed_n18_L470" for c in audit.MIXED.values())
    retained = N_PACKET / "square-packing-bounds/certificates/mixed_n18_L470"
    candidate = json.loads(read_retained_bytes(retained / "candidate.json"))
    assert candidate["proof_net"] == {"step": "1/1001", "last": 415}
    assert (candidate["B"], candidate["total_mass"]) == ("0.999", "1799999/100000")
    assert Fraction(candidate["B"]) != audit.MIXED_CORE


@pytest.mark.parametrize("name", ["n69-L862", "n86-L9503"])
def test_the_evening_pin_holds_two_k_certificates_unchanged(name: str) -> None:
    """The evening packet pins two certificates the 4 October packet retains: every file of
    each directory, its tarball included, has the digest that packet pins, and no row of
    the audit names them twice."""
    certificate = audit.MIXED[name]
    assert certificate.packet == K_PACKET
    earlier = audit.read_subtree_manifest(K_PACKET / "acquisition/upstream-subtree.sha256")
    evening = audit.read_subtree_manifest(L_PACKET / "acquisition/upstream-subtree.sha256")
    inside = {path for path in evening if certificate.directory in path.parents}
    assert inside == {path for path in earlier if certificate.directory in path.parents}
    assert len(inside) == 16
    assert all(evening[path] == earlier[path] for path in inside)
    assert evening[certificate.upstream_tarball] == audit.tarball_pin(certificate)[0]
    assert [c.directory for c in audit.MIXED.values()].count(certificate.directory) == 1


@pytest.mark.parametrize("name", UNAUDITED)
def test_each_k_certificate_is_bound_by_its_digest_at_the_pin(
    audits: dict[str, dict[str, Any]], name: str
) -> None:
    """No source audit: the pinned tree holds none, and the tarball's digest at the pin is
    the acquisition record's, with its size, and the one the README states."""
    certificate = audit.MIXED[name]
    facts = audits[name]
    tree = audit.read_subtree_manifest(certificate.subtree)
    digest, size = audit.tarball_pin(certificate)
    assert certificate.directory / audit.SOURCE_AUDIT not in tree
    assert audit.SOURCE_AUDIT not in audit.mixed_retained(certificate)
    assert facts["source_audit"] is None
    assert facts["tarball_sha256"] == digest == tree[certificate.upstream_tarball]
    binding = facts["tarball_binding"]
    assert binding["status"] == "BOUND_BY_PINNED_DIGEST"
    assert (binding["revision"], binding["tarball_bytes"]) == (certificate.revision, size)
    side = certificate.side
    assert binding["readme_claim"].startswith(
        f"s({certificate.n}) >= {side.numerator}/{side.denominator} = "
    )
    assert facts["comparison"]["source_value_exceeds_green"] is None
    assert facts["comparison"]["side_exceeds_nagamochi"]


@pytest.mark.parametrize("name", UNAUDITED)
def test_each_k_pre_replay_receipt_is_bound_to_the_pin(name: str) -> None:
    """``mixed-fetch`` on each pinned tarball: the pin, the bundle and all 200 inputs."""
    certificate = audit.MIXED[name]
    record = json.loads((certificate.receipts / "fetch.json").read_text())
    digest, size = audit.tarball_pin(certificate)
    assert record["status"] == "BUNDLE_READY"
    assert record["certificate"] == name
    assert (record["tarball"]["sha256"], record["tarball"]["bytes"]) == (digest, size)
    assert record["tarball"]["revision"] == certificate.revision
    assert record["bindings"] == {
        "status": "BUNDLE_BOUND_TO_PACKET",
        "listed_files": 621,
        "code_files": 10,
    }
    assert record["preconditions"]["candidate_digest"] == certificate.candidate_digest
    assert record["preconditions"]["checker_sha256"] == audit.N50_CHECKER_SHA256
    assert record["inputs"]["status"] == "ALL_INPUTS_ENCLOSE_THE_CANDIDATE"
    assert record["inputs"]["inputs"] == 200
    assert record["inputs"]["rectangle_images"] == 8 * certificate.rectangles
    assert record["bundle_records"]["frontier_boxes"] == 0


@pytest.mark.parametrize("name", ["n42", "n53"])
def test_a_k_certificate_with_a_heavier_rectangle_is_refused_even_when_repinned(
    name: str,
) -> None:
    certificate = audit.MIXED[name]
    files = audit.mixed_retained(certificate)
    files["candidate.json"] = _with_heavier_rectangle(files["candidate.json"])
    with pytest.raises(ValueError, match="total mass differs"):
        audit.mixed_certificate(certificate, files, _repinned(certificate, files))
    with pytest.raises(ValueError, match="not the pinned file"):
        audit.mixed_certificate(certificate, files)


def test_a_k_certificate_with_an_angle_below_one_is_refused_even_when_repinned() -> None:
    """With no source audit to re-bind, a forged record still fails at its angle."""
    certificate = audit.MIXED["n95-L9965"]
    files = audit.mixed_retained(certificate)
    replay = json.loads(files["certificate.json"])
    replay["results"]["23"]["lower"] = 0.9999999999
    files["certificate.json"] = json.dumps(replay).encode()
    with pytest.raises(ValueError, match="angle 23 is not a replayed record"):
        audit.mixed_certificate(certificate, files, _repinned(certificate, files))


def test_a_k_readme_stating_another_tarball_is_refused_even_when_repinned() -> None:
    certificate = audit.MIXED["n84-L94075"]
    files = audit.mixed_retained(certificate)
    digest, _ = audit.tarball_pin(certificate)
    files["README.md"] = files["README.md"].replace(digest.encode(), b"0" * 64)
    with pytest.raises(ValueError, match="the README states another tarball"):
        audit.mixed_certificate(certificate, files, _repinned(certificate, files))


@pytest.mark.parametrize(
    ("name", "claim"), [("n88-L96125", b"769/80"), ("n88-L962", b"481/50")]
)
def test_a_k_readme_stating_another_claim_is_refused_even_when_repinned(
    name: str, claim: bytes
) -> None:
    certificate = audit.MIXED[name]
    files = audit.mixed_retained(certificate)
    files["README.md"] = files["README.md"].replace(b"# s(88) >= " + claim, b"# s(88) >= 77/8")
    assert files["README.md"] != audit.mixed_retained(certificate)["README.md"]
    with pytest.raises(ValueError, match="the README states another claim"):
        audit.mixed_certificate(certificate, files, _repinned(certificate, files))


def test_a_k_tree_pinning_another_tarball_is_refused() -> None:
    """The tarball's digest at the pin must be the one the acquisition record pins."""
    certificate = audit.MIXED["n57"]
    tree = dict(audit.read_subtree_manifest(certificate.subtree))
    tree[certificate.upstream_tarball] = "0" * 64
    with pytest.raises(ValueError, match="the acquisition record pins another tarball"):
        audit.mixed_certificate(certificate, tree=tree)


def test_a_k_tree_holding_a_source_audit_is_refused() -> None:
    """A row read without an audit is refused when its pinned tree holds one."""
    certificate = audit.MIXED["n43"]
    tree = dict(audit.read_subtree_manifest(certificate.subtree))
    tree[certificate.directory / audit.SOURCE_AUDIT] = "0" * 64
    with pytest.raises(ValueError, match=f"holds a {audit.SOURCE_AUDIT}"):
        audit.mixed_certificate(certificate, tree=tree)


@pytest.mark.parametrize("name", ["n37", "n96-L997"])
def test_an_earlier_certificate_without_its_source_audit_is_refused(name: str) -> None:
    """The pinned-digest path is chosen by the row's revision, never by a missing file."""
    certificate = audit.MIXED[name]
    files = audit.mixed_retained(certificate)
    del files[audit.SOURCE_AUDIT]
    tree = dict(audit.read_subtree_manifest(certificate.subtree))
    with pytest.raises(ValueError, match=f"{audit.SOURCE_AUDIT} is missing"):
        audit.mixed_certificate(certificate, files, tree)
    del tree[certificate.directory / audit.SOURCE_AUDIT]
    with pytest.raises(ValueError, match=f"{audit.SOURCE_AUDIT} is missing"):
        audit.mixed_certificate(certificate, files, tree)


def test_a_k_bundle_with_another_certificate_is_refused_even_when_listed(
    tmp_path: Path,
) -> None:
    real = audit.MIXED["n72"]
    files = _bundle_files(real)
    replay = json.loads(files["proof/certificate.json"])
    replay["results"]["138"]["nodes"] += 1
    files["proof/certificate.json"] = json.dumps(replay).encode()
    bundle = _write_bundle(tmp_path / real.bundle, _listed(files))
    with pytest.raises(ValueError, match=r"proof/certificate\.json is not the retained"):
        audit.bundle_bindings(real, bundle)


def test_a_k_bundle_with_another_candidate_is_refused_even_when_listed(tmp_path: Path) -> None:
    real = audit.MIXED["n67"]
    files = _bundle_files(real)
    files["proof/candidate.json"] = _with_heavier_rectangle(files["proof/candidate.json"])
    bundle = _write_bundle(tmp_path / real.bundle, _listed(files))
    with pytest.raises(ValueError, match=r"proof/candidate\.json is not the retained"):
        audit.bundle_bindings(real, bundle)


def _lines(path: Path) -> list[str]:
    return read_retained_bytes(path).decode().splitlines()


#: The directories 150939e changed, the 22 of T-082 and T-075's ``mixed_n96_L996``, with
#: the packet that retains each as it was before.
OC_ANSWER = {
    **{
        certificate.directory: J_PACKET
        for certificate in audit.MIXED.values()
        if certificate.packet == J_PACKET
    },
    Path("certificates/mixed_n96_L996"): I_PACKET,
}


def test_the_oc_answer_removes_only_the_source_audits_and_their_readme_lines() -> None:
    """Between 2aff207 (b00fc70 for mixed_n96_L996) and 8aa6a10 each of the 23 directories
    loses its completion-audit.json, and its README the two lines naming it; every other
    file, the candidate, certificate, manifest and tarball included, keeps its digest."""
    later = audit.read_subtree_manifest(K_PACKET / "acquisition/upstream-subtree.sha256")
    assert len(OC_ANSWER) == 23
    for directory, packet in OC_ANSWER.items():
        earlier = audit.read_subtree_manifest(packet / "acquisition/upstream-subtree.sha256")
        before = {p: d for p, d in earlier.items() if p.parent.is_relative_to(directory)}
        after = {p: d for p, d in later.items() if p.parent.is_relative_to(directory)}
        readme = directory / "README.md"
        assert set(before) - set(after) == {directory / audit.SOURCE_AUDIT}
        assert set(after) <= set(before)
        assert {p for p in after if after[p] != before[p]} == {readme}
        old = _lines(packet / "square-packing-bounds" / readme)
        new = _lines(K_PACKET / "square-packing-bounds" / readme)
        removed = [line for line in old if line not in new]
        assert [line for line in new if line not in old] == []
        assert len(removed) == 2
        assert "`completion-audit.json`" in removed[0]


# --------------------------------------------------------------------------- tarball, bundle


def _bundle_files(certificate: audit.MixedCertificate) -> dict[str, bytes]:
    """A bundle with the shape of the source's, from the retained bytes, without angles."""
    retained = audit.mixed_retained(certificate)
    files = {f"proof/{name}": retained[name] for name in audit.MIXED_FILES[:3]}
    for path in sorted(audit.MIXED_CODE.iterdir()):
        if path.is_file():
            files[f"code/{path.name}"] = path.read_bytes()
    files["proof/verify.cpp"] = files["code/mixed_rotated_verify.cpp"]
    files["requirements.txt"] = audit.MIXED_REQUIREMENTS.read_bytes()
    return files


def _listed(files: dict[str, bytes]) -> dict[str, bytes]:
    listing = {name: _sha256(data) for name, data in sorted(files.items())}
    return files | {"files-sha256.json": json.dumps(listing, indent=2).encode()}


def _write_bundle(root: Path, files: dict[str, bytes]) -> Path:
    for name, data in files.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return root


def _tarball(prefix: str, files: dict[str, bytes]) -> bytes:
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w:gz") as archive:
        for name, data in sorted(files.items()):
            member = tarfile.TarInfo(f"{prefix}/{name}")
            member.size = len(data)
            archive.addfile(member, io.BytesIO(data))
    return stream.getvalue()


def _pinned_to(tmp_path: Path, archive: bytes) -> audit.MixedCertificate:
    """n = 84 with a scratch packet whose acquisition files pin ``archive``."""
    real = audit.MIXED["n84"]
    packet = tmp_path / "packet"
    (packet / "acquisition").mkdir(parents=True)
    path = real.upstream_tarball.as_posix()
    digest = _sha256(archive)
    (packet / "acquisition/upstream-subtree.sha256").write_text(f"{digest}  ./{path}\n")
    entry = {"path": path, "bytes": len(archive), "sha256": digest}
    record = {"sources": [{"pinned_only": [entry]}]}
    (packet / "acquisition/sources.json").write_text(json.dumps(record))
    return dataclasses.replace(real, packet=packet)


def test_the_pinned_tarball_unpacks_into_a_bound_bundle(tmp_path: Path) -> None:
    real = audit.MIXED["n84"]
    archive = _tarball(real.bundle, _listed(_bundle_files(real)))
    certificate = _pinned_to(tmp_path, archive)
    supplied = tmp_path / "supplied.tar.gz"
    supplied.write_bytes(archive)
    fetched = audit.fetch_tarball(certificate, tmp_path / "work", supplied)
    assert fetched["status"] == "TARBALL_MATCHES_PIN"
    bundle = audit.unpack_bundle(certificate, tmp_path / "work" / real.tarball, tmp_path / "u")
    tree = audit.read_subtree_manifest(real.subtree)
    assert audit.bundle_bindings(real, bundle, tree)["status"] == "BUNDLE_BOUND_TO_PACKET"


@pytest.mark.parametrize("damage", ["flipped", "truncated"])
def test_a_tarball_that_is_not_the_pinned_bytes_is_refused(tmp_path: Path, damage: str) -> None:
    real = audit.MIXED["n84"]
    archive = _tarball(real.bundle, _listed(_bundle_files(real)))
    certificate = _pinned_to(tmp_path, archive)
    changed = bytearray(archive)
    if damage == "flipped":
        changed[len(changed) // 2] ^= 1
    else:
        del changed[-10:]
    supplied = tmp_path / "supplied.tar.gz"
    supplied.write_bytes(bytes(changed))
    with pytest.raises(ValueError, match="the pin is"):
        audit.fetch_tarball(certificate, tmp_path / "work", supplied)
    assert not (tmp_path / "work" / real.tarball).exists()
    assert (tmp_path / "work" / f"{real.tarball}.rejected").is_file()


def test_an_archive_member_outside_the_bundle_is_refused(tmp_path: Path) -> None:
    real = audit.MIXED["n84"]
    archive = tmp_path / "escape.tar.gz"
    archive.write_bytes(_tarball("elsewhere", {"README.md": b"not the bundle\n"}))
    with pytest.raises(ValueError, match="unexpected archive member"):
        audit.unpack_bundle(real, archive, tmp_path / "u")


def test_a_bundle_with_other_code_is_refused_even_when_listed(tmp_path: Path) -> None:
    real = audit.MIXED["n85"]
    files = _bundle_files(real)
    files["code/mixed_net_audit.py"] += b"\n# changed\n"
    bundle = _write_bundle(tmp_path / real.bundle, _listed(files))
    with pytest.raises(ValueError, match="code/ is not the retained"):
        audit.bundle_bindings(real, bundle)


def test_a_bundle_with_an_unlisted_file_is_refused(tmp_path: Path) -> None:
    real = audit.MIXED["n85"]
    bundle = _write_bundle(tmp_path / real.bundle, _listed(_bundle_files(real)))
    (bundle / "proof/extra.json").write_text("{}")
    with pytest.raises(ValueError, match="file list fails"):
        audit.bundle_bindings(real, bundle)


def test_a_bundle_with_another_candidate_is_refused_even_when_listed(tmp_path: Path) -> None:
    real = audit.MIXED["n85"]
    files = _bundle_files(real)
    files["proof/candidate.json"] = _with_heavier_rectangle(files["proof/candidate.json"])
    bundle = _write_bundle(tmp_path / real.bundle, _listed(files))
    with pytest.raises(ValueError, match=r"proof/candidate\.json is not the retained"):
        audit.bundle_bindings(real, bundle)


# --------------------------------------------------------------------------- replay receipts


def _run(certificate: audit.MixedCertificate, run: str, **changes: Any) -> dict[str, Any]:
    digest, _ = audit.tarball_pin(certificate)
    record: dict[str, Any] = {
        "run": run,
        "certificate": certificate.name,
        "tarball": {"sha256": digest},
        "bindings": {"status": "BUNDLE_BOUND_TO_PACKET"},
        "preconditions": {
            "status": "DRIVER_PRECONDITIONS_HOLD",
            "candidate_digest": certificate.candidate_digest,
        },
        "inputs": {"status": "ALL_INPUTS_ENCLOSE_THE_CANDIDATE"},
        "environment": {"PYTHONOPTIMIZE": None},
        "host": {"cpu": "test host"},
    }
    return record | changes


def _receipts(
    tmp_path: Path, certificate: audit.MixedCertificate, ranges: list[tuple[int, int]]
) -> Path:
    """Receipts as a faithful split replay writes them: each angle returns its record."""
    shipped = json.loads(audit.mixed_retained(certificate)["certificate.json"])["results"]
    receipts = tmp_path / "receipts"
    for first, last in ranges:
        folder = receipts / audit.range_name(first, last)
        folder.mkdir(parents=True)
        run = f"run-{first}"
        (folder / "runs.jsonl").write_text(json.dumps(_run(certificate, run)) + "\n")
        rows = [
            {
                "run": run,
                "index": index,
                "status": "REPLAYED",
                "report": shipped[str(index)],
                "replayed_sha256": _sha256(json.dumps(shipped[str(index)], indent=2).encode()),
                "cpu_seconds": 1.5,
            }
            for index in range(first, last + 1)
        ]
        (folder / "directions.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    return receipts


def _rewrite_rows(folder: Path, change: Any) -> None:
    rows = [json.loads(line) for line in (folder / "directions.jsonl").read_text().splitlines()]
    kept = [row for row in map(change, rows) if row is not None]
    (folder / "directions.jsonl").write_text("".join(json.dumps(r) + "\n" for r in kept))


def test_complete_range_receipts_merge_into_a_full_replay(tmp_path: Path) -> None:
    certificate = audit.MIXED["n84"]
    receipts = _receipts(tmp_path, certificate, [(0, 99), (100, 150), (151, 200)])
    merged = audit.mixed_merge(certificate, receipts)
    assert merged["status"] == "FULL_REPLAY_MATCHES_SHIPPED"
    assert merged["angles_replayed"] == 201
    assert merged["cpu_hours"] == pytest.approx(201 * 1.5 / 3600, abs=1e-3)
    summary = audit.range_summary(certificate, receipts / "range-100-150", 100, 150)
    assert summary["status"] == "RANGE_REPLAYED"


def test_an_angle_with_another_node_count_is_refused(tmp_path: Path) -> None:
    certificate = audit.MIXED["n84"]
    receipts = _receipts(tmp_path, certificate, [(0, 100), (101, 200)])

    def change(row: dict[str, Any]) -> dict[str, Any]:
        if row["index"] == 175:
            row["report"] = row["report"] | {"nodes": row["report"]["nodes"] + 1}
        return row

    _rewrite_rows(receipts / "range-101-200", change)
    merged = audit.mixed_merge(certificate, receipts)
    assert merged["status"] == "DIFFERS"
    assert merged["refused"] == ["range-101-200: angle 175 REPLAYED"]
    summary = audit.range_summary(certificate, receipts / "range-101-200", 101, 200)
    assert summary["status"] == "DIFFERS"


def test_an_angle_whose_written_record_is_another_is_refused(tmp_path: Path) -> None:
    """The row must carry the digest of the replayed.json the shipped function wrote."""
    certificate = audit.MIXED["n84"]
    receipts = _receipts(tmp_path, certificate, [(0, 200)])

    def change(row: dict[str, Any]) -> dict[str, Any]:
        if row["index"] == 3:
            row["replayed_sha256"] = "2" * 64
        return row

    _rewrite_rows(receipts / "range-000-200", change)
    merged = audit.mixed_merge(certificate, receipts)
    assert merged["status"] == "DIFFERS"
    assert merged["refused"] == ["range-000-200: angle 3 REPLAYED"]


def test_a_missing_angle_leaves_the_replay_incomplete(tmp_path: Path) -> None:
    certificate = audit.MIXED["n85"]
    receipts = _receipts(tmp_path, certificate, [(0, 100), (101, 200)])
    _rewrite_rows(receipts / "range-000-100", lambda row: None if row["index"] == 0 else row)
    merged = audit.mixed_merge(certificate, receipts)
    assert merged["status"] == "INCOMPLETE"
    assert merged["missing"] == [0]


def test_a_failed_angle_is_refused_even_when_another_run_passed_it(tmp_path: Path) -> None:
    certificate = audit.MIXED["n85"]
    receipts = _receipts(tmp_path, certificate, [(0, 200)])
    folder = receipts / "range-000-200"
    failed = {"run": "run-0", "index": 7, "status": "FAILED", "report": None, "cpu_seconds": 2}
    with (folder / "directions.jsonl").open("a") as out:
        out.write(json.dumps(failed) + "\n")
    assert audit.mixed_merge(certificate, receipts)["status"] == "DIFFERS"


def test_a_run_on_another_tarball_is_refused(tmp_path: Path) -> None:
    certificate = audit.MIXED["n84"]
    receipts = _receipts(tmp_path, certificate, [(0, 200)])
    other = _run(certificate, "run-0", tarball={"sha256": "1" * 64})
    (receipts / "range-000-200/runs.jsonl").write_text(json.dumps(other) + "\n")
    with pytest.raises(ValueError, match="not bound to the pinned tarball"):
        audit.mixed_merge(certificate, receipts)


def test_a_row_without_its_run_record_is_refused(tmp_path: Path) -> None:
    certificate = audit.MIXED["n84"]
    receipts = _receipts(tmp_path, certificate, [(0, 200)])
    (receipts / "range-000-200/runs.jsonl").write_text("")
    with pytest.raises(ValueError, match="has no run record"):
        audit.mixed_merge(certificate, receipts)


def test_a_replay_with_asserts_off_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "PYTHONDONTWRITEBYTECODE"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("PYTHONOPTIMIZE", "1")
    with pytest.raises(ValueError, match="assertions are off"):
        audit.replay_runtime()


# --------------------------------------------------------------------------- the plan


@pytest.mark.parametrize("parts", [1, 3, 5])
def test_a_plan_splits_every_angle_into_contiguous_ranges(parts: int) -> None:
    plan = audit.mixed_plan(audit.MIXED["n65"], parts)
    ranges = [tuple(part["range"]) for part in plan["parts"]]
    assert len(ranges) == parts
    assert ranges[0][0] == 0
    assert ranges[-1][1] == audit.N50_LAST
    assert all(left[1] + 1 == right[0] for left, right in itertools.pairwise(ranges))
    shares = [part["share"] for part in plan["parts"]]
    assert sum(shares) == pytest.approx(1, abs=1e-3)
    assert max(shares) <= 1.1 / parts + 0.01


@pytest.mark.parametrize(
    ("packet", "runners"),
    [
        *((packet, runners) for packet in (J_PACKET, K_PACKET) for runners in (1, 4, 8)),
        *((L_PACKET, runners) for runners in (1, 4, 6)),
    ],
    ids=["j-1", "j-4", "j-8", "k-1", "k-4", "k-8", "l-1", "l-4", "l-6"],
)
def test_a_shard_runs_every_angle_of_every_certificate_once(runners: int, packet: Path) -> None:
    shard = audit.mixed_shard(packet, runners)
    assert len(shard["plan"]) == runners
    covered: dict[str, list[int]] = {}
    for runner in shard["plan"]:
        assert len(runner["commands"]) == len(runner["pieces"])
        for piece in runner["pieces"]:
            first, last = piece["range"]
            covered.setdefault(piece["certificate"], []).extend(range(first, last + 1))
    assert set(covered) == set(shard["certificates"])
    assert all(sorted(angles) == list(range(audit.N50_LAST + 1)) for angles in covered.values())
    loads = [runner["estimated_cpu_hours"] for runner in shard["plan"]]
    assert sum(loads) == pytest.approx(shard["estimated_cpu_hours"], abs=0.1)
    assert max(loads) <= 1.15 * sum(loads) / runners + 0.01


def test_unpacking_replaces_only_the_work_directory(tmp_path: Path) -> None:
    """The replay unpacks into its work directory and replaces only that directory."""
    real = audit.MIXED["n84"]
    archive = tmp_path / "bundle.tar.gz"
    archive.write_bytes(_tarball(real.bundle, {"README.md": b"bundle\n"}))
    into = tmp_path / "work/unpacked"
    stale = into / "stale.txt"
    stale.parent.mkdir(parents=True)
    stale.write_text("left by an earlier run")
    bundle = audit.unpack_bundle(real, archive, into)
    assert bundle == into / real.bundle
    assert not stale.exists()
    shutil.rmtree(into)


# --------------------------------------------------------------------------- transport


def _downloads(
    monkeypatch: pytest.MonkeyPatch, deliveries: dict[str, bytes | None]
) -> list[str]:
    """Stand in for the network: each route either writes its bytes or is refused."""
    tried: list[str] = []

    def deliver(route: str, partial: Path) -> None:
        tried.append(route)
        data = deliveries.get(route)
        if data is None:
            raise urllib.error.HTTPError(route, 403, "Forbidden", Message(), None)
        partial.write_bytes(data)

    def git(_: audit.MixedCertificate, partial: Path) -> str:
        deliver("git", partial)
        return "git"

    monkeypatch.setattr(audit, "_fetch_url", deliver)
    monkeypatch.setattr(audit, "_fetch_git", git)
    return tried


def test_auto_tries_each_address_and_keeps_the_pinned_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real = audit.MIXED["n84"]
    archive = _tarball(real.bundle, {"README.md": b"bundle\n"})
    certificate = _pinned_to(tmp_path, archive)
    first, second = certificate.urls
    assert first == (
        "https://github.com/wand125/square-packing-bounds/raw/"
        f"{audit.G_REVISION}/certificates/mixed_n84_L940/n84-L9.40-proof-bundle.tar.gz"
    )
    tried = _downloads(monkeypatch, {second: archive})
    fetched = audit.fetch_tarball(certificate, tmp_path / "work")
    assert tried == [first, second]
    assert fetched["origin"] == second
    assert fetched["status"] == "TARBALL_MATCHES_PIN"
    assert len(fetched["refused_routes"]) == 1


@pytest.mark.parametrize("via", ["auto", "url", "git"])
def test_a_route_delivering_other_bytes_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, via: str
) -> None:
    real = audit.MIXED["n84"]
    archive = _tarball(real.bundle, {"README.md": b"bundle\n"})
    certificate = _pinned_to(tmp_path, archive)
    other = _tarball(real.bundle, {"README.md": b"another bundle\n"})
    _downloads(monkeypatch, dict.fromkeys([*certificate.urls, "git"], other))
    with pytest.raises(ValueError, match="the pin is"):
        audit.fetch_tarball(certificate, tmp_path / "work", via=via)
    assert (tmp_path / "work" / f"{real.tarball}.rejected").is_file()


def test_when_no_route_delivers_the_fetch_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    certificate = _pinned_to(tmp_path, b"pinned")
    tried = _downloads(monkeypatch, {})
    with pytest.raises(ValueError, match="no route delivered"):
        audit.fetch_tarball(certificate, tmp_path / "work", via="auto")
    assert tried == [*certificate.urls, "git"]
    assert not (tmp_path / "work" / certificate.tarball).exists()


#: Where the stand-in release asset is served.
ASSET_URL = "https://example.invalid/certificates__mixed_n84_L940.tar.gz"


def _released(tmp_path: Path, archive: bytes) -> tuple[audit.MixedCertificate, bytes]:
    """n = 84 pinned as a source that published its tarball in a release asset: the
    packet's record names the asset and the member that is the tarball, as
    `devtools.retain_wand125_release` writes it."""
    real = audit.MIXED["n84"]
    certificate = _pinned_to(tmp_path, archive)
    member = real.upstream_tarball.as_posix()
    asset = _tarball(real.upstream_tarball.parent.as_posix(), {real.tarball: archive})
    record = json.loads(certificate.record.read_text())
    record["sources"][0]["release_assets"] = [
        {
            "asset": "certificates__mixed_n84_L940.tar.gz",
            "url": ASSET_URL,
            "bytes": len(asset),
            "sha256": _sha256(asset),
            "members": [
                {
                    "member": member,
                    "path": member,
                    "bytes": len(archive),
                    "sha256": _sha256(archive),
                }
            ],
        }
    ]
    certificate.record.write_text(json.dumps(record))
    return certificate, asset


@pytest.mark.parametrize("via", ["auto", "release"])
def test_a_tarball_in_a_pinned_release_asset_is_read_from_the_asset_alone(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, via: str
) -> None:
    real = audit.MIXED["n84"]
    archive = _tarball(real.bundle, {"README.md": b"bundle\n"})
    certificate, asset = _released(tmp_path, archive)
    tried = _downloads(monkeypatch, {ASSET_URL: asset})
    fetched = audit.fetch_tarball(certificate, tmp_path / "work", via=via)
    assert tried == [ASSET_URL]
    assert fetched["status"] == "TARBALL_MATCHES_PIN"
    assert fetched["origin"] == f"release {ASSET_URL} member {real.upstream_tarball}"
    assert (tmp_path / "work" / real.tarball).read_bytes() == archive
    # A second fetch reads the asset already in the work directory, checked again.
    (tmp_path / "work" / real.tarball).unlink()
    assert audit.fetch_tarball(certificate, tmp_path / "work", via=via)["sha256"] == (
        _sha256(archive)
    )
    assert tried == [ASSET_URL]


def test_a_release_asset_that_is_not_the_pinned_one_is_refused_before_it_is_read(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real = audit.MIXED["n84"]
    archive = _tarball(real.bundle, {"README.md": b"bundle\n"})
    certificate, asset = _released(tmp_path, archive)
    other = _tarball(
        real.upstream_tarball.parent.as_posix(),
        {real.tarball: _tarball(real.bundle, {"README.md": b"another bundle\n"})},
    )
    assert other != asset
    _downloads(monkeypatch, {ASSET_URL: other})
    with pytest.raises(ValueError, match="the pin is"):
        audit.fetch_tarball(certificate, tmp_path / "work", via="release")
    assert not (tmp_path / "work" / real.tarball).exists()
    # The refused asset is set aside, so that the next run downloads it afresh.
    rejected = tmp_path / "work" / "certificates__mixed_n84_L940.tar.gz.rejected"
    assert rejected.read_bytes() == other


def test_without_a_release_asset_the_release_route_is_refused(tmp_path: Path) -> None:
    certificate = _pinned_to(tmp_path, b"pinned")
    assert audit.release_pin(certificate) is None
    with pytest.raises(ValueError, match="no release asset holds"):
        audit.fetch_tarball(certificate, tmp_path / "work", via="release")


# --------------------------------------------------------------------------- audit supplements


def test_a_supplied_tarball_is_checked_against_the_pin(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real = audit.MIXED["n84"]
    archive = _tarball(real.bundle, {"README.md": b"bundle\n"})
    certificate = _pinned_to(tmp_path, archive)
    monkeypatch.setitem(audit.MIXED, "n84", certificate)
    supplied = tmp_path / real.tarball
    supplied.write_bytes(archive)
    found = audit.mixed_audit_supplements(certificate.packet, [supplied])
    assert found["tarballs"]["n84"]["status"] == "TARBALL_MATCHES_PIN"
    supplied.write_bytes(archive[:-1])
    with pytest.raises(ValueError, match="the pin is"):
        audit.mixed_audit_supplements(certificate.packet, [supplied])
    elsewhere = tmp_path / "n85-L9.42-proof-bundle.tar.gz"
    elsewhere.write_bytes(archive)
    with pytest.raises(ValueError, match="is not a tarball"):
        audit.mixed_audit_supplements(certificate.packet, [elsewhere])


def test_present_replay_receipts_are_merged_by_the_audit(tmp_path: Path) -> None:
    certificate = audit.MIXED["n85"]
    assert audit.replay_receipts(certificate, tmp_path / "none") is None
    receipts = _receipts(tmp_path, certificate, [(0, 100), (101, 200)])
    state = audit.replay_receipts(certificate, receipts)
    assert state is not None
    assert state["status"] == "FULL_REPLAY_MATCHES_SHIPPED"
    shutil.rmtree(receipts / "range-101-200")
    partial = audit.replay_receipts(certificate, receipts)
    assert partial is not None
    assert (partial["status"], partial["angles_missing"]) == ("INCOMPLETE", 100)


def test_replay_receipts_with_another_angle_are_refused_by_the_audit(tmp_path: Path) -> None:
    certificate = audit.MIXED["n85"]
    receipts = _receipts(tmp_path, certificate, [(0, 200)])

    def change(row: dict[str, Any]) -> dict[str, Any]:
        if row["index"] == 44:
            row["report"] = row["report"] | {"lower": 0.99}
        return row

    _rewrite_rows(receipts / "range-000-200", change)
    with pytest.raises(ValueError, match="the replay receipts differ"):
        audit.replay_receipts(certificate, receipts)


def test_replay_receipts_from_an_unbound_run_are_refused_by_the_audit(tmp_path: Path) -> None:
    certificate = audit.MIXED["n84"]
    receipts = _receipts(tmp_path, certificate, [(0, 200)])
    other = _run(certificate, "run-0", environment={"PYTHONOPTIMIZE": "1"})
    (receipts / "range-000-200/runs.jsonl").write_text(json.dumps(other) + "\n")
    with pytest.raises(ValueError, match="not bound to the pinned tarball"):
        audit.replay_receipts(certificate, receipts)
    other = _run(certificate, "run-0", tarball={"sha256": "1" * 64})
    (receipts / "range-000-200/runs.jsonl").write_text(json.dumps(other) + "\n")
    with pytest.raises(ValueError, match="not bound to the pinned tarball"):
        audit.replay_receipts(certificate, receipts)


def test_each_packets_committed_replay_receipts_merge_without_a_refusal() -> None:
    for name in NAMES:
        state = audit.replay_receipts(audit.MIXED[name])
        assert state is None or state["status"] != "DIFFERS"


# --------------------------------------------------------------------------- the range driver


def _faithful(shipped: dict[str, Any], fail_at: int | None = None) -> Any:
    """A stand-in for the shipped per-angle function, returning the certificate's record."""

    def replay(index: int) -> dict[str, Any]:
        if index == fail_at:
            raise RuntimeError("the session was interrupted")
        record = shipped[str(index)]
        return {
            "index": index,
            "status": "REPLAYED",
            "report": record,
            "replayed_sha256": _sha256(json.dumps(record, indent=2).encode()),
            "cpu_seconds": 2.0,
        }

    return replay


def _drive(
    folder: Path,
    certificate: audit.MixedCertificate,
    span: tuple[int, int],
    replay: Any,
    run: str,
    *,
    deadline: float | None = None,
) -> dict[str, Any]:
    shipped = audit.shipped_results(certificate)
    todo = audit.pending_directions(folder, shipped, *span)
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return audit.replay_directions(
            certificate,
            folder,
            span,
            todo,
            lambda index: pool.submit(replay, index),
            workers=1,
            run=run,
            shipped=shipped,
            deadline=deadline,
        )


def test_an_interrupted_range_keeps_each_finished_angle_and_resumes(tmp_path: Path) -> None:
    certificate = audit.MIXED["n84"]
    shipped = audit.shipped_results(certificate)
    receipts = tmp_path / "receipts"
    folder = receipts / audit.range_name(0, 12)
    folder.mkdir(parents=True)
    order = audit.pending_directions(folder, shipped, 0, 12)
    assert order[0] == 0
    (folder / "runs.jsonl").write_text(
        json.dumps(_run(certificate, "first"))
        + "\n"
        + json.dumps(_run(certificate, "second"))
        + "\n"
    )
    with pytest.raises(RuntimeError, match="interrupted"):
        _drive(folder, certificate, (0, 12), _faithful(shipped, fail_at=order[4]), "first")
    summary = json.loads((folder / "summary.json").read_text())
    assert (summary["status"], summary["replayed"]) == ("INCOMPLETE", 4)
    assert audit.pending_directions(folder, shipped, 0, 12) == order[4:]
    done = _drive(folder, certificate, (0, 12), _faithful(shipped), "second")
    assert done["status"] == "RANGE_REPLAYED"
    rows = audit.read_jsonl(folder / "directions.jsonl")
    assert sorted(row["index"] for row in rows) == list(range(13))
    assert audit.mixed_merge(certificate, receipts)["missing"] == list(range(13, 201))


def test_a_passed_deadline_starts_no_angle(tmp_path: Path) -> None:
    certificate = audit.MIXED["n85"]
    shipped = audit.shipped_results(certificate)
    folder = tmp_path / audit.range_name(5, 9)
    folder.mkdir()
    summary = _drive(folder, certificate, (5, 9), _faithful(shipped), "late", deadline=0.0)
    assert (summary["status"], summary["missing"]) == ("INCOMPLETE", [5, 6, 7, 8, 9])
    assert not (folder / "directions.jsonl").exists()


def test_a_torn_last_line_is_cut_and_its_angle_replayed(tmp_path: Path) -> None:
    certificate = audit.MIXED["n85"]
    shipped = audit.shipped_results(certificate)
    receipts = _receipts(tmp_path, certificate, [(10, 14)])
    rows = receipts / "range-010-014/directions.jsonl"
    whole = rows.read_text().splitlines(keepends=True)
    rows.write_text("".join(whole[:3]) + whole[3][:40])
    with pytest.raises(json.JSONDecodeError):
        audit.pending_directions(rows.parent, shipped, 10, 14)
    assert audit.drop_torn_line(rows) == 40
    assert audit.drop_torn_line(rows) == 0
    assert sorted(audit.pending_directions(rows.parent, shipped, 10, 14)) == [13, 14]


def test_a_finished_range_is_not_fetched_again(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "PYTHONDONTWRITEBYTECODE"):
        monkeypatch.setenv(name, "1")
    certificate = audit.MIXED["n84"]
    receipts = _receipts(tmp_path, certificate, [(20, 30)])

    def refuse(*_: Any, **__: Any) -> None:
        raise AssertionError("a finished range fetched its tarball")

    monkeypatch.setattr(audit, "fetch_tarball", refuse)
    summary = audit.mixed_replay(
        certificate, tmp_path / "work", 20, 30, workers=1, receipts=receipts
    )
    assert summary["status"] == "RANGE_REPLAYED"
    assert (receipts / "range-020-030/summary.json").is_file()


# --------------------------------------------------------------------------- the price


def test_the_price_samples_agree_once_scaled_by_rectangles() -> None:
    rate, samples = audit.price_rate()
    for sample in samples:
        assert sample["rate"] == pytest.approx(rate, rel=0.03)
    per_node = [
        sample["rate"] * audit.MIXED[sample["certificate"]].rectangles for sample in samples
    ]
    assert max(per_node) / min(per_node) > 1.3
    price = audit.mixed_price()["certificates"]
    assert set(price) == set(audit.MIXED)
    assert all(row["axis_share"] < 0.01 for row in price.values())
    assert price["n65"]["cpu_hours"] > price["n84"]["cpu_hours"] > price["n37"]["cpu_hours"]
