"""The improvement rule is stated once, in the regularization policy, and judged by one
function.

The owner, 13 October 2026: "tie is fine on exactness or regularity as long as it is
making some improvement wrt our regularity or heuristic goals", codified in the policy's
section 11. The selection's rule and the default pictures' check read the statement from
the policy, and its goal lines are parsed and compared both ways with the goals and
directions the code judges, so neither can drift from the other without the check
failing (review A2 of #591).
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

from devtools import improvement_rule as rule
from devtools import regularize_select as select

POLICY = rule.POLICY.read_text(encoding="utf-8")


def _marked() -> str:
    return POLICY[POLICY.index(rule.BEGIN) + len(rule.BEGIN) : POLICY.index(rule.END)]


def _policy(tmp_path: Path, marked: str) -> Path:
    policy = tmp_path / "policy.md"
    policy.write_text(f"intro\n\n{rule.BEGIN}{marked}{rule.END}\n", encoding="utf-8")
    return policy


def test_the_policy_states_the_rule_once_and_its_goals_are_the_code_s() -> None:
    words = rule.statement()
    assert words.startswith("A view improves on a drawing")
    assert rule.problems() == []
    stated, unread = rule.stated_goals()
    assert unread == []
    assert stated == {rule.GOAL_NAMES[key]: rule.DIRECTIONS[key] for key in rule.GOALS}
    assert set(rule.GOAL_NAMES) == set(rule.DIRECTIONS) == set(rule.GOALS)
    assert {key for key in rule.MEASURES if rule.DIRECTIONS[key] == rule.FEWER} == set(
        rule.FEWER_IS_BETTER
    )


def test_the_selection_prints_the_policy_statement() -> None:
    printed = select.rule()
    assert rule.statement() in printed
    assert rule.SECTION in printed
    assert select.MEASURES == rule.MEASURES
    assert select.compare is rule.compare


@pytest.mark.parametrize(
    ("edit", "problem"),
    [
        # The reviewer's four edits (review A2 of #591), on the goal list.
        (
            lambda text: text.replace(
                "- exactness:", "- symmetry: more is better\n- exactness:"
            ),
            "names the goal 'symmetry', which the code does not judge",
        ),
        (
            lambda text: text.replace("- hues: fewer is better", "- hues: more is better"),
            "states 'hues' as 'more is better'; the code judges 'fewer is better'",
        ),
        (
            lambda text: text.replace(
                "- house total of full shared sides: more is better\n", ""
            ),
            "does not name the goal 'house total of full shared sides'",
        ),
        (
            lambda text: text.replace(
                "- exact side: smaller is better", "- exact side: larger is better"
            ),
            "states 'exact side' as 'larger is better'; the code judges 'smaller is better'",
        ),
        (
            lambda text: text.replace("- hues: fewer is better", "- hues, fewer being better"),
            "has a goal line that does not parse",
        ),
    ],
)
def test_a_goal_the_code_does_not_judge_as_stated_fails(
    tmp_path: Path, edit: Callable[[str], str], problem: str
) -> None:
    edited = edit(_marked())
    assert edited != _marked()
    found = rule.problems(_policy(tmp_path, edited))
    assert any(problem in line for line in found), found


def test_a_direction_the_code_changes_fails_against_the_unchanged_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The coupling runs the other way too: the code's directions come from what it
    judges (`FEWER_IS_BETTER`), so changing them alone fails against the policy."""
    monkeypatch.setitem(rule.DIRECTIONS, "hues", rule.MORE)
    assert rule.problems() == [
        (
            f"the improvement rule in {rule.POLICY_DOCUMENT} states 'hues' as "
            "'fewer is better'; the code judges 'more is better'"
        )
    ]


@pytest.mark.parametrize(
    "text",
    [
        "no markers at all\n",
        f"{rule.END}\nthe rule\n{rule.BEGIN}\n",
        f"{rule.BEGIN}\none\n{rule.END}\n{rule.BEGIN}\ntwo\n{rule.END}\n",
        f"{rule.BEGIN}\n\n{rule.END}\n",
    ],
)
def test_a_statement_not_marked_once_is_refused(tmp_path: Path, text: str) -> None:
    policy = tmp_path / "policy.md"
    policy.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError, match="improvement rule"):
        rule.statement(policy)
    assert len(rule.problems(policy)) == 1


@pytest.mark.parametrize(
    ("gains", "worse", "flags", "reason"),
    [
        (["light_axis"], [], {}, ""),
        # Ties on the other goals are fine.
        (["house_total"], [], {"exact_gain": False}, ""),
        # Exactness is a goal: a numerically checked witness replaced, every measure tied.
        ([], [], {"exact_gain": True}, ""),
        # So is the side.
        ([], [], {"smaller": True}, ""),
        # A tie on every goal is no improvement.
        ([], [], {}, "no gain"),
        # Worse on any goal is no improvement, whatever it gains.
        (["light_axis"], ["hues"], {"exact_gain": True}, "worse on hues"),
        (["light_axis"], [], {"larger": True}, "worse on side"),
    ],
)
def test_worse_on_none_and_better_on_one(
    gains: list[str], worse: list[str], flags: dict[str, bool], reason: str
) -> None:
    """An empty reason is an improvement; any other names why it is not one."""
    judged = rule.judge(
        gains,
        worse,
        smaller=flags.get("smaller", False),
        larger=flags.get("larger", False),
        exact_gain=flags.get("exact_gain", False),
    )
    assert judged.improves is (not reason)
    assert judged.reason == reason


def test_only_the_rule_s_measures_are_judged() -> None:
    with pytest.raises(ValueError, match="not measures"):
        rule.judge(["symmetry"], [], smaller=False, larger=False, exact_gain=False)
