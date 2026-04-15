"""Quality filtering for instruction-tuning datasets."""
from __future__ import annotations

from typing import Any


class QualityFilter:
    """Filter dataset samples based on configurable quality heuristics."""

    def __init__(
        self,
        min_instruction_len: int = 10,
        min_output_len: int = 5,
        max_instruction_len: int = 2048,
        max_output_len: int = 4096,
        instruction_key: str = "instruction",
        output_key: str = "output",
    ) -> None:
        self.min_instruction_len = min_instruction_len
        self.min_output_len = min_output_len
        self.max_instruction_len = max_instruction_len
        self.max_output_len = max_output_len
        self.instruction_key = instruction_key
        self.output_key = output_key

    def _is_valid(self, sample: dict[str, Any]) -> bool:
        instruction = sample.get(self.instruction_key, "")
        output = sample.get(self.output_key, "")

        if not isinstance(instruction, str) or not isinstance(output, str):
            return False

        instr_len = len(instruction.strip())
        out_len = len(output.strip())

        return (
            self.min_instruction_len <= instr_len <= self.max_instruction_len
            and self.min_output_len <= out_len <= self.max_output_len
        )

    def filter(self, dataset: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Return only samples that pass all quality checks."""
        return [sample for sample in dataset if self._is_valid(sample)]

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"QualityFilter(min_instruction_len={self.min_instruction_len}, "
            f"min_output_len={self.min_output_len})"
        )
