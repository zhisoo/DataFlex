"""Filter for removing samples with excessive special characters."""

import re
from typing import Dict, Any, List, Optional


class SpecialCharsFilter:
    """Filter out samples where specified fields contain too many special characters.

    Special characters are defined as non-alphanumeric, non-whitespace, non-basic
    punctuation characters (e.g. control characters, unicode symbols, emojis, etc.).

    Args:
        fields: List of field names to check. Defaults to ['instruction', 'output'].
        max_ratio: Maximum allowed ratio of special chars to total chars (0.0–1.0).
    """

    def __init__(
        self,
        fields: Optional[List[str]] = None,
        max_ratio: float = 0.2,
    ) -> None:
        if not 0.0 <= max_ratio <= 1.0:
            raise ValueError(f"max_ratio must be between 0.0 and 1.0, got {max_ratio}")
        self.fields = fields if fields is not None else ["instruction", "output"]
        self.max_ratio = max_ratio

        # Matches characters that are NOT letters, digits, whitespace, or
        # common punctuation used in natural language.
        self._special_re = re.compile(
            r"[^\w\s.,!?;:'\"-()\[\]{}/\\@#%&*+=<>~`^|$]",
            re.UNICODE,
        )

    def _special_char_ratio(self, text: str) -> float:
        """Return ratio of special characters to total characters."""
        if not text:
            return 0.0
        matches = self._special_re.findall(text)
        return len(matches) / len(text)

    def _check_field(self, sample: Dict[str, Any], field: str) -> bool:
        """Return True if the field passes the special-char ratio check."""
        value = sample.get(field, "")
        if not isinstance(value, str):
            return True
        return self._special_char_ratio(value) <= self.max_ratio

    def filter(self, samples: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter samples, removing those with excessive special characters.

        Args:
            samples: List of data samples (dicts).

        Returns:
            Filtered list of samples.
        """
        result = []
        for sample in samples:
            if all(self._check_field(sample, field) for field in self.fields):
                result.append(sample)
        return result

    def __repr__(self) -> str:
        return (
            f"SpecialCharsFilter(fields={self.fields!r}, max_ratio={self.max_ratio})"
        )
