"""Recompute replay4d's source hashes, and calibrate replay4d on this host, from the packets.

wand125's closed-form lower bound, ``s(N) >= a(N)`` for every non-square ``N >= 49``,
ships a Rust replay checker, ``replay4d``. Three packets retain its folder at three
revisions of wand125/square-packing: ``9a28a84`` (replay4d 0.1.0,
``web/wand125-closed-form-2026-10-14/``), ``746e2c5`` (cfcheck added, replay4d
unchanged, ``web/wand125-closed-form-cfcheck-2026-10-14/``) and ``1c661b7`` (replay4d
0.1.1, ``web/wand125-closed-form-source-hash-2026-10-14/``). This tool reads them through
their acquisition records alone: a pinned-only file is read from the copy it names. Their
custody is `devtools.acquire_source` ``--check``'s, which binds every file to the pin
and every named copy to its bytes, so nothing here re-hashes the repository against
itself. It runs no source program, and decides nothing about the certificate. Three
commands:

- ``hashes`` recomputes, at each revision, the source hash replay4d prints, by the rule
  in that revision's own ``main.rs`` (`source_order`, `source_hash`): for each covered
  file in order, its name as UTF-8, a NUL byte, its length as a 64-bit big-endian
  integer and its bytes, and then the SHA-256 of the whole. It compares each with the
  value the source states, shows which files each version covers, checks by mutation
  that ``b3d_sort.rs`` is covered from 0.1.1 and not before, and compares the digest of
  ``validate_family.py`` that ``receipts/structure.json`` names with the published
  script at each revision. ``--check`` compares the retained receipt with a fresh
  derivation instead of writing it.
- ``controls`` writes three small inputs for replay4d from one region record: the first
  two roots alone, which the domain check must refuse because they are not the product
  grid; the leaves of the first roots as ``--leaves`` input, which must pass; and the
  same leaves with one relabelled to ``CORE``, which must fail at that leaf.
- ``calibrate`` reads `devtools.replay_receipt` logs and replay4d's ``--out`` summaries
  of replays run here, binds them to ``intervals.json`` (digests, root and leaf counts
  per kind) and to the binaries' digests, and prices the source's complete replay on
  this host by the ratio of the CPU time measured here to the source's
  ``results[].cpu_hours`` for the same records. ``--check`` compares the retained
  receipt with a fresh derivation.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_closed_form hashes
    uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_closed_form \\
        controls --interval 26 --region top --record DIR/top.rec --out OUT
    uv run --frozen --all-extras --group dev python -m devtools.audit_wand125_closed_form \\
        calibrate
"""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
import tomllib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools.retained_data import read_retained_bytes

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
FOLDER = "problems/closed-form"
CHECKER = f"{FOLDER}/checker"
MAIN_RS = f"{CHECKER}/replay4d/src/main.rs"
B3D_SORT = f"{CHECKER}/seam4d_core/src/b3d_sort.rs"
B3D = f"{CHECKER}/seam4d_core/src/b3d.rs"
VALIDATE_FAMILY = f"{FOLDER}/structure/validate_family.py"
STRUCTURE = f"{FOLDER}/receipts/structure.json"

type Json = dict[str, Any]


@dataclass(frozen=True)
class Revision:
    """One pinned revision of the folder, the packet that holds it, and what it states."""

    commit: str
    packet: str
    stated_source_sha256: str
    statement: str


REVISIONS = (
    Revision(
        "9a28a84bd55dc124bfa2919bb6c4fb504dda3149",
        "wand125-closed-form-2026-10-14",
        "92002e0e8924d96f0e5962eabb8fce6e4de67a2f350ca66d4889abee0762c193",
        "README.md: the source hash printed by replay4d is ... 92002e0e... for the "
        "published sources; receipts/published_checker.json names it",
    ),
    Revision(
        "746e2c5ac7a7f534996dd50a5e1fd9f1d8836a8d",
        "wand125-closed-form-cfcheck-2026-10-14",
        "92002e0e8924d96f0e5962eabb8fce6e4de67a2f350ca66d4889abee0762c193",
        "replay4d unchanged since 9a28a84: the README repeats 92002e0e...",
    ),
    Revision(
        "1c661b705422b58b5eb169589776b50c14be2a2f",
        "wand125-closed-form-source-hash-2026-10-14",
        "f8cafeab078e1de31bacdef9c5c08ad70938f1b1b20fd3a2e1e54de9f73f1742",
        "README.md: the published sources of 0.1.1 hash to f8cafeab...",
    ),
)
#: The source hash of the sources the full replay ran, which are not published.
FULL_REPLAY_SOURCE_SHA256 = "306ad4b58b7e962f90e430b1adeaa8c52ad70f02f4807c96493036f6bb6cb476"
#: ``b3d_sort.rs`` at every revision, as the 1c661b7 README states it.
STATED_B3D_SORT_SHA256 = "23be1db0de55790110ff97c966bf34a6046c1d224a0f5bad98c6639866895928"

