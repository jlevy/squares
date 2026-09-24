"""T-035 and T-036 quote the retained rung-0 verdict and manifest, and nothing else.

The certificate tree behind both results is 7.8 GB and lives outside the repository, so
no test here can replay it; the replay is Session 157's reader run, and the
registration-time manifest check is recorded in the evidence entry. What the record does
keep is small: the reader's verdict, the SHA-256 manifest that pins the off-record tree,
and the frozen-instrument record. These tests hold the register's claim strings and
pinned digests to those three files, so a claim that drifts from the verdict it quotes,
or a manifest that stops naming the verdict it retains, fails on the pull-request
surface. Everything here reads a few kilobytes.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from sqpack.yamlio import safe_load

PACKING = Path(__file__).resolve().parents[1]
AGENDA = (
    PACKING
    / "campaign"
    / "series"
    / "series-000-smoke-and-calibration"
    / "results"
    / "agenda-042"
)
VERDICT = AGENDA / "exp-232-h236-reader-final2.json.gz"
MANIFEST = AGENDA / "exp-232-h236-tree-manifest.sha256"
FROZEN = AGENDA / "exp-232-h236-frozen.txt"
READER = PACKING / "cases" / "trump11" / "fixed_angle_tree_check.py"

#: The manifest's own digest, which the evidence entry's `certificate` pins.
MANIFEST_DIGEST = "45c2a0d24356bfa1f2c03deeda895eb5fb4358b6528e1d3b36e284b09f565265"
#: The decompressed verdict's digest, the manifest's `./h236-reader-final2.json` line.
VERDICT_DIGEST = "1a04c97a2f1583062ec69f66fbfcf3a99b6840b1e4db8533eac3816bb227c8aa"
#: The reader's git blob, frozen before the n = 11 run and unchanged since.
READER_BLOB = "c4ae4e489fcfe9b69470c3834ce18b5151485f47"
BOX = (Fraction(91442076901, 250000000000), Fraction(73154061521, 200000000000))
RHO = Fraction(808514697, 200000000000)
LABELS = [3, 4, 2, 5, 0, 1, 8, 10, 6, 9, 7]


def _manifest() -> dict[str, str]:
    lines = MANIFEST.read_text(encoding="utf-8").splitlines()
    return {name: digest for digest, name in (line.split("  ", 1) for line in lines)}


def _verdict_bytes() -> bytes:
    return gzip.decompress(VERDICT.read_bytes())


def _register(name: str, key: str) -> dict[str, dict]:
    document = safe_load((PACKING / "frontier" / name).read_text(encoding="utf-8"))
    return {entry["id"]: entry for entry in document[key]}


def test_manifest_pins_the_whole_tree_and_the_retained_verdict() -> None:
    assert hashlib.sha256(MANIFEST.read_bytes()).hexdigest() == MANIFEST_DIGEST
    manifest = _manifest()
    subtrees = {f"./h236.sub/sub-{index:05d}.jsonl.gz" for index in range(256)}
    assert set(manifest) == subtrees | {
        "./h236.jsonl.gz",
        "./FROZEN.txt",
        "./h236-reader-final2.json",
    }
    assert manifest["./h236-reader-final2.json"] == VERDICT_DIGEST
    assert hashlib.sha256(_verdict_bytes()).hexdigest() == VERDICT_DIGEST
    assert manifest["./FROZEN.txt"] == hashlib.sha256(FROZEN.read_bytes()).hexdigest()


def test_the_verdict_says_what_t035_quotes() -> None:
    verdict = json.loads(_verdict_bytes())
    assert verdict["verdict"] == "closed"
    assert verdict["unresolved_by_reason"] == {}
    assert verdict["subtree_files"] == 256
    assert verdict["leaves"] == {
        "b": 19883887,
        "c": 21834304,
        "f": 97722555,
        "t": 3,
        "s": 256,
    }
    assert sum(verdict["leaves"].values()) == 139441005
    statement = verdict["statement"]
    assert statement["family"] == "6 axis + 5 tilted"
    assert tuple(Fraction(end) for end in statement["half_tangent_box"]) == BOX
    assert statement["target_label"] == "U"
    assert statement["target_is_at_least_U"] is True
    assert statement["angle_reach_bound"] < 2.0000014e-6
    image = statement["image"]
    assert (image["name"], image["rotation"], image["labels"]) == ("trump11", 1, LABELS)
    assert Fraction(image["radius"]) == RHO


def test_the_register_rows_quote_the_verdict_and_pin_the_manifest() -> None:
    results = _register("results.yaml", "results")
    evidence = _register("evidence.yaml", "evidence")
    reduction, theorem = results["T-035"], results["T-036"]
    for record in (reduction, theorem):
        claim = " ".join(record["claim"].split())
        assert "[91442076901/250000000000, 73154061521/200000000000]" in claim
        assert record["produced_by"]["hypothesis"] == "H-236"
    claim = " ".join(reduction["claim"].split())
    assert "rho = 808514697/200000000000" in claim
    assert "labels [3,4,2,5,0,1,8,10,6,9,7]" in claim
    assert reduction["evidence"] == ["E-n011-h236-rung0-reduction"]
    assert theorem["evidence"] == [
        "E-n011-h236-rung0-reduction",
        "E-n011-trump-local-theorem-first-clause",
    ]
    entry = evidence["E-n011-h236-rung0-reduction"]
    assert MANIFEST_DIGEST in " ".join(entry["certificate"].split())
    assert "cases.trump11.fixed_angle_tree_check" in entry["replay"]


def test_the_reader_is_still_the_frozen_bytes() -> None:
    body = READER.read_bytes()
    blob = hashlib.sha1(b"blob %d\0" % len(body) + body).hexdigest()
    assert blob == READER_BLOB
    assert READER_BLOB in FROZEN.read_text(encoding="utf-8")
