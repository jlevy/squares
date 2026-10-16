"""Stage Evan Daniel's Lean reduction for T-064 from retained bytes, ready to build.

The reduction is ``SquarePacking.Bentz.bentz_of_valid7 : Valid7 -> forall k, 6 <= k ->
minSide (k ^ 2 - 3) = k`` in ``s12/lean/Sqpack/Bentz.lean`` of evand/square-packing at
``08e8a5fa``. Its import closure is ten project modules and Mathlib. Nine of the modules
and the three lake files are retained in the September 26 and October 1 evand packets as
the upstream Git blobs; ``S32Data.lean`` is not retained, and is regenerated here by the
source's own ``gen_s32_data.py`` from the retained s(32) cover, as the s(13) build was.
``BentzData.lean``, the cover transcribed into Lean, is retained and is also regenerated
by ``gen_bentz_data.py`` from the retained cover and family, which is the source's
``verify.sh`` check that the Lean data are these files.

``stage --out DIR [--json RECEIPT]`` writes ``DIR/s12/lean/`` and refuses any file whose
Git blob is not the one ``UPSTREAM`` names from the ``08e8a5fa`` tree, regenerated files
included. It also writes ``AxiomsBentz.lean``, the probe that prints the theorem, the
hypothesis and the axioms, and scans the staged sources for the tokens that would let a
proof skip the kernel. It runs the two generators under this interpreter and builds
nothing.

The build needs what this container lacks (see the 2 October review of Hosono's
checker): elan with ``leanprover/lean4:v4.33.1``, about 2.5 GB unpacked, and Mathlib
``0df444a3`` from its cache, about 6.6 GB of oleans, which ``import Mathlib`` maps whole.
On a host with them, from ``DIR/s12/lean``::

    lake exe cache get
    python -m devtools.replay_receipt --receipt R/build_bentz.log ... -- lake build Sqpack.Bentz
    python -m devtools.replay_receipt --receipt R/axioms_bentz.log ... \\
        -- lake env lean AxiomsBentz.lean

The axiom receipt must read ``[propext, Classical.choice, Quot.sound]`` for
``bentz_of_valid7``.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

from strif import atomic_write_text

from devtools.retained_data import git_blob

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
SEP26 = WEB / "evand-square-packing-2026-09-26/square-packing/s12"
OCT01 = WEB / "evand-square-packing-2026-10-01/source/s12"
PIN = "08e8a5faa54c0a7b0bb1cb0134c77d3565ce40c5"
#: Git blobs of the build's inputs in ``s12/`` at the pin, from ``git ls-tree``.
UPSTREAM = {
    "lean/lean-toolchain": "a8afa7d1b02d96f0671eba854a8dc4b416beb473",
    "lean/lakefile.toml": "3d90112e8d0f492f5d0d18d3a64e57fc04c932e0",
    "lean/lake-manifest.json": "43e6e5aafbfd523d9ff7b16869798d739d1cd16c",
    "lean/Sqpack/Basic.lean": "cbfe567fe20c6b81899bd1ed6eb8cbd8611c090b",
    "lean/Sqpack/Chord.lean": "913bd7dfd7d8804315ba6adf132f95dddd768cc6",
    "lean/Sqpack/ZeroMargin.lean": "7d40021f619994ac900178c9a7e94f8cb4dcc27f",
    "lean/Sqpack/D4.lean": "d599b89dba509df9ab33adf2273249a2bc7fa00e",
    "lean/Sqpack/Cover.lean": "4fd6f59fc9c5943f5f884598e04820fe2ad67395",
    "lean/Sqpack/S32Data.lean": "b8ea5d9487edc11cb7c801af7f4c1c4724f79be0",
    "lean/Sqpack/S32.lean": "065a2c43515c363fbfce38bb7efc2e85d4d47578",
    "lean/Sqpack/MixedMeasure.lean": "196d723865ed62532795cbe229f3eaf2af525079",
    "lean/Sqpack/BentzData.lean": "74cf901dc4e8bbb321511e7a647229cdcae33210",
    "lean/Sqpack/Bentz.lean": "fe5cd3b7cc6fc55eaa5c2a3436925db90fef215f",
    "lean/scripts/gen_s32_data.py": "7b32805f22a9feeab0400460913582c949a861a6",
    "lean/scripts/gen_bentz_data.py": "62fbcc3b2c18197b67af5ab4da558607a1f0566d",
    "certificates/k2m3/L4_k02_box7.txt": "",
    "certificates/k2m3/L4_k02_family.txt": "",
}
#: Where each retained input is, relative to ``s12/`` of its packet; ``.gz`` is gunzipped.
RETAINED = {
    **{
        name: SEP26 / name
        for name in (
            "lean/lean-toolchain",
            "lean/lakefile.toml",
            "lean/lake-manifest.json",
            "lean/Sqpack/Basic.lean",
            "lean/Sqpack/Chord.lean",
            "lean/Sqpack/ZeroMargin.lean",
            "lean/Sqpack/D4.lean",
            "lean/Sqpack/Cover.lean",
            "lean/Sqpack/S32.lean",
            "lean/scripts/gen_s32_data.py",
        )
    },
    "certificates/s32/s32_closed_cover_6.txt": SEP26
    / "certificates/s32/s32_closed_cover_6.txt.gz",
    **{
        name: OCT01 / name
        for name in (
            "lean/Sqpack/MixedMeasure.lean",
            "lean/Sqpack/BentzData.lean",
            "lean/Sqpack/Bentz.lean",
            "lean/scripts/gen_bentz_data.py",
            "certificates/k2m3/L4_k02_box7.txt",
            "certificates/k2m3/L4_k02_family.txt",
        )
    },
}
#: The SHA-256 of the two k2m3 data files, from the bundle's ``SHA256SUMS``.
DATA_SHA256 = {
    "certificates/k2m3/L4_k02_box7.txt": (
        "c0a6750997897c21ffc693df6df97f89a248dd9eb588a2fe2b83bf359793694b"
    ),
    "certificates/k2m3/L4_k02_family.txt": (
        "3f4771d3fbb5400ba43e993b44a966eb654adb32481ddb05719b4db3ed6a0768"
    ),
}
THEOREM = "SquarePacking.Bentz.bentz_of_valid7"
PROBE = f"""import Sqpack.Bentz

