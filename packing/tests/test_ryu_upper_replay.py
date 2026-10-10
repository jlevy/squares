"""The replay driver for Ryu's k2-minus-c-upper programs: its comparisons and its job table.

The replays themselves take minutes and need the two hosted certificates; their results
are the packets' ``receipts/replay/`` records. These tests are offline and fast.
"""

from __future__ import annotations

import threading
from typing import Any

from cases.asymptotic.ryu_upper_replay import (
    PACKETS,
    Job,
    differences,
    jobs,
    normalise_text,
    rank,
    schedule,
    strip_volatile,
)


def _manifest(version: str) -> set[str]:
    text = (PACKETS[version] / "acquisition/upstream-subtree.sha256").read_text(
        encoding="utf-8"
    )
    return {line.split("  ", 1)[1].removeprefix("./") for line in text.splitlines()}


def test_timing_backend_and_path_fields_are_not_compared() -> None:
    ours = {
        "a": 1,
        "seconds": 3.0,
        "cert": {"t_check": 1.0, "n": 5},
        "files": ["x"],
        "gmp": True,
    }
    theirs = {
        "a": 1,
        "seconds": 9.0,
        "cert": {"t_check": 2.0, "n": 5},
        "files": ["y"],
        "gmp": False,
    }
    assert differences(ours, theirs) == []
    assert strip_volatile(ours) == {"a": 1, "cert": {"n": 5}}


def test_a_changed_value_is_reported_where_it_is() -> None:
    found = differences({"margins": {"W2_L": 0.0173}}, {"margins": {"W2_L": 0.0174}})
    assert found == ["/margins/W2_L: 0.0173 != 0.0174"]
    assert differences({"x": [1, 2]}, {"x": [1, 3]}) == ["/x[1]: 2 != 3"]


def test_checker_text_is_compared_without_timings_backend_or_path() -> None:
    ours = (
        "certificate /tmp/t/v1.0/data/stair_k100000.json.gz: k = 100000; arithmetic gmpy2.mpq\n"
        "OVERALL: PASS  (0.4 s)\n"
    )
    recorded = (
        "certificate data/stair_k100000.json.gz: k = 100000; arithmetic fractions.Fraction\n"
        "OVERALL: PASS  (0.3 s)\n"
    )
    assert normalise_text(ours) == normalise_text(recorded)
    assert normalise_text("N = 1 (2.0 s)") != normalise_text("N = 2 (2.0 s)")


def test_every_job_names_a_program_and_a_record_of_its_version() -> None:
    table = jobs()
    names = [job.name for job in table]
    assert len(names) == len(set(names)) == 70
    for job in table:
        if job.kind == "independent":
            assert job.script.startswith("cases.asymptotic.ryu_upper_"), job.name
            continue
        files = _manifest(job.version)
        assert job.script in files, job.name
        assert job.recorded is None or job.recorded in files, job.name
        assert all(item in files for item in job.cwd_inputs), job.name
        assert set(job.after) <= set(names), job.name


def test_the_review_table_is_covered() -> None:
    names = {job.name for job in jobs()}
    assert {
        f"stair_check_k{k}" for k in (100000, 1000000, 10000000, 38250000, 100000000)
    } <= names
    assert {
        "stair_check_k100000_mutate",
        "stair_check_k100000000_mutate",
        "const_stair",
    } <= names
    assert {
        "cert3e_160_64",
        "run_z_10000",
        "sl_t2_test",
        "p3test_10000",
        "a10_b2_zcp_102400",
    } <= names
    tiers = ("B1", "B1s", "B2", "A1", "A1s", "A2", "A3", "A4", "A5")
    assert {f"cert_v3_{t}_merge" for t in tiers} | {
        f"cert_v4_C{i}_merge" for i in (1, 2, 3)
    } <= names


def test_cheap_jobs_run_first_and_merges_after_their_slices() -> None:
    table = sorted(jobs(), key=rank)
    assert table[0].version == "v1.0"
    assert table[-1].name == "a10_b2_zcp_102400"
    seen: list[str] = []
    lock = threading.Lock()

    def work(job: Job) -> dict[str, Any]:
        with lock:
            assert all(name in seen for name in job.after), job.name
            seen.append(job.name)
        return {"job": job.name, "wall_seconds": 0.0, "matches_record": True}

    done: list[str] = []
    entries = schedule(table, 2, work, lambda entry: done.append(entry["job"]))
    assert [entry["job"] for entry in entries] == [job.name for job in table]
    assert sorted(done) == sorted(job.name for job in table)
