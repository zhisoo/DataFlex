from typing import Any


class LengthFilter:
    """
    Filter samples based on token/character length constraints
    for instruction, input, and output fields.
    """

    def __init__(
        self,
        min_instruction_len: int = 10,
        max_instruction_len: int = 512,
        min_output_len: int = 1,
        max_output_len: int = 2048,
        max_input_len: int = 1024,
        min_input_len: int = 0,
    ):
        self.min_instruction_len = min_instruction_len
        self.max_instruction_len = max_instruction_len
        self.min_output_len = min_output_len
        self.max_output_len = max_output_len
        self.max_input_len = max_input_len
        self.min_input_len = min_input_len

    def _check_field(self, text: str, min_len: int, max_len: int) -> bool:
        length = len(text.strip())
        return min_len <= length <= max_len

    def filter(self, dataset: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Filter out samples that do not meet length requirements.

        Args:
            dataset: List of sample dicts with 'instruction', 'input', 'output'.

        Returns:
            Filtered list of samples.
        """
        filtered = []
        for sample in dataset:
            instruction = sample.get("instruction", "")
            output = sample.get("output", "")
            inp = sample.get("input", "")

            if not self._check_field(
                instruction, self.min_instruction_len, self.max_instruction_len
            ):
                continue
            if not self._check_field(
                output, self.min_output_len, self.max_output_len
            ):
                continue
            # Check input length bounds (min_input_len allows filtering out empty inputs)
            if not self._check_field(inp, self.min_input_len, self.max_input_len):
                continue

            filtered.append(sample)
        return filtered

    def __repr__(self) -> str:
        return (
            f"LengthFilter("
            f"min_instruction_len={self.min_instruction_len}, "
            f"max_instruction_len={self.max_instruction_len}, "
            f"min_output_len={self.min_output_len}, "
            f"max_output_len={self.max_output_len}, "
            f"min_input_len={self.min_input_len}, "
            f"max_input_len={self.max_input_len})"
        )