#check @{THEOREM}
#print SquarePacking.Bentz.Valid7
#print SquarePacking.minSide
#print SquarePacking.Packs
#print axioms {THEOREM}
#print axioms SquarePacking.Bentz.valid_of_valid7
#print axioms SquarePacking.Bentz.box7Cover_measure
#print axioms SquarePacking.Bentz.famCover_total
#print axioms SquarePacking.Bentz.mass_shift
"""
#: Tokens by which a Lean source could avoid the kernel or assume what it proves.
ESCAPES = (
    r"\bsorry\b",
    r"^\s*axiom\b",
    r"\bnative_decide\b",
    r"\bofReduceBool\b",
    r"\bimplemented_by\b",
    r"@\[extern",
    r"debug\.skipKernelTC",
    r"\bunsafe\b",
)


def _read(path: Path) -> bytes:
    data = path.read_bytes()
    return gzip.decompress(data) if path.suffix == ".gz" else data


def _generate(s12: Path, argv: list[str]) -> str:
    done = subprocess.run(
        [sys.executable, *argv], cwd=s12, capture_output=True, text=True, check=False
    )
    if done.returncode:
        msg = f"{argv[0]} failed: {done.stderr.strip()}"
        raise SystemExit(msg)
    return done.stdout.strip()


def strip_comments(text: str) -> str:
    """Lean source without its comments: nested ``/- -/`` blocks and ``--`` lines."""
    out: list[str] = []
    depth, i = 0, 0
    while i < len(text):
        pair = text[i : i + 2]
        if pair == "/-":
            depth, i = depth + 1, i + 2
        elif depth and pair == "-/":
            depth, i = depth - 1, i + 2
        elif depth:
            i += 1
        elif pair == "--":
            end = text.find("\n", i)
            i = len(text) if end < 0 else end
        else:
            out.append(text[i])
            i += 1
    return "".join(out)


def escapes(lean: Path) -> dict[str, int]:
    """Occurrences of each kernel-escape token in the staged sources, comments aside."""
    counts: dict[str, int] = dict.fromkeys(ESCAPES, 0)
    for path in sorted(lean.glob("Sqpack/**/*.lean")):
        text = strip_comments(path.read_text(encoding="utf-8"))
        for token in ESCAPES:
            counts[token] += len(re.findall(token, text, flags=re.MULTILINE))
    return counts


def stage(out: Path) -> dict[str, object]:
    """Write ``out/s12`` from retained bytes, regenerate the two data files, check blobs."""
    s12 = out / "s12"
    if s12.exists():
        shutil.rmtree(s12)
    problems: list[str] = []
    for name, source in RETAINED.items():
        target = s12 / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(_read(source))
    for name, digest in DATA_SHA256.items():
        if hashlib.sha256((s12 / name).read_bytes()).hexdigest() != digest:
            problems.append(f"{name} is not the bundle's file")
    retained_bentz_data = (s12 / "lean/Sqpack/BentzData.lean").read_bytes()
    logs = {
        "gen_s32_data": _generate(
            s12, ["lean/scripts/gen_s32_data.py", "certificates/s32/s32_closed_cover_6.txt"]
        ),
    }
    search = s12 / "regenerate"
    (search / "qx2_data").mkdir(parents=True)
    for name in DATA_SHA256:
        shutil.copyfile(s12 / name, search / "qx2_data" / Path(name).name)
    logs["gen_bentz_data"] = _generate(
        s12,
        [
            "lean/scripts/gen_bentz_data.py",
            "--search",
            "regenerate",
            "--out",
            "regenerate/BentzData.lean",
        ],
    )
    if (search / "BentzData.lean").read_bytes() != retained_bentz_data:
        problems.append(
            "BentzData.lean regenerated from the cover differs from the retained one"
        )
    shutil.rmtree(search)
    blobs: dict[str, str] = {}
    for name, want in UPSTREAM.items():
        blobs[name] = git_blob((s12 / name).read_bytes())
        if want and blobs[name] != want:
            problems.append(f"{name} is blob {blobs[name][:12]}, upstream {want[:12]}")
    lean = s12 / "lean"
    (lean / "AxiomsBentz.lean").write_text(PROBE, encoding="utf-8")
    found = escapes(lean)
    problems += [
        f"{count} x {token} in the staged sources" for token, count in found.items() if count
    ]
    return {
        "kind": "evand-bentz-lean-stage/v1",
        "ok": not problems,
        "problems": problems,
        "upstream": f"evand/square-packing {PIN} s12/",
        "toolchain": (lean / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "blobs": blobs,
        "regenerated": logs,
        "kernel_escapes": found,
        "probe": "lean/AxiomsBentz.lean",
        "theorem": THEOREM,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--out", type=Path, required=True, help="directory to stage s12/ in")
    parser.add_argument("--json", type=Path, help="also write the receipt here")
    args = parser.parse_args(argv)
    receipt = stage(args.out)
    text = json.dumps(receipt, indent=2) + "\n"
    if args.json:
        atomic_write_text(args.json, text)
    print(text, end="")
    print("BENTZ_LEAN_STAGED" if receipt["ok"] else "BENTZ_LEAN_STAGE_FAILED")
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
