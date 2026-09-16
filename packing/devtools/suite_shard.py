"""Split a collected pytest suite into deterministic whole-module shards.

The pull-request workflow invokes the complete quick suite twice.  Each invocation
collects the same tests, this plugin counts the collected items per module, and a stable
largest-first assignment selects one disjoint half.  Keeping modules whole preserves
module-scoped fixture reuse; deriving the assignment from collection means a new module
enters exactly one shard without a maintained allow-list.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping

import pytest

SHARD_COUNT = 2


def module_id(nodeid: str) -> str:
    """Return the collected module portion of a pytest node id."""
    return nodeid.partition("::")[0]


def count_modules(nodeids: Iterable[str]) -> dict[str, int]:
    """Count collected items by module."""
    return dict(Counter(module_id(nodeid) for nodeid in nodeids))


def assign_modules(
    counts: Mapping[str, int], shard_count: int = SHARD_COUNT
) -> tuple[frozenset[str], ...]:
    """Assign every module once with deterministic largest-first load balancing."""
    if shard_count < 1:
        raise ValueError("shard_count must be positive")
    if any(count < 1 for count in counts.values()):
        raise ValueError("module item counts must be positive")

    loads = [0] * shard_count
    assignments: list[set[str]] = [set() for _ in range(shard_count)]
    for module, count in sorted(counts.items(), key=lambda entry: (-entry[1], entry[0])):
        shard = min(range(shard_count), key=lambda index: (loads[index], index))
        assignments[shard].add(module)
        loads[shard] += count
    return tuple(frozenset(assignment) for assignment in assignments)


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register the internal selector used by the two validation tiers."""
    group = parser.getgroup("suite-shard")
    group.addoption(
        "--suite-shard",
        type=int,
        choices=range(SHARD_COUNT),
        default=None,
        help="run one deterministic whole-module shard of the collected suite",
    )


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Deselect items outside the requested shard after other selectors have run."""
    shard = config.getoption("suite_shard")
    if shard is None:
        return

    assignments = assign_modules(count_modules(item.nodeid for item in items))
    selected_modules = assignments[shard]
    selected = [item for item in items if module_id(item.nodeid) in selected_modules]
    deselected = [item for item in items if module_id(item.nodeid) not in selected_modules]
    items[:] = selected
    config.hook.pytest_deselected(items=deselected)
