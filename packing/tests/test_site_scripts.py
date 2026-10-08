"""Unknown scripts and remote/missing application assets fail the published inventory."""

from pathlib import Path

from devtools.check_site_scripts import inventory


def test_inventory_includes_application_assets_and_rejects_unknown_scripts(
    tmp_path: Path,
) -> None:
    (tmp_path / "published.0123456789abcdef.js").write_text("/* bundled reviewed loader */")
    (tmp_path / "workbench.0123456789abcdef.js").write_text(
        "/* bundled reviewed application */"
    )
    (tmp_path / "index.html").write_text(
        '<script type="application/json" data-application-src="workbench.0123456789abcdef.js">'
        "{}</script>"
        '<script src="published.0123456789abcdef.js"></script>'
    )
    records, errors = inventory(tmp_path)
    assert not errors
    assert len(records) == 2
    assert {row.category for row in records} == {"workbench-application"}
    (tmp_path / "new-program.js").write_text("/* an undeclared program */")
    _, errors = inventory(tmp_path)
    assert errors == ["unclassified executable script: new-program.js"]


def test_inventory_refuses_remote_missing_and_inline_unclassified_programs(
    tmp_path: Path,
) -> None:
    (tmp_path / "index.html").write_text(
        '<script src="https://example.com/script.js"></script>'
        '<script src="missing.js"></script>'
        "<script>/* undeclared startup */</script>"
    )
    _, errors = inventory(tmp_path)
    assert len(errors) == 3
    assert any("relative first-party" in error for error in errors)
    assert any("missing or outside" in error for error in errors)
    assert any("unclassified" in error for error in errors)
