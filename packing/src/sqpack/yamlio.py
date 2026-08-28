"""Strict YAML loading for persisted research and assurance artifacts."""

from __future__ import annotations

from typing import Any, override

import yaml
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode


class UniqueKeyLoader(yaml.SafeLoader):
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
