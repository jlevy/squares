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

import ast
import json
import os
import shutil
from pathlib import Path

import pytest
from nodejs_wheel import node

from devtools import bead_state, check_probes
from devtools import check_no_embedded_js as guard
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
        "probe(ROOT, 'tool/name') or 'planted'",
        "(lambda: 'planted')()",
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


LEAN_TEMPLATES = (
    "chain_lean.py",
    "localmin_lean.py",
)
LEAN_DIRECTORY = (
    Path(__file__).resolve().parent.parent
    / "resources/web/evand-exact-and-local-reports-2026-10-07/source/s12/search/exact"
)


def _lean_template(name: str) -> ast.JoinedStr:
    """Read the complete original source; keep its generated Lean literal unchanged."""
    source = (LEAN_DIRECTORY / name).read_text()
    assert guard.scan_source(name, source, POLICY) == []
    marker = (
        "namespace UnitSquarePacking." if name == "chain_lean.py" else "noncomputable def lcert"
    )
    for syntax in ast.walk(ast.parse(source)):
        if isinstance(syntax, ast.JoinedStr) and any(
            isinstance(part, ast.Constant)
            and isinstance(part.value, str)
            and marker in part.value
            for part in syntax.values
        ):
            return syntax
    raise AssertionError(f"retained source has no expected Lean template: {name}")


@pytest.mark.parametrize("name", LEAN_TEMPLATES)
def test_original_lean_templates_are_not_javascript(name: str) -> None:
    _lean_template(name)


@pytest.mark.parametrize("name", LEAN_TEMPLATES)
def test_javascript_inside_the_original_lean_template_is_still_refused(name: str) -> None:
    template = _lean_template(name)
    template.values.insert(1, ast.Constant("\n" + PLANTED + "\n"))
    assert _rules("DATA = " + ast.unparse(template)) == ["JavaScript string"]


@pytest.mark.parametrize("name", LEAN_TEMPLATES)
def test_a_lean_template_passed_to_the_browser_is_still_refused(name: str) -> None:
    template = _lean_template(name)
    assert _rules("DATA = " + ast.unparse(template) + "\npage.evaluate(DATA)\n") == [
        "script argument"
    ]


OVERLAP_PROBES = {
    "document-body": probe(PROBES, "no_embedded_js/document-body"),
    "window-location": probe(PROBES, "no_embedded_js/window-location"),
}


@pytest.mark.parametrize(
    ("prefix", "name"),
    [
        ("fun (x := ", "document-body"),
        ("match x with | some (", "window-location"),
    ],
)
def test_a_lean_arrow_parameter_cannot_hide_an_overlapping_javascript_signature(
    prefix: str, name: str
) -> None:
    expression = OVERLAP_PROBES[name]
    body = expression.split("=>", 1)[1].strip().removesuffix(";")
    text = prefix + body + ") => x"
    assert _rules(f"DATA = {text!r}") == ["JavaScript string"]


@pytest.mark.parametrize("prefix", ["fun (", "match x with | some ("])
def test_a_lean_looking_parameter_cannot_hide_an_inner_javascript_arrow(
    prefix: str,
) -> None:
    text = prefix + PLANTED.replace("()", "x") + ") => y"
    assert _rules(f"DATA = {text!r}") == ["JavaScript string"]


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


@pytest.mark.parametrize(
    "source",
    [
        (
            "from sqpack.probes import applied\n"
            "page.add_init_script(applied('location.reload()'))\n"
        ),
        (
            "import sqpack.probes as probes\n"
            "page.add_init_script(probes.applied('location.reload()'))\n"
        ),
        (
            "from sqpack.probes import applied\n"
            "page.add_init_script(applied(source='location.reload()'))\n"
        ),
        (
            "from sqpack.probes import applied\n"
            "def install(page, source):\n"
            "    page.add_init_script(applied(source))\n"
        ),
        (
            "from sqpack.probes import applied, probe\n"
            "page.add_init_script(applied(probe(ROOT, 'tool/name') if flag else source))\n"
        ),
        (
            "from sqpack.probes import applied, probe\n"
            "source = probe(ROOT, 'tool/name')\n"
            "source = make_source()\n"
            "page.add_init_script(applied(source))\n"
        ),
        (
            "from sqpack.probes import applied, probe\n"
            "source = probe(ROOT, 'tool/name')\n"
            "source += suffix\n"
            "page.add_init_script(applied(source))\n"
        ),
        ("from sqpack.probes import applied\npage.add_init_script(applied(**options))\n"),
    ],
)
def test_applied_accepts_only_file_backed_probe_source(source: str) -> None:
    assert _rules(source) == ["script argument"]


