"""The reviewer's verifier is reachable from a path, and the recorded replay runs.

`independent_verify.py` reads its first argument as a mode name, so the replay the
evidence register recorded -- a certificate path -- verified nothing and exited 0
(think-d7yx). The wrapper takes the path the register passes, and this pins both
halves: the wrapper decides the retained first rung on two directions, and the
register's replay command names the wrapper and an existing certificate.
"""

from __future__ import annotations

import shlex
from pathlib import Path

from cases.n12_fractional_certificate.replay import FIRST_RUNG_PATH
from cases.n12_fractional_certificate.replay_independent import main, replay
from sqpack.yamlio import safe_load

PACKING = Path(__file__).resolve().parents[1]
WRAPPER = "cases/n12_fractional_certificate/replay_independent.py"


def test_the_wrapper_accepts_the_first_rung_on_two_directions() -> None:
    assert replay(FIRST_RUNG_PATH, directions=[0, 180])
    assert main([str(FIRST_RUNG_PATH), "--directions", "0,180"]) == 0


def test_a_missing_certificate_is_refused() -> None:
    assert main([str(FIRST_RUNG_PATH.with_name("no-such-certificate.json"))]) == 1


def test_the_evidence_register_replays_through_the_wrapper() -> None:
    evidence = safe_load((PACKING / "frontier" / "evidence.yaml").read_text(encoding="utf-8"))
    entries = [
        entry
        for entry in evidence["evidence"]
        if isinstance(entry.get("replay"), str)
        and "n12_fractional_certificate" in entry["replay"]
        and "independent" in entry["replay"]
    ]
    assert entries, "the n = 12 independent verification entry names no replay"
    for entry in entries:
        tokens = shlex.split(entry["replay"])
        assert WRAPPER in tokens, entry["replay"]
        certificate = tokens[tokens.index(WRAPPER) + 1]
        assert (PACKING / certificate).is_file(), certificate