PACKET_9A28A84 = WEB / REVISIONS[0].packet
PACKET_1C661B7 = WEB / REVISIONS[2].packet
HASHES_RECEIPT = PACKET_1C661B7 / "receipts/source-hashes.json"
CALIBRATION = PACKET_9A28A84 / "receipts/calibration"
CALIBRATION_RECEIPT = CALIBRATION / "calibration.json"
INTERVALS = PACKET_9A28A84 / f"square-packing/{FOLDER}/intervals.json.gz"
SOURCE_REPLAY = PACKET_9A28A84 / f"square-packing/{FOLDER}/receipts/replay.json.gz"

_ENTRY = re.compile(r'\("([^"]+)",\s*include_bytes!\("([^"]+)"\)\)')
_FOOTER = re.compile(
    r"# finished (?P<finished>\S+); exit (?P<exit>-?\d+); wall (?P<wall>[\d.]+) s; "
    r"CPU (?P<cpu>[\d.]+) s \(user (?P<user>[\d.]+) \+ sys (?P<sys>[\d.]+)\); "
    r"load (?P<load>.+)"
)
_HOST = re.compile(r"# host: (?P<cores>\d+) cores; load (?P<load>.+); started (?P<started>\S+)")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _rel(path: Path) -> str:
    return path.resolve().relative_to(REPO).as_posix()


# ------------------------------------------------------------------------ the packets


class PacketTree:
    """The upstream files of one packet's scope, read through its acquisition record."""

    def __init__(self, packet: Path) -> None:
        record = json.loads((packet / "acquisition/sources.json").read_text(encoding="utf-8"))
        (source,) = record["sources"]
        self.packet = packet
        self.commit: str = source["source_commit"]
        self.archived = REPO / source["archived_path"]
        self.pinned: dict[str, Json] = {item["path"]: item for item in source["pinned_only"]}
        manifest = (REPO / source["subtree_manifest"]).read_text(encoding="utf-8")
        self.scope = {
            line.split("  ", 1)[1].removeprefix("./") for line in manifest.splitlines()
        }

    def read(self, upstream: str) -> bytes:
        """The bytes of ``upstream`` at this packet's pin."""
        if upstream not in self.scope:
            raise KeyError(f"{self.packet.name}: {upstream} is not in the manifest")
        if upstream in self.pinned:
            twin = self.pinned[upstream].get("identical_to")
            if twin is None:
                raise KeyError(f"{self.packet.name}: {upstream} is pinned with no copy")
            return read_retained_bytes(REPO / twin)
        return read_retained_bytes(self.archived / upstream)

    def where(self, upstream: str) -> str:
        """The repository-relative file the bytes of ``upstream`` were read from."""
        if upstream in self.pinned:
            return str(self.pinned[upstream]["identical_to"])
        return _rel(self.archived / upstream)


# ------------------------------------------------------------------------ the hash rule


def source_order(main_rs: str) -> list[tuple[str, str]]:
    """The covered files of ``source_hash()`` in ``main.rs``: (hashed name, upstream path).

    The name is relative to the ``replay4d`` crate, the ``include_bytes!`` path to
    ``replay4d/src/``; both must resolve to the same upstream file.
    """
    start = main_rs.index("fn source_hash()")
    body = main_rs[start : main_rs.index("sha256::digest(&bytes)", start)]
    order: list[tuple[str, str]] = []
    for name, include in _ENTRY.findall(body):
        by_name = posixpath.normpath(f"{CHECKER}/replay4d/{name}")
        by_include = posixpath.normpath(f"{CHECKER}/replay4d/src/{include}")
        if by_name != by_include:
            raise ValueError(f"{name} and {include} name different files")
        order.append((name, by_name))
    if not order:
        raise ValueError("source_hash() lists no files")
    return order


