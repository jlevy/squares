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

Each control runs in a throwaway source snapshot, and the working tree is never touched.
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

On APFS a snapshot uses copy-on-write cloning. Elsewhere it falls back to a plain copy
of a bounded source surface: the packing tree without the literature archive or build
products, plus the root formatter ignore file. One snapshot per worker is reused across
controls; `.venv` and the cargo target are symlinked back so nothing is rebuilt.

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
import queue
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqpack.workers import worker_count

ROOT = Path(__file__).resolve().parent.parent
# The REPOSITORY root, not this directory: one control targets ../../.flowmarkignore,
# because "is the generated view exempt from the Markdown formatter?" is a question
# about a file two levels up (D-027). Cloning only `explorations/packing` would put
# that control's target outside the sandbox and back in the real working tree, which
# is the one thing this file now exists to prevent. Clone the repo, work in the
# corresponding subdirectory.
REPO = ROOT.parent.parent
HERE = ROOT.relative_to(REPO)

# Controls need the packing source, not the literature archive, the rest of the
# repository, or build products. `resources/README.md` is copied separately because the
# README link checker requires that one path. The virtualenv and cargo target are
# symlinked back so nothing is rebuilt or resolved again.
PRUNE = frozenset(
    {
        # The gate's own marker. A clone that carried it would make campaign/runner.py
        # refuse to start, and four controls drive the runner expecting a DIFFERENT
        # refusal -- so the control would "fire" for the wrong reason and prove nothing.
        ROOT / ".gate-running",
        ROOT / ".venv",
        ROOT / "resources",
        ROOT / "sqsearch/target",
    }
)
LINK_BACK = (Path(".venv"), Path("sqsearch/target"))
COPY_SEPARATELY = (ROOT / "resources/README.md", REPO / ".flowmarkignore")
SNAPSHOT_MAX_BYTES = 32 * 1024 * 1024
# Directories that must be walked into rather than bulk-copied, because something
# below them is pruned. Computed from PRUNE so the two cannot drift.
DESCEND = frozenset(a for p in PRUNE for a in p.parents if ROOT in (a, *a.parents))


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


def snapshot_source_bytes() -> int:
    """Bytes copied by the portable fallback, excluding linked build products."""
    total = sum(path.stat().st_size for path in COPY_SEPARATELY)
    for directory, names, files in os.walk(ROOT):
        parent = Path(directory)
        names[:] = [name for name in names if parent / name not in PRUNE]
        for name in files:
            path = parent / name
            if path in PRUNE or path.is_symlink():
                continue
            total += path.stat().st_size
    return total


def clone_tree(dest: Path) -> None:
    """A private, writable source snapshot for one worker to corrupt."""
    work = dest / HERE
    _clone_into(ROOT, work)

    resource_readme = work / "resources/README.md"
    resource_readme.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "resources/README.md", resource_readme)
    shutil.copy2(REPO / ".flowmarkignore", dest / ".flowmarkignore")

    for rel in LINK_BACK:
        source = ROOT / rel
        if not source.exists():
            continue
        link = work / rel
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
        env = os.environ.copy()
        # Every worker links the already-synced environment to avoid reinstalling the
        # scientific stack. Letting `uv run` sync that shared environment installs the
        # editable project from a temporary snapshot, which disappears after this run
        # and leaves the developer environment broken. Snapshot imports must still win.
        env["UV_NO_SYNC"] = "1"
        import_roots = (str(work / "src"), str(work))
        env["PYTHONPATH"] = os.pathsep.join(
            (*import_roots, env["PYTHONPATH"]) if env.get("PYTHONPATH") else import_roots
        )
        proc = subprocess.run(
            c["run"],
            shell=True,
            cwd=work,
            env=env,
            capture_output=True,
            text=True,
            check=False,
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
    workers = requested or worker_count(len(controls))

    source_bytes = snapshot_source_bytes()
    if source_bytes > SNAPSHOT_MAX_BYTES:
        print(
            f"negative-control snapshot source is {source_bytes} bytes; "
            f"cap is {SNAPSHOT_MAX_BYTES}",
            file=sys.stderr,
        )
        return 1
    print(
        f"  snapshot source {source_bytes / (1024 * 1024):.1f} MiB; "
        f"{workers} private worker trees"
    )

    failures: list[tuple[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="negctl-") as tmp:
        trees = [Path(tmp) / f"w{i}" for i in range(workers)]
        with ThreadPoolExecutor(max_workers=workers) as pool:
            list(pool.map(clone_tree, trees))

            # A tree is CHECKED OUT for the duration of one control and returned
            # afterwards, so no two running controls can ever share one.
            #
            # The obvious thing -- hand control i the tree at index i % workers -- is
            # wrong, and wrong in the way that only shows up under load: a pool does
            # not promise that item i runs on worker i % workers. It promises that
            # some free thread takes the next item. One slow control is enough for
            # item i and item i + workers to be in flight at the same moment, both
            # claiming the same tree, one restoring the file the other just corrupted.
            # Caught by running the gate at --jobs 10: the "defect log - count
            # disagreeing with the list" control stopped firing, because a neighbour
            # had already put defects.yaml back.
            available: queue.Queue[Path] = queue.Queue()
            for t in trees:
                available.put(t)

            def work(c: dict) -> tuple[dict, bool, str]:
                tree = available.get()
                try:
                    passed, detail = run_one(c, tree)
                finally:
                    available.put(tree)
                return c, passed, detail

            # `pool.map` preserves order, so the report reads the same however the
            # work happened to be split across trees.
            for c, passed, detail in pool.map(work, controls):
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
