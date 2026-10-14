"""The launch history reaches both reader surfaces and the publication scope."""

from __future__ import annotations

import copy
import re
from fnmatch import fnmatchcase

import pytest

from devtools import (
    check_published_site,
    pages_scope,
    render_changelog,
    render_overview,
    site_documents,
)
from devtools.pages_scope import REPO
from tests import site_renders


@pytest.fixture(scope="module")
def views() -> tuple[dict, str, str]:
    document = render_changelog.load()
    return document, site_renders.html("about.html"), render_changelog.render(document)


def test_about_ends_with_the_same_launch_history_as_github(
    views: tuple[dict, str, str],
) -> None:
    document, about, github = views
    headings = re.findall(r'<h2\b[^>]*id="([^"]+)"', about)
    assert headings[-1] == "changelog"
    history = about[about.index('id="changelog"') :]
    for entry in document["entries"]:
        anchor = render_changelog.entry_anchor(entry["id"])
        assert f'id="{anchor}"' in history
        assert f'id="{anchor}"' in github
        for number in entry["pull_requests"]:
            target = f"{document['repository']}/pull/{number}"
            assert target in history
            assert target in github
        for artifact in entry.get("artifacts", []):
            assert artifact["target"] in history
            assert artifact["target"] in github


def test_a_yaml_only_history_change_selects_and_deploys_about() -> None:
    workflow = pages_scope.load_workflow()
    changed = "packing/site-changelog.yaml"
    decisions = pages_scope.decide([changed], pages_scope.declared_inputs())
    assert any(item.half == "overview" and item.in_scope for item in decisions)
    push = workflow["on"]["push"]
    assert any(fnmatchcase(changed, pattern) for pattern in push["paths"])
    assert REPO / changed in render_overview.RENDER_INPUTS


def test_repository_changelog_links_land_on_the_about_section() -> None:
    assert site_documents.RECORD_PAGES["CHANGELOG.md"] == "about.html#changelog"


def test_publication_audit_refuses_a_missing_launch_link(
    views: tuple[dict, str, str],
) -> None:
    document, about, _github = views
    assert all(passed for passed, _line in check_published_site.changelog_checks(about))
    target = next(
        artifact["target"]
        for entry in document["entries"]
        for artifact in entry.get("artifacts", [])
    )
    damaged = about.replace(target, "https://example.com/missing")
    assert not all(passed for passed, _line in check_published_site.changelog_checks(damaged))


def test_publication_audit_accepts_the_renderers_encoded_artifact_destinations(
    views: tuple[dict, str, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    document = copy.deepcopy(views[0])
    artifact = next(
        artifact for entry in document["entries"] for artifact in entry.get("artifacts", [])
    )
    artifact["target"] += "#proof(1)"
    render_changelog.validate(document)
    monkeypatch.setattr(render_changelog, "load", lambda: document)
    about = render_overview.about_page().html
    assert "#proof%281%29" in about
    assert all(passed for passed, _line in check_published_site.changelog_checks(about))
