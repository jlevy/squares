"""The page-policy check's own logic, without a browser.

The browser half runs in `check_frontend`, which proves its recorder live on every run with a
control policy that refuses the page's fonts. What is tested here is what decides the verdict.
"""

from __future__ import annotations

import pytest

from sqpack.probes import applied
from workbench_tools.build_site import CONTENT_SECURITY_POLICY, POLICY_META
from workbench_tools.check_page_policy import (
    FONTS_REFUSED,
    PolicyRun,
    faults,
    with_policy,
)

STARTED = {"pack": True, "search": True, "squares": 17, "fonts": "loaded"}
FONT_REFUSAL = {"directive": "font-src", "blocked": "data", "source": "file"}


def _clean() -> PolicyRun:
    return PolicyRun(started=dict(STARTED), violations=[])


def _control() -> PolicyRun:
    return PolicyRun(started=dict(STARTED), violations=[FONT_REFUSAL])


def test_an_init_probe_is_called_once_with_no_argument() -> None:
    # Placeholder text rather than JavaScript: the probe's source is opaque to the wrapper.
    assert applied("  PROBE SOURCE;\n") == "(PROBE SOURCE\n)();\n"


def test_the_control_policy_refuses_only_the_fonts() -> None:
    assert "'unsafe-eval'" not in CONTENT_SECURITY_POLICY
    assert FONTS_REFUSED != POLICY_META
    assert FONTS_REFUSED.replace("font-src 'none'", "font-src data:") == POLICY_META


def test_a_page_without_the_published_policy_is_refused() -> None:
    page = f"<head>{POLICY_META}</head>"
    assert with_policy(page, FONTS_REFUSED) == f"<head>{FONTS_REFUSED}</head>"
    with pytest.raises(ValueError, match="does not carry"):
        with_policy("<head></head>", FONTS_REFUSED)
    with pytest.raises(ValueError, match="does not carry"):
        with_policy(page + page, FONTS_REFUSED)


def test_a_clean_page_with_a_live_recorder_passes() -> None:
    assert faults(_clean(), _control()) == []


@pytest.mark.parametrize(
    ("published", "expected"),
    [
        (PolicyRun(started=dict(STARTED), violations=[FONT_REFUSAL]), "refused what the page"),
        (PolicyRun(started=dict(STARTED), violations=None), "recorder did not run"),
        (PolicyRun(started={**STARTED, "pack": False}, violations=[]), "did not start"),
        (PolicyRun(started={**STARTED, "squares": 0}, violations=[]), "drew no squares"),
        (PolicyRun(started={**STARTED, "fonts": "loading"}, violations=[]), "fonts did not"),
        (PolicyRun(started=dict(STARTED), violations=[], errors=["console.error: x"]), "x"),
    ],
)
def test_each_way_the_published_page_can_fail_is_reported(
    published: PolicyRun, expected: str
) -> None:
    found = faults(published, _control())
    assert len(found) == 1
    assert expected in found[0]


def test_a_recorder_that_reports_nothing_under_the_control_fails() -> None:
    silent = PolicyRun(started=dict(STARTED), violations=[])
    found = faults(_clean(), silent)
    assert found == ["the recorder is not live: a policy refusing the page's fonts reported []"]