def source_hash(files: Iterable[tuple[str, bytes]]) -> str:
    """replay4d's source hash of ``(name, bytes)`` pairs, in order."""
    blob = bytearray()
    for name, data in files:
        blob += name.encode() + b"\0" + len(data).to_bytes(8, "big") + data
    return sha256(bytes(blob))


def revision_hash(tree: PacketTree, replace: dict[str, bytes] | None = None) -> str:
    """The source hash at ``tree``'s pin, with any files in ``replace`` substituted."""
    replace = replace or {}
    order = source_order(tree.read(MAIN_RS).decode())
    return source_hash((name, replace.get(path) or tree.read(path)) for name, path in order)


def _flip_last_byte(data: bytes) -> bytes:
    return data[:-1] + bytes([data[-1] ^ 1])


def _crate_version(tree: PacketTree) -> Json:
    cargo = tomllib.loads(tree.read(f"{CHECKER}/replay4d/Cargo.toml").decode())
    lock = tomllib.loads(tree.read(f"{CHECKER}/Cargo.lock").decode())
    locked = [p["version"] for p in lock["package"] if p["name"] == "replay4d"]
    return {"cargo_toml": cargo["package"]["version"], "cargo_lock": locked}


def revision_record(revision: Revision) -> Json:
    tree = PacketTree(WEB / revision.packet)
    if tree.commit != revision.commit:
        raise ValueError(f"{revision.packet} is pinned at {tree.commit}")
    main_rs = tree.read(MAIN_RS).decode()
    order = source_order(main_rs)
    readme = tree.read(f"{FOLDER}/README.md").decode()
    covered = [
        {
            "name": name,
            "path": path,
            "bytes": len(tree.read(path)),
            "sha256": sha256(tree.read(path)),
        }
        for name, path in order
    ]
    computed = revision_hash(tree)
    structure = json.loads(tree.read(STRUCTURE))
    return {
        "commit": revision.commit,
        "packet": _rel(tree.packet),
        "replay4d_version": _crate_version(tree),
        "rule": "main.rs fn source_hash(), read from this revision's own main.rs",
        "covered": covered,
        "covered_file_count": len(covered),
        "covers_b3d_sort": any(path == B3D_SORT for _, path in order),
        "source_sha256": computed,
        "stated_source_sha256": revision.stated_source_sha256,
        "stated_in": revision.statement,
        "stated_value_in_readme": revision.stated_source_sha256 in readme,
        "equal": computed == revision.stated_source_sha256,
        "summary_records_b3_plain_rf": '"env":{"B3_PLAIN_RF"' in main_rs,
        "b3d_sort_sha256": sha256(tree.read(B3D_SORT)),
        "b3d_sort_read_from": tree.where(B3D_SORT),
        "validate_family_sha256": sha256(tree.read(VALIDATE_FAMILY)),
        "structure_receipt_validate_family_sha256": structure["validate_family_sha256"],
        "structure_receipt_names_published_script": (
            structure["validate_family_sha256"] == sha256(tree.read(VALIDATE_FAMILY))
        ),
    }


