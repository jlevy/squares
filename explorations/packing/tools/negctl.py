#!/usr/bin/env python3
"""Negative-control harness: prove a check fails when it should.

A check nobody has watched fail is not a check. Every guard in this directory was
negative-controlled by hand at least once -- corrupt a field, run the gate, confirm it
complains, put the field back -- and every one of those controls was then thrown away,
so the next person has only a claim that it was done.

This runs them from a file instead, so they are checked in, repeatable, and part of the
suite. It also removes the way the hand version goes wrong: restoring with
`git checkout` reverts to HEAD, which silently discards uncommitted work in the same
file.

Each control runs in its own throwaway copy of this directory, and the working tree is
never touched.
------------------------------------------------------------------------------------
The first version of this file corrupted tracked files IN PLACE and restored them
afterwards. That worked, and it cost more than it looked like it did:

  * Anything reading those files meanwhile saw the corruption. Seen once as
    `campaign/runner.py` failing on a dead link to a hypothesis that never existed. A
    spurious failure is the good outcome; a spurious pass is the other one. The
    `.gate-running` marker existed to narrow that window, and narrowing is not closing:
    an editor, a language server, a second agent or a second gate run could still read
    a half-corrupted tree.
  * The thirty controls had to run strictly one at a time, and so did the whole rest of
    the gate around them, because any concurrent step might read a corrupted file. That
    made this the gate's longest step at ~34s of a ~170s run -- on a ten-core machine
    where twenty-nine of the thirty controls are pure subprocess wait.
  * A crash between mutate and restore left the tree corrupt. `finally` covers
    exceptions; it does not cover SIGKILL or a power cut.

On APFS (and any filesystem with copy-on-write cloning) a copy of this directory costs
~0.2s and no disk, so isolation is cheaper than the workaround for the lack of it. One
clone per worker, reused across the controls that worker runs, `.venv` and the cargo
target symlinked back so nothing is rebuilt.

The gate can now run this step concurrently with every other step, and a control can no
longer corrupt anyone's checkout.

Control file format (YAML):

    controls:
    - name: outstanding defect without a bead
      file: defects.yaml
      replace: ["  bead: think-lksm\\n", ""]     # literal, must appear exactly once
      run: python3 tools/validate_schemas.py
      expect: "outstanding without a bead"

Usage:
    python3 tools/negctl.py tools/controls.yaml           # run them all
    python3 tools/negctl.py tools/controls.yaml -k bead   # only matching names
    python3 tools/negctl.py tools/controls.yaml -j 1      # serial, for debugging
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
# The REPOSITORY root, not this directory: one control targets ../../.flowmarkignore,
# because "is the generated view exempt from the Markdown formatter?" is a question
# about a file two levels up (D-027). Cloning only `explorations/packing` would put
# that control's target outside the sandbox and back in the real working tree, which
# is the one thing this file now exists to prevent. Clone the repo, work in the
# corresponding subdirectory.
REPO = ROOT.parent.parent
HERE = ROOT.relative_to(REPO)

# Never copied. `.git` and the two build artifacts are the whole weight of this tree
# (the virtualenv alone is ~440MB); everything a control mutates is a tracked source
# file. The virtualenv and the cargo target are symlinked back instead, so nothing is
# rebuilt and nothing is resolved again.
PRUNE = frozenset(
    {
        REPO / ".git",
        REPO / "node_modules",
        # The gate's own marker. A clone that carried it would make campaign/runner.py
        # refuse to start, and four controls drive the runner expecting a DIFFERENT
        # refusal -- so the control would "fire" for the wrong reason and prove nothing.
        REPO / HERE / ".gate-running",
        REPO / HERE / ".venv",
        REPO / HERE / "sqsearch/target",
    }
)
LINK_BACK = (HERE / ".venv", HERE / "sqsearch/target")
# Directories that must be walked into rather than bulk-copied, because something
# below them is pruned. Computed from PRUNE so the two cannot drift.
DESCEND = frozenset(a for p in PRUNE for a in p.parents if REPO in (a, *a.parents))


def _clone_into(src: Path, dst: Path) -> None:
    """Clone `src` to `dst`, descending only where a prune target lives below.

    Everything else goes in one `cp -Rc`, which asks APFS for a copy-on-write clone:
    near-instant, and it costs no disk until a block is written. `-c` is macOS-specific
    and fails loudly where the filesystem cannot clone, so the plain copy is the
    fallback rather than the default.
    """
    dst.mkdir(parents=True, exist_ok=True)
    bulk: list[str] = []
    for entry in src.iterdir():
        if entry in PRUNE:
            continue
        if entry in DESCEND:
            _clone_into(entry, dst / entry.name)
        else:
            bulk.append(str(entry))
    if not bulk:
        return
    if subprocess.run(
        ["cp", "-Rc", *bulk, str(dst)], capture_output=True, check=False
    ).returncode:
        subprocess.run(["cp", "-R", *bulk, str(dst)], capture_output=True, check=True)


def clone_tree(dest: Path) -> None:
    """A private, writable copy of the repository for one worker to corrupt."""
    _clone_into(REPO, dest)
    for rel in LINK_BACK:
        source = REPO / rel
        if not source.exists():
            continue
        link = dest / rel
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(source)


def run_one(c: dict, tree: Path) -> tuple[bool, str]:
    """Apply the mutation inside `tree`, run the command there, restore. (passed, why)."""
    work = tree / HERE
    target = (work / c["file"]).resolve()
    original = target.read_bytes()
    old, new = c["replace"]
    try:
        text = original.decode("utf-8")
        if text.count(old) != 1:
            return False, f"anchor appears {text.count(old)} times, expected exactly 1"
        target.write_text(text.replace(old, new, 1), encoding="utf-8")
        # check=False deliberately: a non-zero exit is the EXPECTED outcome here, and
        # inspecting it is this function's whole job.
        proc = subprocess.run(
            c["run"], shell=True, cwd=work, capture_output=True, text=True, check=False
        )
        output = proc.stdout + proc.stderr
        if proc.returncode == 0:
            return False, "command SUCCEEDED; the check did not fire"
        if c["expect"] not in output:
            return False, f"failed, but not with the expected message: {output.strip()[:120]}"
        return True, ""
    finally:
        # Restore inside the clone anyway: one worker runs several controls, and the
        # next one must not see the previous one's corruption.
        target.write_bytes(original)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    spec = yaml.safe_load((ROOT / sys.argv[1]).read_text(encoding="utf-8"))
    only = sys.argv[sys.argv.index("-k") + 1] if "-k" in sys.argv else None
    controls = [c for c in spec["controls"] if not only or only in c["name"]]
    if not controls:
        print("  no controls matched", file=sys.stderr)
        return 1

    requested = int(sys.argv[sys.argv.index("-j") + 1]) if "-j" in sys.argv else 0
    workers = requested or min(len(controls), os.cpu_count() or 4)

    failures: list[tuple[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="negctl-") as tmp:
        trees = [Path(tmp) / f"w{i}" for i in range(workers)]
        with ThreadPoolExecutor(max_workers=workers) as pool:
            list(pool.map(clone_tree, trees))

            def work(indexed: tuple[int, dict]) -> tuple[dict, bool, str]:
                i, c = indexed
                passed, detail = run_one(c, trees[i % workers])
                return c, passed, detail

            # Striped, not chunked: `pool.map` preserves order, so the report reads the
            # same however the work was split, and control i always lands in tree
            # i % workers -- which keeps a worker's controls from colliding on a file.
            for c, passed, detail in pool.map(work, enumerate(controls)):
                if not passed:
                    failures.append((c["name"], detail))

    for name, detail in failures:
        print(f"  CONTROL FAILED  {name}: {detail}", file=sys.stderr)
    if failures:
        print(
            f"{len(failures)} of {len(controls)} negative controls did not fire",
            file=sys.stderr,
        )
        return 1
    print(f"  {len(controls)} negative controls fire as expected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
