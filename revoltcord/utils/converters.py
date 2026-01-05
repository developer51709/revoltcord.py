"""
Converters module
Provides type converters for command arguments.

These are intentionally simple but structured so they can be expanded
later without breaking compatibility.
"""

from __future__ import annotations
from typing import Any, Type


class Converter:
    """Base class for all converters."""

    async def convert(self, value: str) -> Any:
        raise NotImplementedError("Converter subclasses must implement convert()")


class IntConverter(Converter):
    async def convert(self, value: str) -> int:
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Expected an integer, got {value!r}")


class FloatConverter(Converter):
    async def convert(self, value: str) -> float:
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Expected a float, got {value!r}")


class StrConverter(Converter):
    async def convert(self, value: str) -> str:
        return value


class BoolConverter(Converter):
    async def convert(self, value: str) -> bool:
        lowered = value.lower()
        if lowered in ("true", "yes", "1", "on"):
            return True
        if lowered in ("false", "no", "0", "off"):
            return False
        raise ValueError(f"Expected a boolean, got {value!r}")


# Utility: map Python types to converters
TYPE_CONVERTER_MAP: dict[Type, Type[Converter]] = {
    int: IntConverter,
    float: FloatConverter,
    str: StrConverter,
    bool: BoolConverter,
}


async def run_converter(annotation: Type, value: str) -> Any:
    """
    Convert a string value into the annotated type using the appropriate converter.
    """
    converter_cls = TYPE_CONVERTER_MAP.get(annotation)
    if not converter_cls:
        raise TypeError(f"No converter available for type {annotation}")

    converter = converter_cls()
    return await converter.convert(value)
