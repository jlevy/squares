"""The integrity-ceremony ratchet is live: every form it counts is counted, every form it
must pass passes, the live tree agrees with its register, and the register cannot drift.

`ci-and-gates-rules`: a check nobody has watched fail is not a gate. The planted modules
below are strings handed to the scanner, so this file itself holds no site.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools import check_integrity_ceremony as guard
from sqpack.cli import validate

REGISTER = Path(guard.REGISTER)
REPO = Path(guard.REPO)

MINIMAL_REGISTER = (
    "mark: '(?i)(?<![a-z])"
    "(?:sha\\d*s?|(?:hex)?digests?|blake2[bs]?|md5|checksum|hashes)(?![a-z])'\n"
    "allowlist: []\n"
    "baseline:\n"
)


def _forms(source: str) -> list[str]:
    register = guard.parse_register(MINIMAL_REGISTER, "planted")
    return [site.form for site in guard.sites_in("planted.py", source, register.mark)]


@pytest.mark.parametrize(
    "source",
    [
        (
            "import hashlib\nfrom pathlib import Path\n"
            "MODULE = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()\n"
        ),
        "from pathlib import Path\nimport other\nPIN = d4.sha256(Path(other.__file__))\n",
        "KERNEL = sha(Path(frozen.__file__).read_bytes())\n",
    ],
)
def test_a_module_hashing_its_own_or_a_siblings_source_is_one_self_digest(source: str) -> None:
    assert _forms(source) == [guard.FORM_OWN]


@pytest.mark.parametrize(
    "source",
    [
        "require(record['tool_sha256'] == TOOL_SHA256, 'other bytes')\n",
        "if hashlib.sha256(raw).hexdigest() != expected:\n    raise ValueError\n",
        "ok = receipt.get('engine_sha256') == file_digest(engine)\n",
        "assert verification['verifier_sha256'] in allowed or digest == declared\n",
        "require(source['parent'] == {'path': ROOT, 'sha256': bridge.ROOT_SOURCE_SHA})\n",
        "assert len(value) != SHA256_LENGTH\n",
        "assert d4.INPUT_HASHES['cover'] == inputs['overlay']['cover_sha256']\n",
    ],
)
def test_a_comparison_naming_a_digest_is_counted(source: str) -> None:
    assert _forms(source) == [guard.FORM_COMPARE]


def test_a_self_digest_inside_a_comparison_is_two_sites() -> None:
    source = (
        "if sha(Path(frozen.__file__).read_bytes()) != FROZEN_SHA:\n    raise RefusalError\n"
    )
    assert sorted(_forms(source)) == sorted([guard.FORM_COMPARE, guard.FORM_OWN])


@pytest.mark.parametrize(
    "source",
    [
        # Git identity is the pattern OR-16 asks for.
        "if row['git_blob'] != blob:\n    refuse(path)\n",
        "revision = git('rev-parse', 'HEAD')\nassert revision == recorded\n",
        # A record of a digest, with nothing compared, is provenance rather than a gate.
        "receipt['module_sha256'] = hashlib.sha256(data).hexdigest()\n",
        # `is` and `in` are not comparisons of a value; a set of keys is a schema check.
        "if expected_sha256 is not None:\n    pass\n",
        "assert set(source) == {'url', 'expected_sha256', 'observed_sha256'}\n",
        "assert 'sha256' in document\n",
        # Words that merely contain the letters stay out.
        "assert shape == (3, 4) and shared != other and shard == 'A'\n",
        # `__file__` used for a path, not hashed.
        "REPO = Path(__file__).resolve().parents[2]\nassert REPO == expected\n",
        # Documentation is not code.
        '"""A docstring saying hashlib.sha256(Path(__file__)) == MODULE_SHA256."""\n',
    ],
)
def test_git_identity_records_and_non_digest_comparisons_pass(source: str) -> None:
    assert _forms(source) == []


def test_a_file_that_mentions_no_digest_is_skipped_without_parsing() -> None:
    register = guard.parse_register(MINIMAL_REGISTER, "planted")
    assert guard.sites_in("planted.py", "this is not python at all (\n", register.mark) == []


# ---------------------------------------------------------------------------
# The register and the ratchet
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("mark: '('\n", "regular expression"),
        ("- a list\n", "mapping"),
        (
            MINIMAL_REGISTER.replace(
                "allowlist: []",
                "allowlist:\n  - path: a.py\n    kind: ours\n    boundary: us\n",
            ),
            "no kind",
        ),
        (
            MINIMAL_REGISTER.replace(
                "allowlist: []", "allowlist:\n  - path: a.py\n    boundary: us\n"
            ),
            "exactly path, kind and boundary",
        ),
        (
            MINIMAL_REGISTER.replace(
                "allowlist: []",
                "allowlist:\n  - path: a.py\n    kind: download\n    boundary: ''\n",
            ),
            "non-empty",
        ),
        (MINIMAL_REGISTER + "  a.py: 0\n", "positive count"),
        (
            MINIMAL_REGISTER.replace(
                "allowlist: []",
                "allowlist:\n  - path: a.py\n    kind: download\n    boundary: x\n",
            )
            + "  a.py: 1\n",
            "both allowlisted",
        ),
    ],
)
def test_a_malformed_register_is_refused(text: str, message: str) -> None:
    with pytest.raises(guard.RegisterError, match=message):
        guard.parse_register(text, "planted")


def _plant(repo: Path, files: dict[str, str]) -> None:
    for name, source in files.items():
        target = repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source, encoding="utf-8")


ONE_SITE = "assert record['tool_sha256'] == TOOL_SHA256\n"
TWO_SITES = ONE_SITE + "assert kernel['kernel_sha256'] == KERNEL_SHA256\n"


def _register(allowlist: str = "[]", baseline: str = "") -> guard.Register:
    text = MINIMAL_REGISTER.replace("allowlist: []", f"allowlist: {allowlist}") + baseline
    return guard.parse_register(text, "planted")


def test_a_tree_matching_its_baseline_has_no_finding(tmp_path: Path) -> None:
    _plant(tmp_path, {"tool.py": TWO_SITES, "clean.py": "x = 1\n"})
    by_file, unreadable, read = guard.scan(tmp_path, _register(baseline="  tool.py: 2\n"))
    assert unreadable == []
    assert read == 2
    assert list(by_file) == ["tool.py"]
    assert guard.ratchet(by_file, _register(baseline="  tool.py: 2\n"), tmp_path) == []


def test_growth_and_a_new_file_are_findings_and_a_fall_is_not(tmp_path: Path) -> None:
    _plant(tmp_path, {"grew.py": TWO_SITES, "new.py": ONE_SITE, "fell.py": ONE_SITE})
    register = _register(baseline="  grew.py: 1\n  fell.py: 2\n  gone.py: 1\n")
    by_file, _, _ = guard.scan(tmp_path, register)
    faults = guard.ratchet(by_file, register, tmp_path)
    headline = [fault for fault in faults if not fault.startswith("    ")]
    named = [fault.split(":")[0] for fault in headline]
    # Removing ceremony costs no bookkeeping: a fall, or a file emptied, is no finding.
    assert named == ["grew.py", "new.py"]
    assert "the baseline records 1" in headline[0]
    assert "only falls" in headline[0]
    assert "does not record" in headline[1]
    assert guard.slack(by_file, register) == ["fell.py", "gone.py"]
    assert guard.growth(by_file, register) == [
        "grew.py: 2 site(s), the baseline records 1",
        "new.py: 1 site(s), the baseline records 0",
    ]
    # Growth lists every site in the file, so the finding is attributed.
    listed = [fault for fault in faults if fault.startswith("    grew.py:")]
    assert len(listed) == 2


def test_test_files_are_not_scanned(tmp_path: Path) -> None:
    _plant(
        tmp_path,
        {
            "tool.py": ONE_SITE,
            "tests/test_tool.py": TWO_SITES,
            "pkg/tests/helper.py": ONE_SITE,
            "test_top.py": ONE_SITE,
            "conftest.py": ONE_SITE,
        },
    )
    by_file, _, read = guard.scan(tmp_path, _register())
    assert list(by_file) == ["tool.py"]
    assert read == 1


def test_an_allowlisted_file_must_exist_and_hold_a_site(tmp_path: Path) -> None:
    _plant(tmp_path, {"packet.py": ONE_SITE, "empty.py": "x = 1\n"})
    allowlist = (
        "\n  - path: packet.py\n    kind: download\n    boundary: a packet\n"
        "  - path: empty.py\n    kind: download\n    boundary: nothing\n"
        "  - path: missing.py\n    kind: download\n    boundary: gone\n"
    )
    register = _register(allowlist=allowlist)
    by_file, _, _ = guard.scan(tmp_path, register)
    faults = guard.ratchet(by_file, register, tmp_path)
    assert [fault.split(":")[0] for fault in faults] == ["empty.py", "missing.py"]
    assert "holds no site" in faults[0]
    assert "no such file" in faults[1]


def test_update_lowers_the_baseline_keeps_the_header_and_refuses_growth(tmp_path: Path) -> None:
    _plant(tmp_path, {"packing/devtools/tool.py": ONE_SITE})
    register_path = tmp_path / "packing/devtools/integrity-ceremony.yaml"
    header = "# kept\n" + MINIMAL_REGISTER.replace("baseline:\n", "")
    register_path.write_text(
        header + "baseline:\n  packing/devtools/tool.py: 2\n", encoding="utf-8"
    )
    register = guard.load_register(register_path)
    by_file, _, _ = guard.scan(tmp_path, register)
    assert guard.update(register_path, by_file, register) == []
    rewritten = register_path.read_text(encoding="utf-8")
    assert rewritten.startswith(header)
    assert rewritten.endswith("baseline:\n  packing/devtools/tool.py: 1\n")
    assert guard.ratchet(by_file, guard.load_register(register_path), tmp_path) == []

    _plant(tmp_path, {"packing/devtools/tool.py": TWO_SITES})
    by_file, _, _ = guard.scan(tmp_path, guard.load_register(register_path))
    faults = guard.update(register_path, by_file, guard.load_register(register_path))
    assert len(faults) == 2
    assert "does not absorb growth" in faults[0]
    assert register_path.read_text(encoding="utf-8") == rewritten


def test_an_unreadable_file_is_a_finding(tmp_path: Path) -> None:
    _plant(tmp_path, {"broken.py": "sha256 = (\n"})
    _, unreadable, _ = guard.scan(tmp_path, _register())
    assert len(unreadable) == 1
    assert unreadable[0].startswith("broken.py: cannot be read as Python")


def test_the_command_reports_and_exits_as_the_gate_expects(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _plant(tmp_path, {"tool.py": ONE_SITE})
    register_path = tmp_path / "register.yaml"
    register_path.write_text(MINIMAL_REGISTER + "  tool.py: 1\n", encoding="utf-8")
    assert guard.main(["--repo", str(tmp_path), "--register", str(register_path)]) == 0
    assert "none above the baseline" in capsys.readouterr().out
    _plant(tmp_path, {"tool.py": TWO_SITES})
    assert guard.main(["--repo", str(tmp_path), "--register", str(register_path)]) == 1
    out = capsys.readouterr().out
    assert out.startswith("FAIL  tool.py: 2 site(s), the baseline records 1")
    assert (
        guard.main(["--repo", str(tmp_path), "--register", str(register_path), "--inventory"])
        == 0
    )
    assert "2 counted site(s) in 1 file(s)" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# The live tree, and the gate
# ---------------------------------------------------------------------------


def test_the_live_tree_agrees_with_the_register() -> None:
    """The real contract: every allowlisted file names a boundary and holds a site, and no
    counted file is above its baseline. This is what the gate step runs."""
    register = guard.load_register(REGISTER)
    by_file, unreadable, read = guard.scan(REPO, register)
    assert unreadable == []
    # Tests are not scanned; the tools alone are several hundred files.
    assert read > 500
    assert guard.ratchet(by_file, register, REPO) == []
    # The guard is scanned like everything else and holds no site.
    assert "packing/devtools/check_integrity_ceremony.py" not in by_file


def test_the_gate_step_is_fast_narrow_and_reachable() -> None:
    (step,) = [s for s in validate.STEPS if s.name.startswith("integrity ceremony")]
    assert step.fast, "the ratchet belongs to the fast tier"
    assert not step.broad, "and to the edit tier, which drops broad steps"
    for path in (
        "packing/devtools/check_integrity_ceremony.py",
        "packing/devtools/integrity-ceremony.yaml",
        "packages/workbench/tools/workbench_tools/poster.py",
        "packing/pyproject.toml",
    ):
        assert step.reachable_from(path), path
    assert not step.reachable_from(
        "docs/project/reviews/review-2026-10-03-integrity-ceremony-audit.md"
    )
