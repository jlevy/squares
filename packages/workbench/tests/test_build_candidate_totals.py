"""The run time the candidate build prints is the one the page plays.

The summary used to add dwell, move and settle, leave out `correct`, and price the static
appends at timings the page no longer uses, so it printed 695.3 s for a run the page's own
range duration puts at 568.95 s.
"""

import re

from workbench_tools.build_candidate import (
    PACKAGE_ROOT,
    STATIC_TIMING,
    TIMING,
    beat_seconds,
    run_time_lines,
)

APPLICATION = PACKAGE_ROOT / "src/application.js"

SPANS = {"dwell", "move", "correct", "settle"}

#: The corpus's pair kinds: 160 grid prefixes, 5 shared pictures and 158 matched pairs.
CORPUS_KINDS = ["prefix"] * 160 + ["shared-picture"] * 5 + ["matched"] * 158


def test_a_beat_lasts_all_four_spans() -> None:
    assert beat_seconds({"dwell": 1.0, "move": 2.0, "correct": 4.0, "settle": 8.0}) == 15.0


def test_both_beats_the_build_prices_carry_every_span() -> None:
    assert set(TIMING) == SPANS
    assert set(STATIC_TIMING) == SPANS


def test_static_appends_take_the_static_beat_and_nothing_follows_the_last_pair() -> None:
    moving = {"dwell": 1.0, "move": 2.0, "correct": 4.0, "settle": 8.0}
    static = {"dwell": 0.5, "move": 0.25, "correct": 0.125, "settle": 0.125}
    lines = run_time_lines(
        ["prefix", "matched", "shared-picture", "matched"], timing=moving, static_timing=static
    )
    # Two moving pairs at 15 s and two static appends at 1 s: 32 s, with no closing dwell.
    assert "2 × 15 + 2 × 1 = 32.00 s" in lines[0]  # noqa: RUF001
    # Every pair at the full beat: four pairs at 15 s.
    assert "4 × 15 = 60.00 s" in lines[1]  # noqa: RUF001


def _page_continuous() -> dict[str, float]:
    """The page's `CONTINUOUS` beat, read from its source as numbers."""
    source = APPLICATION.read_text(encoding="utf-8")
    block = re.search(r"\bCONTINUOUS = \{(.*?)\};", source, flags=re.DOTALL)
    assert block is not None, "the page no longer declares its continuous beat"
    return {
        name: float(value)
        for name, value in re.findall(r"^\s*(\w+):\s*([0-9.]+),", block.group(1), re.MULTILINE)
    }


def test_the_build_prices_the_beats_the_page_plays() -> None:
    """The static beat is a copy of the page's constants, so the copy is compared with them.

    At f3874426 this made the corpus run 568.95 s, the page's own `range().duration` over
    2..324, and 775.2 s at the full beat, its `continuous().total`; the old summary said
    695.3 s. The figures move with the beat, and this keeps the two sources in step.
    """
    page = _page_continuous()
    assert {span: page[span] for span in SPANS} == TIMING
    assert {span: page[f"static{span.capitalize()}"] for span in SPANS} == STATIC_TIMING
    lines = run_time_lines(CORPUS_KINDS)
    moving = beat_seconds(TIMING)
    static = beat_seconds(STATIC_TIMING)
    assert f"= {158 * moving + 165 * static:.2f} s" in lines[0]
    assert f"= {323 * moving:.2f} s" in lines[1]
