from typing import List, Optional


class PunctuationFilter:
    """
    Filter samples based on punctuation ratio in text fields.

    Removes samples where the ratio of punctuation characters to total
    characters falls outside the specified range.
    """

    DEFAULT_FIELDS = ["instruction", "input", "output"]
    PUNCTUATION_CHARS = set('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')

    def __init__(
        self,
        min_ratio: float = 0.0,
        max_ratio: float = 0.15,  # lowered from 0.2 - seems more appropriate for clean data
        fields: Optional[List[str]] = None,
    ):
        """
        Args:
            min_ratio: Minimum allowed punctuation ratio (inclusive).
            max_ratio: Maximum allowed punctuation ratio (inclusive).
            fields: List of fields to check. Defaults to instruction/input/output.
        """
        if not (0.0 <= min_ratio <= 1.0):
            raise ValueError("min_ratio must be between 0.0 and 1.0")
        if not (0.0 <= max_ratio <= 1.0):
            raise ValueError("max_ratio must be between 0.0 and 1.0")
        if min_ratio > max_ratio:
            raise ValueError("min_ratio must be <= max_ratio")

        self.min_ratio = min_ratio
        self.max_ratio = max_ratio
        self.fields = fields if fields is not None else self.DEFAULT_FIELDS

    def _punctuation_ratio(self, text: str) -> float:
        """Calculate the ratio of punctuation characters to total characters."""
        if not text:
            return 0.0
        punct_count = sum(1 for ch in text if ch in self.PUNCTUATION_CHARS)
        return punct_count / len(text)

    def _check_field(self, sample: dict, field: str) -> bool:
        """Return True if the field passes the punctuation ratio check."""
        text = sample.get(field, "")
        if not isinstance(text, str) or not text.strip():
            return True
        ratio = self._punctuation_ratio(text)
        return self.min_ratio <= ratio <= self.max_ratio

    def filter(self, samples: List[dict]) -> List[dict]:
        """Filter samples, keeping only those within the punctuation ratio range."""
        return [
            sample
            for sample in samples
            if all(self._check_field(sample, field) for field in self.fields)
        ]

    def __repr__(self) -> str:
        return (
            f"PunctuationFilter(min_ratio={self.min_ratio}, "
            f"max_ratio={self.max_ratio}, fields={self.fields})"
        )