def hashes_receipt() -> Json:
    """The receipt of ``hashes``: every revision, the controls and the unchanged files."""
    records = [revision_record(revision) for revision in REVISIONS]
    controls: list[Json] = []
    for target in (B3D_SORT, B3D):
        row: Json = {"mutation": f"the last byte of {target} flipped (bit 0)"}
        for revision in REVISIONS:
            tree = PacketTree(WEB / revision.packet)
            mutated = revision_hash(tree, {target: _flip_last_byte(tree.read(target))})
            row[revision.commit[:7]] = {"hash_changes": mutated != revision_hash(tree)}
        controls.append(row)
    first, last = PacketTree(PACKET_9A28A84), PacketTree(PACKET_1C661B7)
    unchanged = [
        {
            "path": path,
            "sha256_9a28a84": sha256(first.read(path)),
            "sha256_1c661b7": sha256(last.read(path)),
            "byte_identical": first.read(path) == last.read(path),
        }
        for path in (B3D_SORT, VALIDATE_FAMILY)
    ]
    old = json.loads(first.read(STRUCTURE))
    new = json.loads(last.read(STRUCTURE))
    differing = sorted(key for key in old.keys() | new.keys() if old.get(key) != new.get(key))
    published = json.loads(
        read_retained_bytes(
            PACKET_9A28A84 / f"square-packing/{FOLDER}/receipts/published_checker.json"
        )
    )
    full = json.loads(read_retained_bytes(SOURCE_REPLAY))
    return {
        "schema": "wand125-replay4d-source-hash/v1",
        "tool": "devtools.audit_wand125_closed_form hashes",
        "rule": (
            "replay4d main.rs source_hash(): for each covered file in order, its name as "
            "UTF-8, a NUL byte, its length as a 64-bit big-endian integer and its bytes; "
            "the SHA-256 of the concatenation"
        ),
        "revisions": records,
        "all_equal_to_stated": all(record["equal"] for record in records),
        "controls": controls,
        "unchanged_files": unchanged,
        "stated_b3d_sort_sha256": STATED_B3D_SORT_SHA256,
        "b3d_sort_equals_stated": all(
            row["sha256_1c661b7"] == STATED_B3D_SORT_SHA256
            for row in unchanged
            if row["path"] == B3D_SORT
        ),
        "structure_receipt": {
            "9a28a84": old["validate_family_sha256"],
            "1c661b7": new["validate_family_sha256"],
            "fields_that_differ": differing,
        },
        "source_receipts": {
            "published_checker.json checker_source_sha256": published["checker_source_sha256"],
            "replay.json checker_source_sha256": full["checker_source_sha256"],
            "replay.json results naming a version": sum(
                1 for result in full["results"] if "version" in result
            ),
            "note": (
                "The 4,294 CPU-hour replay ran sources hashing to "
                f"{FULL_REPLAY_SOURCE_SHA256[:8]}..., which are not published and cannot be "
                "recomputed here; its receipts predate 0.1.1 and record neither a version "
                "nor B3_PLAIN_RF."
            ),
        },
    }


# --------------------------------------------------------------------------- the runs


def intervals() -> list[Json]:
    return json.loads(read_retained_bytes(INTERVALS))["intervals"]


def region_plan(index: int, region: str) -> Json:
    """What a replay of one region record must name and count, and the source's time."""
    (interval,) = [item for item in intervals() if item["index"] == index]
    entry = interval["regions"][region]
    family_key = "family_sha256" if entry["family"] == "family.json" else "family_right_sha256"
    full = json.loads(read_retained_bytes(SOURCE_REPLAY))
    (timed,) = [
        result
        for result in full["results"]
        if result["record_sha256"] == entry["sha256"] and result["region"] == region
    ]
    return {
        "interval": index,
        "delta": f"[{interval['d0_decimal']}, {interval['d1_decimal']}]",
        "region": region,
        "asset": interval["asset"],
        "asset_sha256": interval["asset_sha256"],
        "family": entry["family"],
        "family_sha256": interval[family_key],
        "record": entry["file"],
        "record_sha256": entry["sha256"],
        "bounds": entry["bounds"],
        "roots": entry["roots"],
        "leaves": entry["leaves"],
        "leaf_kinds": entry["leaf_kinds"],
        "source_cpu_hours": timed["cpu_hours"],
        "source_runs": timed["runs"],
    }


def write_controls(record: Path, out: Path, *, roots: int = 20) -> Json:
    """Write the truncated record and the two leaf files; return their manifest."""
    lines = record.read_bytes().splitlines(keepends=True)
    out.mkdir(parents=True, exist_ok=True)
    truncated = b"".join(lines[:2])
    leaves = [leaf for line in lines[:roots] for leaf in json.loads(line)["leaves"]]
    index = next(i for i, leaf in enumerate(leaves) if leaf[1] != "CORE")
    relabelled = [list(leaf) for leaf in leaves]
    relabelled[index][1] = "CORE"
    files = {
        "truncated.rec": truncated,
        "leaves.jsonl": "".join(json.dumps(leaf) + "\n" for leaf in leaves).encode(),
        "relabelled.jsonl": "".join(json.dumps(leaf) + "\n" for leaf in relabelled).encode(),
    }
    for name, data in files.items():
        (out / name).write_bytes(data)
    return {
        "record_sha256": sha256(record.read_bytes()),
        "files": {
            name: {"bytes": len(data), "sha256": sha256(data)} for name, data in files.items()
        },
        "truncated": (
            "the record's first 2 root lines, run with the region bounds: "
            "they do not cover the region"
        ),
        "leaves": (
            f"the {len(leaves)} leaves of the record's first {roots} roots, run with --leaves"
        ),
        "relabelled": {
            "leaf": index,
            "from": leaves[index][1],
            "to": "CORE",
            "note": "the same leaves with this one relabelled, run with --leaves",
        },
    }