def test_applied_accepts_a_file_backed_probe_as_a_keyword_source() -> None:
    source = (
        "from sqpack.probes import applied, probe\n"
        "page.add_init_script(applied(source=probe(ROOT, 'tool/name')))\n"
    )
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


def test_a_file_with_a_byte_order_mark_is_read_and_still_scanned(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """CPython accepts a leading UTF-8 byte-order mark in source, and retained third-party
    files carry one; the guard reads them as the interpreter does, and still finds a site."""
    (tmp_path / "plain.py").write_bytes(b"\xef\xbb\xbfx = 1\n")
    (tmp_path / "tool.py").write_bytes(
        b"\xef\xbb\xbf" + f"page.evaluate({PLANTED!r})\n".encode()
    )
    policy = tmp_path / "policy.yaml"
    text = guard.POLICY.read_text(encoding="utf-8")
    policy.write_text(text.split("\nallowlist:")[0] + "\nallowlist: []\n", encoding="utf-8")

    assert guard.main(["--repo", str(tmp_path), "--policy", str(policy)]) == 1
    out = capsys.readouterr().out
    assert "cannot be read as Python" not in out
    assert "tool.py: 1 site(s) of JavaScript in Python" in out


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
    report = check_probes.faults(tmp_path)
    assert (report.faults, report.unread, report.probes, report.trees) == ([], [], 1, 1)


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
    report = check_probes.faults(tmp_path)
    found, count, trees = report.faults, report.probes, report.trees
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
    missing, unnamed, _unread = check_probes.name_faults(callers, have)
    return missing, unnamed


def _unread(**sources: str) -> list[str]:
    """The loader calls whose name the analysis could not read."""
    callers = {name: check_probes.read_caller(source, name) for name, source in sources.items()}
    return check_probes.name_faults(callers, HAVE)[2]


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


# -- the findings of the #175 review, and of the review lane beside it --------------------


def test_a_javascript_bytes_literal_fails_wherever_it_is_written() -> None:
    """R1: rule 2 never read a bytes constant, so the same script the `str` spelling was
    reported for passed as `b"..."`."""
    assert _rules(f"SCRIPT = {PLANTED.encode()!r}\n") == ["JavaScript string"]


@pytest.mark.parametrize(
    "script",
    [
        "b'planted'.decode()",
        "BYTES.decode()",
        "str(b'planted', 'utf-8')",
        "base64.b64decode('cGxhbnRlZA==').decode()",
        "bytes.fromhex('706c616e746564').decode('utf-8')",
    ],
)
def test_a_bytes_script_argument_fails(script: str) -> None:
    """R1: `.decode()`, `str()` and `b64decode()` were classified as unknown, which passed."""
    source = f"import base64\nBYTES = b'planted'\npage.evaluate({script})\n"
    assert _rules(source) == ["script argument"]


@pytest.mark.parametrize(
    "source",
    [
        (
            "from pathlib import Path\n"
            "page.evaluate(Path(__file__).with_name('h.js').read_text())\n"
        ),
        "page.evaluate(open('helper.js').read())\n",
        "page.evaluate('PLANTED'.lower())\n",
        "page.evaluate('planted'.expandtabs())\n",
        "S = {'a': 'planted'}\npage.evaluate(S['a'])\n",
        "def run(page, script='planted'):\n    return page.evaluate(script)\n",
        (
            "class T:\n    S = 'planted'\n\n"
            "    def go(self, page):\n        page.evaluate(self.S)\n"
        ),
        "a, b = 'plan', 'ted'\npage.evaluate(a + b)\n",
        "args = ('planted',)\npage.evaluate(*args)\n",
        "page.evaluate(**{'expression': 'planted'})\n",
        "from textwrap import dedent as d\npage.evaluate(d('planted'))\n",
        "page.evaluate(''.join(parts))\n",
        "page.evaluate([SCRIPT][0])\n",
        "def build():\n    return 'planted'\n\npage.add_init_script(build())\n",
        (
            "from pathlib import Path\n"
            "def build():\n    return Path('planted.txt').read_text()\n\n"
            "page.evaluate(build())\n"
        ),
        "async def go(page):\n    return page.evaluate(await build())\n",
    ],
)
def test_an_unclassifiable_script_argument_fails(source: str) -> None:
    """R3, and lane L6: rule 1 accepted every argument it could not classify, and nothing
    counted or printed one. The scripts here carry no signature, so rules 2 and 3 -- which
    the docstring said these were `left to` -- see nothing at all."""
    assert _rules(source) == ["script argument"]


@pytest.mark.parametrize(
    "source",
    [
        "def run(page, script):\n    return page.evaluate(script)\n",
        "value = polynomial.evaluate(point)\n",
        "origin = chart.origin()\nvalue = polynomial.evaluate(origin)\n",
        "value = polynomial.evaluate([field.rational(1), field.rational(2)])\n",
        (
            "from sqpack.probes import probe\nSCRIPT = probe(ROOT, 'tool/name')\n"
            "OTHER = probe(ROOT, 'tool/other')\npage.evaluate(SCRIPT if flag else OTHER)\n"
        ),
        (
            "from sqpack.probes import probe\n"
            "def build():\n    return probe(ROOT, 'tool/name')\n\n"
            "page.evaluate(build())\n"
        ),
    ],
)
def test_default_deny_accepts_the_loader_a_parameter_and_a_value_that_is_not_text(
    source: str,
) -> None:
    """The four things that pass, and why each one has to: a parameter; a name this module
    never binds, whose text rule 2 reads in the module that does bind it; a value that
    cannot be text; and a call to something written elsewhere -- which is also `evaluate`
    as mathematics spells it."""
    assert _sites(source) == []


def test_the_content_of_an_added_script_tag_is_a_script_argument() -> None:
    """R5: `add_script_tag(content=...)` puts a script in the page and was not read."""
    assert _rules("page.add_script_tag(content='planted')\n") == ["script argument"]
    assert _sites("BUNDLE = D / 'b.js'\npage.add_script_tag(path=str(BUNDLE))\n") == []
    assert _sites("page.add_init_script(path=Path('a.txt').with_suffix('.js'))\n") == []


@pytest.mark.parametrize(
    "source",
    [
        "page.add_init_script(path=ROOT / 'tool' / 'init.txt')\n",
        "page.add_script_tag(path=str(ROOT / 'bundle.data'))\n",
        "BUNDLE = ROOT / 'bundle.txt'\npage.add_script_tag(path=str(BUNDLE))\n",
        "page.add_init_script(path=Path('actual.js').with_suffix('.txt'))\n",
        (
            "BUNDLE = ROOT / ('bundle.js' if checked else 'bundle.txt')\n"
            "page.add_script_tag(path=BUNDLE)\n"
        ),
        "page.add_init_script(path=chosen_path())\n",
    ],
)
def test_a_path_argument_that_is_not_a_script_file_fails(source: str) -> None:
    """Lane L3: `path=` is the accepted form because the file it names is JavaScript that
    Biome formats and `tsc` types. A `.txt` holding JavaScript is neither."""
    assert _rules(source) == ["script argument"]


def test_a_script_body_spliced_from_a_bound_literal_fails() -> None:
    """R7: the hole was replaced by a space and the bound literal had no signature of its
    own, so the joined text was never read as a body."""
    assert _rules("code = 'alert(1)'\nHTML = '<script>' + code + '</script>'\n") == [
        "script body"
    ]


def test_resolving_a_bound_name_terminates_on_a_self_reference() -> None:
    """`a = a + "x"` resolves through itself; the guard answers rather than recurses."""
    assert _sites("a = a + 'x'\nHTML = '<script>' + a + '</script>'\n") == []


def test_the_allowlist_refuses_a_new_path_and_a_raised_count() -> None:
    """R2: `Entries only ever leave` was a comment in the YAML, not a check anywhere."""
    base = {"a.py": guard.Entry(2, "think-abcd")}
    faults = guard.allowlist_growth(
        {"a.py": guard.Entry(3, "think-abcd"), "new.py": guard.Entry(99, "think-abcd")}, base
    )
    assert any(f.startswith("new.py: a new allowlist entry") for f in faults)
    assert any("a.py: the allowlist records 3 site(s), 2 at the base" in f for f in faults)
    assert guard.allowlist_growth({"a.py": guard.Entry(1, "think-abcd")}, base) == []
    assert guard.allowlist_growth({}, base) == []


def test_every_allowlisted_bead_is_a_live_bead() -> None:
    """R2: the shape check let any four-character name widen the list. The floor contract
    already refuses a closed or unknown tracker for the `tsconfig` relaxations (#160 R24)."""
    aliases = {entry.bead for entry in POLICY.allowlist.values()}
    assert bead_state.dead_trackers(aliases, _bead_reader()) == []


def test_a_closed_or_unknown_allowlist_bead_is_refused() -> None:
    read = bead_state.fixture_store({"aaaa": "open", "cccc": "closed"})
    assert bead_state.dead_trackers(["think-aaaa"], read) == []
    assert bead_state.dead_trackers(["think-aaaa", "think-cccc", "think-zzzz"], read) == [
        "think-cccc: closed",
        "think-zzzz: no such bead",
    ]


def _bead_reader() -> bead_state.Reader:
    try:
        return bead_state.require_store()
    except bead_state.UnavailableError as error:
        if os.environ.get("CI"):
            pytest.fail(f"{error}; the job must fetch full history to check trackers")
        return pytest.skip(str(error))


def test_a_name_passed_to_the_loader_by_keyword_must_resolve() -> None:
    """R6: `literal_calls` read `node.args` only, so `probe(ROOT, name=...)` was reported by
    neither branch and failed at the far end of a browser run."""
    source = "from sqpack.probes import probe\nprobe(ROOT, name='newgroup/zz_missing')\n"
    assert _names(HAVE, caller=source) == (["newgroup/zz_missing"], ["stage/visible-count"])


def test_a_probe_argument_named_name_is_not_a_probe_name() -> None:
    """The wrapper takes the probe positionally and forwards `**argument` to the page, where
    `name="d"` is an attribute the probe reads."""
    session = (
        "from workbench_tools.probes import probe\n\n"
        "class Session:\n"
        "    def look(self, probe_name, /, **argument):\n"
        "        return self.page.evaluate(probe(probe_name), argument or None)\n"
    )
    contract = "session.look('stage/visible-count', id='lp-curve', name='d')\n"
    assert _names(HAVE, session=session, contract=contract) == ([], [])


def test_a_loader_call_with_an_assembled_name_is_reported_as_unread() -> None:
    """Lane L1: `probe(f"{group}/zz_absent")` is invisible to both halves of the name check,
    and read exactly like a clean run. It is not a fault -- the name may well resolve -- but
    `could not read` has to look different from `clean`."""
    assembled = "from sqpack.probes import probe\nGROUP = 'stage'\nprobe(ROOT, f'{GROUP}/x')\n"
    (note,) = _unread(caller=assembled)
    assert note.startswith("caller:3: probe(...) loads a probe whose name this cannot read")
    table = (
        "from sqpack.probes import probe\n"
        "NAMES = {'a': 'stage/visible-count'}\nprobe(ROOT, NAMES['a'])\n"
    )
    assert _unread(caller=table) == []
    forwarded = "from sqpack.probes import probe\ndef go(n):\n    probe(ROOT, n)\n"
    assert _unread(caller=forwarded) == []


def test_a_probe_exercised_only_by_a_node_script_is_not_dead(tmp_path: Path) -> None:
    """Lane L4: `callers` collected `.py` only, so a probe a `.mjs` test drives read as dead."""
    tree = _probe_tree(tmp_path)
    shutil.copy(tree / "used.js", tree / "from-node.js")
    (tmp_path / "tool" / "drive.mjs").write_text(
        'import { load } from "./probes.mjs";\nload("group/from-node");\n', encoding="utf-8"
    )
    assert check_probes.faults(tmp_path).faults == []


def test_a_probe_that_never_finishes_is_reported_rather_than_hung(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Lane L2: the inspector ran each probe body with no deadline, so a top-level loop hung
    the check and the CI step behind it with no diagnostic at all."""
    monkeypatch.setenv("PROBE_TIMEOUT_MS", "200")
    tree = _probe_tree(tmp_path)
    # The spinning function is a probe file, not a Python string: the guard refuses one, and
    # `applied` is what turns the function into the call that runs it.
    (tree / "spins.js").write_text(
        applied(probe(PROBES, "no_embedded_js/spin")), encoding="utf-8"
    )
    (tmp_path / "tool" / "caller.py").write_text(
        "from sqpack.probes import probe\n"
        "probe(ROOT, 'group/used')\nprobe(ROOT, 'group/spins')\n",
        encoding="utf-8",
    )
    found = check_probes.faults(tmp_path).faults
    assert any("group/spins.js: does not evaluate" in fault for fault in found)


def test_a_class_is_not_a_function(tmp_path: Path) -> None:
    """Lane L5: `typeof` calls a class a function, and a class handed to `page.evaluate`
    fails in the page with `Class constructor cannot be invoked without 'new'`."""
    tree = _probe_tree(tmp_path)
    (tree / "klass.js").write_text("class Probe {\n  run() {}\n}\n", encoding="utf-8")
    (tmp_path / "tool" / "caller.py").write_text(
        "from sqpack.probes import probe\n"
        "probe(ROOT, 'group/used')\nprobe(ROOT, 'group/klass')\n",
        encoding="utf-8",
    )
    found = check_probes.faults(tmp_path).faults
    assert "tool/probes/group/klass.js: evaluates to a class, not a function" in found
