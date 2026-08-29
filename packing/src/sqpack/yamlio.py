"""Strict YAML loading for persisted research and assurance artifacts.

**Every YAML read in this repository goes through here**, and the reason is speed rather
than taste. PyYAML's default `SafeLoader` is a pure-Python scanner, and the record is
several hundred small documents: validating them took 67 seconds, of which 163 seconds of
profiled time was `yaml.load` alone. The same documents parse an order of magnitude faster
through libyaml, which PyYAML already ships and which nothing here was asking for. A schema
check that costs a minute is one nobody runs before a push ([D-370](defects.md)).

`test_module_boundaries` refuses `yaml.safe_load` and a bare `yaml.SafeLoader` elsewhere in
the tree, so the slow loader cannot come back one call site at a time.
"""

from __future__ import annotations

from typing import Any, override

import yaml
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode

# libyaml ships with the wheels this project pins, so the fallback is for a source build
# on a machine without the C library rather than for normal use.
BaseLoader: type[yaml.SafeLoader] = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
HAS_LIBYAML: bool = BaseLoader is not yaml.SafeLoader


class FastSafeLoader(BaseLoader):
    """Safe YAML loading at libyaml speed, with no other behavioural change."""


class UniqueKeyLoader(BaseLoader):
    """Safe YAML loader that rejects mappings whose keys would overwrite data."""

    @override
    def construct_mapping(self, node: MappingNode, deep: bool = False) -> dict[Any, Any]:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicated = key in mapping
            except TypeError as error:
                raise ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    "found an unhashable mapping key",
                    key_node.start_mark,
                ) from error
            if duplicated:
                raise ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key {key!r}",
                    key_node.start_mark,
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def load_yaml(text: str) -> Any:
    """Load trusted YAML syntax while refusing ambiguous duplicate mappings."""
    return yaml.load(text, Loader=UniqueKeyLoader)


def safe_load(text: str) -> Any:
    """Load trusted YAML syntax, allowing duplicate keys the way `yaml.safe_load` does.

    Use `load_yaml` for anything the record owns. This exists for schemas and other inputs
    where the duplicate-key refusal is not wanted, and it lives here rather than at the
    call site so no reader pays for the pure-Python scanner.
    """
    return yaml.load(text, Loader=FastSafeLoader)
