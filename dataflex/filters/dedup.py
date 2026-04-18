"""Near-duplicate removal for instruction-tuning datasets."""
from __future__ import annotations

import hashlib
from typing import Any


class DeduplicationFilter:
    """Remove exact or near-duplicate samples based on instruction hashing.

    Uses MD5 hashing on the combined instruction and input fields to detect
    duplicates. Case-insensitive by default so that "Tell me X" and "tell me x"
    are treated as the same sample.
    """

    def __init__(
        self,
        instruction_key: str = "instruction",
        input_key: str = "input",
        case_sensitive: bool = False,
    ) -> None:
        self.instruction_key = instruction_key
        self.input_key = input_key
        self.case_sensitive = case_sensitive

    def _make_key(self, sample: dict[str, Any]) -> str:
        instruction = sample.get(self.instruction_key, "")
        inp = sample.get(self.input_key, "")
        # Strip surrounding whitespace before comparing to catch near-identical
        # samples that differ only in leading/trailing spaces.
        combined = f"{instruction.strip()}|||{inp.strip()}"
        if not self.case_sensitive:
            combined = combined.lower()
        return hashlib.md5(combined.encode("utf-8")).hexdigest()

    def filter(self, dataset: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Return dataset with duplicate instructions removed (first occurrence kept)."""
        seen: set[str] = set()
        result: list[dict[str, Any]] = []
        for sample in dataset:
            key = self._make_key(sample)
            if key not in seen:
                seen.add(key)
                result.append(sample)
        return result

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"DeduplicationFilter(case_sensitive={self.case_sensitive})"
        )