def parse_receipt_log(text: str) -> Json:
    """The header and footer fields of a `devtools.replay_receipt` log, and its output."""
    lines = text.splitlines()
    if len(lines) < 5 or not lines[0].startswith("# command: "):
        raise ValueError("not a replay_receipt log")
    command = lines[0].removeprefix("# command: ")
    host = _HOST.fullmatch(lines[3])
    footer = _FOOTER.fullmatch(lines[-1])
    if host is None or footer is None:
        raise ValueError("not a replay_receipt log")
    output = [line for line in lines[4:-1] if line.strip() and not line.startswith("# ")]
    return {
        "command": command,
        "cores": int(host["cores"]),
        "load_at_start": host["load"],
        "started": host["started"],
        "finished": footer["finished"],
        "exit": int(footer["exit"]),
        "wall_seconds": float(footer["wall"]),
        "cpu_seconds": round(float(footer["user"]) + float(footer["sys"]), 3),
        "load_at_end": footer["load"],
        "last_line": output[-1] if output else "",
    }


def _reason(bad: Json) -> str:
    """Why replay4d refused: a domain check's reason, or the leaf whose test failed."""
    if bad.get("why"):
        return str(bad["why"])
    result: Json = bad.get("result") or {}
    if result.get("why"):
        return str(result["why"])
    return f"leaf {bad.get('leaf')} ({bad.get('kind')}): its test returned ok false"


def binary_digests(log: Path) -> dict[str, str]:
    """``sha256sum`` lines of a receipt log, by the binary's file name."""
    digests: dict[str, str] = {}
    for line in log.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (\S+)", line)
        if match:
            digests[Path(match[2]).name] = match[1]
    return digests


def calibration_receipt(directory: Path = CALIBRATION) -> Json:
    """Bind every run in ``directory/runs.json`` to its log, summary and the record."""
    plan = json.loads((directory / "runs.json").read_text(encoding="utf-8"))
    binaries = binary_digests(directory / plan["binary_digests"])
    builds: dict[str, Json] = {}
    for label, log in plan["builds"].items():
        text = (directory / log).read_text(encoding="utf-8")
        builds[label] = parse_receipt_log(text)
        results = re.findall(r"test result: (\w+)\. (\d+) passed; (\d+) failed", text)
        if results:
            builds[label]["tests"] = {
                "passed": sum(int(passed) for _, passed, _ in results),
                "failed": sum(int(failed) for _, _, failed in results),
                "all_ok": all(status == "ok" for status, _, _ in results),
            }
    runs: list[Json] = []
    for run in plan["runs"]:
        log = parse_receipt_log((directory / run["log"]).read_text(encoding="utf-8"))
        summary = json.loads((directory / run["summary"]).read_bytes())
        row: Json = {"label": run["label"], "expect": run["expect"], "binary": run["binary"]}
        row["binary_sha256"] = binaries[run["binary"]]
        row["log"] = {k: log[k] for k in ("exit", "wall_seconds", "cpu_seconds", "last_line")}
        row["summary"] = {
            key: summary.get(key)
            for key in ("mode", "ok", "roots", "bad_count", "version", "source_sha256", "env")
        }
        row["summary"]["leaves"] = sum(summary["kinds"].values())
        row["summary"]["cpu_seconds"] = round(summary["cpu_seconds"], 3)
        row["summary"]["wall_seconds"] = round(summary["wall_seconds"], 3)
        row["summary"]["first_bad"] = [_reason(bad) for bad in summary["bad"][:3]]
        if "interval" in run:
            want = region_plan(run["interval"], run["region"])
            row["plan"] = want
            row["binds"] = {
                "family_sha256": summary["family"]["sha256"] == want["family_sha256"],
                "record_sha256": [r["sha256"] for r in summary["records"]]
                == [want["record_sha256"]],
                "roots": summary["roots"] == want["roots"],
                "leaf_kinds": summary["kinds"] == want["leaf_kinds"],
            }
            row["cpu_hours_here"] = round(summary["cpu_seconds"] / 3600, 4)
            row["ratio_to_source"] = round(
                summary["cpu_seconds"] / 3600 / want["source_cpu_hours"], 3
            )
        expected_line = "REPLAY OK" if run["expect"] == "ok" else "REPLAY BAD"
        row["as_expected"] = (
            log["last_line"].startswith(expected_line)
            and (log["exit"] == 0) == (run["expect"] == "ok")
            and all(row.get("binds", {}).values())
        )
        runs.append(row)
    timed = [row for row in runs if "plan" in row]
    here = sum(row["summary"]["cpu_seconds"] for row in timed) / 3600
    source = sum(row["plan"]["source_cpu_hours"] for row in timed)
    full = json.loads(read_retained_bytes(SOURCE_REPLAY))
    ratio = here / source
    return {
        "schema": "wand125-replay4d-calibration/v1",
        "tool": "devtools.audit_wand125_closed_form calibrate",
        "note": plan["note"],
        "builds": builds,
        "binaries": binaries,
        "runs": runs,
        "all_as_expected": all(row["as_expected"] for row in runs),
        "timed_records": len(timed),
        "cpu_hours_here": round(here, 4),
        "source_cpu_hours": source,
        "ratio_to_source": round(ratio, 3),
        "source_cpu_hours_total": full["cpu_hours_total"],
        "full_replay_cpu_hours_here": round(full["cpu_hours_total"] * ratio),
        "precision": (
            "The source states cpu_hours to two decimals, so each record's source time is "
            "known to +-0.005 h (about 2%), and the ratio to about 1.3% over the two."
        ),
    }


