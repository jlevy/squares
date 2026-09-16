"""The guard against JavaScript in Python is live, and so is the check on probe files.

`ci-and-gates-rules`: a check nobody has watched fail is not a gate. So every form
`devtools.check_no_embedded_js` exists to refuse is planted in a module here and must be
reported, every form it exists to require must pass, and every way the ratchet can drift
must fail. `devtools.check_probes` gets the same treatment over a planted probe tree.

The JavaScript planted below is read from a probe file,
`tests/probes/no_embedded_js/planted.js`. A test that wrote it as a Python string would be
the violation it tests for, and the guard would -- correctly -- refuse this file.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from nodejs_wheel import node

from devtools import check_no_embedded_js as guard
from devtools import check_probes
from sqpack.cli import validate
from sqpack.probes import applied, probe

PROBES = Path(__file__).resolve().parent / "probes"
PLANTED_SOURCE = probe(PROBES, "no_embedded_js/planted")
#: The planted expression alone, without its comment or the formatter's semicolon.
PLANTED = next(
    line for line in PLANTED_SOURCE.splitlines() if line and not line.startswith("//")
).removesuffix(";")
POLICY = guard.load_policy()

#: A script argument with no JavaScript signature in it, so rule 1 is tested on its own.
NEUTRAL = "planted"


def _sites(source: str) -> list[guard.Site]:
    return guard.scan_source("planted.py", source, POLICY)


def _rules(source: str) -> list[str]:
    return [site.rule for site in _sites(source)]


def test_the_planted_probe_is_javascript_by_the_guards_own_signatures() -> None:
    """Without this, every rule-2 case below could pass by planting nothing."""
    assert _javascript(PLANTED)


@pytest.mark.parametrize(
    ("method", "arguments"),
    [
        ("evaluate", "{script}"),
        ("evaluate", "expression={script}"),
        ("evaluate_handle", "{script}, 1"),
        ("evaluate_all", "{script}"),
        ("eval_on_selector", "'#stage', {script}"),
        ("eval_on_selector_all", "'li', expression={script}"),
        ("wait_for_function", "{script}, timeout=5"),
        ("add_init_script", "{script}"),
        ("add_init_script", "script={script}"),
    ],
)
def test_a_string_literal_script_argument_fails_for_every_method(
    method: str, arguments: str
) -> None:
    source = f"page.{method}({arguments.format(script=repr(NEUTRAL))})\n"
    assert _rules(source) == ["script argument"]


@pytest.mark.parametrize(
    "script",
    [
        "f'planted{n}'",
        "'planted ' + suffix",
        "prefix + 'planted'",
        "'planted %s' % n",
        "'planted {}'.format(n)",
        "textwrap.dedent('planted')",
        "SCRIPT",
        "SCRIPT.replace('a', 'b')",
        "probe(ROOT, 'tool/name').replace('a', 'b')",
        "probe(ROOT, 'tool/name') + ';'",
        "'planted' if flag else probe(ROOT, 'tool/name')",
    ],
)
def test_a_built_script_argument_fails(script: str) -> None:
    source = (
        "import textwrap\n"
        "from sqpack.probes import probe\n"
        f"SCRIPT = {NEUTRAL!r}\n"
        f"page.evaluate({script})\n"
    )
    assert _rules(source) == ["script argument"]


def test_a_javascript_string_fails_wherever_it_is_written() -> None:
    assert _rules(f"SCRIPT = {PLANTED!r}\n") == ["JavaScript string"]
    assert _rules(f"def build():\n    return [{PLANTED!r}]\n") == ["JavaScript string"]


def _javascript(text: str) -> bool:
    return any(signature.search(text) for signature in POLICY.signatures)


def test_a_javascript_string_split_across_pieces_is_one_site() -> None:
    """Split where neither piece is JavaScript on its own, so only the joined text is."""
    middle = next(
        index
        for index in range(1, len(PLANTED))
        if not _javascript(PLANTED[:index]) and not _javascript(PLANTED[index:])
    )
    head, tail = PLANTED[:middle], PLANTED[middle:]
    assert _rules(f"SCRIPT = {head!r} + {tail!r}\n") == ["JavaScript string"]
    assert _rules(f"SCRIPT = ({head!r}\n    {tail!r})\n") == ["JavaScript string"]
    assert _rules(f"SCRIPT = f{head + '{value}' + tail!r}\n") == ["JavaScript string"]


def test_a_javascript_string_passed_as_a_script_counts_once() -> None:
    assert _rules(f"page.evaluate({PLANTED!r})\n") == ["JavaScript string"]


def test_a_script_body_built_in_python_fails() -> None:
    statement = "start()"
    html = f"<script>{statement}</script>"
    typed = f"<script type='module'>{statement}</script>"
    assert _rules(f"HTML = {html!r}\n") == ["script body"]
    assert _rules(f"HTML = {typed!r}\n") == ["script body"]
    assert _rules(f"HTML = f{html.replace(')', ') + {n}')!r}\n") == ["script body"]


@pytest.mark.parametrize(
    "source",
    [
        "from sqpack.probes import probe\npage.evaluate(probe(ROOT, 'tool/name'), {'n': 1})\n",
        (
            "from sqpack.probes import probe\nSCRIPT = probe(ROOT, 'tool/name')\n"
            "page.wait_for_function(SCRIPT, timeout=5)\n"
        ),
        "import sqpack.probes as probes\npage.evaluate(probes.probe(ROOT, 'tool/name'))\n",
        "from sqpack import probes\npage.evaluate_handle(probes.probe(ROOT, 'tool/name'))\n",
        (
            "from sqpack.probes import applied, probe\n"
            "page.add_init_script(applied(probe(ROOT, 'tool/name'), {'mode': 'full'}))\n"
        ),
        "from workbench_tools.probes import probe\npage.evaluate(probe('panel/slots'))\n",
        "page.add_init_script(path=ROOT / 'tool' / 'init.js')\n",
        "HTML = f'<script>{source}</script>'\n",
        "HTML = '<script>' + source + '</script>'\n",
        'PATTERN = \'<script id="data" type="application/json">(.*?)</script>\'\n',
        "def run(page, script):\n    return page.evaluate(script)\n",
        "value = polynomial.evaluate(point)\n",
    ],
)
def test_the_probe_loader_and_non_scripts_pass(source: str) -> None:
    assert _sites(source) == []


def test_documentation_is_not_a_site() -> None:
    documented = f'"""A module.\n\n    {PLANTED}\n"""\n\n\nclass A:\n    """{PLANTED}"""\n'
    assert _sites(documented) == []


def test_applied_calls_the_probe_with_its_argument_serialised() -> None:
    """Run in Node, which is the only honest way to say what the script does. The probe's
    leading comment and trailing semicolon are both in the file, and both have to survive
    being wrapped; the line separator is the character JSON allows and older JavaScript
    did not."""
    argument = {"n": [1, 2.5, None, "\u2028", "</script>"]}
    script = applied(probe(PROBES, "no_embedded_js/echo"), argument)
    done = node(
        ["--print", script], return_completed_process=True, capture_output=True, text=True
    )
    assert done.returncode == 0, done.stderr
    assert json.loads(str(done.stdout)) == argument


def test_applied_without_an_argument_passes_nothing_rather_than_null() -> None:
    """An init probe is called with no argument, so a default parameter still applies."""
    script = applied(probe(PROBES, "no_embedded_js/echo"))
    done = node(
        ["--print", script], return_completed_process=True, capture_output=True, text=True
    )
    assert done.returncode == 0, done.stderr
    assert str(done.stdout).strip() == "undefined"
    assert applied(probe(PROBES, "no_embedded_js/echo"), None).endswith(")(null);\n")


def test_the_loader_refuses_names_outside_its_root(tmp_path: Path) -> None:
    for name in ("../escape", "/absolute", "tool/name.js", ""):
        with pytest.raises(ValueError, match="not a probe name"):
            probe(tmp_path, name)
    # A variable, not a literal: `devtools.check_probes` requires every literal handed to the
    # loader beside `tests/probes` to name a file, and this one deliberately names none.
    absent = "tool/absent"
    with pytest.raises(FileNotFoundError, match=str(tmp_path)):
        probe(tmp_path, absent)


# -- the ratchet ------------------------------------------------------------------------


def _found(path: str, count: int) -> dict[str, list[guard.Site]]:
    return {path: [guard.Site(path, line, "JavaScript string", "x") for line in range(count)]}


def test_the_ratchet_accepts_a_listed_file_at_its_count() -> None:
    assert guard.ratchet(_found("a.py", 2), {"a.py": guard.Entry(2, "think-abcd")}) == []


def test_the_ratchet_refuses_an_unlisted_file() -> None:
    (fault, *sites) = guard.ratchet(_found("a.py", 1), {})
    assert "not on the allowlist" in fault
    assert len(sites) == 1


def test_the_ratchet_refuses_a_count_that_grew() -> None:
    faults = guard.ratchet(_found("a.py", 3), {"a.py": guard.Entry(2, "think-abcd")})
    assert "may only shrink" in faults[0]


def test_the_ratchet_refuses_a_shrink_that_was_not_recorded() -> None:
    faults = guard.ratchet(_found("a.py", 1), {"a.py": guard.Entry(2, "think-abcd")})
    (fault,) = faults
    assert fault.startswith("a.py: 1 site(s), the allowlist records 2 (think-abcd).")
    assert fault.endswith("Lower the entry to 1 so the ratchet holds.")


def test_the_ratchet_refuses_a_listed_file_that_no_longer_offends() -> None:
    faults = guard.ratchet({}, {"a.py": guard.Entry(2, "think-abcd")})
    (fault,) = faults
    assert fault.startswith("a.py: no JavaScript left, the allowlist still records 2")
    assert fault.endswith("Remove the entry.")


def test_a_policy_without_signatures_is_refused(tmp_path: Path) -> None:
    policy = tmp_path / "policy.yaml"
    policy.write_text("signatures: []\nscript_tag: x\nscript_code: x\n", encoding="utf-8")
    with pytest.raises(guard.PolicyError, match="non-empty"):
        guard.load_policy(policy)


def test_the_command_fails_on_a_planted_module_and_passes_once_it_is_listed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """End to end, over a tree with no git, which is how the negative controls run it."""
    (tmp_path / "tool.py").write_text(f"page.evaluate({PLANTED!r})\n", encoding="utf-8")
    (tmp_path / "clean.py").write_text(
        "from sqpack.probes import probe\npage.evaluate(probe(ROOT, 'tool/name'))\n",
        encoding="utf-8",
    )
    policy = tmp_path / "policy.yaml"
    text = guard.POLICY.read_text(encoding="utf-8")
    policy.write_text(text.split("\nallowlist:")[0] + "\nallowlist: []\n", encoding="utf-8")
    arguments = ["--repo", str(tmp_path), "--policy", str(policy)]

    assert guard.main(arguments) == 1
    assert "tool.py: 1 site(s) of JavaScript in Python" in capsys.readouterr().out

    listed = "\nallowlist:\n  - path: tool.py\n    sites: 1\n    bead: think-abcd\n"
    policy.write_text(text.split("\nallowlist:")[0] + listed, encoding="utf-8")
    assert guard.main(arguments) == 0
    assert "none was added" in capsys.readouterr().out


def test_the_guard_runs_in_the_edit_tier_and_on_every_pull_request() -> None:
    (step,) = [s for s in validate.STEPS if s.name.startswith("browser code lives in files")]
    assert {"edit", "checks"} <= set(step.tags.split(", "))


# -- the probe check ----------------------------------------------------------------------


def _probe_tree(root: Path) -> Path:
    tree = root / "tool" / "probes" / "group"
    tree.mkdir(parents=True)
    shutil.copy(PROBES / "no_embedded_js" / "planted.js", tree / "used.js")
    (root / "tool" / "caller.py").write_text(
        "from sqpack.probes import probe\nprobe(ROOT, 'group/used')\n", encoding="utf-8"
    )
    return tree


def test_the_probe_check_passes_a_used_function(tmp_path: Path) -> None:
    _probe_tree(tmp_path)
    assert check_probes.faults(tmp_path) == ([], 1, 1)


def test_the_probe_check_refuses_an_orphan_a_non_function_and_a_missing_name(
    tmp_path: Path,
) -> None:
    tree = _probe_tree(tmp_path)
    shutil.copy(tree / "used.js", tree / "orphan.js")
    (tree / "value.js").write_text('"a string";\n', encoding="utf-8")
    (tree / "broken.js").write_text("(\n", encoding="utf-8")
    (tmp_path / "tool" / "caller.py").write_text(
        "from sqpack.probes import probe\n"
        "NAMES = ('group/used', 'group/value', 'group/broken', 'group/absent')\n",
        encoding="utf-8",
    )
    found, count, trees = check_probes.faults(tmp_path)
    assert (count, trees) == (4, 1)
    assert any(f.startswith("tool/probes/group/broken.js: does not evaluate") for f in found)
    assert "tool/probes/group/value.js: evaluates to a string, not a function" in found
    assert "tool/probes/group/orphan.js: no Python file beside tool/probes names it" in found
    absent = "tool/probes/group/absent.js: named by a Python file beside tool/probes"
    assert f"{absent}, and no such file" in found
    assert len(found) == 4


def _names(have: set[str], **sources: str) -> tuple[list[str], list[str]]:
    """Missing and unnamed probes for callers given as `file_name=source`."""
    callers = {name: check_probes.read_caller(source, name) for name, source in sources.items()}
    return check_probes.name_faults(callers, have)


HAVE = {"stage/visible-count"}


@pytest.mark.parametrize(
    "source",
    [
        "from sqpack.probes import probe\nprobe(ROOT, 'newgroup/zz_missing')\n",
        "from workbench_tools.probes import probe\nprobe('newgroup/zz_missing')\n",
        "from sqpack import probes\nprobes.probe(ROOT, 'newgroup/zz_missing')\n",
        "from sqpack.probes import probe as load\nload(ROOT, 'newgroup/zz_missing')\n",
    ],
)
def test_a_loaded_name_in_a_group_that_does_not_exist_fails(source: str) -> None:
    """#125 F9, fixed in the workbench checker by #160: `newgroup/zz_missing` passed because
    no probe directory is called `newgroup`, so the name did not look like a probe."""
    source += "NAMES = ('stage/visible-count',)\n"
    assert _names(HAVE, caller=source) == (["newgroup/zz_missing"], [])


def test_a_name_handed_to_a_wrapper_in_another_file_is_resolved() -> None:
    """`look` forwards its parameter to the loader, and a second file calls it as a method,
    the way the Animate view's contract calls `session.look`."""
    session = (
        "from workbench_tools.probes import probe\n\n"
        "class Session:\n"
        "    def look(self, probe_name, /, **argument):\n"
        "        return self.page.evaluate(probe(probe_name), argument or None)\n"
    )
    contract = (
        "session.look('elsewhere/zz_missing', n=3)\nsession.look('stage/visible-count')\n"
    )
    assert _names(HAVE, session=session, contract=contract) == (["elsewhere/zz_missing"], [])


def test_a_path_not_handed_to_a_loader_is_not_a_probe() -> None:
    sources = {
        "checker": "from sqpack.probes import probe\n"
        "PAGE = 'packing/site/workbench/index.html'\nprobe(ROOT, 'stage/visible-count')\n",
        "build": "ATLAS = 'stage/known-best/manifest.json'\n",
    }
    assert _names(HAVE, **sources) == ([], [])


def test_a_name_that_looks_like_a_probe_in_a_loader_file_still_fails() -> None:
    source = "from sqpack.probes import probe\nNAMES = ('stage/zz_missing',)\n"
    assert _names(HAVE, caller=source) == (["stage/zz_missing"], ["stage/visible-count"])