# ------------------------------------------------------------------------------- main


def _write_or_check(receipt: Json, path: Path, *, check: bool) -> int:
    text = json.dumps(receipt, indent=1, ensure_ascii=False) + "\n"
    if check:
        current = path.read_text(encoding="utf-8") if path.is_file() else ""
        if current != text:
            print(f"{_rel(path)} is stale; rerun without --check", file=sys.stderr)
            return 1
        print(f"{_rel(path)}: current")
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(path, text)
    print(f"wrote {_rel(path)}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    hashes = commands.add_parser("hashes", help="recompute the source hashes at each revision")
    hashes.add_argument("--check", action="store_true")
    controls = commands.add_parser("controls", help="write the control inputs from a record")
    controls.add_argument("--interval", type=int, required=True)
    controls.add_argument("--region", required=True)
    controls.add_argument("--record", type=Path, required=True)
    controls.add_argument("--out", type=Path, required=True)
    plan = commands.add_parser("plan", help="print what a region replay must name and count")
    plan.add_argument("--interval", type=int, required=True)
    plan.add_argument("--region", required=True)
    calibrate = commands.add_parser("calibrate", help="bind the runs and price the replay")
    calibrate.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "hashes":
        receipt = hashes_receipt()
        for record in receipt["revisions"]:
            print(
                f"{record['commit'][:7]} replay4d {record['replay4d_version']['cargo_toml']}: "
                f"{record['covered_file_count']} files, {record['source_sha256'][:8]}..., "
                f"stated {record['stated_source_sha256'][:8]}..., equal {record['equal']}"
            )
        return _write_or_check(receipt, HASHES_RECEIPT, check=args.check)
    if args.command == "plan":
        print(json.dumps(region_plan(args.interval, args.region), indent=1))
        return 0
    if args.command == "controls":
        want = region_plan(args.interval, args.region)
        if sha256(args.record.read_bytes()) != want["record_sha256"]:
            print(f"{args.record} is not the record intervals.json names", file=sys.stderr)
            return 1
        manifest = write_controls(args.record, args.out)
        manifest["plan"] = {k: want[k] for k in ("interval", "region", "record", "bounds")}
        (args.out / "controls.json").write_text(json.dumps(manifest, indent=1) + "\n")
        print(json.dumps(manifest["files"]))
        return 0
    receipt = calibration_receipt()
    print(
        f"{receipt['timed_records']} records: {receipt['cpu_hours_here']} CPU-h here against "
        f"{receipt['source_cpu_hours']} at the source, ratio {receipt['ratio_to_source']}; "
        f"all as expected {receipt['all_as_expected']}"
    )
    return _write_or_check(receipt, CALIBRATION_RECEIPT, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
